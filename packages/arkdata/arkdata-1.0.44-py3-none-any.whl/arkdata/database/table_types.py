from __future__ import annotations
from typing_extensions import TypedDict


class BulkInsert(TypedDict, total=True):
    inserted: list
    inserted_count: int
    failed: list
    failed_count: int


class BulkUpdate(TypedDict, total=True):
    updated: list
    updated_count: int
    failed: list
    failed_count: int


class BulkDelete(TypedDict, total=True):
    deleted: list
    deleted_count: int
    failed: list
    failed_count: int
