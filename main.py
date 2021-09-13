#!/usr/bin/env python
import os
import json
import glob
import re
import sys
import argparse

from json.decoder import JSONDecodeError
from typing import List, Tuple


class InvalidDescriptionFormat(Exception):
    pass


class InvalidEpisodeCountError(Exception):
    pass


class InvalidSeasonFormatError(Exception):
    pass


class InvalidInputPathError(Exception):
    pass


def get_description_from_file(input_path: str) -> List[Tuple[str, int]]:
    if not input_path or not os.path.isfile(input_path):
        raise InvalidInputPathError(input_path)

    try:
        with open(input_path) as fd:
            description_data = json.load(fd)
            return [
                (season["name"], int(season["episode_count"]))
                for season in description_data["seasons"]
            ]
    except (AttributeError, JSONDecodeError, TypeError, KeyError) as error:
        raise InvalidDescriptionFormat(error)


def get_file_list(input_path):
    if not input_path or not os.path.isdir(input_path):
        raise InvalidInputPathError(input_path)

    return sorted([f for f in glob.glob(f"{input_path}/*") if os.path.isfile(f)])


def extract_season_number(season: str) -> int:
    number = re.search(r".*(\d+).*", season)
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
    for index, file_path in enumerate(file_list):
        path = os.path.dirname(file_path)
        name, *rest = os.path.basename(file_path).split(".")
        final_name = os.path.join(path, sequential_definitions[index])
        if rest:
            final_name = f"{final_name}.{rest[-1]}"
        final_names.append(final_name)

    return final_names


def parse_args(args: list) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="renamer",
        description="""
Renames a list of files according to a season-to-episode descriptor file.
""",
    )
    parser.add_argument(
        "-f", "--files_location", required=True, help="Path to input files to rename."
    )
    parser.add_argument(
        "-d",
        "--descriptor_location",
        required=True,
        help="Location of season description file.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Do not rename, just verbosely inform od results",
    )
    parser.add_argument("-v", "--verbose", action="count", default=0)

    return parser.parse_args(args)


def main(args: list):
    parsed_args = parse_args(args)
    file_list = get_file_list(parsed_args.files_location)
    description_data = get_description_from_file(parsed_args.descriptor_location)
    new_list = rename_list(file_list, description_data)

    for index in range(0, len(file_list)):
        old_file = file_list[index]
        new_file = new_list[index]
        if parsed_args.dry_run:
            print(f"{old_file} --> {new_file}")
        else:
            os.renames(old_file, new_file)

    return 0


if __name__ == "__main__":  # pragma no cover
    sys.exit(main(sys.argv[1:]))
