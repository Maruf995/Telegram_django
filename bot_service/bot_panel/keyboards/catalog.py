from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from product.models import Category, MiniCategory, Product
from asgiref.sync import sync_to_async

async def catalog_kb():
    categories = await sync_to_async(list)(Category.objects.all())
    buttons = [[InlineKeyboardButton(text=cat.name, callback_data=f"cat_{cat.id}")] for cat in categories]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def mini_catalog_kb(category_id: int):
    category = await sync_to_async(Category.objects.get)(id=category_id)
    mini_categories = await sync_to_async(list)(category.mini_category.all())
    buttons = [[InlineKeyboardButton(text=mc.name, callback_data=f"minicat_{mc.id}")] for mc in mini_categories]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def products_kb(mini_cat_id: int):
    products = await sync_to_async(list)(Product.objects.filter(category__id=mini_cat_id))
    buttons = []
    for product in products:
        buttons.append([
            InlineKeyboardButton(text=product.name, callback_data=f"product_{product.id}"),
            InlineKeyboardButton(text="Добавить в корзину", callback_data=f"add_{product.id}")
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def confirm_add_kb(product_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить добавление в корзину", callback_data=f"confirm_add_{product_id}")]
    ])

