from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import logging

router = Router()

logger = logging.getLogger(__name__)

logger_handler = logging.StreamHandler()

logger.addHandler(logger_handler)

logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:' '{lineno} - {name} - {message}',
    style='{'
  )


@router.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext):
    await message.answer(
        "Привет! Я помогу вычислить оптимальные дни для общения с женщиной. "
        "Отправь первый день её месячных в формате дд.мм.гггг, и я покажу, когда ей будет приятно видеть тебя 😊."
    )

@router.message()
async def process_menstruation_date(message: Message, state: FSMContext):
    # Parsing the date in "d.m.y" format
    try:
        start_date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        return await message.answer('Введите дату в формате "дд.мм.гггг".')

    # Typical cycle settings
    cycle_length = 28  # Average cycle length; user could adjust for accuracy
    ovulation_offset = 14  # Ovulation typically 14 days before next period

    # Calculating key dates
    menstruation_end = start_date + timedelta(days=7)
    follicular_start = menstruation_end
    ovulation_day = start_date + timedelta(days=cycle_length - ovulation_offset)
    fertile_start = ovulation_day - timedelta(days=4)
    fertile_end = ovulation_day + timedelta(days=1)
    affection_day = ovulation_day - timedelta(days=2)
    early_luteal_start = ovulation_day + timedelta(days=1)
    pms_start_day = start_date + timedelta(days=cycle_length - 7)
    next_menstruation = start_date + timedelta(days=cycle_length)
    next_menstruation_end = next_menstruation + timedelta(days=7)

    # Response message
    response = (
        f"Цикл и рекомендации:\n\n"
        f"**🔴 Менструация** (1-7 день):\n"
        f"   - Начало: {start_date.strftime('%d.%m.%Y')}\n"
        f"   - Конец: {menstruation_end.strftime('%d.%m.%Y')}\n"
        f"   - Ожидаемые ощущения: усталость, низкий уровень энергии. Вас не хотят, лучше бы вас не было нахуй!\n\n"
        
        f"**Фолликулярная фаза** (6-13 день):\n"
        f"   - Начало: {follicular_start.strftime('%d.%m.%Y')}\n"
        f"   - Ожидаемые ощущения: подъем настроения, активность, общительность. Хуйня после менстры сразу, в последнии дни этой хуйни вас хотят\n\n"
        
        f"**📅Овуляция** (примерно 14 день):\n"
        f"   - Дата: {ovulation_day.strftime('%d.%m.%Y')}\n"
        f"   - Пик либидо и желание общения ВАС ОЧЕНЬ ХОТЯТ.\n\n"
        
        f"**🌱Окно фертильности ???**:\n"
        f"   - С {fertile_start.strftime('%d.%m.%Y')} по {fertile_end.strftime('%d.%m.%Y')}\n"
        f"   - Идеальный период для физического контакта. ВАС ХОТЯТ.\n\n"
        
        f"**💕Ранний лютеиновый период** (15-21 день):\n"
        f"   - Начало: {early_luteal_start.strftime('%d.%m.%Y')}\n"
        f"   - Спокойное состояние, стабильное настроение. Ну если вы норм, то ВАС хотят\n\n"
        
        f"**⚠️Поздний лютеиновый период / ПМС** (22-28 день):\n"
        f"   - Начало: {pms_start_day.strftime('%d.%m.%Y')}\n"
        f"   - Возможные симптомы: раздражительность, упадок сил, тяга к покою и поддержке. Вас не хотят, но ок\n\n"
        
        f"**🔴Следующие месячные**:\n"
        f"   - С: {next_menstruation.strftime('%d.%m.%Y')} - по {next_menstruation_end.strftime('%d.%m.%Y')}\n"
        f"   - Длительность цикла может варьироваться от 28 до 33 дней. Вас не хотят\n"
    )

    await message.answer(response)
