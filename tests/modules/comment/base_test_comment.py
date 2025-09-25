import json
import unittest
from typing import Tuple

from server import app

from modules.account.account_service import AccountService
from modules.account.internal.store.account_repository import AccountRepository
from modules.account.types import Account, CreateAccountByUsernameAndPasswordParams
from modules.comment.comment_service import CommentService
from modules.comment.errors import CommentBadRequestError
from modules.comment.internal.store.comment_repository import CommentRepository
from modules.comment.types import Comment, CreateCommentParams
from modules.logger.logger_manager import LoggerManager
from modules.task.internal.store.task_repository import TaskRepository
from modules.task.task_service import TaskService
from modules.task.types import CreateTaskParams, Task


class BaseTestComment(unittest.TestCase):
    ACCESS_TOKEN_URL = "http://127.0.0.1:8080/api/access-tokens"
    HEADERS = {"Content-Type": "application/json"}

    DEFAULT_USERNAME = "testuser@example.com"
    DEFAULT_PASSWORD = "testpassword"
    DEFAULT_FIRST_NAME = "Test"
    DEFAULT_LAST_NAME = "User"

    DEFAULT_TASK_TITLE = "Test Task"
    DEFAULT_TASK_DESCRIPTION = "Task for comment testing"
    DEFAULT_COMMENT_TEXT = "This is a test comment"

    def setUp(self) -> None:
        LoggerManager.mount_logger()

    def tearDown(self) -> None:
        CommentRepository.collection().delete_many({})
        TaskRepository.collection().delete_many({})
        AccountRepository.collection().delete_many({})

    # TEST DATA HELPER METHODS
    def create_test_account(self, username: str = None) -> Account:
        if username is None:
            username = self.DEFAULT_USERNAME
        params = CreateAccountByUsernameAndPasswordParams(
            username=username,
            password=self.DEFAULT_PASSWORD,
            first_name=self.DEFAULT_FIRST_NAME,
            last_name=self.DEFAULT_LAST_NAME,
        )
        return AccountService.create_account_by_username_and_password(params=params)

    def create_test_task(self, account_id: str, title: str = None) -> Task:
        if title is None:
            title = self.DEFAULT_TASK_TITLE
        params = CreateTaskParams(account_id=account_id, title=title, description=self.DEFAULT_TASK_DESCRIPTION)
        return TaskService.create_task(params=params)

    def create_test_comment(self, account_id: str, task_id: str, text: str = None) -> Comment:
        if text is None:
            text = self.DEFAULT_COMMENT_TEXT
        params = CreateCommentParams(account_id=account_id, task_id=task_id, text=text)
        return CommentService.create_comment(params=params)

    def get_token(self, username: str = None) -> str:
        if username is None:
            username = self.DEFAULT_USERNAME
        login_data = {"username": username, "password": self.DEFAULT_PASSWORD}

        with app.test_client() as client:
            response = client.post(self.ACCESS_TOKEN_URL, data=json.dumps(login_data), headers=self.HEADERS)
            response_json = response.json
            return response_json.get("token")

    def create_account_and_get_token(self) -> Tuple[Account, str]:
        account = self.create_test_account()
        token = self.get_token(username=account.username)
        return account, token

    # URL HELPER METHODS
    def get_comment_api_url(self, account_id: str, task_id: str, comment_id: str = None):
        url = f"/api/accounts/{account_id}/tasks/{task_id}/comments"
        if comment_id:
            url += f"/{comment_id}"
        return url

    # API CALL HELPER METHODS
    def make_authenticated_request(
        self, method: str, account_id: str, task_id: str, token: str, comment_id: str = None, data: dict = None
    ):
        headers = self.HEADERS.copy()
        headers["Authorization"] = f"Bearer {token}"
        url = self.get_comment_api_url(account_id, task_id, comment_id)

        with app.test_client() as client:
            if method.upper() == "POST":
                return client.post(url, headers=headers, data=json.dumps(data) if data else None)
            elif method.upper() == "GET":
                return client.get(url, headers=headers)
            elif method.upper() == "PATCH":
                return client.patch(url, headers=headers, data=json.dumps(data) if data else None)
            elif method.upper() == "DELETE":
                return client.delete(url, headers=headers)

    def make_unauthenticated_request(
        self, method: str, account_id: str, task_id: str, comment_id: str = None, data: dict = None
    ):
        url = self.get_comment_api_url(account_id, task_id, comment_id)

        with app.test_client() as client:
            if method.upper() == "POST":
                return client.post(url, headers=self.HEADERS, data=json.dumps(data) if data else None)
            elif method.upper() == "GET":
                return client.get(url)
            elif method.upper() == "PATCH":
                return client.patch(url, headers=self.HEADERS, data=json.dumps(data) if data else None)
            elif method.upper() == "DELETE":
                return client.delete(url)

    # ASSERT HELPERS
    def assert_comment_response(self, response_json: dict, expected_text: str = None):
        assert response_json.get("id") is not None
        assert response_json.get("task_id") is not None
        assert response_json.get("account_id") is not None
        if expected_text:
            assert response_json.get("text") == expected_text

    def assert_error_response(self, response, expected_status: int, expected_error_code: str):
        assert response.status_code == expected_status, f"Expected status {expected_status}, got {response.status_code}"
        if response.headers.get("Content-Type") != "application/json":
            raise CommentBadRequestError("Expected JSON response, got non-JSON response.")
        assert response.json is not None, f"Expected JSON response, got None. Response data: {response.data}"
        assert (
            response.json.get("code") == expected_error_code
        ), f"Expected error code {expected_error_code}, got {response.json.get('code')}"
