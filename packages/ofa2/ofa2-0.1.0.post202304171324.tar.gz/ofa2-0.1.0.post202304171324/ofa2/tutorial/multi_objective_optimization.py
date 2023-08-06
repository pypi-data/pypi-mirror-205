import pymoo
import numpy as np
from pymoo.core.individual import Individual
from pymoo.core.problem import Problem
from pymoo.core.sampling import Sampling


class OfaIndividual(Individual):
    def __init__(self, individual, accuracy_predictor, config=None, **kwargs):
        super().__init__(config=None, **kwargs)
        self.X = np.concatenate(
            (
                individual[0]["ks"],
                individual[0]["e"],
                individual[0]["d"],
                individual[0]["r"],
            )
        )
        self.latency = individual[1]
        self.accuracy = 100 - accuracy_predictor.predict_accuracy([individual[0]])
        self.F = np.concatenate((self.latency, [self.accuracy.squeeze().numpy()]))


def individual_to_arch(population, n_blocks):
    archs = []
    for individual in population:
        archs.append(
            {
                "ks": individual[0:n_blocks],
                "e": individual[n_blocks : 2 * n_blocks],
                "d": individual[2 * n_blocks : -1],
                "r": individual[-1:],
            }
        )
    return archs


class OfaProblem(Problem):
    def __init__(self, finder, num_blocks, num_stages):
        super().__init__(
            # n_var = 100,
            vars=num_blocks * [ks] + num_blocks * [e] + num_stages * [d] + [r],
            n_obj=2,
            n_constr=0,
            # xl = -2.0,
            # xu = 2.0
        )
        self.finder = finder
        self.blocks = num_blocks
        self.stages = num_stages

    def _evaluate(self, x, out, *args, **kwargs):
        # x.shape = (population_size, n_var) = (100, 4)
        arch = individual_to_arch(x, self.blocks)
        f1 = self.finder.efficiency_predictor.predict_efficiency(arch)
        f2 = 100 - self.finder.accuracy_predictor.predict_accuracy(arch)
        # f1 = 100 * (x[:, 0]**2 + x[:, 1]**2)
        # f2 = (x[:, 0]-1)**2 + x[:, 1]**2
        out["F"] = np.column_stack([f1, f2])


class OfaSampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        return [
            [np.random.choice(var.options) for var in problem.vars]
            for _ in range(n_samples)
        ]
