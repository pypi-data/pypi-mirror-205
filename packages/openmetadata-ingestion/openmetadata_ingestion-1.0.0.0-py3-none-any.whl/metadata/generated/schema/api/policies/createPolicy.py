# generated by datamodel-codegen:
#   filename:  api/policies/createPolicy.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field

from ...entity.policies import policy
from ...type import basic, entityReference


class CreatePolicyRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    name: basic.EntityName = Field(..., description='Name that identifies this Policy.')
    displayName: Optional[str] = Field(None, description='Title for this Policy.')
    description: Optional[basic.Markdown] = Field(
        None,
        description='A short description of the Policy, comprehensible to regular users.',
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this Policy.'
    )
    rules: policy.Rules
    enabled: Optional[bool] = Field(True, description='Is the policy enabled.')
    location: Optional[basic.Uuid] = Field(
        None, description='UUID of Location where this policy is applied'
    )
