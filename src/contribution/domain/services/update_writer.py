from contribution.domain.constants import Writing
from contribution.domain.models import Writer
from contribution.domain.maybe import Maybe


class UpdateWriter:
    def __call__(
        self,
        writer: Writer,
        *,
        writing: Maybe[Writing],
    ) -> None:
        if writing.is_set:
            writer.writing = writing.value
