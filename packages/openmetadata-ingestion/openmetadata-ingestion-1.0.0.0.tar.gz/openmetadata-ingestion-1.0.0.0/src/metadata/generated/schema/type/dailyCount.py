# generated by datamodel-codegen:
#   filename:  type/dailyCount.json
#   timestamp: 2023-04-25T16:15:11+00:00

from __future__ import annotations

from pydantic import BaseModel, Extra, Field, conint

from . import basic


class DailyCountOfSomeMeasurement(BaseModel):
    class Config:
        extra = Extra.forbid

    count: conint(ge=0) = Field(
        ..., description='Daily count of a measurement on the given date.'
    )
    date: basic.Date
