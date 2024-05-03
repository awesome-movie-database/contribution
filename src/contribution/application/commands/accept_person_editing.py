from dataclasses import dataclass

from contribution.domain.value_objects import EditPersonContributionId


@dataclass(frozen=True, slots=True)
class AcceptPersonEditingCommand:
    contribution_id: EditPersonContributionId
