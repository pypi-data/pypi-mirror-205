# generated by datamodel-codegen:
#   filename:  security/credentials/githubCredentials.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from metadata.ingestion.models.custom_pydantic import CustomSecretStr


class GitHubCredentials(BaseModel):
    class Config:
        extra = Extra.forbid

    repositoryOwner: str = Field(
        ...,
        description='The owner (user or organization) of a GitHub repository. For example, in https://github.com/open-metadata/OpenMetadata, the owner is `open-metadata`.',
        title='Repository Owner',
    )
    repositoryName: str = Field(
        ...,
        description='The name of a GitHub repository. For example, in https://github.com/open-metadata/OpenMetadata, the name is `OpenMetadata`.',
        title='Repository Name',
    )
    token: Optional[CustomSecretStr] = Field(
        None,
        description="Token to use the API. This is required for private repositories and to ensure we don't hit API limits.",
        title='API Token',
    )
