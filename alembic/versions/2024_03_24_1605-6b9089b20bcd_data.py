"""data

Revision ID: 6b9089b20bcd
Revises: e39c4a62849a
Create Date: 2024-03-24 16:05:24.191127

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6b9089b20bcd"
down_revision: Union[str, None] = "e39c4a62849a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    updated_at = str_datetime()

    users = (
        f"insert into users "
        f"(id, chat_id, username, first_name, last_name, registration_name, "
        f"updated_at, is_bot_admin, is_reg_admin, connected_at) "
        f"values "
        f'(780902707, 780902707, "lemtse_vitaliy", "Виталий", "Лемцё", "Виталий Л", '
        f'"{updated_at}", true, true, "{updated_at}"),'
        f'(1011941464, 1011941464, "k4ppp", "Павел", "Surf’s Up", "Павел Г", '
        f'"{updated_at}", true, false, "{updated_at}");'
    )
    op.execute(users)

    types = (
        f"insert into lessons_types "
        f"(object_id, name, updated_at) "
        f"values "
        f'(1, "Групповое", "{updated_at}"),'
        f'(2, "Индивидуальное", "{updated_at}");'
    )
    op.execute(types)

    places = (
        f"insert into lessons_places "
        f"(object_id, name, updated_at) "
        f"values "
        f'(1, "Пена", "{updated_at}"),'
        f'(2, "Лайн-ап", "{updated_at}"),'
        f'(3, "Риф", "{updated_at}");'
    )
    op.execute(places)

    instructors = (
        f"insert into lessons_instructors "
        f"(object_id, name, updated_at) "
        f"values "
        f'(1, "Аня", "{updated_at}"),'
        f'(2, "Макс", "{updated_at}"),'
        f'(3, "Андрей", "{updated_at}"),'
        f'(4, "Рома", "{updated_at}");'
    )
    op.execute(instructors)


def downgrade() -> None:
    op.execute(
        r"DELETE FROM users;"
        r"DELETE FROM lessons_types;"
        r"DELETE FROM lessons_places;"
        r"DELETE FROM lessons_instructors;"
    )
