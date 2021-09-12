import os
import glob
import re
from typing import List, Tuple


class InvalidEpisodeCountError(Exception):
    pass


class InvalidSeasonFormatError(Exception):
    pass


class InvalidInputPathError(Exception):
    pass


def main():
    pass


def get_file_list(input_path):
    if not input_path or not os.path.isdir(input_path):
        raise InvalidInputPathError(input_path)

    return sorted([f for f in glob.glob(f"{input_path}/*") if os.path.isfile(f)])


def extract_season_number(season: str) -> int:
    number = re.search(r".*(\d+).*", season)
    print(number)
    if not number:
        raise InvalidSeasonFormatError()

    return int(number.group(1))


def rename_list(file_list: list, season_definition: List[Tuple[str, int]]) -> list:
    if season_definition is None:
        return file_list

    total_definitions = sum(episode_count for (_, episode_count) in season_definition)
    total_files = len(file_list)
    if total_definitions != total_files:
        raise InvalidEpisodeCountError()

    sequential_definitions = []
    for (season, episode_count) in season_definition:
        season_number = extract_season_number(season)
        sequential_definitions.extend(
            [f"S{season_number:02}E{i:02}" for i in range(1, episode_count + 1)]
        )

    final_names = []
    for index, name in enumerate(file_list):
        name, *rest = name.split(".")
        final_name = sequential_definitions[index]
        if rest:
            final_name = f"{final_name}.{rest[-1]}"
        final_names.append(final_name)

    return final_names


if __name__ == "__main__":
    main()
