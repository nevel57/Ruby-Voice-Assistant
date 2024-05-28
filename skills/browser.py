import webbrowser


def openYandex():
    webbrowser.open('https://ya.ru/', new=2)


def openRequest(req):
    webbrowser.open('https://yandex.ru/search/?text=' + req, new=2)

