import pytest
from unittest.mock import MagicMock
from app.domain.openai import OpenaiInterface


@pytest.fixture
def openai_client_mock():
    return MagicMock()


@pytest.fixture
def openai_interface_mock(openai_client_mock):
    return OpenaiInterface(openai_client_mock, "1234")


class TestOpenaiInterface:
    def test_init(self, openai_client_mock):
        openai_interface = OpenaiInterface(openai_client_mock, "1234")

        assert openai_interface.client == openai_client_mock
        assert openai_interface.assistant_id == "1234"

    def test_get_assistant(self, openai_interface_mock):
        assistant_mock = MagicMock()

        openai_interface_mock.client.beta.assistants.retrieve.return_value = (
            assistant_mock
        )

        result = openai_interface_mock._get_assistant()

        assert result == assistant_mock
        openai_interface_mock.client.beta.assistants.retrieve.assert_called_once_with(
            assistant_id="1234"
        )

    def test_get_thread(self, openai_interface_mock):
        thread_mock = MagicMock()

        openai_interface_mock.client.beta.threads.create.return_value = (
            thread_mock
        )

        chat_history = [MagicMock()]

        result = openai_interface_mock._get_thread(chat_history)

        assert result == thread_mock
        openai_interface_mock.client.beta.threads.create.assert_called_once_with(
            messages=chat_history
        )

    def test_create_message(self, openai_interface_mock):
        message_mock = MagicMock()

        thread_id = 1234
        question = "This is a test question"

        openai_interface_mock.client.beta.threads.messages.create.return_value = message_mock

        result = openai_interface_mock._create_message(thread_id, question)

        assert result == message_mock
        openai_interface_mock.client.beta.threads.messages.create.assert_called_once_with(
            thread_id=thread_id, role="user", content=question
        )

    def test_await_response_succesfull(self, openai_interface_mock):
        message_mock = MagicMock()
        message_mock.content = "This is a test message"

        message_list_mock = MagicMock()
        message_list_mock.data = [message_mock]

        openai_interface_mock.client.beta.threads.messages.list.return_value = message_list_mock

        run_mock = MagicMock()
        run_mock.status = "completed"
        thread_mock = MagicMock()
        thread_mock.id = 1234

        openai_interface_mock._clean_openai_response = MagicMock(
            return_value=("This is a test response", ["test1", "test2"])
        )

        result_question, result_annotations = (
            openai_interface_mock._await_response(run_mock, thread_mock)
        )
        assert result_question == "This is a test response"
        assert result_annotations == ["test1", "test2"]
        openai_interface_mock.client.beta.threads.messages.list.assert_called_once_with(
            thread_id=thread_mock.id, limit=1
        )

        openai_interface_mock._clean_openai_response.assert_called_once_with(
            message_mock.content
        )

    def test_await_response_timeout(self, openai_interface_mock):
        with pytest.raises(
            Exception,
            match="The response took too long to arrive, please try again later.",
        ):
            openai_interface_mock._await_response(
                run=MagicMock(status="running"),
                thread=MagicMock(),
                timeout_sec=1,
            )

    def test_clean_openai_response(self, openai_interface_mock):
        from openai.types.beta.threads.text_content_block import (
            TextContentBlock,
        )
        from openai.types.beta.threads.text import Text
        from openai.types.beta.threads.file_citation_annotation import (
            FileCitationAnnotation,
            FileCitation,
        )

        response = [
            TextContentBlock(
                text=Text(
                    value="This is a test value",
                    annotations=[
                        FileCitationAnnotation(
                            file_citation=FileCitation(file_id="test1"),
                            start_index=0,
                            end_index=4,
                            type="file_citation",
                            text="test",
                        ),
                        FileCitationAnnotation(
                            file_citation=FileCitation(file_id="test2"),
                            start_index=0,
                            end_index=4,
                            type="file_citation",
                            text="test",
                        ),
                    ],
                ),
                type="text",
            )
        ]

        result_question, result_annotations = (
            openai_interface_mock._clean_openai_response(response)
        )

        assert result_question == "This is a test value"
        assert result_annotations == ["test1", "test2"]

    def test_clean_openai_respons_invalid_type(self, openai_interface_mock):
        response = [MagicMock()]

        with pytest.raises(
            Exception,
            match="Openai response did not contain a content block got: <MagicMock",
        ):
            openai_interface_mock._clean_openai_response(response)

    def test_submit_assistant_question_sucesfull(self, openai_interface_mock):
        question_mocks = []
        for index in range(3):
            question_mock = MagicMock()
            question_mock.to_openai_message.return_value = (
                f"Test message {index}"
            )
            question_mock.content = f"Test content {index}"
            question_mocks.append(question_mock)

        chat_history = question_mocks[1:2]
        question = question_mocks[0]

        assistant_mock = MagicMock()
        thread_mock = MagicMock()
        thread_mock.id = 1234
        run_mock = MagicMock()

        openai_interface_mock._get_assistant = MagicMock(
            return_value=assistant_mock
        )
        openai_interface_mock._get_thread = MagicMock(return_value=thread_mock)
        openai_interface_mock._create_message = MagicMock()
        openai_interface_mock.client.beta.threads.runs.create_and_poll = (
            MagicMock(return_value=run_mock)
        )
        openai_interface_mock._await_response = MagicMock(
            return_value=("This is a test response", ["test1", "test2"])
        )

        response, annotations = (
            openai_interface_mock.submit_assistant_question(
                chat_history, question
            )
        )

        assert response == "This is a test response"
        assert annotations == ["test1", "test2"]

        openai_interface_mock._get_assistant.assert_called_once()
        openai_interface_mock._get_thread.assert_called_once_with(
            [message.to_openai_message() for message in chat_history]
        )
        openai_interface_mock._create_message.assert_called_once_with(
            thread_mock.id, question.content
        )

        openai_interface_mock._await_response.assert_called_once_with(
            run_mock, thread_mock
        )

    def test_submit_assistant_question_too_long(self, openai_interface_mock):
        question_mocks = []
        for index in range(3):
            question_mock = MagicMock()
            question_mock.to_openai_message = MagicMock(
                return_value=f"Test message {index}"
            )
            question_mock.content = "A" * 151
            question_mocks.append(question_mock)

        chat_history = [question for question in question_mocks[1:3]]
        question = question_mocks[0]

        warning, nothing = openai_interface_mock.submit_assistant_question(
            chat_history, question
        )

        assert (
            warning
            == """I'm sorry, your question was too long (151 characters).
                    I like OpenAI but I am not made of money, so I've capped the total character count for questions to 150."""
        )
        assert not nothing
