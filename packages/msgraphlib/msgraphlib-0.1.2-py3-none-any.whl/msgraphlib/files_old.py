### IMPORTS ###

# Python Standard Library
import os, sys, time
from typing import Literal
#import json

# 3rd party
from requests.exceptions import HTTPError

#Local
from .client import Config
from .drive import Drive
if 'graph.excel' in sys.modules: 
    from graph.excel import Workbook
from .common import ModuleNotImported
from .common import ArgumentException
from .common import ItemNotFoundError, ItemLockedError, ItemCheckedOutError
from .common import Metadata
import inspect

### CLASSES ###

#inspect.Traceback()
class Files(Drive):

    def __init__(self, config_id=None, config: Config=None, 
                 drive_id=None, check_out_required:bool=False):
        super().__init__(config_id, config, drive_id, check_out_required)
        self.metadata = Metadata(self)
        self.drive_id = drive_id or os.getenv('GRAPH_DRIVE_ID')
        if 'graph.excel' in sys.modules: 
            self._workbook:Workbook = None

    @property
    def workbook(self):
        if not hasattr(self, '_workbook'): 
            raise ModuleNotImported('workbook')
        elif self._workbook is None:
            wb_class = getattr(sys.modules['graph.excel'], "Workbook")
            self._workbook = wb_class(config_id=self.client._id, drive_id = self.drive_id)
        return self._workbook
         
    def set_drive_id(self, drive_id=None, site_id=None, group_id=None, team_name=None, site_name=None):
        if drive_id: self.drive_id = drive_id
        elif team_name or site_name:
            site_id = self._get_site(self.client, team_name, site_name).json['id']
        if any([site_id, group_id]):
            drive = self._get_default_drive(self.client, drive_id, site_id, group_id, None, None)
        self.drive_id = drive.json['id']

    def get_item(self, item_path:str=None, item_id:str=None, err_if_not_found:bool=False):
        self._validate_drive_request(locals().copy(), ['item_'])
        try: item = self._get_item(item_path, item_id)
        except ItemNotFoundError as err: 
            if err_if_not_found: raise err
            else: return None
        except Exception as err: raise
        return item

    def get_item_props(self, item_path:str=None, item_id:str=None, 
                       select:list=[], expand:list=[], http_err=True):
        self._validate_drive_request(locals().copy(), ['item_'])
        expand_query = f"expand={','.join(expand)}" if expand else ''
        select_query = f"select={','.join(select)}" if select else ''
        query = '&'.join(filter(None, [expand_query, select_query]))
        result = self._get_item(item_path, item_id, query, http_err)
        if result == None: return result
        elif getattr(result, 'ok'): 
            if expand or len(select) != 1: return result.json
            else: return result.json[select[0]]
        else: return result

    
    def restore_version(self, ver_id:str, item_id=None, item_path=None):
        return self._manage_item(locals(), 'POST', f'versions/{ver_id}/restoreVersion')

    def update_folder_content_type(self, folder_id:str=None, folder_path:str=None, 
                                   content_type_name:str=None, content_type_id:str=None):
        # Validate arguments
        self._validate_drive_request(locals(), ['folder_', 'content_type_'])
        
        # Get SharePoint Ids 
        ids = self.get_item_props(folder_path, folder_id, ['sharepointIds'])

        # Get Content Type Id
        if content_type_name:
            content_type = self._get_content_type(ids['siteId'], content_type_name)

        # Update folder
        url = f"/sites/{ids['siteId']}/lists/{ids['listId']}/items/{ids['listItemId']}"
        json = {"contentType": {"id": content_type['id']} }
        return self.client.request('PATCH', url, json = json).json
    

            

        

