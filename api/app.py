from datetime import datetime
import logging
import os
import shutil
import uuid

from flask import Flask, request, send_file
from dotenv import load_dotenv

from db.model import Dataset, Job
from db.repository import DatasetRepository, JobRepository
from model import JobStatus

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

@app.post("/api/v1/dataset")
def upload_dataset():
    dataset_id = uuid.uuid4()
    created_at = datetime.isoformat(datetime.utcnow())
    dataset = Dataset(id=dataset_id, created_at=created_at)
    try:
        os.mkdir(f"../files/{dataset_id}")
        with open(f"../files/{dataset_id}/source.csv", "w", encoding="utf-8") as fh:
            fh.write(request.get_data().decode("utf-8"))
    except FileExistsError:
        logger.error(f"Dataset '{dataset_id}' already exists")
        return {"error": f"Dataset '{dataset_id}' already exists"}, 409
    except Exception as exc:
        logger.error(f"Persisting dataset '{dataset_id}' failed. Cleaning up: {exc}")
        shutil.rmtree(f"../files/{dataset_id}")
        return {"error": "Dataset could not be created"}, 500
    
    try:
        dataset_repo = DatasetRepository()
        dataset_repo.create(dataset)
    except Exception as exc:
        logger.exception(f"Could insert dataset '{dataset_id}' into db: {exc}")
        return {"error": f"Dataset '{dataset_id}' could not be created"}

    return {"dataset_id": dataset_id, "created_at": created_at}, 201

@app.get("/api/v1/dataset/<dataset_id>")
def get_synthetic_dataset(dataset_id):
    file_path = f"../files/{dataset_id}"
    if not os.path.exists(file_path) or not os.path.exists(f"{file_path}/synthetic.csv"):
        return {"error": f"Dataset '{dataset_id}' not found"}, 404
    try:
        return send_file(f"{file_path}/synthetic.csv", as_attachment=True, download_name=f"{dataset_id}_synthetic.csv")
    except Exception as exc:
        logger.error(f"Dataset '{dataset_id}' could not be deleted: {exc}")


@app.delete("/api/v1/dataset/<dataset_id>")
def delete_dataset(dataset_id):
    file_path = f"../files/{dataset_id}"
    if not os.path.exists(file_path):
        return {"error": f"Dataset '{dataset_id}' not found"}, 404
    try:
        shutil.rmtree(f"../files/{dataset_id}")
        dataset_repo = DatasetRepository()
        dataset_repo.delete(dataset_id)
        return {"message": f"Dataset '{dataset_id}' deleted successfully"}, 200
    except Exception as exc:
        logger.error(f"Dataset '{dataset_id}' could not be deleted: {exc}")

    return {"error": f"Dataset '{dataset_id}'"}


@app.post("/api/v1/job")
def create_job():
    payload = request.get_json()
    job_id = uuid.uuid4()
    created_at = datetime.isoformat(datetime.utcnow())
    dataset_id = payload["dataset_id"]
    try:
        job = Job(id=job_id, created_at=created_at, status=JobStatus.PENDING.value, dataset_id=dataset_id)
        job_repo = JobRepository()
        job_repo.create(job)
    except Exception as exc:
        logger.error(f"Job '{job_id}' could not be created: {exc}")
        return {"error": f"Job '{job_id}' could not be created"}, 500
    return job.to_dict(), 201


@app.get("/api/v1/job/<job_id>")
def get_job(job_id):
    try:
        job_repo = JobRepository()
        job = job_repo.fetch(job_id)
        if not job:
            return {"error": f"Job '{job_id}' not found"}, 404
        return job.to_dict(), 200
    except Exception as exc:
        logger.exception(f"Job '{job_id}' could not be fetched: {exc}")
        return {"error": f"Job '{job_id}' could not be fetched"}, 500
    

@app.delete("/api/v1/job/<job_id>")
def delete_job(job_id):
    try:
        job_repo = JobRepository()
        job = job_repo.fetch(job_id)
        if not job:
            return {"error": f"Job '{job_id}' not found"}, 404
        # if job.status == JobStatus.RUNNING.value:
        #     return {"error": f"Job '{job_id}' is in RUNNING status. RUNNING jobs cannot be deleted"}, 409
        job_repo.delete(job_id)
        return {"message": f"Job '{job_id}' deleted successfully"}, 200
    except Exception as exc:
        logger.exception(f"Job '{job_id}' could not be deleted: {exc}")
        return {"error": f"Job '{job_id}' could not be deleted"}, 500