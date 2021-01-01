import pyaudio
import wave
import logging
import audioop
import speech_recognition as sr

logging.basicConfig(level=logging.INFO, format='(%(threadName)-9s) %(message)s')

class MicPhraseGrabber:

    FORMAT = pyaudio.paInt16
    WIDTH = pyaudio.get_sample_size(FORMAT)
    CHANNELS = 1
    RATE = 44100
    CHUNK = 512
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "recordedFile.wav"
    DEVICE_INDEX = 1

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.cls = self.__class__

    def get_audio_data(self):
        stream = self.audio.open(
            format=self.cls.FORMAT,
            channels=self.cls.CHANNELS,
            rate=self.cls.RATE,
            input_device_index = self.cls.DEVICE_INDEX,
            frames_per_buffer=self.cls.CHUNK,
            input=True,

        )

        logging.debug(f'Width: {self.cls.WIDTH}')
        recorded_frames = []
        last_quiet_frames = []
        first_loud_frames = []
        while(True):
            for i in range(20):
                data = stream.read(self.cls.CHUNK, exception_on_overflow=False)
                recorded_frames.append(data)

            energy = audioop.rms(b''.join(recorded_frames), self.cls.WIDTH)
            logging.debug(energy)
            if energy < 300:
                last_quiet_frames = recorded_frames
            else:
                first_loud_frames = recorded_frames
                recorded_frames = []
                break
            recorded_frames = []

        logging.info('grabbing phrase')

        for i in range(200):
            data = stream.read(self.cls.CHUNK, exception_on_overflow=False)
            recorded_frames.append(data)

        stream.stop_stream()
        stream.close()

        all_frames = last_quiet_frames + first_loud_frames + recorded_frames
        data = b''.join(all_frames)
        return data

    def write_wav_file(self, data):
        waveFile = wave.open(self.cls.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.cls.CHANNELS)
        waveFile.setsampwidth(self.cls.WIDTH)
        waveFile.setframerate(self.cls.RATE)
        waveFile.writeframes(data)
        waveFile.close()



class AudioTranscriber:

    @classmethod
    def get_transcript(cls, wave_file):
        r = sr.Recognizer()
        with sr.WavFile(wave_file) as source:
            audio = r.record(source)

        logging.debug('processing...')
        response = Response(success=False)
        try:
            response.transcript =  r.recognize_google(audio)
            response.success = True
        except sr.RequestError as err:
            response.error = 'Api not available'
        except sr.UnknownValueError as err:
            response.error = 'Unrecognized speech'
        return response


class Response():

    def __init__(
            self,
            success=None,
            error=None,
            transcript=None,
    ):
        self.success = success
        self.error = error
        self.transcript = transcript


if __name__ == '__main__':
    pg = MicPhraseGrabber()
    while True:
        data = pg.get_audio_data()
        pg.write_wav_file(data)
        resp = AudioTranscriber.get_transcript(MicPhraseGrabber.WAVE_OUTPUT_FILENAME)
        if resp.success:
            txt = resp.transcript
            logging.info('\033[92m' + txt + '\033[0m')
            # self.callback and self.callback(txt)
            # command = CI.interpret_command(resp['transcript'])
            # command and logging.debug(command)
        else:
            logging.error(resp.error)

