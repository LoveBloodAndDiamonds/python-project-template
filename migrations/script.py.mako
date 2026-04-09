"""${message}

ID ревизии: ${up_revision}
Базовая ревизия: ${down_revision | comma,n}
Дата создания: ${create_date}

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    """Применяет изменения схемы."""
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    """Откатывает изменения схемы."""
    ${downgrades if downgrades else "pass"}
