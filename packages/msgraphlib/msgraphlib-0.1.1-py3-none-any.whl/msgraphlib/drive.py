### CONFIG ###

__all__ = ["DriveExplorer"]

### IMPORTS ###

# Python Standard Library
import os, sys
from datetime import datetime
from typing import Literal, Union
from collections import defaultdict

# 3rd party
# ...

#Local
from .core import _BaseApp, Config, Client
from .core import Metadata, HTTPResponse
from .core import ArgumentException, ModuleNotImported
from .core import _GraphObject, ReadOnlyProp, ReadWriteProp, _FileContent
from .core import _xor, _validate_args
from .sharepoint import _Sharepoint
if 'msgraphlib.excel' in sys.modules: from .excel import Workbook

### FUNCTIONS ###

def _validate_drive_item (drive, id, path, json):

    # Check if drive_id exists
    if drive is None: 
        msg  = "Options:\r\n- provide 'drive_id' parameter in method call \r\n"
        msg += "maintain 'GRAPH_DRIVE_ID' environment variable and create a new class instance"
        msg += "\r\ncall 'set_drive_id' method"
        raise ValueError(f"Graph Drive Id missing!\r\n{msg}")
    
    # mutually exclusive arguments check (e.g. id vs path)
    if not json and not _xor(id, path): raise ArgumentException('id', 'path')

    return True

### CLASSES ###

class DriveExplorer(_BaseApp):

    def __init__(self, config_id=None, config: Config=None):
        super().__init__(config_id, config)
        self.metadata = Metadata(self)
        self._drive:dict[Drive] = {}

    def drive(self, id:str=None, check_out_required:bool=False) -> 'Drive':
        return (self._drive.get(id) or 
                self._drive.setdefault(id, Drive(self, id, check_out_required)))
    
    def get_drive(self, drive_id:str=None, site_id:str=None, group_id:str=None, 
                  site_name:str=None, team_name:str=None, doc_lib_name:str='default'):
        if drive_id or doc_lib_name == 'default':
            return self._get_drives(drive_id, site_id, group_id, team_name, site_name, True)
        else:
            drives = self._get_drives(drive_id, site_id, group_id, team_name, site_name, False)
            return {k:v for k, v in drives.items() if v['name'] == doc_lib_name}
    
    def list_drives(self, site_id=None, group_id=None, team_name=None, site_name=None):
        return self._get_drives(None, site_id, group_id, team_name, site_name)
    
    def _get_drives(self, drive_id:str=None, site_id:str=None, group_id:str=None, 
                    site_name:str=None, team_name:str=None, default:bool=False):
        xor_args = {k: v for k, v in locals().items() if k not in ('self', 'doc_lib_name')}
        _validate_args (xor_args)

        endpoint = 'drive' if default else 'drives'
        if drive_id: url = f"/drives/{drive_id}" 
        elif group_id: url = f"/groups/{group_id}/{endpoint}"
        elif site_id: url = f"/sites/{site_id}/{endpoint}"
        elif team_name or site_name: 
            site = self._get_site(team_name, site_name)
            url = f"/sites/{site.json['id']}/{endpoint}"
        return self.client.request('GET', url).json
    
class _DriveResource():

    id = ReadOnlyProp()
    createdDateTime = ReadOnlyProp()
    createdBy = ReadOnlyProp()
    lastModifiedBy = ReadOnlyProp()
    lastModifiedDateTime = ReadOnlyProp()
    sharePointIds = type('DriveProp', (ReadOnlyProp,), {'default': {}})()

class Drive(_GraphObject, _DriveResource):

    name = ReadOnlyProp()

    def __init__(self, app:_BaseApp,
                 id:str=None, check_out_required:bool=False):
        super().__init__(parent=app)
        self.metadata = Metadata(self)
        self.__dict__['id'] = id or os.getenv('GRAPH_DRIVE_ID')
        self.url = f'/drives/{self.id}'
        self.check_out_required = check_out_required
        # self._folder:dict[Folder] = {}
        # self._file:dict[File] = {}
        self._children: dict[tuple[Folder, File]] = {}
    
    def folder(self, path:str=None, id:str=None) -> 'Folder':
        return (self._children.get(id or path) or 
                self._children.setdefault(id or path, Folder(self, path, id)))
    
    def file(self, path:str=None, id:str=None) -> 'File':
        return (self._children.get(id or path) or 
                self._children.setdefault(id or path, File(self, path, id)))
    
    def workbook(self, path:str=None, id:str=None) -> 'Workbook':
        file = (self._children.get(path or id) or 
                self._children.setdefault(path or id, File(self, path, id)))
        return (getattr(file, 'workbook') or 
                file.__dict__.setdefault('workbook', Workbook(self)))

