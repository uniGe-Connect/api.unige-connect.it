import uuid

from faker import Faker
from sqlmodel import Session
from app.core.db import (engine)
from app.models.group_model import GroupModel, GroupTypes
from app.models.user_model import UserModel


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

        session.add_all([first_user, second_user])
        session.commit()

        for _ in range(10):
            group = GroupModel(
                id=uuid.uuid4(),
                name=fake.name(),
                topic=fake.word(),
                description=fake.sentence(50),
                type=GroupTypes.public_open,
                owner_id=first_user.id
            )

            session.add(group)
            session.commit()

    print('Database seeding completed')


if __name__ == "__main__":
    default_seeder()
