from app.controllers.chat_controller import (
    ChatsController,
    ChatResponse,
    QuestionDto,
    ConversationDto,
)

from unittest.mock import MagicMock
from fastapi import HTTPException
from datetime import datetime
import pytest
import re


@pytest.fixture
def conversation_dao_mock():
    return MagicMock()


@pytest.fixture
def notifications_mock():
    return MagicMock()


@pytest.fixture
def openai_client_mock():
    return MagicMock()


@pytest.fixture
def chat_controller(
    conversation_dao_mock, notifications_mock, openai_client_mock
):
    chat_controller_mock = ChatsController(
        db=conversation_dao_mock,
        notifications=notifications_mock,
        openai_client=openai_client_mock,
    )
    chat_controller_mock._start_notification_thread = MagicMock()
    return chat_controller_mock


@pytest.fixture
def question_mock():
    return QuestionDto(
        content="This is a test question",
        role="user",
    )


@pytest.fixture
def conversation_mock():
    question_mock_2 = QuestionDto(
        content="This is a test question 2",
        role="bot",
    )

    question_mock_3 = QuestionDto(
        content="This is a test question 3",
        role="user",
    )

    return ConversationDto(
        questions=[question_mock_2, question_mock_3],
        chat_id="1234",
        start_time=datetime.now(),
    )


@pytest.fixture
def chat_response_mock():
    return ChatResponse(
        content="This is a test response", role="bot", chat_id="1234"
    )


