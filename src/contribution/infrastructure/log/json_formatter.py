import json
import logging
import dataclasses
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any
from uuid import UUID

from typing_extensions import override

from contribution.domain import Maybe


class JsonFormatter(logging.Formatter):
    @override
    def format(self, record: logging.LogRecord) -> str:
        record_as_dict = record.__dict__

        self._remove_useless_fileds_from_record_as_dict(record_as_dict)
        self._add_usefull_fields_to_record_as_dict(record_as_dict)

        self._make_dict_serializable(record_as_dict)
        record_as_json = json.dumps(record_as_dict)

        return record_as_json

    def _remove_useless_fileds_from_record_as_dict(
        self,
        record_as_dict: dict,
    ) -> None:
        record_as_dict.pop("args")
        record_as_dict.pop("levelname")
        record_as_dict.pop("pathname")
        record_as_dict.pop("funcName")
        record_as_dict.pop("created")
        record_as_dict.pop("msecs")
        record_as_dict.pop("relativeCreated")
        record_as_dict.pop("thread")
        record_as_dict.pop("threadName")
        record_as_dict.pop("processName")
        record_as_dict.pop("process")
        record_as_dict.pop("taskName")

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
        if isinstance(value, (date, datetime)):
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
