import pytest

from main import rename_list, InvalidEpisodeCountError


def test_rename_list(tmpdir):
    assert rename_list([], None) == []
    assert rename_list(["a", "b", "c"], None) == ["a", "b", "c"]

    with pytest.raises(InvalidEpisodeCountError):
        rename_list(["a", "b"], {"S01": ["1", "2", "3"]})

