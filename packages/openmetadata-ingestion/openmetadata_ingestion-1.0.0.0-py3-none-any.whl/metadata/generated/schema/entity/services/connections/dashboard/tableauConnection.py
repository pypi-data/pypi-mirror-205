# generated by datamodel-codegen:
#   filename:  entity/services/connections/dashboard/tableauConnection.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional, Union

from pydantic import AnyUrl, BaseModel, Extra, Field

from .....security.credentials import accessTokenAuth, basicAuth
from .....security.ssl import verifySSLConfig
from .. import connectionBasicType


class TableauType(Enum):
    Tableau = 'Tableau'


class TableauConnection(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[TableauType] = Field(
        TableauType.Tableau, description='Service Type', title='Service Type'
    )
    hostPort: AnyUrl = Field(..., description='Tableau Server.', title='Host and Port')
    authType: Optional[
        Union[basicAuth.BasicAuth, accessTokenAuth.AccessTokenAuth]
    ] = Field(
        None,
        description='Types of methods used to authenticate to the tableau instance',
        title='Authentication type for Tableau',
    )
    apiVersion: str = Field(
        ..., description='Tableau API version.', title='API Version'
    )
    siteName: Optional[str] = Field(
        None, description='Tableau Site Name.', title='Site Name'
    )
    siteUrl: Optional[str] = Field(
        None, description='Tableau Site Url.', title='Site Url'
    )
    env: str = Field(
        ..., description='Tableau Environment Name.', title='Tableau Environment'
    )
    verifySSL: Optional[verifySSLConfig.VerifySSL] = verifySSLConfig.VerifySSL.no_ssl
    sslConfig: Optional[verifySSLConfig.SslConfig] = None
    supportsMetadataExtraction: Optional[
        connectionBasicType.SupportsMetadataExtraction
    ] = Field(None, title='Supports Metadata Extraction')
