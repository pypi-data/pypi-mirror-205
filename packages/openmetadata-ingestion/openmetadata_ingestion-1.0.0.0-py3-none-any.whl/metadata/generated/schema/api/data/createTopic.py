# generated by datamodel-codegen:
#   filename:  api/data/createTopic.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Extra, Field, conint

from ...entity.data import topic
from ...type import basic, entityReference, schema, tagLabel


class CreateTopicRequest(BaseModel):
    class Config:
        extra = Extra.forbid

    name: basic.EntityName = Field(
        ..., description='Name that identifies this topic instance uniquely.'
    )
    displayName: Optional[str] = Field(
        None, description='Display Name that identifies this topic.'
    )
    description: Optional[basic.Markdown] = Field(
        None,
        description='Description of the topic instance. What it has and how to use it.',
    )
    service: basic.FullyQualifiedEntityName = Field(
        ...,
        description='Fully qualified name of the messaging service where this topic is hosted in',
    )
    messageSchema: Optional[schema.Topic] = None
    partitions: conint(ge=1) = Field(
        ..., description='Number of partitions into which the topic is divided.'
    )
    cleanupPolicies: Optional[List[topic.CleanupPolicy]] = Field(
        None,
        description='Topic clean up policy. For Kafka - `cleanup.policy` configuration.',
    )
    replicationFactor: Optional[int] = Field(
        None, description='Replication Factor in integer (more than 1).'
    )
    retentionTime: Optional[float] = Field(
        None,
        description='Retention time in milliseconds. For Kafka - `retention.ms` configuration.',
    )
    maximumMessageSize: Optional[int] = Field(
        None,
        description='Maximum message size in bytes. For Kafka - `max.message.bytes` configuration.',
    )
    minimumInSyncReplicas: Optional[int] = Field(
        None,
        description='Minimum number replicas in sync to control durability. For Kafka - `min.insync.replicas` configuration.',
    )
    retentionSize: Optional[float] = Field(
        '-1',
        description='Maximum size of a partition in bytes before old data is discarded. For Kafka - `retention.bytes` configuration.',
    )
    topicConfig: Optional[topic.TopicConfig] = Field(
        None, description='Contains key/value pair of topic configuration.'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this topic'
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this topic'
    )
    extension: Optional[basic.EntityExtension] = Field(
        None,
        description='Entity extension data with custom attributes added to the entity.',
    )
