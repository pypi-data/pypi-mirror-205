### IMPORTS ###

# Python Standard Library
import os
import json

# 3rd party
# ...

#Local
# from graph.api import API
from .core import _BaseApp, Config, Client
from .core import Metadata
from .core import ArgumentException
from .core import Metadata


### CLASSES ###

class _Sharepoint():

    def _get_site(self, site_name=None, team_name=None):
        url = f"/sites/share.lighting.com:" 
        if team_name: url += f"/teams/{team_name}"
        elif site_name: url += f"/sites/{site_name}"
        else: raise ValueError('Provide one of the arguments: team_name, site_name')
        try: site = self.client.request('GET', url)
        except Exception as err:
            if err.args[0]['status'] == 404 and err.args[0]['error']:
                if err.args[0]['error'].get('message') == 'Requested site could not be found':
                    return err.args[0]
            else: raise
        return site

    def _get_content_type(self, site_id, content_type_name):
        url = f"/sites/{site_id}/contentTypes?$filter=name eq '{content_type_name}'"
        result = self.client.request('GET', url)
        return result.json['value'][0]
    
class Site(_BaseApp, _Sharepoint):
    ...
    # def __init__(self, creds_arn_id='', creds: AzureCreds=None, drive_id=''):
    #     self.metadata = Metadata(self)
    #     super().__init__(creds_arn_id, creds)
    #     self.drive_id = drive_id or os.getenv('GRAPH_DRIVE_ID')

    # def get_site(self, team_name=None, site_name=None):
    #     return _Utils._get_site(self.client, team_name, site_name)

class List(_BaseApp):

    # def __init__(self, creds_arn_id='', creds: AzureCreds=None, drive_id=''):
    #     super().__init__(creds_arn_id, creds)
         
    def get_xyz(self, input):
        return '___' + input + '___'

