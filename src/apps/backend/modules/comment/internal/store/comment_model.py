from dataclasses import dataclass
from datetime import datetime

from modules.application.base_model import BaseModel


@dataclass
class CommentModel(BaseModel):
    task_id: str
    account_id: str
    text: str
    created_at: datetime
    updated_at: datetime
    id: str | None = None

    @classmethod
    def from_bson(cls, bson_data: dict) -> "CommentModel":
        return cls(
            id=str(bson_data.get("_id", "")),
            task_id=bson_data.get("task_id", ""),
            account_id=bson_data.get("account_id", ""),
            text=bson_data.get("text", ""),
            created_at=bson_data.get("created_at"),
            updated_at=bson_data.get("updated_at"),
        )

    @staticmethod
    def get_collection_name() -> str:
        return "comments"
