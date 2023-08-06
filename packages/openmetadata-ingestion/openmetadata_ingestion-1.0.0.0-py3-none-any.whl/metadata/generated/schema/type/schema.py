# generated by datamodel-codegen:
#   filename:  type/schema.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field, constr

from . import basic, tagLabel


class SchemaType(Enum):
    Avro = 'Avro'
    Protobuf = 'Protobuf'
    JSON = 'JSON'
    Other = 'Other'
    None_ = 'None'


class DataTypeTopic(Enum):
    RECORD = 'RECORD'
    NULL = 'NULL'
    BOOLEAN = 'BOOLEAN'
    INT = 'INT'
    LONG = 'LONG'
    BYTES = 'BYTES'
    FLOAT = 'FLOAT'
    DOUBLE = 'DOUBLE'
    TIMESTAMP = 'TIMESTAMP'
    TIMESTAMPZ = 'TIMESTAMPZ'
    TIME = 'TIME'
    DATE = 'DATE'
    STRING = 'STRING'
    ARRAY = 'ARRAY'
    MAP = 'MAP'
    ENUM = 'ENUM'
    UNION = 'UNION'
    FIXED = 'FIXED'
    ERROR = 'ERROR'
    UNKNOWN = 'UNKNOWN'


class FieldName(BaseModel):
    __root__: constr(min_length=1, max_length=128) = Field(
        ..., description='Local name (not fully qualified name) of the field. '
    )


class FieldModel(BaseModel):
    class Config:
        extra = Extra.forbid

    name: FieldName
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this field name.'
    )
    dataType: DataTypeTopic = Field(
        ..., description='Data type of the field (int, date etc.).'
    )
    dataTypeDisplay: Optional[str] = Field(
        None,
        description='Display name used for dataType. This is useful for complex types, such as `array<int>`, `map<int,string>`, `struct<>`, and union types.',
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the column.'
    )
    fullyQualifiedName: Optional[basic.FullyQualifiedEntityName] = None
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags associated with the column.'
    )
    children: Optional[List[FieldModel]] = Field(
        None,
        description='Child fields if dataType or arrayDataType is `map`, `record`, `message`',
    )


class Topic(BaseModel):
    class Config:
        extra = Extra.forbid

    schemaText: Optional[str] = Field(
        None,
        description='Schema used for message serialization. Optional as some topics may not have associated schemas.',
    )
    schemaType: Optional[SchemaType] = Field(
        SchemaType.None_, description='Schema used for message serialization.'
    )
    schemaFields: Optional[List[FieldModel]] = Field(
        [], description='Columns in this table.'
    )


FieldModel.update_forward_refs()
