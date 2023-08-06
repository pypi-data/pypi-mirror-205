# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable,OrderedDict, Union


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
from volent.Field import Field as _field
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.query.Query import Query


@dataclass
class Insert(Query):
    def __init__(self,model:_t.model_type,data:dict) -> None:
        self._inserts = {}
        super().__init__(model,data)

    @property
    def query(self):
        if isinstance(self.data,(dict)) is False:
            raise ValueError("Data should be a dictionary.")
        data = self._inserts_from_data()
        # data = self.data
        if len(list(self._inserts.keys())) == 0:
            return (False,False)


        # # data = self.filter_dict_by_columns(data)
        # column_list = ', '.join(list(data.keys()))
        # # total_keys = len(list(data.keys()))
        # ph = []
        # for k in list(data.keys()):
        #     ph.append(f"%({k})s")
        # placeholders = ', '.join(ph)
        template = f"""INSERT INTO {self.model.quoted_name} ({self.column_list_string}) VALUES ({self.placeholder_string})"""
        # data_tuple = data.values()
        # print(f"template: {template}")
        # print(f"data_tuple: {data_tuple}")
        return (template,data)

    @property
    def placeholder_string(self)->str:
        '''
            Get this Insert's placeholder_string

            This is the list of value placeholders used to parameterize the query.

            "%(beep)s,%(boop)s"

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-26-2023 11:15:02
            `@memberOf`: Insert
            `@property`: placeholder_string
        '''
        ph = []
        for k in list(self._inserts.keys()):
            ph.append(f"%({k})s")
        return ', '.join(ph)
        return value

    @property
    def column_list_string(self):
        '''
            Get this Insert's column_list_string

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-26-2023 11:13:45
            `@memberOf`: Insert
            `@property`: column_list_string
        '''
        return ', '.join(list(self._inserts.keys()))

    # @property
    # def query(self):
    #     data = self.data

    #     if isinstance(data,(dict)) is False:
    #         raise ValueError("Data should be a dictionary.")

    #     data = self.filter_dict_by_columns(data)
    #     if len(list(data.keys())) == 0:
    #         return (False,False)
    #     column_list = ', '.join(list(data.keys()))
    #     # total_keys = len(list(data.keys()))
    #     ph = []
    #     for k in list(data.keys()):
    #         ph.append(f"%({k})s")
    #     placeholders = ', '.join(ph)
    #     template = f"""INSERT INTO {self.model.quoted_name} ({column_list}) VALUES ({placeholders})"""
    #     # data_tuple = data.values()
    #     # print(f"template: {template}")
    #     # print(f"data_tuple: {data_tuple}")
    #     return (template,data)
    #     # return (template,data_tuple)


    def _inserts_from_data(self):
        data = self.data
        data = self.filter_dict_by_columns(data)
        for k,v in data.items():
            if v != _t.undefined:
                self.add_insert(k,v)
        for col in self.model.columns:
            if col.on_insert != _t.undefined:
                if col.name not in self._inserts:
                    self.add_insert(col.name,col.on_insert)
        return self._inserts

    def add_insert(self,column_name,value):
        self._inserts[column_name] = value




    def execute(self)->Union[bool,dict,int]:

        sql,args= self.query
        if sql is False:
            return False

        print(f"sql:{sql}")
        print(f"args:{args}")

        # @Mstep [] execute the insert query.
        result = self.database.run(sql,args)
        # @Mstep [IF] if the query was successful.
        if result is True:
            # @Mstep [] get the id of the inserted role.
            result = self.database.last_id()
            self.model.primary_column.value = result
            self.model._saved = True
            # result = self.model.select().is_(self.model.primary_column.name,result).execute()

            # if self.return_row is True:
            #     query = f"""SELECT * FROM {self.model.quoted_name} WHERE {self.model.primary_column.name}={result}"""
            #     # s = self.model.select_query()

            #     # s.correlate_to_table = False
            #     # s.add_where(self.table.primary_id.name,result,"=")
            #     # row = s.execute()
            #     if isinstance(row,(list)):
            #         result = row[0]

        # print(f"sql: {sql}")
        # print(f"args: {args}")
        return result
