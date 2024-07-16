import json
import types
import logging
import traceback
import dataclasses
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any, Optional, Type, override
from uuid import UUID

from contribution.domain import Maybe


ExcInfo = tuple[Type[BaseException], BaseException, types.TracebackType]


class JsonFormatter(logging.Formatter):
    @override
    def format(self, record: logging.LogRecord) -> str:
        record_as_dict = record.__dict__

        self._remove_useless_fields_from_record_as_dict(record_as_dict)
        self._replace_record_as_dict_exc_info_with_traceback(record_as_dict)
        self._add_usefull_fields_to_record_as_dict(record_as_dict)

        self._make_dict_serializable(record_as_dict)
        record_as_json = json.dumps(record_as_dict)

        return record_as_json

    def _remove_useless_fields_from_record_as_dict(
        self,
        record_as_dict: dict,
    ) -> None:
        record_as_dict.pop("args", None)
        record_as_dict.pop("levelno", None)
        record_as_dict.pop("module", None)
        record_as_dict.pop("pathname", None)
        record_as_dict.pop("funcName", None)
        record_as_dict.pop("exc_text", None)
        record_as_dict.pop("stack_info", None)
        record_as_dict.pop("lineno", None)
        record_as_dict.pop("created", None)
        record_as_dict.pop("msecs", None)
        record_as_dict.pop("relativeCreated", None)
        record_as_dict.pop("thread", None)
        record_as_dict.pop("threadName", None)
        record_as_dict.pop("processName", None)
        record_as_dict.pop("process", None)
        record_as_dict.pop("taskName", None)

    def _replace_record_as_dict_exc_info_with_traceback(
        self,
        record_as_dict: dict,
    ) -> None:
        exc_info: Optional[ExcInfo] = record_as_dict.pop("exc_info", None)
        if not exc_info:
            return

        exception = exc_info[1]
        exception_traceback_as_str = traceback.format_exception(
            exception,
        )

        record_as_dict["traceback"] = exception_traceback_as_str

    def _add_usefull_fields_to_record_as_dict(
        self,
        record_as_dict: dict,
    ) -> None:
        current_timestamp = datetime.now(timezone.utc).isoformat()
        record_as_dict.update(timestamp=current_timestamp)

    def _make_dict_serializable(self, dict_: dict) -> None:
        for key, value in dict_.items():
            dict_[key] = self._make_value_serializable(value)

    def _make_value_serializable(self, value: Any) -> Any:
        if isinstance(value, dict):
            return self._make_dict_serializable(value)
        elif isinstance(value, (date, datetime)):
            return value.isoformat()
        elif isinstance(value, UUID):
            return value.hex
        elif isinstance(value, Decimal):
            return str(value)
        elif isinstance(value, Maybe):
            return self._make_value_serializable(value.value)
        elif dataclasses.is_dataclass(value):
            dataclass_as_dict = dataclasses.asdict(value)
            self._make_dict_serializable(dataclass_as_dict)
            return dataclass_as_dict

        return value
