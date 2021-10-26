from typing import Iterable, List, Tuple, Optional
from datetime import date
from calendar import monthrange
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

CALLBACK_TAG = 'CALENDAR'

class CalendarButton:
    EMPTY = f'{CALLBACK_TAG} empty'
    def __init__(self, current_date: date) -> None:
        self.__current_date: date = current_date
        self.__range: Tuple[int, int] = monthrange(self.__current_date.year, self.__current_date.month)
        self.__days: Iterable[str] = self.__generate_days()
    
    def next(self) -> Optional[InlineKeyboardButton]:
        try:
            day: str = next(self.__days)
            text: str = day if day != self.EMPTY else '-'
            return InlineKeyboardButton(text=text, callback_data=self.__meta())
        except StopIteration:
            return None

    def __generate_days(self) -> Iterable[str]:
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
        return f'{CALLBACK_TAG} {self.__current_date}'

    @staticmethod
    def unpack_meta(meta: str) -> Tuple[int, int, int]:
        sp: List[str] = meta.split()
        dts: List[str] = sp[1].split('-')
        return dts[0], dts[1], dts[2]


class CalendarReply(InlineKeyboardMarkup):

    def __init__(self, curr_date: Optional[date] = None) -> None:
        super(CalendarReply, self).__init__()
        self.__date: Optional[date] = curr_date
        self.__build_calendar()
        
    def __week_days(self) -> List[InlineKeyboardButton]:
        arr = ['s', 'm', 't', 'w', 't', 'f', 's']
        return [InlineKeyboardButton(text=item, callback_data='pass') for item in arr]

    def __build_calendar(self) -> None:
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