class _DriveItem(_DriveResource):

    name = ReadWriteProp()
    eTag = ReadOnlyProp()
    size = ReadOnlyProp()
    publication = type('DriveProp',(ReadOnlyProp,), {'default': {'level': ''}})()
    
    def __init__(self, drive:Drive, path:str=None, id:str=None, json:dict=None):
        _validate_drive_item(drive, id, path, json)
        self.drive = drive
        self.__dict__['id'] = id
        self.path = f"/{path.lstrip('/')}" if path else None
        self.__dict__['name'] = path.split("/")[-1] if path else None
        if json: self._update_vars(json); return
        self.url_id = f"{self.drive.url}/items/{id}" if id else None
        self.url_path = f"{self.drive.url}/root:{self.path}:" if path else None
        self.url = self.url_id or self.url_path

    def _update_vars_bis(self):
        if (id := self.__dict__['id']): self.url_id = f"{self.drive.url}/items/{id}" 
        if self.path: self.url_path = f"{self.drive.url}/root:{self.path}:" 
        if not self.path and ((parent := self.__dict__.get('parentReference')) and
                              (name := self.__dict__.get('name'))):
            self.url_path = f"{parent['path']}/{name}"
            self.path = self.url_path.replace(f"{self.drive.url}/root:", '')
        self.url = self.url_id or self.url_path

    def get_props(self, select:list=[], expand:list=[], http_err:bool=True):
        expand_query = f"expand={','.join(expand)}" if expand else ''
        select_query = f"select={','.join(select)}" if select else ''
        url = f"{self.url}?{'&'.join(filter(None, [expand_query, select_query]))}"
        result = self.client.request('GET', url.rstrip('?'), http_err=http_err)
        if result == None: return result
        elif getattr(result, 'ok'): 
            self._update_vars(result.json)
            if expand or len(select) != 1: return result.json
            else: return result.json[select[0]]
        else: return result

    def _manage_item(self, verb:str, endpoint:str=None, body:dict=None, 
                     http_err:bool=True):
        url = f"{self.url}/{endpoint}"
        return self.client.request(verb, url, json = body, http_err=http_err)
    
    def list_children(self):
        print('in_start: ',datetime.now())
        children = self.client.request('GET', f"{self.url}/children").json['value']
        print('in_start: ',datetime.now())
        output = []
        for child in children:
            key = child.get('id') or child.get('name')
            cls = File if 'file' in child.keys() else Folder 
            self.drive._children[key] = cls(self.drive, json=child)
            output.append(self.drive._children[key])
        return output

    def _update(self, built_in_props, custom_props):
        fx_args = locals().copy();  #fx_args.pop('self')
        item = {}
        if built_in_props: 
            item = self.client.request('PATCH', self.url, json=built_in_props).json
        if custom_props: 
            kwargs = {'url': f"{self.url}/ListItem/fields", 'json': custom_props}
            item.update(self.client.request('PATCH', **kwargs).json)
        return item
    
    def _copy(self, new_parent_path, new_name, conflict_behavior):
        new_parent_path = f"/root:/{new_parent_path.strip('/')}"
        new_parent = self.client.request('GET', f'{self.drive.url}{new_parent_path}')
        endpoint = f"copy?@microsoft.graph.conflictBehavior={conflict_behavior}"
        metadata = {"parentReference": {"id": new_parent.json['id']}}
        if new_name: metadata |= {"name": new_name}
        kwargs = {'url': f'{self.url}/{endpoint}', 'json': metadata}
        return self.client.request('POST', **kwargs).json

    def _rename(self, new_name):
        return self.client.request('PATCH', self.url, json={"name": new_name})
    
    def _move(self, new_parent_path, new_name):
        new_parent = self.client.request('GET', f'{self.drive.url}/{new_parent_path}')
        metadata = {"parentReference": {"id": new_parent.json['id']}}
        if new_name: metadata |= {"name": new_name}
        return self.client.request('PATCH', self.url, json=metadata).json
    
