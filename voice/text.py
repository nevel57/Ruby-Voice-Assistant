from words import words
from words.words import TRG_VOL, NUMS


import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 240)  # скорость речи


def speaker(text):
    '''Озвучка текста'''
    engine.say(text)
    engine.runAndWait()


class Request:

    def __init__(self, data):
        self.name = False
        self.trgs = False
        self.text = data

    def name_tag(self):
        if not list(words.TRIGGERS.intersection(self.text.split())):
            return self.name
        else:
            self.name = True
            return self.name

    def delete_name(self):
        if self.name_tag() is True:
            self.text = self.text.replace(self.text.split()[0], '')[1:]
            return self.text
        else:
            return self.text

    def trgs_tag(self):
        if not list(words.TRG_VOL.intersection(self.text.split())):
            return self.trgs
        else:
            self.trgs = True
            return self.trgs

    def delete_trgs(self):
        if self.trgs_tag():
            if sum(list(map(lambda x: x in self.text, TRG_VOL))) == 3:
                self.text = list(set(self.text.split()).difference(TRG_VOL))
                return self.text
        else:
            pass

    def trg_answer(self, data, vectorizer, clf):
        val = NUMS[self.text[0]]
        # получаем вектор полученного текста
        # сравниваем с вариантами, получая наиболее подходящий ответ
        text_vector = vectorizer.transform([data]).toarray()[0]
        answer = clf.predict([text_vector])[0]
        # получение имени функции из ответа из data_set
        func_name = answer.split()[0]
        print(func_name)
        # озвучка ответа из модели data_set
        speaker(answer.replace(func_name, ''))
        # запуск функции из skills
        exec('skills.' + func_name + '(' + val + ')')

    def answer_ruby(self, data, vectorizer, clf):
        # получаем вектор полученного текста
        # сравниваем с вариантами, получая наиболее подходящий ответ
        text_vector = vectorizer.transform([data]).toarray()[0]
        answer = clf.predict([text_vector])[0]
        # получение имени функции из ответа из data_set
        func_name = answer.split()[0]
        print(func_name)
        # озвучка ответа из модели data_set
        speaker(answer.replace(func_name, ''))
        # запуск функции из skills
        exec('skills.' + func_name + '()')

    def answer_request(self, vectorizer, clf):
        if self.name_tag() is False:
            pass
        else:
            if self.trgs_tag() is False:
                self.delete_name()
                print(self.text, 1)
                self.answer_ruby(self.text, vectorizer, clf)
            else:
                self.delete_name()
                self.delete_trgs()
                print(self.text, 0)
                self.trg_answer(self.text, vectorizer, clf)

