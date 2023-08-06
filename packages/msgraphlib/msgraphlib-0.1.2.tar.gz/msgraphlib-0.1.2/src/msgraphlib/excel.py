### IMPORTS ###

# Python Standard Library
import os
from typing import Union, Literal
from datetime import datetime

# 3rd party
# ...

#Local
from .core import Config, _BaseApp
from .core import Metadata
from .core import _GraphObject, _GraphCollection, _CollectionProp
from .core import ReadOnlyProp, ReadWriteProp
from .core import ArgumentException, ValidationError
from .core import _validate_args
#from .common import _xor
from .drive import Drive, File

### CLASSES ###

# class Excel(_BaseApp):

#     def __init__(self, config_id=None, config: Config=None, 
#                  drive_id:str=None, check_out_required:bool=False):
#         super().__init__(config_id, config)
#         self.metadata = Metadata(self)
#         self._drive:dict[Drive] = {}
#         self.active_drive = self._drive.setdefault(drive_id, Drive(self.client, drive_id, check_out_required))
#         self._workbook:dict[Workbook] = {}

#     def __call__(self, drive_id:str=None, check_out_required:bool=False):
#         drive_id = drive_id or os.getenv('GRAPH_DRIVE_ID')
#         self.active_drive = self._drive.setdefault(
#             drive_id, Drive(drive_id, check_out_required))
  
#     def workbook(self, drive_id:str, file_path:str=None, file_id:str=None) -> 'Workbook':
#         _validate_args(locals(), ['file_'])
#         key = file_id or file_path
#         return (self._workbook.get(key) or self._workbook.setdefault(
#             key, Workbook(self, file_path, file_id)))
#         # return next((wb for wb in self._workbook if wb['file_id'] == file_id), 
#         #             Workbook(self, file_id))

class Worksheets(_GraphObject, _GraphCollection):

    def __init__(self, parent:'Workbook'):
        super().__init__(parent=parent, name='worksheets',
                         stock_name='_worksheet', member_class=Worksheet)
        self._dict = parent._worksheet
        
    def add(self, name:str) -> 'Worksheet':
        return self.parent.worksheet(name).add()

class Tables(_GraphObject, _GraphCollection):

    def __init__(self, parent:_GraphObject):
        super().__init__(parent=parent, name='tables',
                         stock_name='_table', member_class=Table)
        self._dict = parent._tables

    def add(self, address:str, has_headers:bool=True) -> 'Table':
        return self.parent.table().add(address, has_headers)

class Names(_GraphObject, _GraphCollection):

    def __init__(self, parent:_GraphObject):
        super().__init__(parent=parent, name='names',
                         stock_name='_name', member_class=Name)
        
    def add(self, reference:str=None) -> 'Name':
        return self.parent.add(reference)
    
