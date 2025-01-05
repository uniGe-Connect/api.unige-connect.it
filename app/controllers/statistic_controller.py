import uuid
from app.api.deps import SessionDep, CurrentUser
from typing import Any

class StatisticController():
      
    def get_statistics(self, prof: CurrentUser, session: SessionDep) -> Any:

        statistics = [
        {
            "course_id": course.id,
            "course_name": course.name,
            "total_groups": len(course.groups),
            "total_members": sum(len(group.users) for group in course.groups),
            "avg_members": round(sum(len(group.users) for group in course.groups) / len(course.groups), 2) if course.groups else 0.0,
            "min_members": min(len(group.users) for group in course.groups) if course.groups else 0,
            "max_members": max(len(group.users) for group in course.groups) if course.groups else 0,
        }
        for course in prof.courses
        ]

        return statistics


statistic_controller = StatisticController()
