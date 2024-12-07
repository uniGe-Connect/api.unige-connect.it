import uuid
import random

from faker import Faker
from sqlmodel import Session
from app.core.db import (engine)
from app.models.group_model import GroupModel, GroupTypes
from app.models.user_model import UserModel
from app.models.member_model import MemberModel, MemberTypes

def default_seeder():
    fake = Faker()

    print("Starting seeding the database ....")

    with Session(engine) as session:
        first_user = UserModel(
            id=fake.uuid4(),
            name=fake.name(),
            last_name=fake.last_name(),
            email=fake.email(),
            serial_number='s123456'
        )

        second_user = UserModel(
            id=uuid.uuid4(),
            name=fake.name(),
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

        session.add_all([first_user, second_user,test_user])
        session.commit()

        for i in range(10):
            group = GroupModel(
                id=uuid.uuid4(),
                name=fake.name(),
                topic=fake.word(),
                description=fake.sentence(50),
                type=GroupTypes.public_open,
                owner_id=first_user.id,
            )

            session.add(group)
            session.commit()

            for j in range(10):
                role = MemberTypes.owner if i == 0 else MemberTypes.member
                user = UserModel(
                    id=fake.uuid4(),
                    name=fake.name(),
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
                group.member_count = i + 1
                session.commit

                        
    print('Database seeding completed')


if __name__ == "__main__":
    default_seeder()