class Workbook(_GraphObject):

    worksheets = type('XLSheetCollection',(_CollectionProp,), {'cls': Worksheets})()
    tables = type('XLTableCollection',(_CollectionProp,), {'cls': Tables})()
    names = type('XLNameCollection',(_CollectionProp,), {'cls': Names})()

    def __init__(self, file:File):
        super().__init__(file)
        self.file_id = file.id #or self.get_item_id(file_path) 
        self.file_path = file.path
        self.url_id = f'{file.url_id}/workbook' if file.url_id else None
        self.url_path = f'{file.url_path}/workbook' if file.url_path else None
        self.url = self.url_id or self.url_path
        self.workbook_session = {}
        self.requests_session = ...
        self.worksheets:Worksheets #DBG
        self._worksheet:dict[Worksheet] = {}
        self.tables:Tables #DBG
        self._table:dict[Table] = {}
        self.names:Names #DBG
        self._name:dict[Name] = {}

    def request(self, verb, url, headers, data, json, files, http_err):
        return self.client.request(verb, url, headers, data, json, files, 
                                   http_err, self.requests_session)

    # @property
    # def worksheets(self) -> 'Worksheets':
    #     return (getattr(self, '_worksheets', None) or 
    #             self.__dict__.setdefault('_worksheets', Worksheets(self)))
    
    def worksheet(self, name:str=None, id:str=None, first:bool=False) -> 'Worksheet':
        if first: 
            sheet = list(self._worksheet.items())[0:1] or Worksheet(self, first=first)
            return self._worksheet.setdefault(vars(sheet)['name'], sheet)
        return (self._worksheet.get(name or id) or 
                self._worksheet.setdefault(name or id, Worksheet(self, name, id, first)))

    # @property
    # def tables(self) -> 'Tables':
    #     return (getattr(self, '_tables', None) or 
    #             self.__dict__.setdefault('_tables', Tables(self)))
    
    def table(self, name:str=None, id:str=None) -> 'Table':
        return (self._table.get(name or id) or 
                self._table.setdefault(name or id, Table(self, name=name, id=id)))
    
    # @property
    # def names(self) -> 'Tables':
    #     return (getattr(self, '_names', None) or 
    #             self.__dict__.setdefault('_names', Names(self)))

    def name(self, name:str) -> 'Name':
        return (self._name.get(name) or 
                self._name.setdefault(name, Name(self, name)))

    def create_session (self, persist_changes:bool=True):
        if self.workbook_session: raise ValidationError('Session already exists')
        data = f'{ "persistChanges": {persist_changes} }'
        result = self.client.request('POST', f"{self.url}/createSession", data).json
        self.workbook_session = result
        self.requests_session = self.client.session(result['id'])
        header = {'workbook-session-id': self.session['id']} if self.session else {}
        self.requests_session.headers.update(header)
        return result

    def close_session (self, file_id, session_id):
        headers = { "workbook-session-id": f"'{self.workbook_session['id']}'" }
        result = self.client.request('POST', f"{self.url}/closeSession", headers = headers)
        if result.status_code == 204: 
            self.requests_session = None
            self.workbook_session = None
        return result
    
    def list_worksheets(self, limit:int=None):
        top = f"?$top={limit}" if limit else ''
        sheets = self.request('GET', f"{self.url}/worksheets{top}").json['value']
        output = []
        for sheet in sheets:
            self._worksheet[['name']] = Worksheet(self, json=sheet)
            output.append(self._worksheet[['name']])
        return output

    def list_tables(self):
        tables = self.request('GET', F"{self.url}/tables").json['value']
        output = []
        for table in tables:
            self._table[table['name']] = Table(self, json=table)
            output.append(self._table[table['name']])
        return output
    
    def list_names(self):
        names = self.request('GET', F"{self.url}/names").json['value']
        output = []
        for name in names:
            self._name[name['name']] = Name(self, json=name)
            output.append(self._name[name['name']])
        return output

    def function(self, function_name:str, fx_args:dict):
        kwargs = {'url': f"{self.url}/functions{function_name}", 'json': fx_args}
        return self.request('POST', **kwargs)

    def vlookup(self, lookup_value, range_address:'Range', col_idx:int, 
                match_mode:Literal['exact', 'approx']='exact'):
        json = {
            "lookupValue": lookup_value,
            "tableArray": { "Address": range_address },
            "colIndexNum": col_idx,
            "rangeLookup": False if match_mode == 'exact' else True
        }
        return self.function('vlookup', json)

# class _WorkbookObject():

#     def __init__(self, parent, **kwargs):
#         self.workbook:Workbook = getattr(parent, 'workbook', parent)

class Worksheet(_GraphObject):

    id = ReadOnlyProp()
    name = ReadWriteProp()
    visibility = ReadWriteProp()
    tables = type('XLTableCollection',(_CollectionProp,), {'cls': Tables})()
    names = type('XLNameCollection',(_CollectionProp,), {'cls': Names})()

    def __init__(self, workbook:Workbook, name:str=None, id:str=None,
                 first:bool=False, json:dict=None):
        self.workbook = workbook
        self.__dict__['name'] = name
        if first: 
            url = f"{workbook.url}/worksheets?$top=1"
            json = workbook.request('GET', url).json['value'][0]
        super().__init__(parent=workbook, json = json)
        self.tables:Tables #DBG
        self._table:dict[Table] = {}
        self.names:Names #DBG
        self._name:dict[Name] = {}
        self._range:dict[Range] = {}
        self.url = f"{workbook.url}/worksheets/{vars(self)['name'] or id}"
        self.url_add = f"{workbook.url}/worksheets"

    def add (self) -> 'Worksheet':
        data = { "name": self.name } if self.__dict__['name'] else None
        sheet = self.workbook.request('POST', self.url_add, json=data).json
        self._update_vars(sheet)
        return self
    
    def delete(self):
        response = self.workbook.request('DELETE', self.url).json
        del self.workbook._worksheet[self.__dict__['name']]
        return response

    def table(self, name:str=None, id:str=None) -> 'Table':
        return (self._table.get(name or id) or 
                self._table.setdefault(name or id, Table(self, name, id)))
    
    def range(self, address:str=None) -> 'Range':
        return (self._range.get(address) or 
                self._range.setdefault(address, Range(self, address=address)))
    
    @property
    def used_range(self) -> 'Range':
        return (self._range.get('usedRange') or self._range.setdefault(
            'usedRange', Range(table=self, type='usedRange')))

