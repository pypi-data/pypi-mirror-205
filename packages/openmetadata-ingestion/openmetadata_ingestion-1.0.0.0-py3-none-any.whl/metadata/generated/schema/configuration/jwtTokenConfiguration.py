# generated by datamodel-codegen:
#   filename:  configuration/jwtTokenConfiguration.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field


class JWTTokenConfiguration(BaseModel):
    class Config:
        extra = Extra.forbid

    rsapublicKeyFilePath: Optional[str] = Field(
        None, description='RSA Public Key File Path'
    )
    rsaprivateKeyFilePath: Optional[str] = Field(
        None, description='RSA Private Key File Path'
    )
    jwtissuer: str = Field(..., description='JWT Issuer')
    keyId: str = Field(..., description='Key ID')
