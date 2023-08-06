# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The full text index module

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 04-28-2023 06:53:30
    `name`: FullTextIndex
    * @xxx [04-28-2023 06:53:50]: documentation for FullTextIndex
'''




from dataclasses import dataclass
from typing import Iterable
import colemen_utils as c
# import volent.settings as _settings
import volent.settings.types as _t
from volent.mixins.MySQLGeneratorMixin import MySQLGeneratorMixin

@dataclass
class FullTextIndex(MySQLGeneratorMixin):
    '''The class used to define a fulltext index on a model.'''
    main:_t._main_type = None
    # database:_t.database_type = None
    model:_t.model_type = None
    name:str = None
    comment:str = None
    columns:Iterable[_t.column_type] = None
    # comment:str = None




    def __init__(
        self,
        columns:Iterable[_t.column_type],
        name:str=None,
        # comment:str=None,
        ):
        '''
            Create a full text index on a model's column(s).

            ----------

            Arguments
            -------------------------
            `Columns` {list,column}
                A column or list of columns to create a fulltext index on.

            `name` {str}
                The name of this fulltext index, this does not appear in the SQL but can be used
                within volent to find a specific fulltext index.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 06:54:27
            `memberOf`: FullTextIndex
            `version`: 1.0
            `method_name`: FullTextIndex
            * @xxx [04-28-2023 06:56:30]: documentation for FullTextIndex
        '''
        self.name = name
        # self.comment = comment
        self.columns = c.arr.force_list(columns)



        # _parse_parent(self,parent)


    @property
    def summary(self):
        '''
            Get this FullTextIndex's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-23-2023 14:53:39
            `@memberOf`: FullTextIndex
            `@property`: summary
        '''
        value = {
            "name":self.name,
            # "comment":self.comment,
            "columns":[x.name for x in self.columns],
        }
        return value


    def __hash__(self):
        col_names = [x.name for x in self.columns]
        val = col_names.append(self.name)
        return hash(val)

    def __eq__(self,other):
        if isinstance(other,FullTextIndex):
            return self.__hash__() == other.__hash__()
        return False

