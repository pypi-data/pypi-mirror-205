# generated by datamodel-codegen:
#   filename:  entity/data/mlmodel.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field

from ...type import basic, entityHistory, entityReference, tagLabel, usageDetails
from ..services import mlmodelService


class FeatureType(Enum):
    numerical = 'numerical'
    categorical = 'categorical'


class FeatureSourceDataType(Enum):
    integer = 'integer'
    number = 'number'
    string = 'string'
    array = 'array'
    date = 'date'
    timestamp = 'timestamp'
    object = 'object'
    boolean = 'boolean'


class MlHyperParameter(BaseModel):
    class Config:
        extra = Extra.forbid

    name: Optional[str] = Field(None, description='Hyper parameter name.')
    value: Optional[str] = Field(None, description='Hyper parameter value.')
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the Hyper Parameter.'
    )


class MlStore(BaseModel):
    class Config:
        extra = Extra.forbid

    storage: Optional[basic.Href] = Field(
        None, description='Storage Layer containing the ML Model data.'
    )
    imageRepository: Optional[basic.Href] = Field(
        None, description='Container Repository with the ML Model image.'
    )


class FeatureSource(BaseModel):
    class Config:
        extra = Extra.forbid

    name: Optional[basic.EntityName] = None
    dataType: Optional[FeatureSourceDataType] = Field(
        None, description='Data type of the source (int, date etc.).'
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the feature source.'
    )
    fullyQualifiedName: Optional[basic.FullyQualifiedEntityName] = None
    dataSource: Optional[entityReference.EntityReference] = Field(
        None, description='Description of the Data Source (e.g., a Table).'
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags associated with the feature source.'
    )


class MlFeature(BaseModel):
    class Config:
        extra = Extra.forbid

    name: Optional[basic.EntityName] = None
    dataType: Optional[FeatureType] = Field(
        None, description='Data type of the column (numerical vs. categorical).'
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the ML Feature.'
    )
    fullyQualifiedName: Optional[basic.FullyQualifiedEntityName] = None
    featureSources: Optional[List[FeatureSource]] = Field(
        None, description='Columns used to create the ML Feature.'
    )
    featureAlgorithm: Optional[str] = Field(
        None,
        description='Description of the algorithm used to compute the feature, e.g., PCA, bucketing...',
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags associated with the feature.'
    )


class MlModel(BaseModel):
    class Config:
        extra = Extra.forbid

    id: basic.Uuid = Field(
        ..., description='Unique identifier of an ML Model instance.'
    )
    name: basic.EntityName = Field(
        ..., description='Name that identifies this ML Model.'
    )
    fullyQualifiedName: Optional[basic.FullyQualifiedEntityName] = Field(
        None, description='A unique name that identifies an ML Model.'
    )
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this ML Model.'
    )
    description: Optional[basic.Markdown] = Field(
        None, description='Description of the ML Model, what it is, and how to use it.'
    )
    algorithm: str = Field(..., description='Algorithm used to train the ML Model.')
    mlFeatures: Optional[List[MlFeature]] = Field(
        None, description='Features used to train the ML Model.'
    )
    mlHyperParameters: Optional[List[MlHyperParameter]] = Field(
        None, description='Hyper Parameters used to train the ML Model.'
    )
    target: Optional[basic.EntityName] = Field(
        None, description='For supervised ML Models, the value to estimate.'
    )
    dashboard: Optional[entityReference.EntityReference] = Field(
        None, description='Performance Dashboard URL to track metric evolution.'
    )
    mlStore: Optional[MlStore] = Field(
        None,
        description='Location containing the ML Model. It can be a storage layer and/or a container repository.',
    )
    server: Optional[basic.Href] = Field(
        None,
        description='Endpoint that makes the ML Model available, e.g,. a REST API serving the data or computing predictions.',
    )
    href: Optional[basic.Href] = Field(
        None, description='Link to the resource corresponding to this entity.'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this ML Model.'
    )
    followers: Optional[entityReference.EntityReferenceList] = Field(
        None, description='Followers of this ML Model.'
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this ML Model.'
    )
    usageSummary: Optional[usageDetails.UsageDetails] = Field(
        None, description='Latest usage information for this ML Model.'
    )
    version: Optional[entityHistory.EntityVersion] = Field(
        None, description='Metadata version of the entity.'
    )
    updatedAt: Optional[basic.Timestamp] = Field(
        None,
        description='Last update time corresponding to the new version of the entity in Unix epoch time milliseconds.',
    )
    updatedBy: Optional[str] = Field(None, description='User who made the update.')
    service: entityReference.EntityReference = Field(
        ..., description='Link to service where this pipeline is hosted in.'
    )
    serviceType: Optional[mlmodelService.MlModelServiceType] = Field(
        None, description='Service type where this pipeline is hosted in.'
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
