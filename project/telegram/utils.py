def get_current_month_and_year(
    month: str, year: str, move: str
) -> tuple[int, int]:
    """Получение года и месяца для прохода по календарю.

    Args:
        month: Месяц - число строкой
        year: Год - число строкой
        move: Вектор движения
    Returns:
         (month, year): кортеж чисел
    """

    year = int(year)
    if move == 'back':
        if len(month) > 1 and month[0] == '0':
            month = int(month[1:])
        else:
            month = int(month)
        month -= 1

        if month == 0:
            month = 12
            year -= 1
    else:
        if len(month) > 1 and month[0] == '0':
            month = int(month[1:])
        else:
            month = int(month)
        month += 1

        if month > 12:
            month = 1
            year += 1

    return month, year


def get_workout_days(workout_notes) -> set:
    """Получение дней в которые были тренировки.
    Args:
        workout_notes: db record
    Returns:
        set: множество дней
    """
    workout_days = set()
    for note in workout_notes:
        day_ = note.date.strftime('%d')

        # вырезать ноль
        if len(day_) > 1 and day_[0] == '0':
            day_ = day_[1]
        workout_days.add(day_)

    return workout_days


def get_msg_for_records_workout(
    record_number: int, records_amount: int, text_record: str
) -> str:
    return f"""
        Запись №{record_number} из {records_amount} за день\n
    ----------------------------------------\n
    {text_record}
    """


def get_russian_category_name(category: str) -> str:
    res = None
    if category == 'health':
        res = 'здоровье'
    if category == 'transport':
        res = 'транспорт'
    if category == 'food':
        res = 'еда'
    if category == 'entertainment':
        res = 'развлечения'
    if category == 'purchases':
        res = 'покупки'
    if category == 'present':
        res = 'подарки'
    if category == 'other':
        res = 'прочее'

    return res


def get_non_zero_keys(d: dict) -> str:
    for key, value in d.items():
        if key not in ('id', 'date', '_sa_instance_state') and value != 0:
            return key
