from functools import partial
from typing import Sequence

import jax.numpy as jnp
from equinox import filter_jit
from jax import vmap
from jaxtyping import ArrayLike

from ..distribution import pchisq
from ._base import HypoTest


class BartlettTest(HypoTest):
    """Class for performing a Bartlett's test.

    This class is used to perform a Bartlett's test, which tests the null hypothesis that all input samples are from populations with equal variances.

    Attributes:
        statistic (float): The test statistic.
        parameters (int): The degrees of freedom.
        p_value (float): The p-value of the test.
    """

    def __init__(
        self,
        statistic=None,
        parameters=None,
        p_value=None,
        estimate=None,
        null_value=None,
        alternative=None,
    ):
        super().__init__(
            statistic,
            parameters,
            p_value,
            estimate,
            null_value,
            alternative,
            name="BartlettTest",
        )

    def __repr__(self):
        return f"{self.name}(statistic={self.statistic}, parameters={self.parameters}, p_value={self.p_value})"

    @property
    def df(self):
        return self.parameters


def bartlett_test(*samples: Sequence[ArrayLike], axis=0) -> BartlettTest:
    """Calculates the Bartlett test statistic for multiple samples.

    Args:
        *samples Sequence[ArrayLike]): A sequence of 1-D arrays, each containing
            a sample of scores. All samples must have the same length.

    Returns:
        BartlettTest: The Bartlett Test object.

    Example:
        >>> from stamox.functions import bartlett_test
        >>> bartlett_test([1, 2, 3], [1, 2, 3])
        BartlettTest(statistic=0.0, parameters=1, p_value=1.0)
    """
    samples = jnp.vstack(samples)
    return _bartlett(samples, axis)


@filter_jit
def _bartlett(samples, axis):
    k = samples.shape[0]
    Ni = jnp.asarray(vmap(jnp.size, in_axes=(axis,))(samples), dtype=samples.dtype)
    ssq = vmap(partial(jnp.var, ddof=1), in_axes=(axis,))(samples)
    Ntot = jnp.sum(Ni, axis=axis)
    spsq = jnp.sum((Ni - 1) * ssq, axis=axis) / (1.0 * (Ntot - k))
    numer = (Ntot * 1.0 - k) * jnp.log(spsq) - jnp.sum(
        (Ni - 1.0) * jnp.log(ssq), axis=axis
    )
    denom = 1.0 + 1.0 / (3 * (k - 1)) * (
        (jnp.sum(1.0 / (Ni - 1.0), axis=axis)) - 1.0 / (Ntot - k)
    )
    stats = numer / denom
    param = k - 1
    stats = stats.squeeze()
    pval = pchisq(stats, param, lower_tail=False)
    return BartlettTest(statistic=stats, parameters=param, p_value=pval)
