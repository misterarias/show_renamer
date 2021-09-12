import pytest

from main import (
    rename_list,
    InvalidEpisodeCountError,
    extract_season_number,
    InvalidSeasonFormatError,
    get_file_list,
    InvalidInputPathError
)


def test_get_file_list(tmpdir):
    with pytest.raises(InvalidInputPathError):
        get_file_list(None)
    with pytest.raises(InvalidInputPathError):
        get_file_list('/non/existant/path')

    assert get_file_list(tmpdir.strpath) == []

    show1 = tmpdir.mkdir('show1')
    [show1.join(f).write('') for f in [
        'first', 'second', 'third'
    ]]
    show1_files = get_file_list(show1.strpath)
    assert len(show1_files) == 3
    assert show1_files[0] == f"{show1.strpath}/first"

    show2 = tmpdir.mkdir('show2')
    [show2.join(f"show2_{i:02d}.mkv").write('') for i in range(1, 5)]
    show2_files = get_file_list(show2.strpath)
    assert len(show2_files) == 4
    assert show2_files[0] == f"{show2.strpath}/show2_01.mkv"


def test_extract_season_number():
    assert extract_season_number("S1") == 1
    assert extract_season_number("S01") == 1
    assert extract_season_number("Season 1") == 1

    with pytest.raises(InvalidSeasonFormatError):
        extract_season_number("First season")


def test_rename_list():
    assert rename_list([], None) == []
    assert rename_list(["a", "b", "c"], None) == ["a", "b", "c"]

    with pytest.raises(InvalidEpisodeCountError):
        rename_list(["a", "b"], [("S1", 3)])

    with pytest.raises(InvalidEpisodeCountError):
        rename_list(["a", "b", "c", "d"], [("S1", 1), ("S2", 3), ("S3", 1)])

    assert rename_list(["a", "b", "c"], [("S01", 3)]) == [
        "S01E01",
        "S01E02",
        "S01E03",
    ]
    assert rename_list(["a", "b", "c"], [("S1", 3)]) == [
        "S01E01",
        "S01E02",
        "S01E03",
    ]
    assert rename_list(
        [
            "Dragon_Ball_1024x768_1.mkv",
            "Dragon_Ball_1024x768_2.mkv",
            "Dragon_Ball_1024x768_3.mkv",
        ],
        [("S1", 3)],
    ) == [
        "S01E01.mkv",
        "S01E02.mkv",
        "S01E03.mkv",
    ]

    assert rename_list(
        [
            "Dragon_Ball_1024x768_1.mkv",
            "Dragon_Ball_1024x768_2.mkv",
            "Dragon_Ball_1024x768_3.mkv",
            "Dragon_Ball_1024x768_4.mkv",
            "Dragon_Ball_1024x768_5.mkv",
        ],
        [("S1", 3), ("S2", 2)],
    ) == [
        "S01E01.mkv",
        "S01E02.mkv",
        "S01E03.mkv",
        "S02E01.mkv",
        "S02E02.mkv",
    ]
