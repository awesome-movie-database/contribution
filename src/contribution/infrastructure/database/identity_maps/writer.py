from typing import Optional

from contribution.domain import WriterId, Writer


class WriterMap:
    def __init__(self):
        self._writers: list[Writer] = list()

    def by_id(self, id: WriterId) -> Optional[Writer]:
        for writer in self._writers:
            if writer.id == id:
                return writer
        return None

    def save(self, writer: Writer) -> None:
        """
        Saves writer in identity map if writer doesn't
        exist, otherwise raises Exception.
        """
        writer_from_map = self.by_id(writer.id)
        if writer_from_map:
            message = "Writer already exists in identity map"
            raise Exception(message)
        self._writers.append(writer)
