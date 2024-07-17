import pytest
import datetime
from unittest.mock import MagicMock
from app.db.dao import ConversationsDao, ConversationDto
from app.models import Role, QuestionDto


@pytest.fixture
def db_client_mock():
    return MagicMock()


@pytest.fixture
def dao_mock(db_client_mock):
    return ConversationsDao(db_client_mock)


class TestConversationsDao:
    def test_init(self, db_client_mock):
        dao = ConversationsDao(db_client_mock)
        assert dao.client == db_client_mock

    def test_append_chat_no_annotations(self, dao_mock):
        mock_question = MagicMock()
        question_dict = {"content": "This is a test question"}
        mock_question.to_dict.return_value = question_dict

        dao_mock.append_chat(question=mock_question, chat_id="1234")

        mock_question.to_dict.assert_called_once()
        dao_mock.client["PersonalWebsite"][
            "Conversations"
        ].update_one.assert_called_once_with(
            {"_id": "1234"}, {"$push": {"questions": question_dict}}
        )

    def test_append_chat_annotations(self, dao_mock):
        mock_question = MagicMock()

        annotations = ["test1", "test2"]
        question_dict = {
            "content": "This is a test question",
        }

        mock_question.to_dict.return_value = question_dict

        dao_mock.append_chat(
            question=mock_question, chat_id="1234", annotations=annotations
        )

        mock_question.to_dict.assert_called_once()
        dao_mock.client["PersonalWebsite"][
            "Conversations"
        ].update_one.assert_called_once_with(
            {"_id": "1234"}, {"$push": {"questions": question_dict}}
        )

        assert question_dict["annotations"] == annotations

    def test_get_chat_by_id(self, dao_mock):
        chat = {
            "_id": "1234",
            "start_time": "2021-01-01T00:00:00",
            "questions": [
                {"content": "This is a test question", "role": "user"}
            ],
        }

        dao_mock.client["PersonalWebsite"][
            "Conversations"
        ].find_one.return_value = chat

        conversation = dao_mock.get_chat_by_id("1234")

        assert conversation.chat_id == "1234"
        assert conversation.start_time == datetime.datetime.strptime(
            "2021-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"
        )
        assert len(conversation.questions) == 1
        assert conversation.questions[0].content == "This is a test question"
        assert conversation.questions[0].role.value == "user"

    def test_create_chat(self, dao_mock):
        mock_question_1 = QuestionDto(
            content="This is a test question", role=Role.USER
        )

        mock_question_2 = QuestionDto(
            content="This is a test question", role=Role.BOT
        )

        conversation = ConversationDto(
            chat_id="1234",
            start_time=datetime.datetime.strptime(
                "2021-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"
            ),
            questions=[mock_question_1, mock_question_2],
        )

        dao_mock.create_chat(conversation)

        dao_mock.client["PersonalWebsite"][
            "Conversations"
        ].insert_one.assert_called_once_with(
            {
                "_id": "1234",
                "start_time": datetime.datetime.strptime(
                    "2021-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"
                ),
                "questions": [
                    {
                        "content": "This is a test question",
                        "role": "user",
                        "annotations": [],
                    }
                ],
            }
        )

    def test_get_recent_chats_count(self, dao_mock):
        dao_mock.client["PersonalWebsite"][
            "Conversations"
        ].count_documents.return_value = 5

        test_time = datetime.datetime.strptime(
            "2021-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S"
        )

        assert dao_mock.get_recent_chats_count(test_time) == 5
        dao_mock.client["PersonalWebsite"][
            "Conversations"
        ].count_documents.assert_called_once_with(
            {"start_time": {"$gte": test_time}}
        )
