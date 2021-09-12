import pytest

from main import rename_list, InvalidEpisodeCountError, extract_season_number, InvalidSeasonFormatError


def test_extract_season_number():
    assert extract_season_number("S1") == 1
    assert extract_season_number("S01") == 1
    assert extract_season_number("Season 1") == 1

    with pytest.raises(InvalidSeasonFormatError):
        extract_season_number("First season")


def test_rename_list(tmpdir):
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
    assert rename_list([
        "Dragon_Ball_1024x768_1.mkv",
        "Dragon_Ball_1024x768_2.mkv",
        "Dragon_Ball_1024x768_3.mkv",
    ], [("S1", 3)]) == [
        "S01E01.mkv",
        "S01E02.mkv",
        "S01E03.mkv",
    ]

    assert rename_list([
        "Dragon_Ball_1024x768_1.mkv",
        "Dragon_Ball_1024x768_2.mkv",
        "Dragon_Ball_1024x768_3.mkv",
        "Dragon_Ball_1024x768_4.mkv",
        "Dragon_Ball_1024x768_5.mkv",
    ], [("S1", 3), ("S2", 2)]) == [
        "S01E01.mkv",
        "S01E02.mkv",
        "S01E03.mkv",
        "S02E01.mkv",
        "S02E02.mkv",
    ]
