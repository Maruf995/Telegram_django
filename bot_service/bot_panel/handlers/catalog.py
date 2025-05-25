from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from product.models import Product
from users.models import User, CartItem
from asgiref.sync import sync_to_async
from keyboards.catalog import catalog_kb, mini_catalog_kb, products_kb, confirm_add_kb  # импорт клавиатур

router = Router()

@router.callback_query(F.data == "catalog")
async def show_catalog_menu(callback: CallbackQuery):
    kb = await catalog_kb()
    await callback.message.edit_text("Выберите категорию:", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("cat_"))
async def show_mini_catalog(callback: CallbackQuery):
    category_id = int(callback.data.split("_")[1])
    kb = await mini_catalog_kb(category_id)
    await callback.message.edit_text("Выберите подкатегорию:", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("minicat_"))
async def show_products(callback: CallbackQuery):
    mini_cat_id = int(callback.data.split("_")[1])
    kb = await products_kb(mini_cat_id)
    await callback.message.edit_text("Выберите продукт:", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("product_"))
async def show_product_info(callback: CallbackQuery):
    prod_id = int(callback.data.split("_")[1])
    product = await sync_to_async(Product.objects.get)(id=prod_id)
    caption = f"<b>{product.name}</b>"
    kb = confirm_add_kb(prod_id)
    if product.image:
        photo = FSInputFile(product.image.path)
        await callback.message.answer_photo(photo=photo, caption=caption, parse_mode="HTML", reply_markup=kb)
    else:
        await callback.message.answer(caption, parse_mode="HTML", reply_markup=kb)
    await callback.answer()

@router.callback_query(F.data.startswith("confirm_add_"))
async def add_to_cart(callback: CallbackQuery):
    prod_id = int(callback.data.split("_")[2])
    telegram_id = callback.from_user.id

    user, _ = await sync_to_async(User.objects.get_or_create)(telegram_id=telegram_id)
    product = await sync_to_async(Product.objects.get)(id=prod_id)

    try:
        cart_item = await sync_to_async(CartItem.objects.get)(user=user, product=product)
        cart_item.quantity += 1
        await sync_to_async(cart_item.save)()
    except CartItem.DoesNotExist:
        await sync_to_async(CartItem.objects.create)(user=user, product=product, quantity=1)

    await callback.message.answer(f"Товар <b>{product.name}</b> добавлен в корзину!", parse_mode="HTML")
    await callback.answer("Добавлено в корзину", show_alert=True)