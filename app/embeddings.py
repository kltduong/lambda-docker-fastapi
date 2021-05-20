import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text  # This is always need for loading model

from typing import List


model = hub.load("./app/model/")
print("Loaded model successfully from local")


def get_embeddings(inputs: List[str]):
    batch = 1000
    res = np.concatenate(
        [model(inputs[i : i + batch]).numpy() for i in range(0, len(inputs), batch)]
    )
    return res
