"""data

Revision ID: e377380cc40b
Revises: b70de2c8b8b0
Create Date: 2024-03-16 01:18:40.791617

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.db.models import *

# revision identifiers, used by Alembic.
revision: str = "e377380cc40b"
down_revision: Union[str, None] = "b70de2c8b8b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from sqlalchemy import orm
    from app.db.models import LessonTypeDb, LessonPlaceDb
    from app.funcs import str_datetime

    user = UserDb(
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

    place1 = LessonPlaceDb(object_id=1, name="Пена", updated_user_id=780902707)
    place2 = LessonPlaceDb(object_id=2, name="Лайн-ап", updated_user_id=780902707)
    place3 = LessonPlaceDb(object_id=3, name="Риф", updated_user_id=780902707)

    i1 = LessonInstructorDb(object_id=1, name="Аня", updated_user_id=780902707)
    i2 = LessonInstructorDb(object_id=2, name="Макс", updated_user_id=780902707)
    i3 = LessonInstructorDb(object_id=3, name="Андрей", updated_user_id=780902707)
    i4 = LessonInstructorDb(object_id=4, name="Рома", updated_user_id=780902707)

    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.add_all([user, type1, type2, place1, place2, place3, i1, i2, i3, i4])
    session.commit()
    session.close()


def downgrade() -> None:
    pass
