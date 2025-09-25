from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Comment:
    id: str
    task_id: str
    account_id: str
    text: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class CreateCommentParams:
    account_id: str
    task_id: str
    text: str


@dataclass(frozen=True)
class UpdateCommentParams:
    account_id: str
    task_id: str
    comment_id: str
    text: str


@dataclass(frozen=True)
class DeleteCommentParams:
    account_id: str
    task_id: str
    comment_id: str


@dataclass(frozen=True)
class GetCommentParams:
    account_id: str
    task_id: str
    comment_id: str


@dataclass(frozen=True)
class CommentErrorCode:
    NOT_FOUND: str = "COMMENT_ERR_01"
    BAD_REQUEST: str = "COMMENT_ERR_02"


@dataclass(frozen=True)
class CommentDeletionResult:
    comment_id: str
    deleted_at: datetime
    success: bool
