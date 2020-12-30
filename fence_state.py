import logging

class StateHelper:
    POSITION_KEY = 'position'
    MIN_POSITION_KEY = 'min_position'
    MAX_POSITION_KEY = 'max_position'

    @classmethod
    def get_default_state(cls):
        return {
            cls.POSITION_KEY: 15,
            cls.MIN_POSITION_KEY: 0,
            cls.MAX_POSITION_KEY: 15,
        }

class Limits:
    @classmethod
    def get_postion_in_limits(cls, position) -> float:
        position = float(position)
        postion = max(position, cls.get_min_position())
        frequency = min(position, cls.get_max_position())
        return frequency

    @classmethod
    def get_min_position(cls):
        return StateHelper.get_default_state()[StateHelper.MIN_POSITION_KEY]

    @classmethod
    def get_max_position(cls):
        return StateHelper.get_default_state()[StateHelper.MAX_POSITION_KEY]


class FenceState:
    def __init__(self):
        self.state = StateHelper.get_default_state()

    def get_state(self):
        return self.state

    def get_position(self):
        return self.get_state()[StateHelper.POSITION_KEY]

    def set_position(self, position):
        self.state[StateHelper.POSITION_KEY] = Limits.get_postion_in_limits(position)
        return self