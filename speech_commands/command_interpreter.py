import re

class Command:
    def __init__(self, path, payload):
        self.path = path
        self.payload = payload

class CommandInterpreter:
    KEYWORDS = [
        'volume',
        'frequency',
        'power',
    ]

    NUMBER_WORDS = {
        'zero': 0,
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
        'ten': 10,
    }

    NUMBER_REGEX = re.compile('\d+')
    UP_DOWN_REGEX = re.compile(r'\bup\b|\bdown\b')
    ON_OFF_REGEX = re.compile(r'\bon\b|\boff\b')

    def __init__(self, request_paths, state_helper):
        self.request_paths = request_paths
        self.state_helpler = state_helper

    def preprocess(self, txt):
        return txt.lower()

    def interpret_command(self, txt):
        txt = self.preprocess(txt)
        kwd = self.get_keyword(txt)
        if kwd:
            if kwd == 'power':
                path = self.request_paths.SAVE_POWER_PATH
                on_off = self.get_on_off(txt)
                if on_off == 'on':
                    return Command(path, {self.state_helpler.POWER_KEY:True})
                elif on_off == 'off':
                    return Command(path, {self.state_helpler.POWER_KEY:False})
                else:
                    return None

            elif kwd == 'volume':
                num = self.get_number(txt)
                up_down = self.get_up_down(txt)

                if not num and not up_down:
                    return None
                elif not num and up_down:
                    num = 10

                if not up_down:
                    return Command(self.request_paths.SAVE_VOLUME_PATH, {self.state_helpler.VOLUME_KEY: num})
                elif up_down == 'up':
                    return Command(self.request_paths.CHANGE_VOLUME_PATH, {self.state_helpler.VOLUME_KEY: num})
                elif up_down == 'down':
                    return Command(self.request_paths.CHANGE_VOLUME_PATH, {self.state_helpler.VOLUME_KEY: -num})

            elif kwd == 'frequency':
                num = self.get_number(txt)
                up_down = self.get_up_down(txt)

                if not num and not up_down:
                    return None
                elif not num and up_down:
                    num = 10

                if not up_down:
                    return Command(self.request_paths.SAVE_FREQUENCY_PATH, {self.state_helpler.FREQUENCY_KEY: num})
                elif up_down == 'up':
                    return Command(self.request_paths.CHANGE_FREQUENCY_PATH, {self.state_helpler.FREQUENCY_KEY: num})
                elif up_down == 'down':
                    return Command(self.request_paths.CHANGE_FREQUENCY_PATH, {self.state_helpler.FREQUENCY_KEY: -num})
        return None

    def get_keyword(self, txt):
        for kwd in self.__class__.KEYWORDS:
            if kwd in txt:
                return kwd
        return False

    def get_number(self, txt):
        for word in self.__class__.NUMBER_WORDS:
            if word in txt:
                return self.__class__.NUMBER_WORDS[word]
        match = self.__class__.NUMBER_REGEX.search(txt)
        return match and int(match.group())

    def get_up_down(self, txt):
        match = self.__class__.UP_DOWN_REGEX.search(txt)
        return match and match.group().strip()

    def get_on_off(self, txt):
        match = self.__class__.ON_OFF_REGEX.search(txt)
        return match and match.group().strip()

if __name__ == '__main__':

    class RequestPaths:
        WOOFER_PATH = '/woofer'
        SAVE_POWER_PATH = WOOFER_PATH + '/save_power'
        SAVE_VOLUME_PATH = WOOFER_PATH + '/save_volume'
        SAVE_FREQUENCY_PATH = WOOFER_PATH + '/save_frequency'
        CHANGE_VOLUME_PATH = WOOFER_PATH + '/change_volume'
        CHANGE_FREQUENCY_PATH = WOOFER_PATH + '/change_frequency'

    class StateHelper:
        POWER_KEY = 'power'
        MIN_VOLUME_KEY = 'min_volume'
        VOLUME_KEY = 'volume'
        MAX_VOLUME_KEY = 'max_volume'
        DEFAULT_VOLUME_KEY = 'default_volume'
        MIN_FREQUENCY_KEY = 'min_frequency'
        FREQUENCY_KEY = 'frequency'
        MAX_FREQUENCY_KEY = 'max_frequency'
        DEFAULT_FREQUENCY_KEY = 'default_frequency'

    ci = CommandInterpreter(RequestPaths, StateHelper)
    print(ci.get_number('lkjasdf ljsadlj 567 asdflj 56'))
    print(ci.get_number('lkj zero ljsadlj 567 asdflj 56'))
    print(ci.get_number('lkj foo bar'))
    print(ci.get_up_down('frequency down 10'))
    print(ci.get_on_off('power on'))
    c = ci.interpret_command('volume down nine')
    print(c.path)
    print(c.payload)