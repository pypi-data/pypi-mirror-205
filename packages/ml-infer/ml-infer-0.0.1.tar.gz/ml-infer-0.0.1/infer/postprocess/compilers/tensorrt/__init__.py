try:
    import tensorrt  # noqa, pylint: disable=import-error
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "The TensorRT backend is not supported because TensorRT is not installed; TensorRT can be installed using "
        "`pip install --extra-index-url https://pypi.ngc.nvidia.com nvidia-tensorrt`"
    ) from e
