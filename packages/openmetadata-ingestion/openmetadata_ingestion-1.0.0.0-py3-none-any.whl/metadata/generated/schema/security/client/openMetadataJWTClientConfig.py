# generated by datamodel-codegen:
#   filename:  security/client/openMetadataJWTClientConfig.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from pydantic import BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr


class OpenMetadataJWTClientConfig(BaseModel):
    class Config:
        extra = Extra.forbid

    jwtToken: CustomSecretStr = Field(
        ..., description='OpenMetadata generated JWT token.'
    )
