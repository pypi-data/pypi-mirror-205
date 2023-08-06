# generated by datamodel-codegen:
#   filename:  configuration/taskNotificationConfiguration.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Extra, Field


class TaskNotificationConfiguration(BaseModel):
    class Config:
        extra = Extra.forbid

    enabled: Optional[bool] = Field(False, description='Is Task Notification Enabled?')
