from packaging.version import Version, parse

import malariagen


def test_version():
    assert hasattr(malariagen, "__version__")
    assert isinstance(malariagen.__version__, str)
    version = parse(malariagen.__version__)
    assert isinstance(version, Version)