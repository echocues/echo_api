from echo_api.database import Base

from sqlalchemy.orm import relationship, Mapped, mapped_column

__all__ = ("User",)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()

    projects: Mapped["Project"] = relationship(back_populates="owner")
