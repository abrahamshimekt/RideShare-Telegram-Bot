
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    Register = State()
    Contact_info = State()
    Role = State()
    EditFullname = State()
    Menu_Passenger = State()
    Menu_Driver = State()
    Book = State()
    BookLocation = State()
    BookDestination = State()
    DriverStatus = State()
    RideComplete = State()
    RideAccept = State()
    DriverReview = State()
    PassengerReview = State()
    Rating = State()