class TestChatController:
    def test_init(
        self, conversation_dao_mock, notifications_mock, openai_client_mock
    ):
        controller = ChatsController(
            db=conversation_dao_mock,
            notifications=notifications_mock,
            openai_client=openai_client_mock,
        )

        assert controller.db == conversation_dao_mock
        assert controller.notifications == notifications_mock
        assert controller.openai_client == openai_client_mock

    def test_check_recent_chat_limits_passsed(
        self, chat_controller, notifications_mock
    ):
        chat_controller.db.get_recent_chats_count.return_value = 24
        question_mock = MagicMock()
        question_mock.content = "This is a test question"

        chat_controller._check_recent_chats_limit(question=question_mock)

        chat_controller.db.get_recent_chats_count.assert_called_once()

    def test_check_recent_chat_limits_failed(self, chat_controller):
        notifications_mock.send_update_notification = MagicMock()

        chat_controller.db.get_recent_chats_count.return_value = 26

        question_mock = MagicMock()
        question_mock.content = "This is a test question"

        with pytest.raises(
            HTTPException,
            match="""503: Appologies, too many conversations have been
                started in the last hour, please try again later.""",
        ):
            chat_controller._check_recent_chats_limit(question=question_mock)

        chat_controller._start_notification_thread.assert_called_once_with(
            "Max conversations count triggered: This is a test question"
        )

    def test_check_current_chat_limit_passed(self, chat_controller):
        current_chat = MagicMock()
        current_chat.questions = [MagicMock() for _ in range(9)]

        assert not chat_controller._check_current_chat_limit(current_chat)

    def test_check_current_chat_limit_failed(self, chat_controller):
        current_chat = MagicMock()
        current_chat.chat_id = "1234"
        current_chat.questions = [MagicMock() for _ in range(10)]

        with pytest.raises(
            HTTPException,
            match=re.escape(
                """503: It seems you have a lot of questions,
                let's connect via [**linkedin** (link)](https://nl.linkedin.com/in/roel-huijskens)
                I can answer more there."""
            ),
        ):
            chat_controller._check_current_chat_limit(current_chat)

    def test_get_or_create_conversation_new(self, chat_controller):
        chat_controller.db.create_chat = MagicMock()

        question_mock = QuestionDto(
            content="This is a test question",
            role="user",
        )

        new_chat = chat_controller._get_or_create_conversation(
            question=question_mock, conversation_id=None
        )

        chat_controller._start_notification_thread.assert_called_once()

        assert isinstance(new_chat, ConversationDto)

        assert new_chat.questions == [question_mock]
        assert isinstance(new_chat.start_time, datetime)
        assert isinstance(new_chat.chat_id, str)

        chat_controller.db.create_chat.assert_called_once_with(new_chat)

    def test_get_or_create_conversation_existing(self, chat_controller):
        current_chat_mock = MagicMock()
        current_chat_mock.chat_id = "1234"
        chat_controller.db.get_chat_by_id.return_value = current_chat_mock
        chat_controller.db.append_chat = MagicMock()

        question_mock = QuestionDto(
            content="This is a test question",
            role="user",
        )

        existing_chat = chat_controller._get_or_create_conversation(
            question=question_mock, conversation_id="1234"
        )

        assert existing_chat == chat_controller.db.get_chat_by_id.return_value

        chat_controller.db.append_chat.assert_called_once_with(
            question_mock, "1234"
        )

    def test_get_or_create_conversation_existing_not_found(
        self, chat_controller
    ):
        chat_controller.db.get_chat_by_id.return_value = None

        question_mock = QuestionDto(
            content="This is a test question",
            role="user",
        )

        with pytest.raises(
            HTTPException,
            match="404: Failed to retrieve specified chat, try refreshing your page",
        ):
            chat_controller._get_or_create_conversation(
                question=question_mock, conversation_id="1234"
            )

    def test_format_and_store_response(self, chat_controller):
        chat_controller.db.append_chat = MagicMock()

        response = chat_controller._format_and_store_response(
            response="This is a test response",
            annotations=["test1", "test2"],
            chat_id="1234",
        )

        assert response.content == "This is a test response"
        assert response.role.value == "bot"
        assert response.chat_id == "1234"

        chat_controller.db.append_chat.assert_called_once_with(
            response, chat_id="1234", annotations=["test1", "test2"]
        )

    def test_handle_user_question(
        self,
        chat_controller,
        question_mock,
        conversation_mock,
        chat_response_mock,
    ):
        chat_controller._check_recent_chats_limit = MagicMock()
        chat_controller._get_or_create_conversation = MagicMock(
            return_value=conversation_mock
        )
        chat_controller._check_current_chat_limit = MagicMock(
            return_value=None
        )
        chat_controller._format_and_store_response = MagicMock(
            return_value=chat_response_mock
        )

        chat_controller.openai_client.submit_assistant_question = MagicMock(
            return_value=("This is a test response", ["test1", "test2"])
        )

        result = chat_controller.handle_user_question(
            question=question_mock, conversation_id="1234"
        )

        assert result == chat_response_mock
        chat_controller._check_recent_chats_limit.assert_called_once_with(
            question_mock
        )
        chat_controller._get_or_create_conversation.assert_called_once_with(
            question_mock, "1234"
        )
        chat_controller._check_current_chat_limit.assert_called_once_with(
            current_chat=conversation_mock
        )
        chat_controller.openai_client.submit_assistant_question.assert_called_once_with(
            chat_history=conversation_mock.questions, question=question_mock
        )

    def test_handle_conversations_limit_reached(
        self, question_mock, chat_controller
    ):
        chat_controller._check_recent_chats_limit = MagicMock(
            side_effect=HTTPException(
                detail="Appologies, too many conversations have been started in the last hour, please try again later.",
                status_code=503,
            )
        )

        with pytest.raises(
            HTTPException,
            match="Appologies, too many conversations have been started in the last hour, please try again later.",
        ):
            chat_controller.handle_user_question(
                question=question_mock, conversation_id="1234"
            )

    def test_handle_question_limit_reached(
        self,
        question_mock,
        chat_response_mock,
        chat_controller,
        conversation_mock,
    ):
        chat_controller._check_recent_chats_limit = MagicMock()
        chat_controller._get_or_create_conversation = MagicMock(
            return_value=conversation_mock
        )
        chat_controller._check_current_chat_limit = MagicMock(
            side_effect=HTTPException(detail="Ooh boy", status_code=503)
        )

        with pytest.raises(HTTPException, match="503: Ooh boy"):
            chat_controller.handle_user_question(
                question=question_mock, conversation_id="1234"
            )

    def test_get_chat_success(self, chat_controller, conversation_mock):
        chat_controller._get_security_hash = MagicMock(return_value="4321")

        chat_controller.db.get_chat_by_id.return_value = conversation_mock

        result = chat_controller.get_chat(conversation_id="1234", hash="4321")

        assert result == conversation_mock.model_dump()

        chat_controller.db.get_chat_by_id.assert_called_once_with("1234")

    def test_get_chat_not_found(self, chat_controller):
        chat_controller._get_security_hash = MagicMock(return_value="4321")

        chat_controller.db.get_chat_by_id.return_value = None

        with pytest.raises(HTTPException, match="Could not find chat 1234"):
            chat_controller.get_chat(conversation_id="1234", hash="4321")

        chat_controller.db.get_chat_by_id.assert_called_once_with("1234")

    def test_get_chat_invalid_hash(self, chat_controller):
        chat_controller._get_security_hash = MagicMock(return_value="4321")

        chat_controller.db.get_chat_by_id.return_value = None

        with pytest.raises(
            HTTPException,
            match="What on earth are you doing here\?\? Please leave..",
        ):
            chat_controller.get_chat(conversation_id="1234", hash="1234")

        chat_controller.db.get_chat_by_id.assert_not_called()
