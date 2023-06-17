import logging

import pandas as pd
from sdv.single_table import CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
from table_evaluator import TableEvaluator

logger = logging.getLogger(__name__)


def train_data(df: pd.DataFrame) -> pd.DataFrame:
    metadata = SingleTableMetadata()
    metadata.detect_from_dataframe(df)
    logger.info(metadata.to_dict())
    synthesizer = CTGANSynthesizer(
        metadata, # required
        epochs=100,
        verbose=True
    )
    synthesizer.fit(df)
    synthetic_data = synthesizer.sample(
        num_rows=2000
    )
    return synthetic_data


def evaluate_data(df: pd.DataFrame, synthetic_data: pd.DataFrame, save_dir: str):
    table_evaluator =  TableEvaluator(df, synthetic_data)
    try:
        table_evaluator.visual_evaluation(save_dir=save_dir)
    except Exception:
        pass