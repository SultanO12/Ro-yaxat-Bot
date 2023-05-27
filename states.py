from aiogram.dispatcher.filters.state import StatesGroup, State

class Reg(StatesGroup):
  full_name = State()
  age = State()
  phone_number = State()
  addres = State()
  yonalish= State()
  photo = State()
  wh = State()
