# generated by datamodel-codegen:
#   filename:  metadataIngestion/messagingServiceMetadataPipeline.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra, Field

from ..type import filterPattern


class MessagingMetadataConfigType(Enum):
    MessagingMetadata = 'MessagingMetadata'


class MessagingServiceMetadataPipeline(BaseModel):
    class Config:
        extra = Extra.forbid

    type: Optional[MessagingMetadataConfigType] = Field(
        MessagingMetadataConfigType.MessagingMetadata, description='Pipeline type'
    )
    topicFilterPattern: Optional[filterPattern.FilterPattern] = Field(
        None, description='Regex to only fetch topics that matches the pattern.'
    )
    generateSampleData: Optional[bool] = Field(
        False,
        description='Option to turn on/off generating sample data during metadata extraction.',
    )
    markDeletedTopics: Optional[bool] = Field(
        True,
        description='Optional configuration to soft delete topics in OpenMetadata if the source topics are deleted. Also, if the topic is deleted, all the associated entities like sample data, lineage, etc., with that topic will be deleted',
    )
