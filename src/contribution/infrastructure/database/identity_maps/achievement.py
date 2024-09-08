from typing import Optional

from contribution.domain import AchievementId, Achievement


class AchievementMap:
    def __init__(self):
        self._achievements: list[Achievement] = list()

    def by_id(self, id: AchievementId) -> Optional[Achievement]:
        for achievement in self._achievements:
            if achievement.id == id:
                return achievement
        return None

    def save(self, achievement: Achievement) -> None:
        """
        Saves achievement in identity map if achievement doesn't
        exist, otherwise raises Exception.
        """
        achievement_from_map = self.by_id(achievement.id)
        if achievement_from_map:
            message = "Achievement already exists in identity map"
            raise Exception(message)
        self._achievements.append(achievement)
