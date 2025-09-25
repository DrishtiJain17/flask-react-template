from dataclasses import asdict
from typing import Any

from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.types import Comment


class CommentUtil:
    @staticmethod
    def convert_comment_bson_to_comment(comment_bson: dict[str, Any]) -> Comment:
        validated_comment_data = CommentModel.from_bson(comment_bson)
        return Comment(
            account_id=validated_comment_data.account_id,
            id=str(validated_comment_data.id),
            task_id=validated_comment_data.task_id,
            text=validated_comment_data.text,
            created_at=validated_comment_data.created_at,
            updated_at=validated_comment_data.updated_at,
        )

    @staticmethod
    def comment_to_dict(comment: Comment) -> dict:
        """Convert Comment dataclass to JSON-safe dict (datetime → isoformat)."""
        data = asdict(comment)
        data["created_at"] = comment.created_at.isoformat()
        data["updated_at"] = comment.updated_at.isoformat()
        return data
