from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.comment.comment_service import CommentService
from modules.comment.errors import CommentBadRequestError
from modules.comment.internal.comment_util import CommentUtil
from modules.comment.types import CreateCommentParams, DeleteCommentParams, GetCommentParams, UpdateCommentParams


class CommentView(MethodView):
    @access_auth_middleware
    def get(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        if comment_id:
            comment_params = GetCommentParams(account_id=account_id, task_id=task_id, comment_id=comment_id)
            comment = CommentService.get_comment(params=comment_params)
            comment_dict = CommentUtil.comment_to_dict(comment)
            return jsonify(comment_dict), 200
        else:
            raise CommentBadRequestError("Comment ID is required for fetching a specific comment")

    @access_auth_middleware
    def post(self, account_id: str, task_id: str) -> ResponseReturnValue:
        request_data = request.json
        if request_data is None or "text" not in request_data:
            raise CommentBadRequestError("Missing 'text' in request body.")

        params = CreateCommentParams(account_id=account_id, task_id=task_id, text=request_data["text"])
        comment = CommentService.create_comment(params=params)
        comment_dict = CommentUtil.comment_to_dict(comment)
        return jsonify(comment_dict), 201

    @access_auth_middleware
    def patch(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        request_data = request.get_json()
        if request_data is None:
            raise CommentBadRequestError("Request body is required")

        if not request_data.get("text"):
            raise CommentBadRequestError("Text is required")

        update_comment_params = UpdateCommentParams(
            account_id=account_id, comment_id=comment_id, task_id=task_id, text=request_data["text"]
        )
        updated_comment = CommentService.update_comment(params=update_comment_params)
        comment_dict = CommentUtil.comment_to_dict(updated_comment)
        return jsonify(comment_dict), 200

    @access_auth_middleware
    def delete(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        delete_params = DeleteCommentParams(account_id=account_id, comment_id=comment_id, task_id=task_id)
        CommentService.delete_comment(params=delete_params)
        return "", 204
