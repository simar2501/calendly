from fastapi import FastAPI
from .models import User
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, get_db
from .routes import event_types, availability, bookings, meetings, contacts, SingleUseLink
from .routes import polls
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Schedulr API", redirect_slashes=False)

def create_default_user():
    db = next(get_db())
    user = db.query(User).filter(User.id == 1).first()
    if not user:
        new_user = User(
            id=1,
            name="John Doe",
            email="john@example.com",
            timezone="UTC"
        )
        db.add(new_user)
        db.commit()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://calendly-kappa.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(event_types.router, prefix="/api/event-types", tags=["Event Types"])
app.include_router(availability.router, prefix="/api/availability", tags=["Availability"])
app.include_router(bookings.router, prefix="/api/booking", tags=["Booking"])
app.include_router(meetings.router, prefix="/api/meetings", tags=["Meetings"])
app.include_router(contacts.router, prefix="/api/contacts", tags=["Contacts"])
app.include_router(SingleUseLink.router, prefix="/api/single-use-links", tags=["single-use-links"])
app.include_router(polls.router, prefix="/api/polls", tags=["Polls"])

@app.on_event("startup")
def startup():
    create_default_user()

@app.get("/")
def root():
    return {"message": "Schedulr API Running"}