class Table(_GraphObject):

    id = ReadOnlyProp()
    name = ReadWriteProp()
    highlightFirstColumn = ReadWriteProp()
    highlightLastColumn = ReadWriteProp()
    showBandedRows = ReadWriteProp()
    showBandedRows = ReadWriteProp()
    showFilterButton = ReadWriteProp()
    showHeaders = ReadWriteProp()
    showTotals = ReadWriteProp()
    style = ReadWriteProp()

    def __init__(self, workbook:Workbook=None, worksheet:Worksheet=None, 
                 name:str=None, id:str=None, json:dict=None):
        self.__dict__['id'] = id 
        self.__dict__['name'] = name   
        super().__init__(parent = workbook or worksheet, json = json)
        self.workbook = workbook or self.parent.workbook
        self.url = f"{self.parent.url}/tables/{id or name}"
        self.url_add = f"{self.parent.url}/tables/add"
        self._range:dict[Range] = {}

    def add (self, address:str=None, has_headers:bool=True) -> 'Table':
        data = { "address": address, 'hasHeaders': has_headers }
        table = self.workbook.request('POST', self.url_add, data).json
        if self.__dict__.get('name') != table['name']:
            self.name = table['name']
        self._update_vars(table)
        return table
    
    @property
    def range(self) -> 'Range':
        return (self._range.get('full') or 
                self._range.setdefault('full', Range(table=self)))
    
    @property
    def data_body_range(self):
        return (self._range.get('dataBody') or self._range.setdefault(
            'dataBody', Range(table=self, type='dataBodyRange')))
    
    @property
    def header_row_range(self):
        return (self._range.get('headerRow') or self._range.setdefault(
            'headerRow', Range(table=self, type='headerRowRange')))
    
    @property
    def total_row_range(self):
        return (self._range.get('totalRow') or self._range.setdefault(
            'totalRow', Range(table=self, type='totalRowRange')))
    
class Name(_GraphObject):

    name = ReadOnlyProp()
    scope = ReadOnlyProp()
    type = ReadOnlyProp()
    value = ReadOnlyProp()
    query = False

    def __init__(self, workbook:Workbook, worksheet:Worksheet=None, 
                 name:str=None, json:dict=None):
        self.__dict__['name'] = name
        super().__init__(parent = workbook or worksheet, json = json)
        self.workbook = self.parent.workbook
        self.url = f"{self.parent.url}/names/{name}"
        self.url_add = f"{self.parent.url}/names/add"
        self.value = {}
        self.range:Range = None
        self.visible = True

    def add (self, reference:str=None) -> 'Name':
        data = { "name": self.name, 'reference': reference }
        name_item = self.workbook.request('POST', self.url_add, data).json
        self._update_vars(name_item); self.request
        return name_item

    @property
    def range(self) -> 'Range':
        return (self.range or self.__dict__.setdefault('range', Range(name=self)))
    
