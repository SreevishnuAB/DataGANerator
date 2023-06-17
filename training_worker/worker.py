from datetime import datetime
import logging
import os
import time

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from db.repository import JobRepository
from utils import train_data, evaluate_data

logging.basicConfig(format="%(asctime)s - %(levelname)s: %(message)s", filename="../logs/worker.log", level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    while True:
        pending_jobs = JobRepository().fetch_all_running()
        logger.info(f"Pending jobs: {len(pending_jobs)}")
        for job in pending_jobs:
            JobRepository().update(job.id, {"status": "RUNNING"})
            df = pd.read_csv(f"../files/{job.dataset_id}/source.csv", dtype="str")
            synthetic_data = train_data(df)
            save_dir = f"../files/{job.dataset_id}/metrics"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            evaluate_data(df, synthetic_data, save_dir)
            synthetic_data.to_csv(f"../files/{job.dataset_id}/synthetic.csv", index=False, header=True)
            JobRepository().update(job.id, {"status": "COMPLETED", "completed_at": datetime.isoformat(datetime.utcnow())})
            time.sleep(5)

if __name__ == "__main__":
    main()