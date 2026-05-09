from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def project_path(*parts: str) -> Path:
    return PROJECT_ROOT.joinpath(*parts)


def ensure_directories() -> None:
    for path in [
        project_path("data", "raw"),
        project_path("data", "processed"),
        project_path("data", "warehouse"),
        project_path("logs"),
    ]:
        path.mkdir(parents=True, exist_ok=True)


def require_columns(frame, required_columns: list[str], dataset_name: str) -> None:
    missing = sorted(set(required_columns) - set(frame.columns))
    if missing:
        raise ValueError(f"{dataset_name} is missing required columns: {missing}")
