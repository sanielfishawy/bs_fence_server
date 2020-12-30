import speech_recognition as sr
import platform

class MicrophoneHelper:

    # USB phone conference mic
    I_TALK_MIC = 'iTalk'
    # USB mic that is like a small dongle
    USB_BUTTON_MIC = 'USB PnP Sound Device'
    MAC_BUILT_IN_MIC = 'Built-in Microphone'
    PULSE_AUDIO = 'pulse'

    @classmethod
    def get_microphone_index(cls, mic=None):
        if not mic:
            return 0
        else:
            return cls.index_of_string_in_array_of_strings(mic, cls.get_microphone_names())

    @staticmethod
    def index_of_string_in_array_of_strings(string, arr):
        for idx, name in enumerate(arr):
            if name.find(string) >= 0:
                return idx
        return 0

    @classmethod
    def get_microphone_name_with_index(cls, idx):
        return cls.get_microphone_names()[idx]

    @staticmethod
    def is_pi():
        return platform.system().lower() == 'linux'

    @staticmethod
    def is_mac():
        return platform.system().lower() == 'darwin'

    @staticmethod
    def get_microphone_names():
        return sr.Microphone.list_microphone_names()

if __name__ == '__main__':
    m = MicrophoneHelper
    print(m.get_microphone_names())
    print(m.get_microphone_index(mic=m.USB_BUTTON_MIC))
    print(m.get_microphone_index(mic=m.I_TALK_MIC))