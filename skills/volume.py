from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# Библиотека для управления микшером Windows определенных приложений
sessions = AudioUtilities.GetAllSessions()
for session in sessions:
    volume_object = session._ctl.QueryInterface(ISimpleAudioVolume)
    if session.Process and session.Process.name() == "Y.Music.exe":
        print(volume_object.GetMasterVolume())


def set_volume(application_name, volume):
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        volume_object = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == application_name:
            volume_object.SetMasterVolume(max(0, min(volume_object.GetMasterVolume() + volume, 1)), None)
