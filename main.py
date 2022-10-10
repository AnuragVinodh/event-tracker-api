from asyncio import events
from fastapi import FastAPI
from datetime import datetime

from DataModels.EventModel import EventModel
from DataModels.UserModel import UserModel
from sqlmodel import Session, SQLModel, create_engine, select

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app = FastAPI()

GlobalUser = []
GlobalEvents = []


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# User Routes


@app.post("/users")
async def root(user: UserModel):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@app.get("/users/")
async def root():
    with Session(engine) as session:
        users = session.exec(select(UserModel)).all()
        return users


# Event Routes


@app.post("/events/")
async def root(event: EventModel):
    with Session(engine) as session:
        session.add(event)
        session.commit()
        session.refresh(event)
        return event


@app.get("/events/")
async def root():
    with Session(engine) as session:
        events = session.exec(select(EventModel)).all()
        return events


# Event Given User Routes


@app.get("/{uid}/events")
async def root(uid: int):

    with Session(engine) as session:
        statement = select(EventModel).filter(EventModel.uid == uid)
        print(statement)
        results = session.exec(statement)
        # for events in results:
        #     print("events : ", events)
        return results.all()


@app.delete("/{eid}/events")
async def root(eid: int):
    with Session(engine) as session:
        event = session.get(EventModel, eid)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        session.delete(event)
        session.commit()
        return {"ok": True}


@app.delete("/{uid}/events")
async def root(uid: int):
    with Session(engine) as session:
        statement = select(EventModel).filter(EventModel.uid == uid)
        events = session.get(statement)
        if not events:
            raise HTTPException(status_code=404, detail="Events not found")
        session.delete(events)
        session.commit()
        return {"ok": True}