class Range(_GraphObject):

    address = ReadOnlyProp()
    cellCount = ReadOnlyProp()
    columnCount = ReadOnlyProp()
    formulas = ReadWriteProp()
    numberFormat = ReadWriteProp()
    text = ReadOnlyProp()
    valueTypes = ReadOnlyProp()
    values = ReadWriteProp()
    query = False

    def __init__(self, worksheet:Worksheet=None, table:Table=None, name:Name=None, 
                 range:'Range'=None, scope:Name=None, address:str=None, json:dict=None):
        self.address = address
        self.scope = scope
        super().__init__(parent = worksheet or table or name or range, json = json)
        self.workbook = self.parent.workbook
        self.url = self._url(self.parent, scope, self.address)
        self._values = {}

    def _url (self, parent, scope, address:str):
        address = f"(address='{address}')" if address else ''
        if parent.__class__.__name__ == 'Range': 
            url = parent.url.rpartition('/range')
            return f"{url[0]}{url[1]}{address}"
        else: return f"{parent.url}/{scope or 'range'}{address}"
    
    def update(self, values: list[list]=None, format: list[str]=None) -> 'Range':
        json = {}
        if values: json["values"] = values
        if format: json["numberFormat"] = format * len(values)
        response = self.workbook.request('PATCH', self.url, json = json)
        self._update_vars(response.json)
        return self

    def intersection(self, another_range_address:str) -> 'Range':
        json = {'anotherRange': another_range_address}
        response = self.workbook.request('GET', f"{self.url}/intersection", json = json)
        return Range(range=self, json = response.json)
    
    def used_range(self, values_only:bool=True) -> 'Range':
        json = {'valuesOnly': values_only}
        response = self.workbook.request('GET', f"{self.url}/usedRange", json = json)
        return Range(range=self, json = response.json)

class _ExcelCollection(_CollectionProp):

    objects = {'worksheets': Worksheets,
               'tables': Tables,
               'names': Names}
#---------------------------------------------------------------------------
    # def col_idx_to_id(self, idx, base=1):
    #     # 26 = number of ASCII letters | chr(65) = 'A'
    #     d, m = divmod((idx - base), 26) 
    #     return self.col_idx_to_id(d - 1 + base, base) + chr(m + 65) if d else chr(m + 65) 

    # def _url(self, file_id, sheet=None, name=None, table=None, range=None):
    #     if sheet: target_range = f"worksheets/{sheet}/range(address='{range}')"
    #     elif name: target_range = f"names/{name}/range"
    #     elif table: target_range = f"tables/{table}/{range}"
    #     return f'/drives/{self.drive_id}/items/{file_id}/workbook/{target_range}'
    

    # def get_range(self, file_id:str=None, file_path:str=None,
    #               sheet_name: str=None, range_address: str=None, range_name: str=None,
    #               used_range:bool=False,
    #               intersect:str=None,
    #               row_resize:int=None, col_resize:int=None,
    #               row_offset:int=None, col_offset:int=None):
    #     self._validate_drive_request(locals().copy(), ['file_'])
    #     file_id = file_id or self.get_item_id(file_path)   
    #     url = self._url(file_id, sheet_name, range_name, range=range_address)
    #     if used_range: url += "/usedRange"
    #     return self.client.request('GET', url, headers = self.session.get(file_id)).json



    # def update_range(self, file_id:str=None, file_path:str=None, 
    #                  sheet_name: str=None, range_address: str=None, range_name: str=None,
    #                  used_range:bool=False,
    #                  values: list[list]=None, format: list[str]=None, auto_format: bool=False,
    #                  row: int=None, col: Union[int, str]=None):
    #     self._validate_drive_request(locals().copy(), ['file_', 'range_'])
    #     if not range_address:
    #         first_cell = f"{self.col_idx_to_id(col) if col.isnumeric() else col}{row}"
    #         last_cell = f"{self.col_idx_to_id(col - 1 + len(values[0]))}{row - 1 + len(values)}"
    #         range_address = f"{first_cell}:{last_cell}"
    #     url = self._url(file_id, sheet_name, range_name, range=range_address) + "/usedRange"
    #     json = {"values" : values}
    #     if format: data |= {"numberFormat": format * len(values)}
    #     return self.client.request('PATCH', url, json = json)



    # def get_number_format(self, value):
    #     if isinstance(value, int): format = ''
    #     elif isinstance(value, int): format = ''
    #     else: format = ''
    #     return format
    
    # def get_date_format(date_string):
    #     formats = {
    #         "%Y{*}%m{*}%d": "yyyy{*}mm{*}dd",
    #         "%Y{*}%m{*}%d %H:%M:%S": "yyyy{*}mm{*}dd hh:mm:ss",
    #         "%d{*}%m{*}%Y": "dd{*}mm{*}yyyy",
    #     }
    #     for f in formats: 
    #         for s in ['-','/','.']: 
    #             try:
    #                 if datetime.strptime(date_string, f.replace('{*}', s)):
    #                     return formats[f].replace('{*}', s)
    #             except: pass

