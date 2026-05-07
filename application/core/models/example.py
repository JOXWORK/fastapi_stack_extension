from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Example(Base):
    example: Mapped[str] = mapped_column(
        default="example",
        server_default="example",
    )
