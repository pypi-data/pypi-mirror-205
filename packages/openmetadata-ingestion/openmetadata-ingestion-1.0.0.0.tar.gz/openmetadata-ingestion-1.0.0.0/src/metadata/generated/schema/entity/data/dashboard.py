# generated by datamodel-codegen:
#   filename:  entity/data/dashboard.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ...type import basic, entityHistory, entityReference, tagLabel, usageDetails
from ..services import dashboardService


class Dashboard(BaseModel):
    class Config:
        extra = Extra.forbid

    id: basic.Uuid = Field(
        ..., description='Unique identifier that identifies a dashboard instance.'
    )
    name: basic.EntityName = Field(
        ..., description='Name that identifies this dashboard.'
    )
    displayName: Optional[str] = Field(
        None,
        description='Display Name that identifies this Dashboard. It could be title or label from the source services.',
    )
    fullyQualifiedName: Optional[basic.FullyQualifiedEntityName] = Field(
        None,
        description="A unique name that identifies a dashboard in the format 'ServiceName.DashboardName'.",
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the dashboard, what it is, and how to use it.'
    )
    version: Optional[entityHistory.EntityVersion] = Field(
        None, description='Metadata version of the entity.'
    )
    updatedAt: Optional[basic.Timestamp] = Field(
        None,
        description='Last update time corresponding to the new version of the entity in Unix epoch time milliseconds.',
    )
    updatedBy: Optional[str] = Field(None, description='User who made the update.')
    dashboardUrl: Optional[str] = Field(
        None, description='Dashboard URL suffix from its service.'
    )
    charts: Optional[entityReference.EntityReferenceList] = Field(
        None, description='All the charts included in this Dashboard.'
    )
    dataModels: Optional[entityReference.EntityReferenceList] = Field(
        None,
        description='List of data models used by this dashboard or the charts contained on it.',
    )
    href: Optional[basic.Href] = Field(
        None, description='Link to the resource corresponding to this entity.'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this dashboard.'
    )
    followers: Optional[entityReference.EntityReferenceList] = Field(
        None, description='Followers of this dashboard.'
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this dashboard.'
    )
    service: entityReference.EntityReference = Field(
        ..., description='Link to service where this dashboard is hosted in.'
    )
    serviceType: Optional[dashboardService.DashboardServiceType] = Field(
        None, description='Service type where this dashboard is hosted in.'
    )
    usageSummary: Optional[usageDetails.UsageDetails] = Field(
        None, description='Latest usage information for this database.'
    )
    changeDescription: Optional[entityHistory.ChangeDescription] = Field(
        None, description='Change that lead to this version of the entity.'
    )
    deleted: Optional[bool] = Field(
        False, description='When `true` indicates the entity has been soft deleted.'
    )
    extension: Optional[basic.EntityExtension] = Field(
        None,
        description='Entity extension data with custom attributes added to the entity.',
    )
