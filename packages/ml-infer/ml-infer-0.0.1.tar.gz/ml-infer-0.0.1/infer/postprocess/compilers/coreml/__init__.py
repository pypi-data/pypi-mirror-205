try:
    import coremltools  # noqa, pylint: disable=import-error
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "The CoreML backend is not supported because CoreML is not installed; CoreML can be installed using "
        "`pip install coremltools`"
    ) from e
