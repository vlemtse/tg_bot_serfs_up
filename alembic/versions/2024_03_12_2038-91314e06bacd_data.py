"""data

Revision ID: 91314e06bacd
Revises: b8f32bf9c394
Create Date: 2024-03-12 20:38:06.731095

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.db import Users

# revision identifiers, used by Alembic.
revision: str = "91314e06bacd"
down_revision: Union[str, None] = "b8f32bf9c394"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    from sqlalchemy import orm
    from app.db.models import LessonTypeDb
    from app.funcs import str_datetime

    user = Users(
        id=780902707,
        username="lemtse_vitaliy",
        first_name="Виталий",
        last_name="Лемцё",
        registration_name="Виталий Л",
        updated_at=str_datetime(),
        is_admin=True,
    )

    type1 = LessonTypeDb(object_id=1, name="Групповое", updated_user_id=780902707)
    type2 = LessonTypeDb(object_id=2, name="Индивидуальное", updated_user_id=780902707)

    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.add_all([user, type1, type2])
    session.commit()
    session.close()


def downgrade() -> None:
    pass
