# generated by datamodel-codegen:
#   filename:  entity/services/connections/database/pinotDBConnection.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr

from .. import connectionBasicType


class PinotDBType(Enum):
    PinotDB = 'PinotDB'


class PinotDBScheme(Enum):
    pinot = 'pinot'
    pinot_http = 'pinot+http'
    pinot_https = 'pinot+https'


class PinotDBConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[PinotDBType] = Field(
        PinotDBType.PinotDB, description='Service Type', title='Service Type'
    )
    scheme: Optional[PinotDBScheme] = Field(
        PinotDBScheme.pinot,
        description='SQLAlchemy driver scheme options.',
        title='Connection Scheme',
    )
    username: Optional[str] = Field(
        None,
        description='username to connect  to the PinotDB. This user should have privileges to read all the metadata in PinotDB.',
        title='Username',
    )
    password: Optional[CustomSecretStr] = Field(
        None, description='password to connect  to the PinotDB.', title='Password'
    )
    hostPort: str = Field(
        ..., description='Host and port of the PinotDB service.', title='Host and Port'
    )
    pinotControllerHost: str = Field(
        ...,
        description='Pinot Broker Host and Port of the data source.',
        title='Pinot Broker Host and Port',
    )
    database: Optional[str] = Field(
        None,
        description='Database of the data source. This is optional parameter, if you would like to restrict the metadata reading to a single database. When left blank, OpenMetadata Ingestion attempts to scan all the databases.',
        title='Database',
    )
    connectionOptions: Optional[connectionBasicType.ConnectionOptions] = Field(
        None, title='Connection Options'
    )
    connectionArguments: Optional[connectionBasicType.ConnectionArguments] = Field(
        None, title='Connection Arguments'
    )
    supportsMetadataExtraction: Optional[
        connectionBasicType.SupportsMetadataExtraction
    ] = Field(None, title='Supports Metadata Extraction')
    supportsDBTExtraction: Optional[connectionBasicType.SupportsDBTExtraction] = None
    supportsProfiler: Optional[connectionBasicType.SupportsProfiler] = Field(
        None, title='Supports Profiler'
    )
    supportsQueryComment: Optional[connectionBasicType.SupportsQueryComment] = Field(
        None, title='Supports Query Comment'
    )
