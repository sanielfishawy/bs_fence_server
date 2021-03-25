import logging
from types import ClassMethodDescriptorType

class Limits:
    @classmethod
    def get_postion_in_limits(cls, position) -> float:
        position = float(position)
        position = max(position, cls.get_min_position())
        position = min(position, cls.get_max_position())
        return position

    @classmethod
    def get_min_position(cls):
        return SawState.get_min_position()

    @classmethod
    def get_max_position(cls):
        return SawState.get_max_position()


class SawState:
    POSITION_KEY = 'position'
    POSITION_INCHES_KEY = 'position_inches'
    MIN_POSITION_KEY = 'min_position'
    MAX_POSITION_KEY = 'max_position'
    MIN_POSITION_INCHES_KEY = 'min_position_inches'
    MAX_POSITION_INCHES_KEY = 'max_position_inches'
    REVOLUTIONS_PER_INCH_KEY = 'revolutions_per_inch'
    LIMITS_SET_KEY = 'limits_set'
    ZERO_POSITION_KEY = 'zero_position'

    POSITION = 0
    MIN_POSITION = -50
    MAX_POSITION = 50
    REVOLUTIONS_PER_INCH = 5.0
    LIMITS_SET = False
    ZERO_POSITION = 0

    @classmethod
    def get_state(cls):
        return {
            cls.POSITION_KEY: cls.get_position(),
            cls.POSITION_INCHES_KEY: cls.get_position_inches(),
            cls.MAX_POSITION_KEY: cls.get_max_position(),
            cls.MIN_POSITION_KEY: cls.get_min_position(),
            cls.MAX_POSITION_INCHES_KEY: cls.get_max_position_inches(),
            cls.MIN_POSITION_INCHES_KEY: cls.get_min_position_inches(),
            cls.REVOLUTIONS_PER_INCH_KEY: cls.get_revolutions_per_inch(),
            cls.LIMITS_SET_KEY: cls.get_limits_set(),
            cls.ZERO_POSITION_KEY: cls.get_zero_position(),
        }

    @classmethod
    def get_position(cls):
        return cls.POSITION

    @classmethod
    def set_position(cls, position):
        cls.POSITION = Limits.get_postion_in_limits(position)
        return cls

    @classmethod
    def set_position_inches(cls, inches):
        cls.set_position(cls.get_position_with_inches(inches))
        return cls.get_position_inches()

    @classmethod
    def get_position_inches(cls):
        return cls.get_inches_with_position(cls.get_position())

    @classmethod
    def get_zero_position(cls):
        return cls.ZERO_POSITION

    @classmethod
    def set_zero_position(cls, pos):
            cls.ZERO_POSITION = pos
            return cls

    @classmethod
    def change_position(cls, change):
        cls.set_position(cls.get_position() + change)
        return cls.get_position()

    @classmethod
    def set_max_position(cls, pos):
        cls.MAX_POSITION = pos
        return cls

    @classmethod
    def get_max_position(cls):
        return cls.MAX_POSITION

    @classmethod
    def get_max_position_inches(cls):
        return cls.get_inches_with_position(cls.get_max_position())

    @classmethod
    def set_min_position(cls, pos):
        cls.MIN_POSITION= pos
        return cls

    @classmethod
    def get_min_position(cls):
        return cls.MIN_POSITION

    @classmethod
    def get_min_position_inches(cls):
        return cls.get_inches_with_position(cls.get_min_position())

    @classmethod
    def set_min_and_max_position(cls, min, max):
        cls.set_min_position(min)
        cls.set_max_position(max)
        cls.set_limits_set(True)

    @classmethod
    def set_limits_set(cls, setting):
        cls.LIMITS_SET = setting
        return cls

    @classmethod
    def get_limits_set(cls):
        return cls.LIMITS_SET

    @classmethod
    def get_inches_with_position(cls, pos):
        return (pos - cls.ZERO_POSITION) / cls.REVOLUTIONS_PER_INCH

    @classmethod
    def get_position_with_inches(cls, inches):
        return (inches * cls.REVOLUTIONS_PER_INCH) + cls.ZERO_POSITION

    @classmethod
    def set_revolutions_per_inch(cls, rpi):
        cls.REVOLUTIONS_PER_INCH = rpi
        return cls

    @classmethod
    def get_revolutions_per_inch(cls):
        return cls.REVOLUTIONS_PER_INCH