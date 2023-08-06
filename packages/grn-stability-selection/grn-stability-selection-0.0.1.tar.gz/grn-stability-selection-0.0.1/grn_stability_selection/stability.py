import numpy as np
import random
from typing import Callable

class StabilitySelection:
    def __init__(
            self,
            estimator:Callable,
            lambdas = None,
            K = None,
            v = None,
            B = 100
    ) -> None:
        self._estimator = estimator
        self._lambdas = lambdas
        self._K = K
        self._v = v
        self._B = B
        if self._lambdas is None:
            raise ValueError(
                "Please provide a list of regularization parameters!"
            )

    def bootstrap(self, expression):
        n = expression.shape[1]
        index = [i for i in range(n)]
        idx = [random.choice(index) for _ in range(n // 2)]
        return expression[:, idx]


    def __call__(self, **kwargs):
        try:
            expression = kwargs['expression']
        except:
            raise ValueError("Please provide an expression parameter!")

        output_shape = self._estimator(**kwargs).shape
        max_scores = np.zeros(output_shape)
        for _lambda in self._lambdas:
            counts = np.zeros(output_shape)
            for i in range(self._B):
                expr_i = self.bootstrap(expression)
                kwargs['expression'] = expr_i
                kwargs['regularization'] = _lambda
                G = self._estimator(**kwargs)
                G = np.where(G > np.sort(G.flatten())[::-1][self._K], 1, 0)
                counts += G
            counts /= self._B
            max_scores = np.maximum(max_scores, counts)
        return max_scores >= min(.5 + self._K ** 2 / (2 * self._v * output_shape[0] * output_shape[1]), 1)