class Folder(_GraphObject, _DriveItem):

    def __init__(self, drive:Drive, path:str=None, id:str=None, json:dict=None):
        super().__init__(parent = drive, drive = drive, path = path, id = id, json = json)

    def create(self) -> 'Folder': 
        headers = {'Content-Type': 'application/json'}
        json = {"folder": {}}
        folder = self.client.request('PATCH', self.url, headers, json=json).json
        self._update_vars(folder)
        return folder
    
    def update(self, built_in_props:dict=None, custom_props:dict=None) -> 'Folder': 
        return self._update(built_in_props, custom_props) 

    def copy(self, new_parent_path:str, new_name:str=None, 
             conflict_behavior:Literal['replace','rename','fail']='replace') -> 'Folder': 
        return self._copy(new_parent_path, new_name, conflict_behavior)

    def rename(self, new_name:str) -> 'Folder': 
        return self._rename(new_name) 

    def move(self, new_parent_path:str, new_name:str=None) -> 'Folder': 
        return self._move(new_parent_path, new_name)
    
    def update_content_type(self, content_type_name:str=None, content_type_id:str=None):
        # Validate arguments
        _validate_args(locals(), 'content_type_') 
        
        # Get SharePoint Ids 
        ids = self.get_props(['sharepointIds'])

        # Get Content Type Id
        if content_type_name:
            content_type_id = self.app._get_content_type(ids['siteId'], content_type_name)

        # Update folder
        url = f"/sites/{ids['siteId']}/lists/{ids['listId']}/items/{ids['listItemId']}"
        json = {"contentType": {"id": content_type_id['id']} }
        return self.client.request('PATCH', url, json = json).json

