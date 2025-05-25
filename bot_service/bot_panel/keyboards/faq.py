from aiogram import Router
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import hashlib

router = Router()

FAQ_DATA = {
    "Как оформить заказ?": "Чтобы оформить заказ, добавьте товары в корзину и нажмите кнопку 'Оформить заказ'.",
    "Как удалить товар из корзины?": "Нажмите кнопку ❌ рядом с товаром в корзине.",
    "Какие способы оплаты доступны?": "Мы принимаем оплату картой, наличными и онлайн-платежами.",
    "Как связаться с поддержкой?": "Напишите нам в Telegram @SupportBot или по телефону +7 123 456 78 90.",
}

@router.inline_query()
async def inline_faq(inline_query: InlineQuery):
    query_text = inline_query.query.lower().strip()

    results = []
    for question, answer in FAQ_DATA.items():
        if query_text in question.lower():
            result_id = hashlib.md5(question.encode()).hexdigest()
            results.append(
                InlineQueryResultArticle(
                    id=result_id,
                    title=question,
                    input_message_content=InputTextMessageContent(
                        message_text=f"❓ <b>{question}</b>\n\n{answer}",
                        parse_mode="HTML"
                    ),
                    description=answer[:50] + ("..." if len(answer) > 50 else ""),
                )
            )

    if not results:
        results.append(
            InlineQueryResultArticle(
                id="no_result",
                title="Вопрос не найден",
                input_message_content=InputTextMessageContent(
                    message_text="Извините, я не знаю ответа на этот вопрос."
                ),
                description="Попробуйте задать вопрос иначе",
            )
        )

    await inline_query.answer(results, cache_time=60, is_personal=True)
