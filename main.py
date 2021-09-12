class InvalidEpisodeCountError(Exception):
    pass


def main():
    pass


def rename_list(file_list: list, season_definition: dict) -> list:
    if season_definition is None:
        return file_list

    total_definitions = sum(len(episodes) for _, episodes in season_definition.items())
    total_files = len(file_list)
    if total_definitions != total_files:
        raise InvalidEpisodeCountError()


if __name__ == "__main__":
    main()
