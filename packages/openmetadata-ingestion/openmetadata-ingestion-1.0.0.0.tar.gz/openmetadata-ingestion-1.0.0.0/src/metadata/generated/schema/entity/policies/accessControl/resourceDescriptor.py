# generated by datamodel-codegen:
#   filename:  entity/policies/accessControl/resourceDescriptor.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field


class Operation(Enum):
    All = 'All'
    Create = 'Create'
    Delete = 'Delete'
    ViewAll = 'ViewAll'
    ViewBasic = 'ViewBasic'
    ViewUsage = 'ViewUsage'
    ViewTests = 'ViewTests'
    ViewQueries = 'ViewQueries'
    ViewDataProfile = 'ViewDataProfile'
    ViewSampleData = 'ViewSampleData'
    EditAll = 'EditAll'
    EditCustomFields = 'EditCustomFields'
    EditDataProfile = 'EditDataProfile'
    EditDescription = 'EditDescription'
    EditDisplayName = 'EditDisplayName'
    EditLineage = 'EditLineage'
    EditPolicy = 'EditPolicy'
    EditOwner = 'EditOwner'
    EditQueries = 'EditQueries'
    EditReviewers = 'EditReviewers'
    EditRole = 'EditRole'
    EditSampleData = 'EditSampleData'
    EditStatus = 'EditStatus'
    EditTags = 'EditTags'
    EditTeams = 'EditTeams'
    EditTier = 'EditTier'
    EditTests = 'EditTests'
    EditUsers = 'EditUsers'


class ResourceDescriptor(BaseModel):
    class Config:
        extra = Extra.forbid

    name: Optional[str] = Field(
        None,
        description='Name of the resource. For entity related resources, resource name is same as the entity name. Some resources such as lineage are not entities but are resources.',
    )
    operations: Optional[List[Operation]] = Field(
        None, description='List of operations supported by the resource.'
    )
