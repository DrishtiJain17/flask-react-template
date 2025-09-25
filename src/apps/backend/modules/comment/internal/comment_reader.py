from bson.objectid import ObjectId

from modules.comment.errors import CommentNotFoundError
from modules.comment.internal.comment_util import CommentUtil
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import Comment, GetCommentParams


class CommentReader:
    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        comment_bson = CommentRepository.collection().find_one(
            {"_id": ObjectId(params.comment_id), "task_id": str(params.task_id)}
        )
        if comment_bson is None:
            raise CommentNotFoundError(comment_id=params.comment_id)
        return CommentUtil.convert_comment_bson_to_comment(comment_bson)
