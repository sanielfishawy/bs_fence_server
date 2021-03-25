import saw_calibration
from saw_state import SawState
from saw_calibration import SawCalibration

class TextUI:

    @classmethod
    def run_ui(cls):
        if not SawState.get_limits_set():
            cls.set_stops()

    @classmethod
    def set_stops(cls):
        val = 'n'
        while val.lower()[0] != 'y':
            print('I need to find the top and bottom stops.')
            print('Can I move the blade up and down to the limits?')
            val = input(('(y)es / (n)o: \n>>> '))
        SawCalibration.set_both_stops()

    @classmethod
    def set_zero(cls):


if __name__ == '__main__':
    TextUI.run_ui()



