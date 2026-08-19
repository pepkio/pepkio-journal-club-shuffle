from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict

ActionType = Literal["shuffle", "export", "resolve_doi"]
FrequencyType = Literal["weekly", "biweekly"]
WeightingModeType = Literal["equal", "seniority"]
ExportFormatType = Literal["csv", "ical", "markdown", "slack", "plain"]


class Member(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: str
    seniorityFactor: Optional[float] = None


class Paper(BaseModel):
    model_config = ConfigDict(extra="allow")

    label: Optional[str] = None
    raw: Optional[str] = None
    doi: Optional[str] = None


class Settings(BaseModel):
    model_config = ConfigDict(extra="allow")

    startDate: Optional[str] = None
    time: Optional[str] = None
    durationMin: Optional[int] = None
    frequency: Optional[FrequencyType] = None
    skipDates: Optional[List[str]] = None
    sessionCount: Optional[int] = None
    weightingMode: Optional[WeightingModeType] = None


class Session(BaseModel):
    model_config = ConfigDict(extra="allow")

    sessionNumber: Optional[int] = None
    date: Optional[str] = None
    time: Optional[str] = None
    durationMin: Optional[int] = None
    presenter: Optional[str] = None
    paper: Optional[str] = None
    manualPresenter: Optional[str] = None
    manualPaper: Optional[str] = None


class JournalClubShuffleInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    action: ActionType
    members_text: Optional[str] = None
    papers_text: Optional[str] = None
    members: Optional[List[Member]] = None
    papers: Optional[List[Paper]] = None
    settings: Optional[Settings] = None
    seed: Optional[int] = None
    sessions: Optional[List[Dict[str, Any]]] = None
    past_presenters: Optional[List[str]] = None
    past_papers: Optional[List[str]] = None
    format: Optional[ExportFormatType] = None
    doi: Optional[str] = None


class RunResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    run_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[Any] = None
    result_url: Optional[str] = None
    permalink: Optional[str] = None
    duration_ms: Optional[int] = None
    tool_id: Optional[str] = None
    label: Optional[str] = None
    input: Optional[Dict[str, Any]] = None
    artifacts: Optional[List[Any]] = None
    created_at: Optional[str] = None
