# generated by datamodel-codegen:
#   filename:  entity/services/connections/dashboard/powerBIConnection.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr

from .. import connectionBasicType


class PowerBiType(Enum):
    PowerBI = 'PowerBI'


class PowerBIConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[PowerBiType] = Field(
        PowerBiType.PowerBI, description='Service Type', title='Service Type'
    )
    clientId: str = Field(..., description='client_id for PowerBI.', title='Client ID')
    clientSecret: CustomSecretStr = Field(
        ..., description='clientSecret for PowerBI.', title='Client Secret'
    )
    tenantId: str = Field(..., description='Tenant ID for PowerBI.', title='Tenant ID')
    authorityURI: Optional[str] = Field(
        'https://login.microsoftonline.com/',
        description='Authority URI for the PowerBI service.',
        title='Authority URI',
    )
    hostPort: Optional[AnyUrl] = Field(
        'https://app.powerbi.com',
        description='Dashboard URL for PowerBI service.',
        title='Host and Port',
    )
    scope: Optional[List[str]] = Field(
        ['https://analysis.windows.net/powerbi/api/.default'],
        description='PowerBI secrets.',
        title='Scope',
    )
    pagination_entity_per_page: Optional[int] = Field(
        100,
        description='Entity Limit set here will be used to paginate the PowerBi APIs',
        title='Pagination Entity Per Page',
    )
    useAdminApis: Optional[bool] = Field(
        True,
        description='Fetch the PowerBI metadata using admin APIs',
        title='Use PowerBI Admin APIs',
    )
    supportsMetadataExtraction: Optional[
        connectionBasicType.SupportsMetadataExtraction
    ] = Field(None, title='Supports Metadata Extraction')
