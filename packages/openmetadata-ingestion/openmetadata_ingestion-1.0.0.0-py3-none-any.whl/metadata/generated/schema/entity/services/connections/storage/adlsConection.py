# generated by datamodel-codegen:
#   filename:  entity/services/connections/storage/adlsConection.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from .....security.credentials import azureCredentials
from .. import connectionBasicType


class AzureType(Enum):
    Adls = 'Adls'


class AzureStoreConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[AzureType] = Field(
        AzureType.Adls, description='Service Type', title='Service Type'
    )
    credentials: azureCredentials.AzureCredentials = Field(
        ..., description='Azure Credentials', title='Azure Credentials'
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
