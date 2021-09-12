from main import rename_list


def test_rename_list(tmpdir):
    assert rename_list([], None) is None
