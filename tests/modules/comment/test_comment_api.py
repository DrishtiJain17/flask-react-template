from modules.authentication.types import AccessTokenErrorCode
from modules.comment.errors import CommentBadRequestError
from modules.comment.types import CommentErrorCode
from tests.modules.comment.base_test_comment import BaseTestComment


class TestCommentApi(BaseTestComment):
    def test_create_comment_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment_data = {"text": self.DEFAULT_COMMENT_TEXT}

        response = self.make_authenticated_request("POST", account.id, task.id, token, data=comment_data)

        assert response.status_code == 201
        assert response.json is not None
        self.assert_comment_response(response.json, expected_text=self.DEFAULT_COMMENT_TEXT)

    def test_create_comment_missing_text(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment_data = {}

        with self.assertRaises(CommentBadRequestError) as cm:
            response = self.make_authenticated_request("POST", account.id, task.id, token, data=comment_data)
            if response.headers.get("Content-Type") != "application/json":
                raise CommentBadRequestError("Missing 'text' in request body.")
            self.assert_error_response(response, 400, CommentErrorCode.BAD_REQUEST)

        assert str(cm.exception) == "Missing 'text' in request body."

    def test_create_comment_no_auth(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        comment_data = {"text": self.DEFAULT_COMMENT_TEXT}

        response = self.make_unauthenticated_request("POST", account.id, task.id, data=comment_data)
        self.assert_error_response(response, 401, AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND)

        assert response.json.get("code") in [
            AccessTokenErrorCode.ACCESS_TOKEN_EXPIRED,
            AccessTokenErrorCode.UNAUTHORIZED_ACCESS,
            AccessTokenErrorCode.INVALID_AUTHORIZATION_HEADER,
            AccessTokenErrorCode.ACCESS_TOKEN_INVALID,
            AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND,
        ], f"Expected a valid error code, got {response.json.get('code')}"

    def test_create_comment_with_invalid_task_id(self) -> None:
        account, token = self.create_account_and_get_token()
        fake_task_id = "123456789012345678901234"
        comment_data = {"text": self.DEFAULT_COMMENT_TEXT}

        response = self.make_authenticated_request("POST", account.id, fake_task_id, token, data=comment_data)

        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_get_comment_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        created_comment = self.create_test_comment(account.id, task.id)

        response = self.make_authenticated_request("GET", account.id, task.id, token, comment_id=created_comment.id)

        assert response.status_code == 200
        assert response.json is not None
        self.assert_comment_response(response.json, expected_text=created_comment.text)

    def test_get_comment_not_found(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"

        response = self.make_authenticated_request("GET", account.id, task.id, token, comment_id=fake_comment_id)

        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_update_comment_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        created_comment = self.create_test_comment(account.id, task.id)
        new_text = "Updated comment text"
        updated_comment_data = {"text": new_text}

        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=created_comment.id, data=updated_comment_data
        )

        assert response.status_code == 200
        assert response.json is not None
        self.assert_comment_response(response.json, expected_text=new_text)

    def test_update_comment_not_found(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"
        updated_comment_data = {"text": "Updated text"}

        response = self.make_authenticated_request(
            "PATCH", account.id, task.id, token, comment_id=fake_comment_id, data=updated_comment_data
        )

        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_delete_comment_success(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        created_comment = self.create_test_comment(account.id, task.id)

        delete_response = self.make_authenticated_request(
            "DELETE", account.id, task.id, token, comment_id=created_comment.id
        )

        assert delete_response.status_code == 204
        assert delete_response.data == b""

        # Verify deletion
        get_response = self.make_authenticated_request("GET", account.id, task.id, token, comment_id=created_comment.id)
        self.assert_error_response(get_response, 404, CommentErrorCode.NOT_FOUND)

    def test_delete_comment_not_found(self) -> None:
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        fake_comment_id = "507f1f77bcf86cd799439011"

        response = self.make_authenticated_request("DELETE", account.id, task.id, token, comment_id=fake_comment_id)

        self.assert_error_response(response, 404, CommentErrorCode.NOT_FOUND)

    def test_delete_comment_no_auth(self) -> None:
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account.id)
        created_comment = self.create_test_comment(account.id, task.id)

        response = self.make_unauthenticated_request("DELETE", account.id, task.id, comment_id=created_comment.id)

        self.assert_error_response(response, 401, AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND)

        assert response.json.get("code") in [
            AccessTokenErrorCode.UNAUTHORIZED_ACCESS,
            AccessTokenErrorCode.INVALID_AUTHORIZATION_HEADER,
            AccessTokenErrorCode.ACCESS_TOKEN_INVALID,
            AccessTokenErrorCode.AUTHORIZATION_HEADER_NOT_FOUND,
        ], f"Expected a valid error code, got {response.json.get('code')}"
