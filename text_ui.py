from threading import Thread
from saw_state import SawState
from saw_up_down_control import SawUpDownControl

class TextUI(Thread):

    def run(self):
        self.__class__.run_ui()

    @classmethod
    def run_ui(cls):
        while True:
            cls.print_ui()
            val = input('Select >>> ')
            if val == '1':
                SawUpDownControl.set_both_stops()
            elif val == '2':
                pass
            elif val == '3':
                SawUpDownControl.change_position(1)
            elif val == '4':
                SawUpDownControl.change_position(-1)
            elif val == '5':
                SawUpDownControl.change_position_inches(1)
            elif val == '6':
                SawUpDownControl.change_position_inches(-1)
            elif val == 'q':
                break

            print(SawState.get_state())

    @classmethod
    def print_ui(cls):
        print('\n\n\n')
        print('1. Find stops')
        print('2. Print state')
        print('3. Move up 1 rev')
        print('4. Move down 1 rev')
        print('5. Move up 1 inch')
        print('6. Move down 1 inch')
        print('7. Set zero')
        print('q. Quit')


if __name__ == '__main__':
    pass
    # TextUI().start()



