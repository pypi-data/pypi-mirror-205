# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from time import time
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
    def __init__(self,model:_t.model_type,data:Union[dict,list]) -> None:
        self._inserts = {}
        self._multi_inserts = []
        self._is_multi = False
        self._unique_columns = []
        super().__init__(model,data)

    @property
    def query(self):
        if isinstance(self.data,(dict,list)) is False:
            raise ValueError("Data should be a dictionary or list.")
        data = self._inserts_from_data()
        if self._is_multi is True:
            return self._multi_query
        # data = self.data
        if len(list(self._inserts.keys())) == 0:
            return (False,False)

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
        if self._is_multi is True:
            master_ph = []
            ph_data = {}
            for idx,row in enumerate(self._multi_inserts):
                ph = []
                for k,v in row.items():
                    key = f"{k}{idx}"
                    ph_key = f"%({key})s"
                    ph.append(ph_key)
                    ph_data[key] = v
                ph_string = ', '.join(ph)
                master_ph.append(f"({ph_string})")
            master_ph = ', '.join(master_ph)
            return (master_ph,ph_data)

        ph = []
        for k in list(self._inserts.keys()):
            ph.append(f"%({k})s")
        return ', '.join(ph)

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
        if self._is_multi is True:
            return ','.join(self._unique_columns)
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

    @property
    def _multi_query(self):
        '''
            Get this Insert's _multi_query

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-27-2023 09:31:16
            `@memberOf`: Insert
            `@property`: _multi_query
        '''

        place_holders,data = self.placeholder_string

        template = f"""INSERT INTO {self.model.quoted_name} ({self.column_list_string}) VALUES {place_holders}"""

        return (template,data)

    def _inserts_from_data(self):
        data = self.data
        # @Mstep [IF] if the data is a list.
        if isinstance(data,(list)):
            self._is_multi = True


            # @Mstep [LOOP] iterate the list of datas
            for d in data:
                # @Mstep [IF] if the element is not a dictionary
                if isinstance(d,(dict)) is False:
                    # @Mstep [] skip that shit.
                    continue
                d_insert = {}

                # @Mstep [] filter and sort the element by the columns of the model.
                d = self.sort_dict_by_columns(self.filter_dict_by_columns(d))
                # @Mstep [IF] if the filtered dict has no keys
                if len(d.keys()) == 0:
                    # @Mstep [] skip this element.
                    continue


                # @Mstep [loop] Iterate the items in the dict.
                for k,v in d.items():
                    self.__add_unique_coluumn(k)
                    # @Mstep [IF] if the value is not undefined.
                    if v != _t.undefined:
                        # @Mstep [] add the key and value to the d_insert dict.
                        d_insert[k] = v
                # @Mstep [LOOP] iterate the model columns.
                for col in self.model.columns:
                    # @Mstep [IF] if thhe column has an on_insert value.
                    if col.on_insert != _t.undefined:
                        # @Mstep [IF] if the column is not already being set.
                        if col.name not in d_insert:
                            # @Mstep [] set the key and value on d_insert.
                            d_insert[col.name] = col.on_insert
                            self.__add_unique_coluumn(col.name)
                # @Mstep [] append the d_insert dictionary to self._multi_inserts.
                self._multi_inserts.append(d_insert)

            # @Mstep [RETURN] return the _multi_inserts list.
            return self._multi_inserts

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

    def __add_unique_coluumn(self,name):
        '''Add a name to the unique columns list if it is not already apart.'''
        if name not in self._unique_columns:
            self._unique_columns.append(name)


    def execute(self,return_result:bool=False,foreign_key_checks:bool=True)->Union[bool,dict,int]:
        '''
            Execute the insert operation on the model.

            ----------

            Arguments
            -------------------------
            [`return_result`=False] {bool}
                If True, it will run a select query to gather the newly inserted row.
                If False, it will return only the ID of the newly inserted row.

            [`foreign_key_checks`=True] {bool}
                If False, the query will not perform foreign key checks before executing the insertion.
                Be careful, this can cause integrity issues and will NOT warn you about it.


            Return {bool,dict,int}
            ----------------------
            The id of the inserted row or the entire row if return_result is True.



            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:34:05
            `memberOf`: Delete
            `version`: 1.0
            `method_name`: execute
            * @xxx [04-28-2023 07:40:57]: documentation for execute
        '''
        sql,args= self.query
        if sql is False:
            return False

        # print(f"volent.query.insert.sql:{sql}")
        # print(f"volent.query.insert.args:{args}")
        start = time()
        # @Mstep [] execute the insert query.
        result = self.database.run(sql,args,foreign_key_checks=foreign_key_checks)
        # @Mstep [IF] if the query was successful.
        if result is True and return_result is True:
            # @Mstep [] get the id of the inserted role.
            result = self.database.last_id()
            self.model.primary_column.value = result
            self.model._saved = True
            result = self.model.select().is_(self.model.primary_column.name,result).execute()
        if result is True and return_result is False:
            result = self.database.last_id()


        # print(f"sql: {sql}")
        # print(f"args: {args}")
        print(f"insert execute duration: {time() - start}")
        return result
