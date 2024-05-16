from typing import Optional

from contribution.domain import WriterId, Writer


class WriterMap:
    def __init__(self):
        self._writers: set[Writer] = set()

    def with_id(self, id: WriterId) -> Optional[Writer]:
        for writer in self._writers:
            if writer.id == id:
                return writer
        return None

    def save(self, writer: Writer) -> None:
        """
        Saves writer in identity map if writer doesn't
        exist, otherwise raises ValueError.
        """
        writer_from_map = self.with_id(writer.id)
        if writer_from_map:
            message = "Writer already exists in identity map"
            raise ValueError(message)
        self._writers.add(writer)

    def update(self, writer: Writer) -> None:
        """
        Updates writer in identity map if writer exists,
        otherwise raises ValueError.
        """
        writer_from_map = self.with_id(writer.id)
        if not writer_from_map:
            message = "Writer doesn't exist in identity map"
            raise ValueError(message)
        self._writers.remove(writer_from_map)
        self._writers.add(writer)
