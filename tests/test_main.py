import json
import glob
import pytest

from main import (
    rename_list,
    InvalidEpisodeCountError,
    extract_season_number,
    InvalidSeasonFormatError,
    get_file_list,
    InvalidInputPathError,
    main,
    get_description_from_file,
    InvalidDescriptionFormat,
)


@pytest.fixture
def show1_descriptor() -> str:
    return json.dumps(
        {
            "name": "Show 1",
            "seasons": [
                {"name": "S1", "episodes": ["1", "2"], "episode_count": 2},
                {"name": "S2", "episodes": ["1", "2"], "episode_count": 2},
            ],
        }
    )


def test_get_description_from_file(tmpdir, show1_descriptor):
    with pytest.raises(InvalidInputPathError):
        get_description_from_file(tmpdir.strpath)

    description_file = tmpdir.mkdir("desc").join("description.json")
    description_file.write("")

    with pytest.raises(InvalidDescriptionFormat):
        get_description_from_file(description_file.strpath)

    description_file.write(show1_descriptor)
    assert get_description_from_file(description_file.strpath) == [("S1", 2), ("S2", 2)]


def test_main(tmpdir, show1_descriptor):
    show1 = tmpdir.mkdir("show1")
    [show1.join(f"show1_{i:02d}.mkv").write("") for i in [2, 4, 3, 1]]

    description_file = tmpdir.mkdir("desc").join("description.json")
    description_file.write(show1_descriptor)

    assert (
        main(f"-f {show1.strpath} -d {description_file.strpath} --dry-run".split()) == 0
    )
    assert sorted(list(glob.glob(f"{show1.strpath}/*.mkv"))) == [
        f"{show1.strpath}/show1_01.mkv",
        f"{show1.strpath}/show1_02.mkv",
        f"{show1.strpath}/show1_03.mkv",
        f"{show1.strpath}/show1_04.mkv",
    ]

    assert main(f"-f {show1.strpath} -d {description_file.strpath}".split()) == 0
    assert sorted(list(glob.glob(f"{show1.strpath}/*.mkv"))) == [
        f"{show1.strpath}/S01E01.mkv",
        f"{show1.strpath}/S01E02.mkv",
        f"{show1.strpath}/S02E01.mkv",
        f"{show1.strpath}/S02E02.mkv",
    ]


def test_get_file_list(tmpdir):
    with pytest.raises(InvalidInputPathError):
        get_file_list(None)
    with pytest.raises(InvalidInputPathError):
        get_file_list("/non/existant/path")

    assert get_file_list(tmpdir.strpath) == []

    show1 = tmpdir.mkdir("show1")
    [show1.join(f).write("") for f in ["first", "second", "third"]]
    show1_files = get_file_list(show1.strpath)
    assert len(show1_files) == 3
    assert show1_files[0] == f"{show1.strpath}/first"

    show2 = tmpdir.mkdir("show2")
    [show2.join(f"show2_{i:02d}.mkv").write("") for i in range(1, 5)]
    show2_files = get_file_list(show2.strpath)
    assert len(show2_files) == 4
    assert show2_files[0] == f"{show2.strpath}/show2_01.mkv"

    # Add some tainted files
    [show2.join(f"show2_{i:02d}.jpg").write("") for i in range(1, 5)]
    show2_files = get_file_list(show2.strpath, "mkv")
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
            "/path/to/Dragon_Ball_1024x768_1.mkv",
            "/path/to/Dragon_Ball_1024x768_2.mkv",
            "/path/to/Dragon_Ball_1024x768_3.mkv",
            "/path/to/Dragon_Ball_1024x768_4.mkv",
            "/path/to/Dragon_Ball_1024x768_5.mkv",
        ],
        [("S1", 3), ("S2", 2)],
    ) == [
        "/path/to/S01E01.mkv",
        "/path/to/S01E02.mkv",
        "/path/to/S01E03.mkv",
        "/path/to/S02E01.mkv",
        "/path/to/S02E02.mkv",
    ]
