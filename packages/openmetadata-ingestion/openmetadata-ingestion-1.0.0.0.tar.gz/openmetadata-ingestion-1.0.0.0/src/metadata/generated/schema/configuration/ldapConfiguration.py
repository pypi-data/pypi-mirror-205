# generated by datamodel-codegen:
#   filename:  configuration/ldapConfiguration.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from .ldapTrustStoreConfig import truststoreConfig


class TruststoreConfigType(Enum):
    TrustAll = 'TrustAll'
    JVMDefault = 'JVMDefault'
    HostName = 'HostName'
    CustomTrustStore = 'CustomTrustStore'


class LdapConfiguration(BaseModel):
    class Config:
        extra = Extra.forbid

    host: str = Field(
        ..., description='LDAP server address without scheme(Example :- localhost)'
    )
    port: int = Field(..., description='Port of the server')
    maxPoolSize: Optional[int] = Field(
        3, description='No of connection to create the pool with'
    )
    isFullDn: Optional[bool] = Field(
        False, description='If enable need to give full dn to login'
    )
    dnAdminPrincipal: str = Field(
        ..., description='Distinguished Admin name with search capabilities'
    )
    dnAdminPassword: str = Field(..., description='Password for LDAP Admin')
    sslEnabled: Optional[bool] = Field(False, description='LDAPS (secure LDAP) or LDAP')
    userBaseDN: str = Field(..., description='User base distinguished name')
    mailAttributeName: str = Field(..., description='Email attribute name')
    truststoreFormat: Optional[str] = Field(
        None, description='Truststore format e.g. PKCS12, JKS.'
    )
    truststoreConfigType: Optional[TruststoreConfigType] = Field(
        None,
        description='Truststore Type e.g. TrustAll, HostName, JVMDefault, CustomTrustStore.',
    )
    trustStoreConfig: Optional[truststoreConfig.TruststoreConfig] = Field(
        None, description='Truststore Configuration'
    )
