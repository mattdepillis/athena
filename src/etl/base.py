# etl/base.py
from db.lib import common as db


def start(job: str, user_id: str) -> int:
    return db.start_run(job, user_id)


def finish(
    run_id: int, rows: int = 0, ok: bool = True, error: str | None = None
) -> None:
    return db.finish_run(
        run_id, rows_written=rows, status=("success" if ok else "fail"), error=error
    )


def get_cursor(job: str, user_id: str) -> str | None:
    return db.get_cursor(job, user_id)


def set_cursor(job: str, user_id: str, value: str) -> None:
    return db.set_cursor(job, user_id, value)


def stage(job: str, payload_json: str) -> None:
    return db.stage_raw(job, payload_json)
