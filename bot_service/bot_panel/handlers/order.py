from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from users.models import User
from states import OrderStates

router = Router()

@router.callback_query(F.data == "place_order")
async def start_order(callback: CallbackQuery, state: FSMContext):
    telegram_id = callback.from_user.id
    user = await sync_to_async(User.objects.get_or_create)(telegram_id=telegram_id)
    user = user[0]

    if all([user.first_name, user.second_name, user.email, user.number, user.address]):
        confirm_text = (
            "<b>Ваши данные уже сохранены:</b>\n\n"
            f"Имя: {user.first_name}\n"
            f"Фамилия: {user.second_name}\n"
            f"email: {user.email}\n"
            f"Телефон: {user.number}\n"
            f"Адрес: {user.address}\n\n"
            "Нажмите <b>Подтвердить</b>, если всё верно."
        )
        from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_order")]
        ])
        await callback.message.answer(confirm_text, reply_markup=kb, parse_mode="HTML")
        await state.clear()
    else:
        await callback.message.answer("Введите ваше имя:")
        await state.set_state(OrderStates.first_name)

    await callback.answer()

@router.message(OrderStates.first_name)
async def get_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введите вашу фамилию:")
    await state.set_state(OrderStates.second_name)

@router.message(OrderStates.second_name)
async def get_second_name(message: Message, state: FSMContext):
    await state.update_data(second_name=message.text)
    await message.answer("Введите ваш email:")
    await state.set_state(OrderStates.email)

@router.message(OrderStates.email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите ваш номер телефона:")
    await state.set_state(OrderStates.number)

@router.message(OrderStates.number)
async def get_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer("Введите ваш адрес:")
    await state.set_state(OrderStates.address)

@router.message(OrderStates.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    data = await state.get_data()

    # Сохраняем пользователя
    user = await sync_to_async(User.objects.get)(telegram_id=message.from_user.id)
    user.first_name = data["first_name"]
    user.second_name = data["second_name"]
    user.email = data["email"]
    user.number = data["number"]
    user.address = data["address"]
    await sync_to_async(user.save)()

    # Подтверждение
    confirm_text = (
        "<b>Проверьте данные:</b>\n\n"
        f"Имя: {data['first_name']}\n"
        f"Фамилия: {data['second_name']}\n"
        f"Email: {data['email']}\n"
        f"Телефон: {data['number']}\n"
        f"Адрес: {data['address']}"
    )

    await message.answer(confirm_text, parse_mode="HTML")
    await state.clear()
