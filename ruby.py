from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from voice.voice import speaker
from words.words import TRG_VOL, TRIGGERS, NUMS, data_set, OTHER_TRG
from skills import *

vectorizer = CountVectorizer()
clf = LogisticRegression()
vect = vectorizer.fit_transform(list(data_set.keys()))
clff = clf.fit(vect, list(data_set.values()))


def vector_data(data):
    text_vector = vectorizer.transform([data]).toarray()[0]
    answer = clf.predict([text_vector])[0]
    return answer


def fname(data):
    fn = vector_data(data).split()[0]
    return fn


def speak_answer(data):
    speaker(vector_data(data).replace(fname(data), ''))


class Ruby:
    def __init__(self, data):
        self.name = False
        self.trggs = False
        self.flag_fol = False
        self.request = data
        self.data = data

    def name_tag(self):
        if not list(TRIGGERS.intersection(self.request.split())):
            return self.name
        else:
            self.name = True
            return self.name

    def trggs_tag(self):
        if not (list(TRG_VOL.intersection(self.request.split())) or list(OTHER_TRG.intersection(self.request.split()))):
            return self.trggs
        else:
            self.trggs = True
            return self.trggs

    def delete_name(self):
        if self.name_tag() is True:
            self.request = self.request.replace(self.request.split()[0], '')[1:]
            return self.request
        else:
            return self.request

    def delete_trggs(self):
        if self.trggs_tag():
            if sum(list(map(lambda x: x in self.request, TRG_VOL))) == 3:
                self.flag_fol = True
                self.request = list(set(self.request.split()).difference(TRG_VOL))
                return self.request
            else:
                self.request = list(set(self.request.split()).difference(OTHER_TRG))
                return self.request
        else:
            pass

    def task(self):
        if self.name_tag() is True:
            if self.trggs_tag() is True:
                self.delete_name()
                self.delete_trggs()
                if self.flag_fol is True:
                    return self.request
                else:
                    return ' '.join(self.data.split(' ')[2::])
            else:
                self.delete_name()
                return self.request

    def running_task(self):
        print(self.data)
        if self.name_tag() is True:
            if self.trggs_tag() is True:
                speak_answer(self.data)
                if self.flag_fol is True:
                    exec(str(fname(self.data)).split('.')[1] + '(' + f'{NUMS[self.task()[0]]}' + ')')
                else:
                    exec(str(fname(self.data)).split('.')[1] + '(' + "\'" + self.task() + "\'" + ')')
            else:
                speak_answer(self.data)
                exec(str(fname(self.data)) + '()')



