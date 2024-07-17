from openai import OpenAI
from app.domain.openai import OpenaiInterface
import os
from pymongo import MongoClient
from app.db.dao import ConversationsDao
from app.logging.nofications import NotificationsInterface
from app.controllers.chat_controller import ChatsController


openai_client = OpenAI()
assistant_id = os.getenv("OPENAI_ASS_ID")


def get_openai_interface() -> OpenaiInterface:
    """Get openai Interface

    Returns:
        OpenaiInterface: instance of openai interface
    """
    if not assistant_id:
        raise ValueError("OPENAI_ASS_ID not set")
    return OpenaiInterface(client=openai_client, assistant_id=assistant_id)


def get_mongodb_client() -> ConversationsDao:
    """Get mongodb client

    Raises:
        Exception: Exception if environment variables are not set.

    Returns:
        ConversationsDao: Instance of monodb Dao for chats.
    """

    USER_NAME = os.getenv("DB_USER_NAME")
    PW = os.getenv("DB_PASSWORD")

    if not USER_NAME or not PW:
        raise Exception("Forgto to set DB_USER_NAME or DB_PASSWORD")
    connection_string = f"mongodb+srv://{USER_NAME}:{PW}@conversations-info.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"  # noqa E501

    # Create a MongoDB client
    client: MongoClient = MongoClient(connection_string)

    return ConversationsDao(client)


def get_notification_interface() -> NotificationsInterface:
    """Get notifications interface

    Returns:
        NotificationsInterface: Notifications interface for sending emails.
    """
    return NotificationsInterface(
        endpoint=os.getenv("AZURE_MAIL_SERVICE_ENDPOINT"),  # type: ignore
        notification_email=os.getenv("NOTIFICATION_MAIL"),  # type: ignore
        sender_adress=os.getenv("AZURE_MAIL_SERVICE_DOMAIN"),  # type: ignore
    )


async def get_chat_controller():
    """Get chat controller

    Yields:
        AsyncGenerator: Generator yielding chat controller instance.
    """
    chat_controller = ChatsController(
        db=get_mongodb_client(),
        notifications=get_notification_interface(),
        openai_client=get_openai_interface(),
    )

    yield chat_controller

    chat_controller.db.client.close()
