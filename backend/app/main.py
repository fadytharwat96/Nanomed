from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.models import NurseStatusModel, User
from app.routers import auth, health, nurse_requests, nurses, profiles, requests

app = FastAPI(title="Nanomed MVP API", version="0.4.0")


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        existing_nurse = db.scalar(select(NurseStatusModel.nurse_id).limit(1))
        if not existing_nurse:
            db.add_all(
                [
                    NurseStatusModel(
                        nurse_id="nurse_1",
                        full_name="Nurse Aya",
                        lat=30.0444,
                        lng=31.2357,
                        online=True,
                        skills="iv_cannula,iv_fluids,blood_draw",
                    ),
                    NurseStatusModel(
                        nurse_id="nurse_2",
                        full_name="Nurse Mariam",
                        lat=30.0333,
                        lng=31.2333,
                        online=True,
                        skills="blood_draw,home_visit",
                    ),
                ]
            )

        users = [
            ("admin-seed-1", "0000000000", "System Admin", "admin"),
            ("nurse_1", "01111111111", "Nurse Aya", "nurse"),
            ("nurse_2", "02222222222", "Nurse Mariam", "nurse"),
        ]
        for user_id, phone, name, role in users:
            existing_user = db.get(User, user_id)
            if not existing_user:
                db.add(User(id=user_id, phone=phone, full_name=name, role=role))

        db.commit()


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(profiles.router)
app.include_router(nurses.router)
app.include_router(requests.router)
app.include_router(nurse_requests.router)
