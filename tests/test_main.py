from main import rename_list


def test_rename_list(tmpdir):
    assert rename_list([], None) == []
    assert rename_list(['a', 'b', 'c'], None) == ['a', 'b', 'c']
