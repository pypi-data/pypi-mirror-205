import psycopg
from psycopg import postgres
from psycopg.types.datetime import DateLoader, DateBinaryLoader
from psycopg.types.datetime import TimestampLoader, TimestampBinaryLoader
from psycopg.types.datetime import TimestamptzLoader, TimestamptzBinaryLoader
from psycopg.pq import Format
from psycopg.adapt import Dumper, Loader
import datetime as dt
from typing import Tuple, Any, Union, Type
from types import ModuleType

Connection = psycopg.Connection[Tuple[Any, ...]]
Cursor = psycopg.Cursor[Tuple[Any, ...]]

__all__ = ('register_inf_date_handler',
           'date_plus_infinity', 'PlusInfDate',
           'date_minus_infinity', 'MinusInfDate',
           'datetime_plus_infinity', 'PlusInfDatetimeNoTz',
           'datetime_minus_infinity', 'MinusInfDatetimeNoTz',
           'datetime_tz_plus_infinity', 'PlusInfDatetime',
           'datetime_tz_minus_infinity', 'MinusInfDatetime')


class _BaseInfDate:
    _inf_str: str
    _inf_text: bytes
    _inf_binary: bytes
    _inf_oid: int
    __slots__ = ()

    def __init__(self):
        pass

    def __add__(self, other):
        if isinstance(other, dt.timedelta):
            return self
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, dt.timedelta):
            return self
        if isinstance(other, (PlusInfDate, MinusInfDate)):
            raise ValueError('Cannot subtract infinite dates')
        return NotImplemented

    def pg_dump_text(self):
        return self._inf_text

    def pg_dump_binary(self):
        return self._inf_binary

    def __repr__(self):
        return self.__class__.__name__

    def __str__(self):
        return self._inf_str

    @classmethod
    def register_dumper(cls, obj: Union[Connection, Cursor, ModuleType]):

        class InfDateTextDumper(Dumper):
            oid = cls._inf_oid
            format = Format.TEXT

            def dump(self, _):
                return cls._inf_text

        class InfDateBinaryDumper(Dumper):
            oid = cls._inf_oid
            format = Format.BINARY

            def dump(self, _):
                return cls._inf_binary

        obj.adapters.register_dumper(cls, InfDateTextDumper)
        obj.adapters.register_dumper(cls, InfDateBinaryDumper)


class _BasePlusInfDate(_BaseInfDate):
    _inf_str = 'infinity'
    _inf_text = b'infinity'
    __slots__ = ()

    def __gt__(self, other):
        if isinstance(other, (dt.date, dt.datetime, _BaseMinusInfDate)):
            return True
        if isinstance(other, _BasePlusInfDate):
            return False
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, (dt.date, dt.datetime, _BaseInfDate)):
            return False
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, _BasePlusInfDate):
            return True
        if isinstance(other, (dt.date, dt.datetime, _BaseMinusInfDate)):
            return False
        return NotImplemented


class _BaseMinusInfDate(_BaseInfDate):
    _inf_str = '-infinity'
    _inf_text = b'-infinity'
    __slots__ = ()

    def __lt__(self, other):
        if isinstance(other, (dt.date, dt.datetime, _BasePlusInfDate)):
            return True
        if isinstance(other, _BaseMinusInfDate):
            return False
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, (dt.date, dt.datetime, _BasePlusInfDate, _BaseMinusInfDate)):
            return False
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, _BasePlusInfDate):
            return True
        if isinstance(other, (dt.date, dt.datetime, _BaseMinusInfDate)):
            return False
        return NotImplemented


class PlusInfDate(_BasePlusInfDate):
    _inf_binary = b'\x7f\xff\xff\xff'
    _inf_oid = postgres.types["date"].oid
    __slots__ = ()


class MinusInfDate(_BaseMinusInfDate):
    _inf_binary = b'\x80\x00\x00\x00'
    _inf_oid = postgres.types["date"].oid
    __slots__ = ()


class PlusInfDatetimeNoTz(_BasePlusInfDate):
    _inf_binary = b'\x7f\xff\xff\xff\xff\xff\xff\xff'
    _inf_oid = postgres.types["timestamp"].oid
    __slots__ = ()


