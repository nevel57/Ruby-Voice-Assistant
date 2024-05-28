
from skills.volume import set_volume

application_name = "Y.Music.exe"  # Имя процесса плеера


def Y_change_volume_up(val):
    set_volume(application_name, val)


def Y_change_volume_down(val):
    set_volume(application_name, -val)


