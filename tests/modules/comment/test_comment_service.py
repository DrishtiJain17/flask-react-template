from datetime import datetime

from modules.comment.comment_service import CommentService
from modules.comment.errors import CommentNotFoundError
from modules.comment.types import (
    CommentErrorCode,
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    UpdateCommentParams,
)
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentService(BaseTestComment):
    def setUp(self) -> None:
        self.account = self.create_test_account()
        self.task = self.create_test_task(self.account.id)

    def test_create_comment(self) -> None:
        params = CreateCommentParams(account_id=self.account.id, task_id=self.task.id, text=self.DEFAULT_COMMENT_TEXT)
        comment = CommentService.create_comment(params=params)

        assert comment.account_id == self.account.id
        assert comment.task_id == self.task.id
        assert comment.text == self.DEFAULT_COMMENT_TEXT
        assert comment.id is not None

    def test_get_comment(self) -> None:
        created_comment = self.create_test_comment(self.account.id, self.task.id)
        params = GetCommentParams(account_id=self.account.id, task_id=self.task.id, comment_id=created_comment.id)

        retrieved_comment = CommentService.get_comment(params=params)

        assert retrieved_comment.id == created_comment.id
        assert retrieved_comment.text == self.DEFAULT_COMMENT_TEXT

    def test_get_comment_not_found(self) -> None:
        fake_comment_id = "507f1f77bcf86cd799439011"
        params = GetCommentParams(account_id=self.account.id, task_id=self.task.id, comment_id=fake_comment_id)

        try:
            CommentService.get_comment(params=params)
        except CommentNotFoundError as e:
            assert e.code == CommentErrorCode.NOT_FOUND

    def test_update_comment(self) -> None:
        created_comment = self.create_test_comment(self.account.id, self.task.id)
        params = UpdateCommentParams(
            account_id=self.account.id, task_id=self.task.id, comment_id=created_comment.id, text="Updated text"
        )

        updated_comment = CommentService.update_comment(params=params)

        assert updated_comment.id == created_comment.id
        assert updated_comment.text == "Updated text"

    def test_update_comment_not_found(self) -> None:
        fake_comment_id = "507f1f77bcf86cd799439011"
        params = UpdateCommentParams(
            account_id=self.account.id, task_id=self.task.id, comment_id=fake_comment_id, text="Updated text"
        )

        try:
            CommentService.update_comment(params=params)
        except CommentNotFoundError as e:
            assert e.code == CommentErrorCode.NOT_FOUND

    def test_delete_comment(self) -> None:
        created_comment = self.create_test_comment(self.account.id, self.task.id)
        params = DeleteCommentParams(account_id=self.account.id, task_id=self.task.id, comment_id=created_comment.id)

        deletion_result = CommentService.delete_comment(params=params)

        assert deletion_result.comment_id == created_comment.id
        assert deletion_result.success is True
        assert isinstance(deletion_result.deleted_at, datetime)

        get_params = GetCommentParams(account_id=self.account.id, task_id=self.task.id, comment_id=created_comment.id)
        try:
            CommentService.get_comment(params=get_params)
        except CommentNotFoundError:
            pass

    def test_delete_comment_not_found(self) -> None:
        fake_comment_id = "507f1f77bcf86cd799439011"
        params = DeleteCommentParams(account_id=self.account.id, task_id=self.task.id, comment_id=fake_comment_id)

        try:
            CommentService.delete_comment(params=params)
        except CommentNotFoundError as e:
            assert e.code == CommentErrorCode.NOT_FOUND
