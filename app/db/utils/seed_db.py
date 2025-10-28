import datetime
from datetime import timedelta
from random import choice, randint

from clear_db import clear_database
from faker import Faker

from app.db.session import SessionLocal
from app.models.models import DailyActivity, Heartbeat, Machine, User

fake = Faker()
db = SessionLocal()


def seed_users(n=5):
    users = []
    for _ in range(n):
        user = User(
            username=fake.user_name(),
            email=fake.unique.email(),
        )
        db.add(user)
        users.append(user)
    db.commit()
    for u in users:
        db.refresh(u)
    return users


def seed_machines(users):
    machines = []
    for user in users:
        for _ in range(randint(1, 2)):
            machine = Machine(
                user_id=user.id, machine_name=f"{fake.word()}-{randint(100, 999)}"
            )
            db.add(machine)
            machines.append(machine)
    db.commit()
    for m in machines:
        db.refresh(m)
    return machines


def seed_heartbeats(users, machines, n=20):
    for _ in range(n):
        user = choice(users)
        machine = choice(machines)
        hb = Heartbeat(
            user_id=user.id,
            machine_id=machine.id,
            entity=fake.file_name(category="text"),
            type="file",
            category=choice(["coding", "debugging", "testing", "browsing"]),
            time=datetime.datetime.now(datetime.UTC)
            - timedelta(seconds=randint(0, 3600)),
            project=choice(["enigmatica", "wakatime-clone", "personal-site"]),
            branch=choice(["main", "dev", "feature-x"]),
            language=choice(["python", "javascript", "typescript"]),
            lines=randint(1, 200),
            lineno=randint(1, 100),
            cursorpos=randint(1, 500),
            is_write=choice([True, False]),
        )
        db.add(hb)
    db.commit()


def seed_daily_activity(users):
    for user in users:
        da = DailyActivity(
            user_id=user.id,
            date=datetime.datetime.now(datetime.UTC).date(),
            total_active_seconds=randint(1000, 20000),
            project_worked_on={
                "enigmatica": randint(100, 200),
                "wakatime-clone": randint(50, 100),
            },
        )
        db.add(da)
    db.commit()


if __name__ == "__main__":
    clear_database()
    print("Seeding database...")
    users = seed_users(5)
    machines = seed_machines(users)
    seed_heartbeats(users, machines, n=50)
    seed_daily_activity(users)
    db.close()
    print("[SUCCESS] Database seeded successfully.")
