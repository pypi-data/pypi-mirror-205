# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The main module of the volent library.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 04-28-2023 07:03:18
    `name`: volent
    * @xxx [04-28-2023 07:03:34]: documentation for volent
'''



from dataclasses import dataclass
import os
from string import Template
from typing import Iterable, Union
import colemen_utils as c
import volent.settings as _settings



@dataclass
class ReverseEngineer():
    def __init__(
        self
        ):
        pass

    def from_dict(self,data:Union[str,dict]):
        if isinstance(data,(str)):
            if c.file.exists(data):
                data = c.file.read.as_json(data)
        # from volent.Model import Model as Model
        dbs = data['databases']
        for db in dbs:
            models = []
            for model in db['models']:
                models.append(_gen_model_from_dict(model))


MODEL_CREATE_TEMPLATE = """
@dataclass
class $class_name(Model):
    '''$description'''
    __table_name__ = "$name"
    __database_name__ = "$data_base_name"
    __meta_columns__ = $meta_columns

    def __init__(
        self,
$col_args
        _is_root:bool = False
        ) -> None:
        data = {}

$col_declarations
$relationship_declarations
$unique_constraint_declarations
$fulltext_declarations
        
        
        for col in self.columns:
            lcl = locals()
            if col.name in lcl:
                data[col.name] = lcl[col.name]


        super().__init__(_is_root=_is_root,**data)

"""
def _gen_model_from_dict(data:dict):

    def __col_arg_list(cols:list):
        args = []
        for col in cols:
            val = f"{' ' * 8}{col['name']}:{col['data_type']['python_type_name']} = None"
            args.append(val)
        return ',\n'.join(args)

    def __col_declarations(cols:list):
        args = []
        for col in cols:
            args.append(_gen_column_create(col))
        return '\n'.join(args)
    def __relationship_declarations(rels:list):
        args = []
        for rel in rels:
            args.append(_gen_relationship(rel))
        return '\n'.join(args)
    def __unique_constraint_declarations(rels:list):
        args = []
        for rel in rels:
            args.append(_gen_unique_constraint(rel))
        return '\n'.join(args)
    def __fulltext_declarations(rels:list):
        args = []
        for rel in rels:
            args.append(_gen_fulltext_index(rel))
        return '\n'.join(args)


    s = Template(MODEL_CREATE_TEMPLATE)
    name = c.obj.get_kwarg('name',None,(str),**data)
    class_name = c.obj.get_kwarg('class_name',c.string.to_pascal_case(name),(str),**data)
    description = c.obj.get_kwarg('description',f"Defines a {name} entity",(str),**data)
    data_base_name = c.obj.get_kwarg(['data_base_name','database_name'],"",(str),**data)
    meta_columns = c.obj.get_kwarg('meta_columns',True,(bool),**data)



    val = s.substitute(
        name=name,
        class_name=class_name,
        description=description,
        data_base_name=data_base_name,
        meta_columns=meta_columns,
        col_args=__col_arg_list(data['columns']),
        col_declarations=__col_declarations(data['columns']),
        relationship_declarations=__relationship_declarations(data['relationships']),
        unique_constraint_declarations=__unique_constraint_declarations(data['unique_constraints']),
        fulltext_declarations=__fulltext_declarations(data['fulltext_indexes']),

    )

    return val

COLUMN_CREATE_TEMPLATE = """${indent}self.$name = Column($data_type($data_length)$args)"""
def _gen_column_create(col:dict):
    indent = " " * 8
    s = Template(COLUMN_CREATE_TEMPLATE)

    unique = c.obj.get_kwarg('unique',None,(bool),**col)
    fulltext = c.obj.get_kwarg('fulltext',None,(bool),**col)
    is_foreign_key = c.obj.get_kwarg('is_foreign_key',None,(bool),**col)
    is_primary = c.obj.get_kwarg('is_primary',None,(bool),**col)
    auto_increment = c.obj.get_kwarg('auto_increment',None,(bool),**col)
    nullable = c.obj.get_kwarg('nullable',None,(bool),**col)
    on_insert = c.obj.get_kwarg('on_insert',"no_on_insert",None,**col)
    on_update = c.obj.get_kwarg('on_update',"no_on_update",None,**col)
    default = c.obj.get_kwarg('default',None,None,**col)
    comment = c.obj.get_kwarg('comment',None,(str),**col)

    args = []

    if unique is True:
        args.append("unique=True")

    if fulltext is True:
        args.append("fulltext=True")

    if is_foreign_key is True:
        args.append("is_foreign_key=True")

    if is_primary is True:
        args.append("is_primary=True")

    if auto_increment is True:
        args.append("auto_increment=True")

    if nullable is True:
        args.append("nullable=True")

    if on_insert != "no_on_insert":
        args.append(f"on_insert={col['on_insert']}")

    if on_update != "no_on_update":
        args.append(f"on_update={col['on_update']}")

    if default != "no default":
        args.append(f"default={col['default']}")

    if isinstance(comment,(str)):
        if len(comment) > 0:
            comment = comment.replace("'","\'")
            args.append(f"comment='{comment}'")

    arg_string_list = ""
    if len(args) > 0:
        arg_string_list = ', '.join(args)
        arg_string_list = f",{arg_string_list}"

    data_length = ""
    if isinstance(col['data_type']['data_length'],(int)):
        data_length = col['data_type']['data_length']


    val = s.substitute(
        indent=indent,
        name=col['name'],
        data_type=col['data_type']['class_name'],
        data_length=data_length,
        args=arg_string_list,
    )


    return val

RELATIONSHIP_CREATE_TEMPLATE = """${indent}self.$name = Relationship(self.$child_column,"$parent_string",on_delete="CASCADE",on_update="CASCADE")"""
def _gen_relationship(rel:dict):
    indent = " " * 8
    s = Template(RELATIONSHIP_CREATE_TEMPLATE)

    args = []

    name = c.obj.get_kwarg('name',None,(str),**rel)
    parent_string = c.obj.get_kwarg('parent_string',None,(str),**rel)
    if parent_string is None:
        parent_model = c.obj.get_kwarg(['parent_model','parent_table'],None,(str),**rel)
        parent_column = c.obj.get_kwarg(['parent_column'],None,(str),**rel)
        parent_string = f"{parent_model}.{parent_column}"
    on_delete = c.obj.get_kwarg('on_delete',None,(str),**rel)
    on_update = c.obj.get_kwarg('on_update',None,(str),**rel)
    child_column = c.obj.get_kwarg('child_column',None,(str),**rel)
    
    if isinstance(on_delete,(str)):
        args.append(f"on_delete='{on_delete}'")
    if isinstance(on_update,(str)):
        args.append(f"on_update='{on_update}'")

    arg_string_list = ""
    if len(args) > 0:
        arg_string_list = ', '.join(args)
        arg_string_list = f",{arg_string_list}"

    val = s.substitute(
        indent=indent,
        name=name,
        parent_string=parent_string,
        child_column=child_column,
        args=arg_string_list,
    )


    return val

UNIQUE_CONSTRAINT_TEMPLATE = """${indent}self.$name = UniqueConstraint(columns=[$columns])"""
def _gen_unique_constraint(rel:dict):
    indent = " " * 8
    s = Template(UNIQUE_CONSTRAINT_TEMPLATE)

    args = []

    name = c.obj.get_kwarg('name',None,(str),**rel)
    columns = c.obj.get_kwarg('columns',None,(list),**rel)
    # if parent_string is None:
    #     parent_model = c.obj.get_kwarg(['parent_model','parent_table'],None,(str),**rel)
    #     parent_column = c.obj.get_kwarg(['parent_column'],None,(str),**rel)
    #     parent_string = f"{parent_model}.{parent_column}"
    # on_delete = c.obj.get_kwarg('on_delete',None,(str),**rel)
    # on_update = c.obj.get_kwarg('on_update',None,(str),**rel)
    # child_column = c.obj.get_kwarg('child_column',None,(str),**rel)
    
    # if isinstance(on_delete,(str)):
    #     args.append(f"on_delete='{on_delete}'")
    # if isinstance(on_update,(str)):
    #     args.append(f"on_update='{on_update}'")

    column_list_string = ""
    if len(columns) > 0:
        cols = [f"self.{x}" for x in columns]
        column_list_string = ', '.join(cols)

    val = s.substitute(
        indent=indent,
        name=name,
        columns=column_list_string,
    )


    return val

FULLTEXT_TEMPLATE = """${indent}self.$name = FullTextIndex([$columns])"""
def _gen_fulltext_index(rel:dict):
    indent = " " * 8
    s = Template(FULLTEXT_TEMPLATE)

    # args = []

    name = c.obj.get_kwarg('name',None,(str),**rel)
    columns = c.obj.get_kwarg('columns',None,(list),**rel)

    column_list_string = ""
    if len(columns) > 0:
        cols = [f"self.{x}" for x in columns]
        column_list_string = ', '.join(cols)

    val = s.substitute(
        indent=indent,
        name=name,
        columns=column_list_string,
    )


    return val






td ={
    "name": "task_id",
    "data_type": {
        "sql_type_name": "INTEGER",
        "data_length": None,
        "python_type_name": "int",
        "class_name": "Integer"
    },
    "default": "no default",
    "unique": False,
    "fulltext": False,
    "nullable": False,
    "comment": None,
    "is_foreign_key": False,
    "is_primary": True,
    "auto_increment": True
}

td = {
        "name": "timestamp",
        "data_type": {
            "sql_type_name": "INTEGER",
            "data_length": None,
            "python_type_name": "int",
            "class_name": "Integer"
        },
        "default": None,
        "unique": False,
        "fulltext": False,
        "nullable": True,
        "comment": "The unix timestamp of when this was last modified, None otherwise.",
        "is_foreign_key": False,
        "is_primary": False,
        "auto_increment": False
    }

tdr =                         {
    "name": "parent_task",
    "fk_name": "FK_DQGjBpjafi0D",
    "on_delete": "CASCADE",
    "on_update": "CASCADE",
    "parent_model": "tasks",
    "parent_column": "task_id",
    "child_model": "tasks",
    "child_column": "parent_task_id"
}
tdu = {
    "name": "UQ_tasks_title",
    "comment": "Ensure the title is unique.",
    "columns": [
        "title"
    ]
}
tdft =                         {
                            "name": "FT_tasks_title",
                            "columns": [
                                "title"
                            ]
                        }


table =                 {
                    "name": "tasks",
                    "description": "Defines a Task Entity",
                    "columns": [
                        {
                            "name": "task_id",
                            "data_type": {
                                "sql_type_name": "INTEGER",
                                "data_length": None,
                                "python_type_name": "int",
                                "class_name": "Integer"
                            },
                            "default": "no default",
                            "unique": False,
                            "fulltext": False,
                            "nullable": False,
                            "comment": None,
                            "is_foreign_key": False,
                            "is_primary": True,
                            "auto_increment": True
                        },
                        {
                            "name": "title",
                            "data_type": {
                                "sql_type_name": "VARCHAR",
                                "data_length": 255,
                                "python_type_name": "str",
                                "class_name": "String"
                            },
                            "default": "no default",
                            "unique": True,
                            "fulltext": True,
                            "nullable": False,
                            "comment": None,
                            "is_foreign_key": False,
                            "is_primary": False,
                            "auto_increment": False
                        },
                        {
                            "name": "description",
                            "data_type": {
                                "sql_type_name": "VARCHAR",
                                "data_length": 500,
                                "python_type_name": "str",
                                "class_name": "String"
                            },
                            "default": "no default",
                            "unique": False,
                            "fulltext": False,
                            "nullable": False,
                            "comment": None,
                            "is_foreign_key": False,
                            "is_primary": False,
                            "auto_increment": False
                        },
                        {
                            "name": "start_timestamp",
                            "data_type": {
                                "sql_type_name": "INTEGER",
                                "data_length": None,
                                "python_type_name": "int",
                                "class_name": "Integer"
                            },
                            "default": None,
                            "unique": False,
                            "fulltext": False,
                            "nullable": True,
                            "comment": None,
                            "is_foreign_key": False,
                            "is_primary": False,
                            "auto_increment": False
                        },
                        {
                            "name": "end_timestamp",
                            "data_type": {
                                "sql_type_name": "INTEGER",
                                "data_length": None,
                                "python_type_name": "int",
                                "class_name": "Integer"
                            },
                            "default": None,
                            "unique": False,
                            "fulltext": False,
                            "nullable": True,
                            "comment": None,
                            "is_foreign_key": False,
                            "is_primary": False,
                            "auto_increment": False
                        },
                        {
                            "name": "timestamp",
                            "data_type": {
                                "sql_type_name": "INTEGER",
                                "data_length": None,
                                "python_type_name": "int",
                                "class_name": "Integer"
                            },
                            "default": None,
                            "unique": False,
                            "fulltext": False,
                            "nullable": True,
                            "comment": "The unix timestamp of when this was last modified, None otherwise.",
                            "is_foreign_key": False,
                            "is_primary": False,
                            "auto_increment": False
                        },
                        {
                            "name": "parent_task_id",
                            "data_type": {
                                "sql_type_name": "INTEGER",
                                "data_length": None,
                                "python_type_name": "int",
                                "class_name": "Integer"
                            },
                            "default": "no default",
                            "unique": False,
                            "fulltext": False,
                            "nullable": True,
                            "comment": None,
                            "is_foreign_key": True,
                            "is_primary": False,
                            "auto_increment": False
                        },
                        {
                            "name": "task_list_id",
                            "data_type": {
                                "sql_type_name": "INTEGER",
                                "data_length": None,
                                "python_type_name": "int",
                                "class_name": "Integer"
                            },
                            "default": "no default",
                            "unique": False,
                            "fulltext": False,
                            "nullable": False,
                            "comment": None,
                            "is_foreign_key": True,
                            "is_primary": False,
                            "auto_increment": False
                        },
                        {
                            "name": "modified_timestamp",
                            "data_type": {
                                "sql_type_name": "INTEGER",
                                "data_length": None,
                                "python_type_name": "int",
                                "class_name": "Integer"
                            },
                            "default": None,
                            "unique": False,
                            "fulltext": False,
                            "nullable": True,
                            "comment": "The unix timestamp of when this was last modified, None otherwise.",
                            "is_foreign_key": False,
                            "is_primary": False,
                            "auto_increment": False
                        },
                        {
                            "name": "deleted",
                            "data_type": {
                                "sql_type_name": "INTEGER",
                                "data_length": None,
                                "python_type_name": "int",
                                "class_name": "Integer"
                            },
                            "default": None,
                            "unique": False,
                            "fulltext": False,
                            "nullable": True,
                            "comment": "The unix timestamp of when this was deleted, None otherwise.",
                            "is_foreign_key": False,
                            "is_primary": False,
                            "auto_increment": False
                        }
                    ],
                    "relationships": [
                        {
                            "name": "parent_task",
                            "fk_name": "FK_DQGjBpjafi0D",
                            "on_delete": "CASCADE",
                            "on_update": "CASCADE",
                            "parent_model": "tasks",
                            "parent_column": "task_id",
                            "child_model": "tasks",
                            "child_column": "parent_task_id"
                        },
                        {
                            "name": "fk_tasklist_task",
                            "fk_name": "FK_bQR3YdseJ2J2",
                            "on_delete": "CASCADE",
                            "on_update": "CASCADE",
                            "parent_model": "task_lists",
                            "parent_column": "task_list_id",
                            "child_model": "tasks",
                            "child_column": "task_list_id"
                        }
                    ],
                    "unique_constraints": [
                        {
                            "name": "UQ_tasks_title",
                            "comment": "Ensure the title is unique.",
                            "columns": [
                                "title"
                            ]
                        }
                    ],
                    "fulltext_indexes": [
                        {
                            "name": "FT_tasks_title",
                            "columns": [
                                "title"
                            ]
                        }
                    ],
                    "parent_tables": [
                        "tasks",
                        "task_lists"
                    ],
                    "child_tables": [
                        "tasks"
                    ]
                }




if __name__ == '__main__':
    # result = _gen_column_create(td)
    # result = _gen_relationship(tdr)
    # result = _gen_unique_constraint(tdu)
    # result = _gen_fulltext_index(tdft)
    result = _gen_model_from_dict(table)
    
    
    print(f"result: {result}")