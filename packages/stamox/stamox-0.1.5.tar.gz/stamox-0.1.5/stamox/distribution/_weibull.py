from typing import Optional, Union

import jax.numpy as jnp
import jax.random as jrand
from equinox import filter_grad, filter_jit
from jax import lax
from jax._src.random import KeyArray, Shape
from jaxtyping import ArrayLike, Float

from ._utils import (
    _check_clip_distribution_domain,
    _check_clip_probability,
    _post_process,
    _promote_dtype_to_floating,
    svmap_,
)


@filter_jit
def _pweibull(
    x: Union[Float, ArrayLike],
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
):
    concentration = lax.convert_element_type(concentration, x.dtype)
    scale = lax.convert_element_type(scale, x.dtype)
    scaled_x = lax.div(x, scale)
    powered = jnp.float_power(scaled_x, concentration)
    return 1 - jnp.exp(-powered)


def pweibull(
    q: Union[Float, ArrayLike],
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    lower_tail: bool = True,
    log_prob: bool = False,
    dtype=jnp.float_,
) -> ArrayLike:
    """Computes the cumulative distribution function of the Weibull distribution.

    Args:
        q (Union[Float, ArrayLike]): The value at which to evaluate the CDF.
        concentration (Union[Float, ArrayLike], optional): The concentration parameter of the Weibull distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): The scale parameter of the Weibull distribution. Defaults to 1.0.
        lower_tail (bool, optional): Whether to compute the lower tail of the CDF. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.
        dtype (jnp.dtype, optional): The dtype of the output. Defaults to jnp.float_.

    Returns:
        Array: The cumulative distribution function of the Weibull distribution evaluated at `q`.

    Example:
        >>> pweibull(1.0, concentration=1.0, scale=1.0)
    """
    q, _ = _promote_dtype_to_floating(q, dtype)
    q = _check_clip_distribution_domain(q, lower=0.0)
    p = svmap_(_pweibull, q, concentration, scale)
    p = _post_process(p, lower_tail=lower_tail, log_prob=log_prob)
    return p


_dweibull = filter_grad(filter_jit(_pweibull))


def dweibull(
    x, concentration=0.0, scale=1.0, lower_tail=True, log_prob=False, dtype=None
) -> ArrayLike:
    """Computes the probability density function of the Weibull distribution.

    Args:
        x (Union[Float, ArrayLike]): The value at which to evaluate the PDF.
        concentration (Union[Float, ArrayLike], optional): The concentration parameter of the Weibull distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): The scale parameter of the Weibull distribution. Defaults to 1.0.
        lower_tail (bool, optional): Whether to compute the lower tail of the CDF. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.
        dtype (Optional[jnp.dtype], optional): The dtype of the output. Defaults to None.


    Returns:
        Array: The probability density function of the Weibull distribution evaluated at `x`.

    Example:
        >>> dweibull(0.5, 1.0, 1.0)
    """
    x, _ = _promote_dtype_to_floating(x, dtype)
    x = _check_clip_distribution_domain(x, lower=0.0)
    grads = svmap_(_dweibull, x, concentration, scale)
    grads = _post_process(grads, lower_tail=lower_tail, log_prob=log_prob)
    return grads


@filter_jit
def _qweibull(
    q: Union[Float, ArrayLike],
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
) -> ArrayLike:
    concentration = lax.convert_element_type(concentration, q.dtype)
    scale = lax.convert_element_type(scale, q.dtype)
    one = lax.convert_element_type(1, q.dtype)
    nlog_q = -lax.log(lax.sub(one, q))
    inv_concentration = lax.div(one, concentration)
    powerd = jnp.float_power(nlog_q, inv_concentration)
    x = lax.mul(powerd, scale)
    return x


def qweibull(
    p: Union[Float, ArrayLike],
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    lower_tail: bool = True,
    log_prob: bool = False,
    dtype=jnp.float_,
) -> ArrayLike:
    """Computes the quantile function of the Weibull distribution.

    Args:
        p (Union[Float, ArrayLike]): The quantiles to compute.
        concentration (Union[Float, ArrayLike], optional): The concentration parameter of the Weibull distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): The scale parameter of the Weibull distribution. Defaults to 1.0.
        lower_tail (bool, optional): Whether to compute the lower tail of the distribution. Defaults to True.
        log_prob (bool, optional): Whether to compute the log probability of the distribution. Defaults to False.
        dtype (jnp.dtype, optional): The dtype of the output. Defaults to jnp.float_.


    Returns:
        Array: The computed quantiles.

    Example:
        >>> qweibull(0.5, 1.0, 1.0)
    """
    p, _ = _promote_dtype_to_floating(p, dtype)
    p = _check_clip_probability(p, lower_tail, log_prob)
    q = svmap_(_qweibull, p, concentration, scale)
    return q


@filter_jit
def _rweibull(
    key: KeyArray,
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    sample_shape: Optional[Shape] = None,
    dtype=jnp.float_,
):
    return jrand.weibull_min(key, scale, concentration, sample_shape, dtype=dtype)


def rweibull(
    key: KeyArray,
    sample_shape: Optional[Shape] = None,
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    lower_tail: bool = True,
    log_prob: bool = False,
    dtype=jnp.float_,
) -> ArrayLike:
    """Generates samples from the Weibull distribution.

    Args:
        key (KeyArray): Random key used for generating random numbers.
        sample_shape (Optional[Shape], optional): Shape of the output sample. Defaults to None.
        concentration (Union[Float, ArrayLike], optional): Concentration parameter of the Weibull distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): Scale parameter of the Weibull distribution. Defaults to 1.0.
        lower_tail (bool, optional): Whether to return the lower tail probability. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.
        dtype (Optional[jnp.dtype], optional): The dtype of the output. Defaults to jnp.float_.


    Returns:
        rvs (ArrayLike): Probability of the Weibull distribution.

    Example:
        >>> key = jax.random.PRNGKey(0)
        >>> rweibull(key, 1.0, 1.0)
    """
    rvs = _rweibull(key, concentration, scale, sample_shape, dtype=dtype)
    rvs = _post_process(rvs, lower_tail=lower_tail, log_prob=log_prob)
    return rvs
