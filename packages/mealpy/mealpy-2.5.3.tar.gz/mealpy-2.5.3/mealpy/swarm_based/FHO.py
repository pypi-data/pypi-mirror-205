#!/usr/bin/env python
# Created by "Thieu" at 21:16, 26/10/2022 ----------%                                                                               
#       Email: nguyenthieu2102@gmail.com            %                                                    
#       Github: https://github.com/thieu1995        %                         
# --------------------------------------------------%

import numpy as np
from mealpy.optimizer import Optimizer


class OriginalFHO(Optimizer):
    """
    The original version of: Fire Hawk Optimization (FHO)

    Links:
        1. https://link.springer.com/article/10.1007/s10462-022-10173-w
        2. https://www.mathworks.com/matlabcentral/fileexchange/114325-fire-hawk-optimizer-fho-a-novel-metaheuristic-algorithm

    Notes:
        1. Two variables that authors consider it as a constants (aa = 0.7 and zz = 0.05)
    Examples
    ~~~~~~~~
    >>> import numpy as np
    >>> from mealpy.swarm_based.FHO import OriginalFHO
    >>>
    >>> def fitness_function(solution):
    >>>     return np.sum(solution**2)
    >>>
    >>> problem_dict1 = {
    >>>     "fit_func": fitness_function,
    >>>     "lb": [-10, -15, -4, -2, -8],
    >>>     "ub": [10, 15, 12, 8, 20],
    >>>     "minmax": "min",
    >>> }
    >>>
    >>> epoch = 1000
    >>> pop_size = 50
    >>> model = OriginalFHO(epoch, pop_size)
    >>> best_position, best_fitness = model.solve(problem_dict1)
    >>> print(f"Solution: {best_position}, Fitness: {best_fitness}")

    References
    ~~~~~~~~~~
    [1] Azizi, M., Talatahari, S., & Gandomi, A. H. (2022). Fire Hawk Optimizer: a novel metaheuristic algorithm. Artificial Intelligence Review, 1-77.
    """

    def __init__(self, epoch=10000, pop_size=100, **kwargs):
        """
        Args:
            epoch (int): maximum number of iterations, default = 10000
            pop_size (int): number of population size, default = 100
        """
        super().__init__(**kwargs)
        self.epoch = self.validator.check_int("epoch", epoch, [1, 100000])
        self.pop_size = self.validator.check_int("pop_size", pop_size, [10, 10000])
        self.set_parameters(["epoch", "pop_size"])
        self.n_firehawks = np.random.choice(range(1, int(self.pop_size/5)+1))       # Maximum number of FireHawks
        self.nfe_per_epoch = self.pop_size
        self.sort_flag = True

