import logging

from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from states import Reg
from buttons import royhat, get_num, yonalish_markup, yesorno
from aiogram.types import ReplyKeyboardRemove

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'], state='*')
async def do_start(message: types.Message, state: FSMContext):
  user = message.from_user.full_name
  await message.answer(f"<b>Assalomu aleykum {user}!</b> Onlayn ro'yxatdan o'tish botimizga xush kelibsiz!\n\nRo'yxatdan o'tishni boshlash uchun <b>\"Ro'yxatdan o'tishni boshlash\"</b> tugmasini bosing ⬇️", reply_markup=royhat)
  await state.finish()


@dp.message_handler(text_contains="Ro'yxatdan o'tishni boshlash")
async def get_full_name(message: types.Message):
  await message.answer("<b>Ismingiz va familiyangizni kiriting:</b>\n\n<i>Misol: Abdulla Rozmetov</i>", reply_markup=ReplyKeyboardRemove())
  await Reg.full_name.set()

@dp.message_handler(state=Reg.full_name)
async def get_name(message: types.Message, state: FSMContext):
  full_name = message.text
  await state.update_data(data={"full_name": full_name})
  await message.answer("<b>Necha yoshda ekanligingizni kiriting:</b>\n\n<i>Masalan: 18</i>")
  await  Reg.next()

@dp.message_handler(lambda message: message.text.isdigit() and 12 <= int(message.text) <=45, state=Reg.age)
async def get_age(message: types.Message, state: FSMContext):
  age = int(message.text)
  await state.update_data({"age":age})
  
  await message.answer("<b>Iltimos, yuboring yoki telefon raqamingizni yozing:</b>\n\n<i>Masalan: +998912345678</i>", reply_markup=get_num)
  await Reg.phone_number.set()

@dp.message_handler(content_types=['contact'], state=Reg.phone_number)
@dp.message_handler(state=Reg.phone_number)
async def get_phone_number(message: types.Message, state: FSMContext):
  if message.text:
    if message.text[:4] == "+998" and len(message.text) <= 15:
      await state.update_data({"phone_number":message.text})
      await message.answer("Yashash joyingizni yuboring:\n\n<i>Masalan: Urganch shahri...</i>", reply_markup=ReplyKeyboardRemove())
      await Reg.next()
    else:
      await message.answer("Siz telefon raqamingizni noto'g'ri yozdingiz!")
  else:
    if message.contact.phone_number[:3] == "998" or message.contact.phone_number[:4] == "+998" and len(message.contact.phone_number) <=15:
      await state.update_data({"phone_number":message.contact.phone_number})
      await message.answer("<b>Yashash joyingizni yuboring:</b>\n\n<i>Masalan: Urganch shahri...</i>", reply_markup=ReplyKeyboardRemove())
      await Reg.next()
    else:
      await message.answer("Siz telefon raqamingizni noto'g'ri yozdingiz!")
  

@dp.message_handler(state=Reg.addres)
async def get_addres(message: types.Message, state: FSMContext):
  addres = message.text
  await state.update_data({"address":addres})
  await message.answer("<b>Yo'nalishni tanlang:</b>", reply_markup=yonalish_markup)
  await Reg.next()

@dp.callback_query_handler(text=["Python", "JAVA", "JavaScript", "C++"], state=Reg.yonalish)
async def get_yonalish(call: types.CallbackQuery, state: FSMContext):
  yonalish = call.data
  await call.message.delete()
  await state.update_data({"yonalish":yonalish})
  await call.message.answer("<b>4x5 fotosuratni yuboring:</b>", reply_markup=ReplyKeyboardRemove())
  await Reg.next()

@dp.message_handler(content_types=['photo'], state=Reg.photo)
async def get_photo(message: types.Message, state: FSMContext):
  photo = message.photo[-1].file_id
  await state.update_data({"photo_id":photo})
  malumot = await state.get_data()
  await message.answer_photo(photo=malumot['photo_id'], caption=f"<b>Ism va familiya:</b> {malumot['full_name']}\n<b>Yosh:</b> {malumot['age']}\n<b>Telefon raqami: </b>{malumot['phone_number']}\n<b>Manzil:</b> {malumot['address']}\n<b>Yonalish:</b> {malumot['yonalish']}")
  await message.answer("Ma'lumotlaringiz saqlanishini xohlaysizmi?", reply_markup=yesorno)
  await Reg.next()


@dp.callback_query_handler(text=['yes', 'no'], state=Reg.wh)
async def get_or(call: types.CallbackQuery, state: FSMContext):
  yesorno = call.data
  await call.message.delete()
  if yesorno == 'yes':
    await call.message.answer("<b>Siz ma'lumotlar bazasiga muvaffaqiyatli yozildingiz! ✅</b>")
  else:
    await call.message.answer("Ma'lumotlar o'chirildi!")

  



  






if __name__ == '__main__':
  executor.start_polling(dp, skip_updates=True)