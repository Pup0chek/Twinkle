import asyncio
import logging
import sys
import psycopg2
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os

API_TOKEN = '7657082866:AAHF_oqPX3GDsC3ivtakEnfwc7gKWuHq-pM'
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Almaty111@localhost:5432/lol")

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
scheduler = AsyncIOScheduler()

class UserState(StatesGroup):
    waiting_for_login = State()
    waiting_for_reminder_time = State()
    waiting_for_action_choice = State()
    waiting_for_deletion_choice = State()

def get_db_connection():
    """Устанавливает соединение с базой данных."""
    return psycopg2.connect(DATABASE_URL, options="-c client_encoding=UTF8")

async def send_water_reminder(chat_id: int):
    """Отправляет напоминание пользователю."""
    try:
        await bot.send_message(chat_id, "Не забудьте выпить воды! 💧")
    except Exception as e:
        logging.error(f"Ошибка при отправке напоминания: {e}")

def schedule_reminders():
    """Запланировать задачи для отправки напоминаний."""
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT w.user_id, w.chat_id, w.frequency
                FROM water_intake w
                WHERE w.is_active = true
            """)
            reminders = cursor.fetchall()

    # Планируем каждое напоминание
    for user_id, chat_id, reminder_time in reminders:
        # Используем reminder_time напрямую, так как он уже типа time
        scheduler.add_job(
            send_water_reminder,
            trigger='cron',
            hour=reminder_time.hour,
            minute=reminder_time.minute,
            args=[chat_id],
            id=f"reminder_{user_id}_{reminder_time.hour}_{reminder_time.minute}",
            replace_existing=True
        )

    logging.info("Запланированы напоминания для всех пользователей.")

@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Привет! Пожалуйста, введите свой логин для авторизации.")
    await state.set_state(UserState.waiting_for_login)

@dp.message(UserState.waiting_for_login)
async def process_login(message: Message, state: FSMContext) -> None:
    login = message.text
    chat_id = message.chat.id

    try:
        # Проверяем наличие пользователя в базе данных
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM users WHERE username = %s", (login,))
                user = cursor.fetchone()

        if user:
            # Сохраняем user_id во временное хранилище состояния
            await state.update_data(user_id=user[0])

            # Проверяем, есть ли уже запись с данным user_id в таблице water_intake
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM water_intake WHERE user_id = %s", (user[0],))
                    record = cursor.fetchone()

                    if record:
                        # Если запись существует, обновляем chat_id
                        cursor.execute(
                            """
                            UPDATE water_intake
                            SET chat_id = %s
                            WHERE user_id = %s
                            """,
                            (chat_id, user[0])
                        )
                    else:
                        # Если записи нет, добавляем новую запись
                        cursor.execute(
                            """
                            INSERT INTO water_intake (user_id, chat_id, is_active)
                            VALUES (%s, %s, true)
                            """,
                            (user[0], chat_id)
                        )
                    connection.commit()

            # Переход к выбору действия
            await message.answer(
                f"Добро пожаловать, {login}! Пожалуйста, выберите действие:\n1. Добавить напоминание\n2. Удалить напоминание\n3. Изменить напоминание")
            await state.set_state(UserState.waiting_for_action_choice)
        else:
            # Пользователь не найден
            await message.answer("Пользователь с таким логином не найден. Попробуйте еще раз.")
    except psycopg2.Error as e:
        logging.error(f"Ошибка при подключении к базе данных: {e}")
        await message.answer("Произошла ошибка при подключении к базе данных.")
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {e}")
        await message.answer("Произошла непредвиденная ошибка. Попробуйте позже.")

@dp.message(UserState.waiting_for_action_choice)
async def handle_action_choice(message: Message, state: FSMContext) -> None:
    choice = message.text
    if choice == "1":
        await message.answer("Введите время для напоминания в формате ЧЧ:ММ.")
        await state.set_state(UserState.waiting_for_reminder_time)
    elif choice == "2":
        # Получение user_id из состояния
        data = await state.get_data()
        user_id = data.get("user_id")

        # Получение всех временных точек для удаления
        try:
            with get_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT frequency FROM water_intake
                        WHERE user_id = %s AND is_active = true
                        """,
                        (user_id,)
                    )
                    reminders = cursor.fetchall()

            # Проверка наличия напоминаний
            if reminders:
                reminder_times = [f"- {reminder[0]}" for reminder in reminders]
                reminder_list = "\n".join(reminder_times)
                await message.answer(f"Текущие активные напоминания:\n{reminder_list}\n\nВведите время напоминания, которое хотите удалить (в формате ЧЧ:ММ).")
                await state.set_state(UserState.waiting_for_deletion_choice)
            else:
                await message.answer("У вас нет активных напоминаний для удаления.")
                await state.clear()

        except psycopg2.Error as e:
            logging.error(f"Ошибка при получении напоминаний: {e}")
            await message.answer("Произошла ошибка при получении списка напоминаний.")
    elif choice == "3":
        await message.answer("Функционал изменения напоминания пока недоступен.")
    else:
        await message.answer("Пожалуйста, выберите корректное действие (1, 2 или 3).")

@dp.message(UserState.waiting_for_reminder_time)
async def process_reminder_time(message: Message, state: FSMContext) -> None:
    reminder_time = message.text
    chat_id = message.chat.id
    try:
        # Проверка формата времени
        hours, minutes = map(int, reminder_time.split(":"))
        if not (0 <= hours < 24 and 0 <= minutes < 60):
            raise ValueError("Неверный формат времени")

        # Получаем user_id из состояния
        data = await state.get_data()
        user_id = data.get("user_id")

        # Добавление времени напоминания и chat_id в таблицу water_intake
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO water_intake (user_id, frequency, chat_id, is_active)
                    VALUES (%s, %s, %s, true)
                    """,
                    (user_id, reminder_time, chat_id)
                )

        # Перепланировать задачи после добавления времени
        schedule_reminders()

        # Подтверждение установки времени напоминания
        await message.answer(f"Напоминание будет приходить каждый день в {reminder_time}.", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите время в правильном формате ЧЧ:ММ.")
    except psycopg2.Error as e:
        logging.error(f"Ошибка при обновлении времени напоминания: {e}")
        await message.answer("Произошла ошибка при обновлении времени напоминания.")
    except Exception as e:
        logging.error(f"Неизвестная ошибка: {e}")
        await message.answer("Произошла непредвиденная ошибка. Попробуйте позже.")

async def main() -> None:
    # Запуск планировщика
    scheduler.start()

    # Планируем напоминания при запуске
    schedule_reminders()

    # Запуск поллинга бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
