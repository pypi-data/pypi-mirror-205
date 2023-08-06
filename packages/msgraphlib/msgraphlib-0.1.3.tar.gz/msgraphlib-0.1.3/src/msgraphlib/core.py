### IMPORTS ###

# Python Standard Library
import os
import time
from enum import Enum 
from typing import Literal
from dataclasses import dataclass, field, fields, InitVar
import json
from importlib.metadata import version 
from datetime import datetime # DBG

# 3rd party
import requests
from requests.models import Response as HTTPResponse
from requests import Session
import msal

#Local
# ...

### EXCEPTIONS ###

class ConfigException(ValueError):
    pass

class AuthException(ValueError):
    pass

class ModuleNotImported(ImportError):
    def __init__(self, module_name):
        msg = ''.join(("Module '" , module_name, "' has not been loaded.", '\n',
                       "You have to include it in the import statement."))
        super().__init__(msg)

class ArgumentException(TypeError):
    def __init__(self, *args):
        msg = "You have to provide value for exactly one of the following parameters: "
        super().__init__(f"{msg}{', '.join(filter(None, args))}")

class ValidationError(ValueError):
    pass

class ResourceNotFoundError(requests.exceptions.HTTPError):
    pass    
class ResourceLockedError(requests.exceptions.HTTPError):
    pass
class ResourceModifiedError(requests.exceptions.HTTPError):
    pass
class ResourceCheckedOutError(requests.exceptions.HTTPError):
    pass
class NameAlreadyExistsError(requests.exceptions.HTTPError):
    pass
class ResourceConflictError(requests.exceptions.HTTPError):
    pass

### PACKAGE METADATA ###
       
class Metadata():
    PACKAGE_NAME = __name__.split('.')[0]
    PACKAGE_VERSION = version(PACKAGE_NAME)

    @classmethod
    def __init__(cls, caller):
        cls.MODULE_NAME = caller.__class__.__module__
        cls.CLASS_NAME = caller.__class__.__name__

### FUNCTIONS ###

def _validate_args (kwargs:dict, name:str=None, xor_sets:tuple=()):
    if xor_sets:
        for set in xor_sets:
            xors = {k:kwargs[k] for k in set if k in kwargs.keys()} 
            if not _xor(xors.values()): raise ArgumentException(xors.keys())
    else:
        if name: xors = {k:v for k, v in kwargs.items() if k.startswith(name)} 
        else: xors = kwargs
        if not _xor(xors.values()): raise ArgumentException(xors.keys())

def _xor(*args):
    return sum(bool(i) for i in args) == 1 

# def tree(): return defaultdict(tree) #from collections import defaultdict

### OBJECT POOLS ###

class _ClientPool:
    _stock = {}
    
