import json
import queue
import sounddevice as sd
import vosk

from ruby import Ruby
from words import words

q = queue.Queue()  # Создаем очередь

model = vosk.Model('model_small')  # Голосовая модель Vosk с https://alphacephei.com/vosk/models

device = sd.default.device  # Микрофон и динамики поумолчанию
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])


def callback(indata, *args):
    q.put(bytes(indata))  # Добaвляем в очередь полученные данные из samplerate в байтах


def rec_mic():
    del words.data_set  # Очищаем оперативную память от словаря
    # Необработаный входящий поток с микрофона с параметрами:
    # Частота дискридитации микрофона, Кол-во семплов*, микрофон, разряднось data, канал,
    # *семпел -
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0], dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()  # Забираем данные из очереди
            if rec.AcceptWaveform(data):
                data = json.loads(rec.Result())['text']
                ruby = Ruby(data)
                ruby.running_task()
