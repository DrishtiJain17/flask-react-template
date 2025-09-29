from typing import Any

from flask import Blueprint, jsonify

from modules.comment.errors import CommentBadRequestError
from modules.comment.rest_api.comment_view import CommentView


class CommentRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>/comments",
            view_func=CommentView.as_view("comment_view"),
            methods=["POST", "GET"],
        )
        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>/comments/<comment_id>",
            view_func=CommentView.as_view("comment_view_by_id"),
            methods=["GET", "PATCH", "DELETE"],
        )

        @blueprint.errorhandler(CommentBadRequestError)
        def handle_bad_request_error(error : CommentBadRequestError) -> Any:
            response = jsonify({"code": error.code, "message": error.message})
            response.status_code = error.http_status_code
            return response

        return blueprint
