from uuid import UUID

from models.manager import Manager
from models import UserSession


def register_user_session(user_id: int, session_uuid: UUID):
    session = UserSession()
    session.userId = user_id
    session.uuid = session_uuid
    Manager.check_and_save(session)


def delete_user_session(user_id: int, session_uuid: UUID):
    session = UserSession.query \
        .filter_by(userId=user_id, uuid=session_uuid) \
        .first()
    Manager.delete(session)


def existing_user_session(user_id: int, session_uuid: UUID) -> bool:
    session = UserSession.query \
        .filter_by(userId=user_id, uuid=session_uuid) \
        .first()
    return session is not None