class _CredsPool:
    _stock = {}

    @classmethod
    def get_creds(cls, arn):
        creds = cls._stock.get(arn)
        if not creds:
            aws_creds = cls._get_aws_creds(arn)
            if aws_creds:
                secret_key = ('aad_client_secret', 'secret', 'client_secret', 'value')
                secret = [v for (k,v) in aws_creds.items() if k.lower() in secret_key]
                if secret: cls._stock[arn] = {'aad_client_secret': secret[-1]}
        return cls._stock.get(arn)
    
    @staticmethod
    def _get_aws_creds(creds_arn):
        # Requires layer 'AWS Parameters and Secrets Lambda Extension'
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_Operations.html
        # The secret name can contain ASCII letters, numbers, and the following characters: /_+=.@-
        # Secret's ARN includes the name of the secret followed by six random characters
        port = os.getenv('PARAMETERS_SECRETS_EXTENSION_HTTP_PORT', 2773) #AWS default: 2773
        secrets_url = (f"http://localhost:{port}/secretsmanager/get?secretId={creds_arn}")
        headers = { "X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN') }
        response = requests.get(secrets_url, headers = headers)
        # req = urllib.request.Request(secrets_url, headers = headers, method = 'GET')
        # with urllib.request.urlopen(req) as response:
        creds = json.loads(response.content.decode())['SecretString']
        if type(creds) == str: creds = json.loads(creds)
        #creds = json.loads(self.__retrieve_extension_value(secrets_url)['SecretString'])
        return creds

### CONFIG ###

@dataclass
class Config:
    id: InitVar[str]=None
    aws_creds_arn_graph: str=None
    aad_tenant_id: str=None
    aad_client_id: str=None
    aad_client_secret: str=None
    aad_cert_thumbprint: str=None 
    aad_cert_priv_key: str=None
    aad_public_cert: str=None 
    aad_client_certificate: dict = field(init=False,default=None)
    graph_base_url: str=f"https://graph.microsoft.com/v1.0"
    graph_scope: list = field(default_factory=lambda: ['https://graph.microsoft.com/.default'])
    http_err = True
    if_not_found:Literal[None, 'response'] = None
    retry = {'count': 1, 'pause': 15, 'errors': (429, 500, 503, 504)}
    _id: str = field(init=False,default=None)

    def __post_init__(self, id):

        # Check if preset/default config requested (no manual values provided)
        if {x.name:x.default for x in fields(self) if x.init} == vars(self):
            self._id = self.id or 'default'
            
        # Otherwise assign a unique id
        else: self._id = f"{self.id or 'default'}_{len(_ClientPool._stock) + 1}"
            
        # Check if 'aad_tenant_id' and 'aad_client_id' are available
        for field_name in ['aad_tenant_id', 'aad_client_id']:
            if not self._resolve_value(field_name, config_id = id):
                err_msg = f"Value '{field_name}' not provided or not maintained in environment variables"
                raise ConfigException(err_msg)

        # Check if certificate details or client secret are available
        for field_name in ['aad_cert_priv_key', 'aad_cert_thumbprint', 'aad_public_cert']:
            self._resolve_value(field_name, config_id = id)
        if self.try_build_cert(): return
        if self._resolve_value('aad_client_secret', config_id = id): return

        # If credentials not found, check if script is running on AWS Lambda
        if not self._is_aws_env():
            raise ConfigException("Unable to find valid credentials")
        
        # If running as Lambda, try to find creds on AWS (or get from the Pool)
        else:
            if self._resolve_value('aws_creds_arn_graph', config_id = id):
                creds = _CredsPool.get_creds(self.aws_creds_arn_graph)
                if creds: self.merge_creds_with_config(creds)
                self.try_build_cert()
            if not any(self.aad_client_certificate, self.aad_client_secret):
                ConfigException("Unable to find valid credentials")

    def _resolve_value(self, field_name, config_id=None) -> bool:
        value_init = getattr(self, field_name) or ''
        # If path provided, try to get value from file
        if os.path.isfile(value_init): 
            setattr(self, field_name, self._get_file_data(value_init))
        # If config id provided, try to get from env vars using id
        elif not value_init and config_id:
            setattr(self, field_name, os.getenv(f"{field_name}_{config_id}".upper()))
        # If still not found try the 'non-id' version of env vars
        if not getattr(self, field_name): 
            setattr(self, field_name, os.getenv(field_name.upper()))
        # return True if value found
        return True if getattr(self, field_name) else False

    def _get_file_data(self, file_path) -> str:
        if os.path.exists(file_path):
            with open(file_path) as f:
                content = f.read()
                if content: return content
                else: ConfigException(f"File {file_path} is empty")
        else: raise ResourceNotFoundError(f"Filepath: {file_path}")

    def _is_aws_env(self):
        return os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
    
    def merge_creds_with_config(self, creds):
        for cred_type, cred_value in creds.items():
            if hasattr(self, cred_type): setattr(self, cred_type, cred_value)
            else: raise ConfigException("Unable to match AWS Secret item with Config fields")

    def try_build_cert(self):
        if self.aad_cert_priv_key and self.aad_cert_thumbprint:
            self.aad_client_certificate = {
                'thumbprint': self.aad_cert_thumbprint,
                'private_key': self.aad_cert_priv_key,
            }
            if self.aad_public_cert: 
                self.aad_client_certificate['public_certificate'] = self.aad_public_cert
                return True

### API CLIENT ###

class Client:

    def __init__(self, config: Config=None):
        self.metadata = Metadata(self)
        self.config = config
        self.default_session:Session = requests.session()
        self._session:dict[Session] = {}
        self.headers = {}
        self.app_msal = self._get_msal()
        self._id = config._id

    def _get_msal(self):
        # Create MSAL instance (used to get auth token)
        kwargs = {
            'authority': f"https://login.microsoftonline.com/{self.config.aad_tenant_id}",
            'client_id': self.config.aad_client_id
        }
        if self.config.aad_client_certificate != None:
            kwargs |= {'client_credential': self.config.aad_client_certificate}
        elif self.config.aad_client_secret != None:
            kwargs |= {'client_credential': self.config.aad_client_secret}
        else:
            raise AuthException('Invalid or missing credentials')
        return msal.ConfidentialClientApplication(**kwargs)      
    
    def _refresh_access_token(self):
        # First try to lookup an access token in cache
        access_token = self.app_msal.acquire_token_silent(
            self.config.graph_scope, account=None)

        # If the token is not available in cache, acquire a new one from Azure AD 
        if not access_token: 
            access_token = self.app_msal.acquire_token_for_client(
                scopes=self.config.graph_scope)

        # Refresh token value in request header
        self.headers['Authorization'] = access_token['access_token']

    def session(self, id) -> Session:
        return self._session.get(id) or self._session.setdefault(id, requests.session())

    def request(self, verb, url:str, headers:dict={}, 
                data=None, json=None, files=None, 
                http_err:bool=True, session:Session=None):
        session = session or self.default_session
        kwargs = {'data': data, 'json': json, 'files': files}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        for attempt in range(1 + self.config.retry['count']):
            try:
                # Add defaults for Graph API endpoints
                if url[0] == '/' or url.startswith(self.config.graph_base_url): 
                    if url[0:1] == '/': url = self.config.graph_base_url + url 
                    self._refresh_access_token()
                    headers = self.headers | (headers or {})
                # If succesful return the formatted response
                #print('Req: ', verb, url) #DBG
                #print('Req before: ',datetime.now()) #DBG
                response = session.request(verb, url, headers=headers, **kwargs)
                #print('Req after: ',datetime.now()) #DBG
                #print(response.status_code, response.reason) #DBG
                # if response.status_code == 404 and 'itemNotFound' in response.text: 
                #     if self.config.if_not_found == None: return None
                if self.config.http_err and http_err: 
                    response.raise_for_status()
                if 'application/json' in response.headers.get('Content-Type', ''): 
                    setattr(response, 'json', response.json()) 
                return response
                
            except requests.exceptions.HTTPError as err:
                error = response.json()['error']
                # Retry in case of 'Too Many Requests', 'Service Unavailable' or 'Gateway Timeout'
                if attempt < self.config.retry['count']:
                    if response.status_code in (429, 500, 503, 504):
                        pause = response.headers.get('Retry-After', self.config.retry['pause'])
                        time.sleep(pause); continue
                    elif response.status_code == 409 and error['code'] == 'resourceModified':
                        time.sleep(5); continue

                # Otherwise re-throw with HTTP data from the response
                err_msg = {'status': response.status_code, 'reason': response.reason}
                err_msg |= {'error': error, 'text': response.text} 

                match response.status_code:
                    case 403 if 'WAC access token' in response.text:
                         raise # AccessDenied - Could not obtain a WAC access token
                    case 404 if error['code'] == 'itemNotFound':
                         raise ResourceNotFoundError(err_msg)
                    case 423 if error['code'] == 'resourceCheckedOut': 
                        raise ResourceCheckedOutError(err_msg)
                    case 423:
                        raise ResourceLockedError(err_msg)
                    case 409 if error['code'] == 'nameAlreadyExists':
                        raise NameAlreadyExistsError(err_msg)
                    case 409 if error['code'] == 'resourceModified':
                        raise ResourceModifiedError(err_msg)                    
                    case _: raise requests.exceptions.HTTPError(err_msg)

            except requests.exceptions.ConnectionError as err_c:
                if attempt < self.config.retry['count']: time.sleep(self.config.retry['pause'])
                else: raise (err_c)
            except requests.exceptions.Timeout as err_t:
                raise (err_t)
            except requests.exceptions.RequestException as err_r:
                raise (err_r)     
            except Exception as err:
                raise err

### BASE CLASSES ###

class _BaseApp():

    def __init__(self, config_id=None, config: Config=None, client: Client=None): 

        # Use Client object passed from child class
        if client: self.client = client

        # error if both config_id and Config object were provided
        elif all((config_id, config)): raise ArgumentException('config_id', 'config')

        # error if config object provided in place of config_id
        elif type(config_id).__name__ == 'Config': 
            raise ConfigException("Config object has to be passed as a keyword argument")

        # If Client not provided -> get / create API Client 
        else:
            config_id = config_id or getattr(config, '_id', None) or 'default'
            # first check in the Client Pool using config id or default
            self.client = (_ClientPool._stock.get(config_id, None) or 
                # if not found - create Client and Config (if not provided) 
                _ClientPool._stock.setdefault(
                    config_id, Client(config or Config(config_id or 'default'))))

    # def request(self, verb, url, headers=None, data=None, json=None, files=None):
    #     return self.client.request(verb, url, headers, data, json, files)

class _GraphObject():

    def __init__(self, parent, json:dict=None, **kwargs):
        self._exists = None
        self.parent = parent
        self.app:_BaseApp = getattr(parent, 'app', parent)
        self.client:Client = self.app.client
        self.request = getattr(self.parent, 'request', self.client.request) 
        if json: self._update_vars(json)
        super().__init__(**kwargs)

    def _update_vars(self, resource):
        self.__dict__.update(resource)
        self._exists = True
        if callable(getattr(self, '_update_vars_bis', None)): self._update_vars_bis()

    @property
    def exists(self):
        if self._exists != None: return self._exists
        resource = self.client.request('GET', self.url, http_err=False).json
        if resource: self._update_vars(resource); return True
        else: return False

class _GraphCollection():

    def __init__(self, parent:_GraphObject, request=None, **kwargs):
        self.app = parent.app
        self.request = request or parent.request
        self.parent = parent
        self.name = kwargs['name']
        self.stock_name = kwargs['stock_name']
        # self.member_name = None
        self.member_class = kwargs['member_class']
        self.url = f"{parent.url}/{self.name}"        
        # super().__init__(**kwargs)

    def __getitem__(self, item):
        return self._dict[item]

    def list(self) -> list:
        collection = self.request('GET', self.url).json['value']
        output = []
        for obj in collection:
            key = obj.get('id') or obj.get('name')
            getattr(self.parent, self.stock_name)[key] = self.member_class(self, json=obj)
            output.append(getattr(self.parent, self.stock_name)[key])
        return output

class _FileContent():
    binary:bytes
    text:str
    dict:dict

### ENHANCED BASE DATA TYPES ###

class GraphArray(list):

    def to_list_of_dict(self) -> list[dict]:
        return [dict(zip(self[0], v)) for v in self[1:]]

    def to_dict_of_dict(self, index_column:str) -> dict[dict]:
        #list of dicts to dict of dicts
        return {row[index_column]: row for row in self.to_list_of_dict()}

### DESCRIPTORS ###

class ReadOnlyProp():

    default = None
    objects = {'values': GraphArray}

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, obj_type=None):
        print(f'{datetime.now().strftime("%H:%M:%S")} | __get__ | {self.__class__.__name__} | {self.name}') #DBG 
        value = obj.__dict__.get(self.name, self.default)
        if value == self.default:    
            if (url := obj.__dict__.get('url')):
                if not getattr(obj, 'query'): url = url
                elif obj.__dict__.get('_exists'): url = f"{url}?select={self.name}"
                else: url = f"{url}?expand={self.name}"
                item = obj.client.request('GET', url).json
                obj._update_vars(item)
        value = obj.__dict__.get(self.name, None)
        return value if not (cls:=self.objects.get(self.name)) else cls(value) #cls(obj, value)

class ReadWriteProp(ReadOnlyProp):

    def __set__(self, obj, value):
        print(f'{datetime.now().strftime("%H:%M:%S")} | __set__ | {self.__class__.__name__} | {self.name}') #DBG
        kwargs = {'verb': 'PATCH', 'url': obj.__dict__['url'], 'json': {self.name: value}}
        obj._update_vars(obj.client.request(**kwargs).json)

class _CollectionProp():

    def __set_name__(self, owner, name:str):
        self.name = name

    def __get__(self, obj, obj_type=None):
        # cls = self.objects.get(self.name)
        cls = self.cls
        value = getattr(self, f'_{self.name}', None)
        # return (getattr(self, f'_{self.name}', None) or 
        #         self.__dict__.setdefault(f'_{self.name}', cls(self)))
        return value or cls(parent=obj)
        # return (getattr(self, f'_{self.name}', None) or self.__dict__.setdefault(
        #     f'_{self.name.title()}', type(self.name, (object,), {})(self)))

    def __set__(self, obj, value):
        raise ValidationError(f"Creating collections of {self.name} is not supported")

### ??? ###

class Basic(_BaseApp):

    def __init__(self, config_id=None, config: Config=None): 
        super().__init__(config_id, config)