class MinusInfDatetimeNoTz(_BaseMinusInfDate):
    _inf_binary = b'\x80\x00\x00\x00\x00\x00\x00\x00'
    _inf_oid = postgres.types["timestamp"].oid
    __slots__ = ()


class PlusInfDatetime(_BasePlusInfDate):
    _inf_binary = b'\x7f\xff\xff\xff\xff\xff\xff\xff'
    _inf_oid = postgres.types["timestamptz"].oid
    __slots__ = ()


class MinusInfDatetime(_BaseMinusInfDate):
    _inf_binary = b'\x80\x00\x00\x00\x00\x00\x00\x00'
    _inf_oid = postgres.types["timestamptz"].oid
    __slots__ = ()


date_plus_infinity = PlusInfDate()
date_minus_infinity = MinusInfDate()
datetime_plus_infinity = PlusInfDatetimeNoTz()
datetime_minus_infinity = MinusInfDatetimeNoTz()
datetime_tz_plus_infinity = PlusInfDatetime()
datetime_tz_minus_infinity = MinusInfDatetime()


def text_loader(text_loader_superclass: Type[Loader],
                plus_inf_type: Type[_BasePlusInfDate], minus_inf_type: Type[_BaseMinusInfDate],
                plus_inf: _BasePlusInfDate, minus_inf: _BaseMinusInfDate):
    class InfDateTextLoader(text_loader_superclass):
        def load(self, data):
            # noinspection PyProtectedMember
            if data == plus_inf_type._inf_text:
                return plus_inf
            # noinspection PyProtectedMember
            if data == minus_inf_type._inf_text:
                return minus_inf
            return super().load(data)

    return InfDateTextLoader


def binary_loader(binary_loader_superclass: Type[Loader],
                  plus_inf_type: Type[_BasePlusInfDate], minus_inf_type: Type[_BaseMinusInfDate],
                  plus_inf: _BasePlusInfDate, minus_inf: _BaseMinusInfDate):
    class InfDateBinaryLoader(binary_loader_superclass):
        def load(self, data):
            # noinspection PyProtectedMember
            if data == plus_inf_type._inf_binary:
                return plus_inf
            # noinspection PyProtectedMember
            if data == minus_inf_type._inf_binary:
                return minus_inf
            return super().load(data)

    return InfDateBinaryLoader


def register_inf_date_handler(obj: Union[Connection, Cursor, ModuleType]):
    # Sending data to the database

    PlusInfDate.register_dumper(obj)
    MinusInfDate.register_dumper(obj)

    PlusInfDatetimeNoTz.register_dumper(obj)
    MinusInfDatetimeNoTz.register_dumper(obj)

    PlusInfDatetime.register_dumper(obj)
    MinusInfDatetime.register_dumper(obj)

    # Fetching data from the database

    obj.adapters.register_loader("date", text_loader(DateLoader,
                                                     PlusInfDate, MinusInfDate,
                                                     date_plus_infinity, date_minus_infinity))
    obj.adapters.register_loader("date", binary_loader(DateBinaryLoader,
                                                       PlusInfDate, MinusInfDate,
                                                       date_plus_infinity, date_minus_infinity))
    obj.adapters.register_loader("timestamp", text_loader(TimestampLoader,
                                                          PlusInfDatetimeNoTz, MinusInfDatetimeNoTz,
                                                          datetime_plus_infinity, datetime_minus_infinity))
    obj.adapters.register_loader("timestamp", binary_loader(TimestampBinaryLoader,
                                                            PlusInfDatetimeNoTz, MinusInfDatetimeNoTz,
                                                            datetime_plus_infinity, datetime_minus_infinity))
    obj.adapters.register_loader("timestamptz", text_loader(TimestamptzLoader,
                                                            PlusInfDatetime, MinusInfDatetime,
                                                            datetime_tz_plus_infinity, datetime_tz_minus_infinity))
    obj.adapters.register_loader("timestamptz", binary_loader(TimestamptzBinaryLoader,
                                                              PlusInfDatetime, MinusInfDatetime,
                                                              datetime_tz_plus_infinity, datetime_tz_minus_infinity))
