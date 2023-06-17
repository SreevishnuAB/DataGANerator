from typing import Optional
from uuid import UUID
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Dataset(Base):

    __tablename__ = "dataset"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    created_at: Mapped[str]

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}

    def __repr__(self) -> str:
        return f"Dataset(id={self.id}, created_at={self.created_at})"


class Job(Base):
    __tablename__ = "job"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    status: Mapped[str]
    created_at: Mapped[str]
    completed_at: Mapped[Optional[str]]
    dataset_id: Mapped[UUID] = mapped_column(ForeignKey("dataset.id", ondelete="CASCADE"))

    def to_dict(self):
        return {field.name:getattr(self, field.name) for field in self.__table__.c}

    def __repr__(self) -> str:
        return f"Job(id={self.id}, status={self.status}, created_at={self.created_at}, completed_at={self.completed_at}, dataset_id={self.dataset_id})"