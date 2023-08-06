from pydantic import BaseModel, Extra
import datetime as dt
from typing import Union
from enum import Enum


class TagAttribute(BaseModel):
    type: str
    name: str
    value: str


class TagDisplay(BaseModel):
    url: str
    hash: str


class ProvenanceTag(BaseModel):
    name: str
    unique: bool
    description: str
    attributes: list[TagAttribute]
    display: TagDisplay