class File(_GraphObject, _DriveItem):

    def __init__(self, drive:Drive, path:str=None, id:str=None, json:dict=None):
        super().__init__(parent = drive, drive = drive, path = path, id = id, json = json)
        self._workbook:dict[Workbook] = {}

    @property
    def workbook(self) -> 'Workbook':
        if 'msgraphlib.excel' not in sys.modules: raise ModuleNotImported('msgraphlib.exel')
        else: from .excel import Workbook
        if not vars(self).get('id'): self.get_props()
        return (self._workbook.get(self.path or vars(self)['id']) or 
                self._workbook.setdefault(self.path or vars(self)['id'], Workbook(self)))
    
    @property
    def content (self) ->_FileContent:
        content = self.client.request('GET', f"{self.url}/content")
        props = {'binary': content.content, 'text': content.text, 'dict': content.json}
        return type('Content',(_FileContent,), props)()

    def update(self, built_in_props:dict=None, custom_props:dict=None) -> 'File': 
        return self._update(built_in_props, custom_props) 

    def copy(self, new_parent_path:str, new_name:str=None, 
             conflict_behavior:Literal['replace','rename','fail']='replace') -> 'File': 
        return self._copy(new_parent_path, new_name, conflict_behavior)

    def rename(self, new_name:str) -> 'File': 
        return self._rename(new_name) 

    def move(self, new_parent_path:str, new_name:str=None) -> 'File': 
        return self._move(new_parent_path, new_name)
    
    def check_in(self, comment:str=None) -> HTTPResponse:
        json = {"comment": comment} if comment else None
        kwargs = {'url': f"{self.url}/checkin", 'json': json}
        if (res := self.client.request('POST', **kwargs)).status_code == 204:
            self.__dict__['publication'] | {'level': 'published'}
            defaultdict()
        return res
    
    def check_out(self) -> 'File':
        if (res := self.client.request('POST', f"{self.url}/checkout")).status_code == 204:
            publication = self.__dict__.setdefault("publication", {'level': 'checkout'})
            if publication.get('level') != 'checkout': 
                self.__dict__.setdefault("publication", {'level': 'checkout'})
            try: self.__dict__["publication"].update({'level': 'checkout'})
            except KeyError: self.__dict__["publication"] = {'level': 'checkout'}
        return self

    def restore_version(self, ver_id:str):
        url = f"{self.url}/versions/{ver_id}/restoreVersion"
        if (response := self.client.request('POST', url)).status_code == 204:
            self.__dict__['publication'].update(self.get_props(['publication']))
        return response
    
    def upload (self, source_path:str=None, source_bytes:bytes=None, 
                     conflict_behavior:Literal['replace','rename','fail']='replace',
                     check_in:bool=False, check_in_comment:str=None,) -> 'File': 
        #https://learn.microsoft.com/en-us/graph/api/driveitem-createuploadsession?view=graph-rest-1.0
        #https://python.plainenglish.io/all-you-need-to-know-file-handing-in-sharepoint-using-python-df43fde60813
        
        # Validate request details
        _validate_args(locals().copy(), 'source_')

        # Initiate variables
        result = []; headers = {}; checked_out = False

        # Check out file if check out required and file already exists
        if self.drive.check_out_required and conflict_behavior == 'replace':
            # original_file = self.get_props(select=['publication'], http_err=False)
            if self.get_props(['publication'], http_err=False):
                if self.publication['level'] == 'published': checked_out = self.check_out()

        # Get source size, open file if requested
        if source_path: 
            file_bytes = open(source_path, 'rb')
            file_size = os.stat(source_path).st_size 
        elif source_bytes:
            file_size = len(source_bytes) 

        try:
            ### File < 4MB - simple upload ###
            if  file_size / (1024 * 1024) < 4: #DBG  4
                upload_url = f"{self.url}/content"
                upload_url += f"?@microsoft.graph.conflictBehavior={conflict_behavior}"
                all_bytes = source_bytes or file_bytes.read()
                result.append(self.client.request('PUT', upload_url, data = all_bytes))

            ### File > 4MB - upload with Upload Session ###
            else:
                # Get upload url from Upload Session 
                url = f"{self.url}:/createUploadSession"
                json = {'item': {'@microsoft.graph.conflictBehavior': conflict_behavior}}
                upload_url = self.client.request('POST', url, json=json).json['uploadUrl']

                ### File < 50MB - upload the entire file
                if file_size / (1024 * 1024) < 50: #DBG  50
                    headers['Content-Length'] = str(file_size)
                    headers['Content-Range'] = f'bytes 0-{file_size - 1}/{file_size}'
                    data = {'data': source_bytes or file_bytes.read()}
                    result.append(self.client.request('PUT', upload_url, headers, **data))

                ### File > 50MB - Upload bytes in chunks 
                else:
                    chunk_max_size = 1 * 320 * 1024 #max chunk size must be a multiple of 320 KiB
                    start = 0
                    while start < file_size:
                        if source_path: chunk_bytes = file_bytes.read(chunk_max_size)
                        elif source_bytes: chunk_bytes = source_bytes[start:start + chunk_max_size] 
                        chunk_size = len(chunk_bytes)
                        headers['Content-Length'] = str(chunk_size)
                        headers['Content-Range'] = f'bytes {start}-{start + chunk_size - 1}/{file_size}'
                        result.append(self.client.request('PUT', upload_url, headers, data = chunk_bytes))
                        start += chunk_size
        
        except: 
            if 'uploadSession' in upload_url:
                self.client.request('DELETE', upload_url, http_err=False) 
            if checked_out: 
                self.check_in(comment='HTTP error')
                if not self.drive.check_out_required: #otherwise it fails with 500
                    '' # self.restore_version(original_file['versionId'], item_path=dest_path) 
            raise
        else:
            if check_in: self.check_in(item_id=result[-1].json['id'], comment=check_in_comment)
            self._update_vars(result[-1].json)
            return self
        finally:
            if source_path: file_bytes.close()

    def replace (self, source_path:str=None, source_bytes:bytes=None) -> 'File': 
        return self.upload(source_path, source_bytes, 'replace')
    