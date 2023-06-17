import logging
from typing import Optional
from sqlalchemy import delete, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.setup import Dataset, Job, get_session


logger = logging.getLogger(__name__)

class DatasetRepository:
    def __init__(self) -> None:
        self._session = get_session()

    def create(self, dataset: Dataset) -> None:
        try:
            with self._session.begin() as session:
                session.add_all([dataset])
        except Exception as exc:
            logger.exception(f"Dataset '{dataset.id}' could not be created: {exc}")
            raise

    def delete(self, dataset_id: str):
        try:
            with self._session.begin() as session:
                stmt = delete(Dataset).where(Dataset.id == dataset_id)
                session.execute(stmt)
        except Exception as exc:
            logger.exception(f"Dataset '{dataset_id}' could not be deleted: {exc}")
            raise    


class JobRepository:
    def __init__(self) -> None:
        self._session = get_session()

    def create(self, job: Job) -> None:
        try:
            with self._session.begin() as session:
                session.add_all([job])
        except Exception as exc:
            logger.exception(f"Job '{job.id}' could not be created: {exc}")
            raise

    def delete(self, job_id: str) -> None:
        try:
            with self._session.begin() as session:
                stmt = delete(Job).where(Job.id == job_id)
                session.execute(stmt)
        except Exception as exc:
            logger.exception(f"Job '{job_id}' could not be deleted: {exc}")
            raise
    
    def fetch(self, job_id: str) -> Optional[Job]:
        try:
            with self._session.begin() as session:
                query = select(Job).where(Job.id == job_id)
                return session.scalars(query).one()
        except NoResultFound:
            logger.warning(f"No job '{job_id}' found")
            return None
        except Exception as exc:
            logger.exception(f"Job '{job_id}' could not be fetched: {exc}")
            raise   