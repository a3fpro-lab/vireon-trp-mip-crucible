import numpy as np

def softmax_from_scores(scores, beta: float = 1.0) -> np.ndarray:
    scores = np.asarray(scores, dtype=float)
    if scores.size == 0:
        raise ValueError("Empty scores array.")
    shifted = scores - scores.max()
    z = np.exp(beta * shifted)
    q = z / z.sum()
    return q
