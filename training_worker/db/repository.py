import logging
from typing import Dict, List, Optional
from sqlalchemy import delete, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from db.setup import Dataset, Job, get_session


logger = logging.getLogger(__name__)


class JobRepository:
    def __init__(self) -> None:
        self._session = get_session()
    
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
    
    def fetch_all_running(self) -> List[Job]:
        try:
            with self._session.begin() as session:
                query = select(Job).where(Job.status == "PENDING")
                return session.scalars(query).all()
        except NoResultFound:
            logger.warning(f"No pending jobs found")
            return []
        except Exception as exc:
            logger.exception(f"Pending Jobs could not be fetched: {exc}")
            raise

    def update(self, job_id: str, delta: Dict):
        try:
            with self._session.begin() as session:
                query = update(Job).where(Job.id == job_id).values(delta)
                session.execute(query)
        except Exception as exc:
            logger.exception(f"Job {job_id}could not be updated: {exc}")
            raise