from dishka import Provider, Scope

from contribution.application import (
    OnEventOccurred,
    MovieAddedEvent,
    MovieEditedEvent,
    PersonAddedEvent,
    PersonEditedEvent,
    AchievementEarnedEvent,
)
from contribution.infrastructure.message_broker import (
    publish_movie_added_event_factory,
    publish_movie_edited_event_factory,
    publish_person_added_event_factory,
    publish_person_edited_event_factory,
    publish_achievement_earned_event_factory,
)


def event_publishers_provider_factory() -> Provider:
    provider = Provider(Scope.REQUEST)

    provider.provide(
        publish_movie_added_event_factory,
        provides=OnEventOccurred[MovieAddedEvent],
    )
    provider.provide(
        publish_movie_edited_event_factory,
        provides=OnEventOccurred[MovieEditedEvent],
    )
    provider.provide(
        publish_person_added_event_factory,
        provides=OnEventOccurred[PersonAddedEvent],
    )
    provider.provide(
        publish_person_edited_event_factory,
        provides=OnEventOccurred[PersonEditedEvent,],
    )
    provider.provide(
        publish_achievement_earned_event_factory,
        provides=OnEventOccurred[AchievementEarnedEvent],
    )

    return provider
