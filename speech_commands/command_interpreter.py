import re

class Command:
    def __init__(self, path, payload):
        self.path = path
        self.payload = payload

class CommandInterpreter:
    TRIGGER_WORDS = [
        'bandsaw',
        'band saw',
        'bandsaw fence',
        'band saw fence',
    ]

    KEYWORDS = []

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

    UNITS_NORMALIZE = {
        'millimeter': 'mm',
        'centimeter': 'cm',
        'meter': 'm',
        'inch': 'in',
        'feet': 'ft',
    }

    UNITS_REGEX = re.compile(r'\binch|\bin\b|\bfeet\b|\bft\b|\bmm\b|\bmillimeter|\bcm\b|\bcentimeter|\bm\b|\bmeter')
    NUMBER_REGEX = re.compile(r'\d*\.?\d+')
    SMALLER_BIGGER_REGEX = re.compile(r'\bsmaller\b|\bbigger\b')

    def __init__(self, request_paths, state_helper):
        self.request_paths = request_paths
        self.state_helpler = state_helper

    def preprocess(self, txt):
        txt = txt.lower()
        txt = self.separate_text_stuck_to_number(txt)
        return txt

    # makes '34.5in' into '34.5 in'
    def separate_text_stuck_to_number(self, txt):
        ex = re.compile(r'[0-9][a-z]')
        match = ex.search(txt)
        if match:
            txt = txt[:match.span()[0]+1] + ' ' + txt[match.span()[0]+1:]
        return txt


    def interpret_command(self, txt):
        txt = self.preprocess(txt)

        if not self.get_trigger_word(txt):
            return None

        num = self.get_number(txt)
        in_out = self.get_smaller_bigger(txt)

        if not num and not in_out:
            return None
        elif not num and in_out:
            num = .25

        if not in_out:
            return Command(self.request_paths.SAVE_POSTION_PATH, {self.state_helpler.POSITION_KEY: num})
        elif in_out == 'bigger':
            return Command(self.request_paths.CHANGE_POSITION_PATH, {self.state_helpler.POSITION_KEY: num})
        elif in_out == 'smaller':
            return Command(self.request_paths.CHANGE_POSITION_PATH, {self.state_helpler.POSITION_KEY: -num})
        return None

    def get_trigger_word(self, txt):
        for kwd in self.__class__.TRIGGER_WORDS:
            if kwd in txt:
                return kwd
        return False

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

        return match and float(match.group())

    def get_smaller_bigger(self, txt):
        match = self.__class__.SMALLER_BIGGER_REGEX.search(txt)
        return match and match.group().strip()

    def get_units(self, txt):
        match = self.__class__.UNITS_REGEX.search(txt)
        return match and self.normalize_units(match.group().strip())

    def normalize_units(self, units):
        if units in self.__class__.UNITS_NORMALIZE:
            return self.__class__.UNITS_NORMALIZE[units]
        else:
            return units

if __name__ == '__main__':

    class RequestPaths:
        FENCE_PATH = '/fence'
        SAVE_POSITION_PATH = FENCE_PATH + '/save_position'
        CHANGE_POSITION_PATH = FENCE_PATH + '/change_position'

    class StateHelper:
        POSITION_KEY = 'position'

    ci = CommandInterpreter(RequestPaths, StateHelper)
    print(ci.get_number('lkjasdf ljsadlj 5.67 asdflj 56'))
    print(ci.get_number('four ljsadlj 5.67 asdflj 56'))
    print(ci.get_number('lkj 0.567 asdflj 56'))
    print(ci.get_number('lkj 567 asdflj 56'))
    print(ci.get_number('lkj .567 asdflj 56'))
    print(ci.get_number('lkj foo bar'))

    print(ci.get_smaller_bigger('blah blah smaller 10'))
    print(ci.get_smaller_bigger('blah blah bigger 1.0'))

    print(ci.separate_text_stuck_to_number('asd 1.0ab'))
    print(ci.preprocess('aSD 1.0Rb'))

    print(ci.get_units('band saw out 3.4in'))
    print(ci.get_units('band saw out 3.4 inches'))
    print(ci.get_units('band saw out 3.4 m'))
    print(ci.get_units('band saw out 3.4 meters'))
    print(ci.get_units('band saw out 3.4 mm'))
    print(ci.get_units('band saw out 3.4 millimeters'))
    print(ci.get_units('band saw out 3.4 cm'))
    print(ci.get_units('band saw out 3.4 centimeters'))
    print(ci.get_units('band saw out 3.4 feet'))



    # print(ci.get_on_off('power on'))
    # c = ci.interpret_command('volume down nine')
    # print(c.path)
    # print(c.payload)