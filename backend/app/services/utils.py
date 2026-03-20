def split_csv(value: str) -> list[str]:
    return [item for item in value.split(",") if item]


def join_csv(value: list[str]) -> str:
    return ",".join(value)
