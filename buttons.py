from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

royhat = ReplyKeyboardMarkup(keyboard=[
  [KeyboardButton("📋 Ro'yxatdan o'tishni boshlash")]
],resize_keyboard=True)

get_num = ReplyKeyboardMarkup(keyboard=[
  [KeyboardButton("📞 Telefon raqamini yuborish", request_contact=True)]
], resize_keyboard=True)

yonalish_markup = InlineKeyboardMarkup(row_width=1)
yonalish_markup.row(InlineKeyboardButton("Python", callback_data="Python"))
yonalish_markup.row(InlineKeyboardButton("JAVA", callback_data="JAVA"))
yonalish_markup.row(InlineKeyboardButton("JavaScript", callback_data="JavaScript"))
yonalish_markup.row(InlineKeyboardButton("C++", callback_data="C++"))

yesorno = InlineKeyboardMarkup()
yesorno.row(InlineKeyboardButton("Ha ✅", callback_data='yes'), InlineKeyboardButton("Yo'q ❌", callback_data='no'))