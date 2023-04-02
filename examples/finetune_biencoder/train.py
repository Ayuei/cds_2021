# coding: utf-8

import datasets
from sentence_transformers import evaluation

from debeir.training.hparm_tuning.config import HparamConfig
from debeir.training.hparm_tuning.trainer import SentenceTransformerTrainer
from debeir.training.utils import SentDataset

TASK_NAME = "trec_contrastive_passage"
OUTPUT_DIR = f"./outputs/cross_encoder/{TASK_NAME}/"
DATA_DIR = "../data/"


def remap_label(ex):
    # Normalize 0, 1, 2 -> 0, 1
    # We treat neutral the same as a contradiction
    ex['label'] = ex['label'] // 2

    return ex


def load_dataset():
    """
    Load and preprocess the SNLI dataset

    1. Re-normalize the labels to binary
    2. Remove examples with no gold labels.
    """

    dataset = datasets.load_dataset('snli')

    # Use our sentence transformer dataset adapter pattern, allows for huggingface datasets to be used with
    # Sentence transformer API
    train = SentDataset(dataset['train'].map(remap_label).filter(lambda k: k['label'] != -1),
                        text_cols=['premise', 'hypothesis'],
                        label_col='label')

    val = SentDataset(dataset['test'].map(remap_label).filter(lambda k: k['label'] != -1),
                      text_cols=['premise', 'hypothesis'],
                      label_col='label')

    # Make sure our validation and train column name are correct for the trainer
    return {'train': train, 'val': val}


if __name__ == "__main__":
    trainer = SentenceTransformerTrainer(
        # Reuse the dataset with lazy static, so we don't have to do the preprocessing repeatedly
        dataset=load_dataset(),
        hparams_config=HparamConfig.from_json("hparam_cfg.json"),
        evaluator_fn=evaluation.BinaryClassificationEvaluator,
    )

    trainer.fit()