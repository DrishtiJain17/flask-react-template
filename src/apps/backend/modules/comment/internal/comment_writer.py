from datetime import datetime

from bson.objectid import ObjectId
from pymongo import ReturnDocument

from modules.comment.errors import CommentNotFoundError
from modules.comment.internal.comment_util import CommentUtil
from modules.comment.internal.store.comment_model import CommentModel
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import (
    Comment,
    CommentDeletionResult,
    CreateCommentParams,
    DeleteCommentParams,
    UpdateCommentParams,
)
from modules.task.internal.store.task_repository import TaskRepository


class CommentWriter:
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        if TaskRepository.collection().find_one({"_id": ObjectId(params.task_id)}) is None:
            raise CommentNotFoundError(comment_id=params.task_id)
        comment_bson = CommentModel(
            account_id=str(params.account_id),
            task_id=str(params.task_id),
            text=params.text,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ).to_bson()

        query = CommentRepository.collection().insert_one(comment_bson)
        created_comment_bson = CommentRepository.collection().find_one({"_id": query.inserted_id})

        return CommentUtil.convert_comment_bson_to_comment(created_comment_bson)

    @staticmethod
    def update_comment(*, params: UpdateCommentParams) -> Comment:
        updated_comment_bson = CommentRepository.collection().find_one_and_update(
            {"_id": ObjectId(params.comment_id), "task_id": str(params.task_id), "account_id": params.account_id},
            {"$set": {"text": params.text, "updated_at": datetime.now()}},
            return_document=ReturnDocument.AFTER,
        )

        if updated_comment_bson is None:
            raise CommentNotFoundError(comment_id=params.comment_id)

        return CommentUtil.convert_comment_bson_to_comment(updated_comment_bson)

    @staticmethod
    def delete_comment(*, params: DeleteCommentParams) -> CommentDeletionResult:
        result = CommentRepository.collection().delete_one(
            {"_id": ObjectId(params.comment_id), "task_id": str(params.task_id), "account_id": params.account_id}
        )
        if result.deleted_count == 0:
            raise CommentNotFoundError(comment_id=params.comment_id)
        return CommentDeletionResult(comment_id=params.comment_id, deleted_at=datetime.now(), success=True)
