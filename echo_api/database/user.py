from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from echo_api.database import Base

if TYPE_CHECKING:
    from .project import Project


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()

    projects: Mapped["Project"] = relationship(back_populates="owner")
