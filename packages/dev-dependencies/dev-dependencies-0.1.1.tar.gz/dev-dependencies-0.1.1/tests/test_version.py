import devdeps


def test_version_is_set() -> None:
    print(devdeps.VERSION)
    assert devdeps.VERSION is not None


# We can't really test the unset case since it's all global state. Once the
# module is imported, the value is set and the code won't be executed again.
