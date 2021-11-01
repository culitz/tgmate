from typing import Iterable, List, Tuple, Optional
from datetime import date, datetime
from calendar import monthrange
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import CallbackQuery
from telebot import TeleBot


CALLBACK_TAG = 'CALENDAR'
CALLBACK_TAG_PREV = 'PREV'
CALLBACK_TAG_NEXT = 'NEXT'


def build_callback_data(curr_date: date) -> str:
    return f'{CALLBACK_TAG} {curr_date}'

def is_callback_contain_tag(c: CallbackQuery, substring: str) -> bool:
    """
    It is callback from prev navigation button?
    :param c: callback query
    :type callback: CallbackQuery
    :param substring: Substring to gfind
    :type substring: str
    :return: bool 
    """
    prev_sign: int = c.data.find(substring)
    return False if prev_sign == -1 else True

class CalendarButton:
    # Empty sign
    EMPTY = f'{CALLBACK_TAG} empty'

    def __init__(self, current_date: date) -> None:
        """
        Construsctor
        :param current_date: Date and month for calendar
        """
        self.__current_date: date = current_date
        self.__range: Tuple[int, int] = monthrange(self.__current_date.year, self.__current_date.month)
        self.__days: Iterable[str] = self.__generate_days()
    
    def next(self) -> Optional[InlineKeyboardButton]:
        """
        Getting nex button of calendar 
        """
        try:
            day: str = next(self.__days)
            text: str = day if day != self.EMPTY else '-'
            return InlineKeyboardButton(text=text, callback_data=self.__meta())
        except StopIteration:
            return None

    def __generate_days(self) -> Iterable[str]:
        """
        Generate day table for calendar
        """
        result: List[str] = []
        first_day: int = 1
        last_day: int = self.__range[1]
        begin_wheek_day: int = self.__current_date.weekday()
        days: List[str] = [str(item) for item in range(first_day, last_day, 1)]

        # Make offset
        for i in range(begin_wheek_day):
            result.insert(0, self.EMPTY)

        for item in days:
            result.append(item)
        
        # Fill end
        last_wheek_days: int = len(days) % 7
        append_days: int = 7 - last_wheek_days         
        for i in range(append_days):
            result.append(self.EMPTY)
        return (i for i in result)

    def __meta(self) -> str:
        """
        Metadata for callback 
        """
        return build_callback_data(self.__current_date)

    @staticmethod
    def unpack_meta(meta: str) -> Tuple[int, int, int]:
        """
        Static method to convert metadata into datetime.date
        return year, month, day
        """
        sp: List[str] = meta.split()
        dts: List[str] = sp[1].split('-')
        return dts[0], dts[1], dts[2]


class CalendarReply(InlineKeyboardMarkup):
    def __init__(self, bot: TeleBot, curr_date: Optional[date] = None) -> None:
        super(CalendarReply, self).__init__()
        self.__date: Optional[date] = curr_date if curr_date is not None else date.today()
        self.__build_calendar()
        self.__telebot = bot
        self.__subscribe()
        
    def __week_days(self) -> List[InlineKeyboardButton]:
        """
        Row with weekday's names
        """
        arr = ['s', 'm', 't', 'w', 't', 'f', 's']
        return [InlineKeyboardButton(text=item, callback_data='pass') for item in arr]

    def __navigation_prev_meta(self) -> str:
        return f"{build_callback_data(self.__date)} {CALLBACK_TAG_PREV}"

    def __navigation_next_meta(self) -> str:
        return f"{build_callback_data(self.__date)} {CALLBACK_TAG_NEXT}"

    def __navigation_keyboard(self):
        """
        Navigation buttons
        """
        return [
            InlineKeyboardButton(
                '<-', 
                callback_data=self.__navigation_prev_meta()),
            InlineKeyboardButton(
                '->', 
                callback_data=self.__navigation_next_meta())
        ]

    def __build_calendar(self) -> None:
        """
        Calendar rows
        """
        calendar_btn = CalendarButton(self.__date)
        btn_list: List[InlineKeyboardButton] = []
        stop: bool = False

        while not stop:
            btn = calendar_btn.next()
            if btn is None:
                stop = True
                continue
            btn_list.append(btn)

        self.row(*self.__week_days())
        self.row(*btn_list[:7])
        self.row(*btn_list[7:14])
        self.row(*btn_list[14:21])
        self.row(*btn_list[21:28])
        self.row(*btn_list[28:35])
        self.row(*self.__navigation_keyboard())

    @staticmethod
    def __is_callback_prev(c: CallbackQuery) -> bool:
        """
        It is callback from prev navigation button?
        :param c: callback query
        :type CallbackQuery:

        :return: is prev button 
        """
        return is_callback_contain_tag(c, CALLBACK_TAG_PREV)

    @staticmethod
    def __is_callback_next(c: CallbackQuery) -> bool:
        """
        It is callback from prev navigation button?
        :param c: callback query
        :type CallbackQuery:

        :return: is prev button 
        """
        return is_callback_contain_tag(c, CALLBACK_TAG_NEXT)

    def __navigate(self, c: CallbackQuery, direction: int) -> date:
        if direction not in (1, -1):
            raise ValueError(f'{direction} unexpected value must be in (1,-1)')

        year, month, day = CalendarButton.unpack_meta(c.data)
        year_begin, year_end = month == 1, month == 12
        
        if year_begin and direction < 0:
            year += direction
            month = 1
        
        elif year_end and direction > 0:
            year += direction
            month = 1
        
        else:
            month += 1
        return date(year, month, day)

    def nevigate_prev(self, c: CallbackQuery) -> date:
        return self.__navigate(c, -1)

    def navigate_next(self, c: CallbackQuery) -> date:
        return self.__navigate(c, 1)

    def __subscribe(self):
        """
        Calendars's callbacks
        """
        @self.__telebot.callback_query_handler(func=self.__is_callback_prev)
        def next_callback(callback_query: CallbackQuery):
            self.__telebot.answer_callback_query(
                callback_query_id=callback_query.id, 
                show_alert=False,
                text='next')

            d: date = CalendarButton.unpack_meta(callback_query.data)

            self.__telebot.send_message(
                callback_query.message.chat.id,
                'prev text callback',
                reply_markup=CalendarReply(self.__telebot))

        @self.__telebot.callback_query_handler(func=self.__is_callback_next)
        def prev_callback(callback_query: CallbackQuery):
            self.__telebot.answer_callback_query(
                callback_query_id=callback_query.id,
                show_alert=False,
                text='next'
            )
            self.__telebot.send_message(
                callback_query.message.chat.id,
                'next text callback',
                reply_markup=CalendarReply(self.__telebot)
            )