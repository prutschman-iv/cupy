import os


from cupy.testing._pytest_impl import is_available, check_available


if is_available():
    import pytest

    _gpu_limit = int(os.getenv('CUPY_TEST_GPU_LIMIT', '-1'))

    def cudnn(*args, **kwargs):
        return pytest.mark.cudnn(*args, **kwargs)

    def slow(*args, **kwargs):
        return pytest.mark.slow(*args, **kwargs)

else:
    def _dummy_callable(*args, **kwargs):
        check_available('pytest attributes')
        assert False  # Not reachable

    cudnn = _dummy_callable
    slow = _dummy_callable


def multi_gpu(gpu_num):
    """Decorator to indicate number of GPUs required to run the test.

    Tests can be annotated with this decorator (e.g., ``@multi_gpu(2)``) to
    declare number of GPUs required to run. When running tests, if
    ``CUPY_TEST_GPU_LIMIT`` environment variable is set to value greater
    than or equals to 0, test cases that require GPUs more than the limit will
    be skipped.
    """

    check_available('multi_gpu attribute')
    # at this point we know pytest is available for sure
    return pytest.mark.skipif(
        0 <= _gpu_limit < gpu_num,
        reason='{} GPUs required'.format(gpu_num))


def gpu(f):
    """Decorator to indicate that GPU is required to run the test.

    Tests can be annotated with this decorator (e.g., ``@gpu``) to
    declare that one GPU is required to run.
    """

    check_available('gpu attribute')
    return multi_gpu(1)(pytest.mark.gpu(f))
