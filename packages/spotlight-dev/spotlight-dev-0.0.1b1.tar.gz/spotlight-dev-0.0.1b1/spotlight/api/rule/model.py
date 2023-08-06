from typing import Optional, List

from pydantic import Field

from spotlight.core.common.base import Base
from spotlight.core.common.enum import Severity


class RuleRequest(Base):
    name: str
    predicate: str
    description: Optional[str] = Field(default=None)
    threshold: Optional[int] = Field(default=None)
    severity: Optional[Severity] = Field(default=Severity.ERROR)


class RuleResponse(Base):
    id: str
    name: str
    description: Optional[str]
    predicate: str
    threshold: int
    severity: Severity
    created_by: str
    created_at: int
    updated_by: Optional[str]
    updated_at: Optional[int]


class RuleTagResponse(Base):
    tag_id: str
    rule_id: str
    created_by: str
    created_at: int
