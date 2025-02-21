import uuid
import random

from faker import Faker
from app.alembic.seeders.faker_group_provider import group_name_provider
from app.alembic.seeders.faker_course_provider import course_name_provider, courses
from sqlmodel import Session

from app.controllers.course_controller import course_controller
from app.core.db import (engine)
from app.models.group_model import GroupModel, GroupTypes
from app.models.user_model import UserModel
from app.models.member_model import MemberModel, MemberTypes
from app.models.course_model import CourseModel
from app.models.course_teacher_model import CourseTeacherModel

def default_seeder():
    fake = Faker()
    fake.add_provider(group_name_provider)
    fake.add_provider(course_name_provider)

    print("Starting seeding the database ....")

    with Session(engine) as session:
        first_user = UserModel(
            id=fake.uuid4(),
            name=fake.first_name(),
            last_name=fake.last_name(),
            email='student@unige.it',
            serial_number='s123456'
        )

        second_user = UserModel(
            id=uuid.uuid4(),
            name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            serial_number='s123457'
        )

        test_user = UserModel(
            id=uuid.UUID("123e4567-e89b-12d3-a456-426614174000"),
            name = "TEST_USER",
            last_name="TU",
            email=fake.email(),
            serial_number='s000000'
        )

        professor = UserModel(
            id=uuid.UUID("875d44c6-8a42-4292-b9f3-c0362ec4bd43"),
            name = "Professor",
            last_name = "at uniGe",
            email= "professor@unige.it",
            serial_number='101010',
            type = 'professor')        

        session.add_all([first_user, second_user,test_user, professor])
        session.commit()

        for i in range (10):
            course = CourseModel(
                id=uuid.uuid4(),
                name=fake.course_name(),
            )
            session.add(course)
            session.commit()

        all_courses = course_controller.get_all(session=session)

        for i in range(3):
            course_teacher = CourseTeacherModel(
                course_id = all_courses[i].id,
                user_id = professor.id)            
            session.add(course_teacher)
            session.commit()

        for i in range(10):
            course = random.choice(all_courses)
            group = GroupModel(
                id=uuid.uuid4(),
                name=fake.group_name(),
                course_id=course.id,
                description=fake.sentence(50),
                type=GroupTypes.public_open,
                owner_id=first_user.id,
                created_at=fake.date_time_this_year(),
            )

            session.add(group)
            session.commit()

            for j in range(10):
                role = MemberTypes.owner if j == 0 else MemberTypes.member
                user = UserModel(
                    id=fake.uuid4(),
                    name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    serial_number=f"s12345{i}{j}"
                )

                session.add(user)
                session.commit()

                member = MemberModel(
                    id=fake.uuid4(),
                    user_id=user.id,
                    group_id=group.id,
                    role=role
                )

                session.add(member)
                group.member_count = j + 1
                session.commit()

                        
    print('Database seeding completed')


if __name__ == "__main__":
    default_seeder()
