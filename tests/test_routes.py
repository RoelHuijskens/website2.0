from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from unittest.mock import MagicMock
import pytest
from app.dependencies import get_chat_controller
from app.models import ChatResponse


@pytest.fixture
def chat_controller_mock():
    return MagicMock()


@pytest.fixture
def client_mock(chat_controller_mock):
    app.dependency_overrides[get_chat_controller] = (
        lambda: chat_controller_mock
    )
    return TestClient(app)


class TestRoutes:
    def test_chat_post_no_chat_id_succesfull(
        self, client_mock, chat_controller_mock
    ):
        test_response_dict = {
            "content": "This is a test response",
            "role": "bot",
            "chat_id": "1234",
        }

        test_response = ChatResponse(**test_response_dict)

        chat_controller_mock.handle_user_question.return_value = test_response

        response = client_mock.post(
            "/chat",
            json={"content": "This is a test question", "role": "user"},
        )

        assert response.status_code == 200
        assert response.json() == test_response_dict

    def test_chat_post_no_chat_id_failed(
        self, client_mock, chat_controller_mock
    ):
        chat_controller_mock.handle_user_question.side_effect = Exception(
            "Test exception"
        )

        response = client_mock.post(
            "/chat",
            json={"content": "This is a test question", "role": "user"},
        )

        assert response.status_code == 503
        assert response.json() == {
            "detail": "Something went wrong while processing your request, please try again later"
        }

    def test_chat_post_no_chat_id_http_exception(
        self, client_mock, chat_controller_mock
    ):
        chat_controller_mock.handle_user_question.side_effect = HTTPException(
            detail="Test specific exception", status_code=503
        )

        response = client_mock.post(
            "/chat",
            json={"content": "This is a test question", "role": "user"},
        )

        assert response.status_code == 503
        assert response.json() == {"detail": "Test specific exception"}

    def test_chat_post_chat_id_success(
        self, client_mock, chat_controller_mock
    ):
        test_response_dict = {
            "content": "This is a test response",
            "role": "bot",
            "chat_id": "1234",
        }

        test_response = ChatResponse(**test_response_dict)

        chat_controller_mock.handle_user_question.return_value = test_response

        response = client_mock.post(
            "/chat?conversation_id=1234",
            json={"content": "This is a test question", "role": "user"},
        )

        assert response.status_code == 200
        assert response.json() == test_response_dict

    def test_chat_get_success(self, client_mock, chat_controller_mock):
        expected = {"test": "ok"}

        chat_controller_mock.get_chat = MagicMock(return_value=expected)

        response = client_mock.get("/chat?conversation_id=1234&hash=4321")

        assert response.status_code == 200
        assert response.json() == expected

        chat_controller_mock.get_chat.assert_called_once_with(
            conversation_id="1234", hash="4321"
        )
