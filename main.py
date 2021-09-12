from typing import List, Tuple


class InvalidEpisodeCountError(Exception):
    pass


def main():
    pass


def rename_list(file_list: list, season_definition: List[Tuple[str, int]]) -> list:
    if season_definition is None:
        return file_list

    total_definitions = sum(episode_count for (_, episode_count) in season_definition)
    total_files = len(file_list)
    if total_definitions != total_files:
        raise InvalidEpisodeCountError()

    sequential_definitions = []
    for (season, episode_count) in season_definition:
        sequential_definitions.extend([f"{season}E{i:02}" for i in range(1, episode_count + 1)])

    return sequential_definitions


if __name__ == "__main__":
    main()
