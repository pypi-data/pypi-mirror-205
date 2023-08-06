# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The relationship module.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 04-28-2023 10:06:56
    `name`: relationship
    * @xxx [04-28-2023 10:07:06]: documentation for relationship
'''


from dataclasses import dataclass
from typing import Iterable, Union
import colemen_utils as c
import volent.settings as _settings
import volent.settings.types as _t

from volent.mixins.MySQLGeneratorMixin import MySQLGeneratorMixin

@dataclass
class Relationship(MySQLGeneratorMixin):
    main:_t._main_type = None
    # database:_t.database_type = None
    model:_t.model_type = None
    name:str = None
    '''The name of this relationship'''
    on_delete:str = None
    '''The action to perform with the parent is deleted'''
    on_update:str = None
    '''The action to perform with the parent is updated'''
    fk_name:str = None
    '''The name used to uniquely identify this relationship in the database.'''

    # _parent_database_name:str = None
    # _parent_model_name:str = None
    # _parent_column_name:str = None

    parent_model:_t.model_type = None
    '''A reference to the parent model instance'''
    parent_column:_t.column_type = None
    '''A reference to the parent model's column instance'''

    child_model:_t.model_type = None
    '''A reference to the child model instance'''
    child_column:_t.model_type = None
    '''A reference to the child model's column instance'''
    # schemas:Iterable[_t.schema_type] = None



    def __init__(
        self,
        child:Union[str,_t.column_type],
        parent:str,
        name:str=None,
        on_delete:str = None,
        on_update:str = None,
        fk_name:str = None,
        ):
        '''
            Create a relationship instance.

            ----------

            Arguments
            -------------------------
            `child` {column}
                The child column of this relationship

            `parent` {str}
                The name (dot path) of the parent column that this relationship represents.

                "tasks.task_id"

            [`name`=None] {str}
                The name of this relationship, if not provided, the variable name is used from its declaration
                in the model.

            [`on_delete`=None] {str}
                The action to perform when the parent row is deleted.

            [`on_update`=None] {str}
                The action to perform when the parent row is updated.

            [`fk_name`=None] {str}
                The name used to uniquely identify this relationship in the database.
                If not provided, a random one will be generated.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 10:07:32
            `memberOf`: Relationship
            `version`: 1.0
            `method_name`: relationship
            * @xxx [04-28-2023 10:11:24]: documentation for relationship
        '''
        self.name = name
        self.on_delete = on_delete
        self.on_update = on_update
        self.parent = parent
        self.child_column = child
        self.fk_name = f"FK_{c.rand.rand()}" if fk_name is None else fk_name




    @property
    def summary(self):
        '''
            Get this Relationship's summary

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 03-23-2023 14:53:39
            `@memberOf`: Relationship
            `@property`: summary
        '''
        value = {
            "name":self.name,
            "fk_name":self.fk_name,
            "on_delete":self.on_delete,
            "on_update":self.on_update,
            "parent_model":self.parent_model.name,
            "parent_column":self.parent_column.name,
            "child_model":self.child_model.name,
            "child_column":self.child_column.name,
            "parent_string":self.parent,
        }
        return value


    # def locate_parent(self):
    #     database = self._parent_database_name
    #     model = self._parent_model_name
    #     column = self._parent_column_name
    #     if database is not None:
    #         self.main






# def _parse_parent(relationship:Relationship,value):
#     value = c.string.strip_excessive_chars(value,["."])
#     pl = value.split(".")
#     if len(pl) == 3:
#         relationship._parent_database_name = pl[0]
#         relationship._parent_model_name = pl[1]
#         relationship._parent_column_name = pl[2]
#     if len(pl) == 2:
#         relationship._parent_model_name = pl[0]
#         relationship._parent_column_name = pl[1]
#     if len(pl) == 1:
#         relationship._parent_column_name = pl[0]