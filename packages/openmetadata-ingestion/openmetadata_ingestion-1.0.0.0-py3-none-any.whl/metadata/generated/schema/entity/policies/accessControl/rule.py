# generated by datamodel-codegen:
#   filename:  entity/policies/accessControl/rule.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ....type import basic
from . import resourceDescriptor


class Effect(Enum):
    allow = 'allow'
    deny = 'deny'


class Rule(BaseModel):
    class Config:
        extra = Extra.forbid

    name: str = Field(..., description='Name of this Rule.')
    fullyQualifiedName: Optional[basic.FullyQualifiedEntityName] = Field(
        None, description='FullyQualifiedName in the form `policyName.ruleName`.'
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the rule.'
    )
    effect: Effect
    operations: List[resourceDescriptor.Operation] = Field(
        ...,
        description='List of operation names related to the `resources`. Use `*` to include all the operations.',
    )
    resources: List[str] = Field(
        ...,
        description='Resources/objects related to this rule. Resources are typically `entityTypes` such as `table`, `database`, etc. It also includes `non-entityType` resources such as `lineage`. Use `*` to include all the resources.',
    )
    condition: Optional[basic.Expression] = Field(
        None,
        description='Expression in SpEL used for matching of a `Rule` based on entity, resource, and environmental attributes.',
    )
