import pygame,os,pathlib,json
from assets.managers import common,constants
pygame.mixer.init()
#common.SoundLibrary.update({"test": pygame.mixer.music.load(os.path.join("assets","sounds","music","test.wav"))})
class Music():
    def __init__(self,filename,data):
        self.filename = os.path.join("assets","sounds","music",filename+".wav")
        self.levels = data.get("levels",())
        self.volume = data.get("volume",1)
    def play_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout()
            pygame.mixer.music.queue(self.filename)
        else:
            pygame.mixer.music.load(self.filename)
            pygame.mixer.music.play()
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.set_endevent(constants.MUSIC_END_EVENT)
    def stop_music():
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
music_files = os.listdir(os.path.join("assets","sounds","music"))
for i in music_files:
    item = pathlib.Path("assets","sounds","music",i)
    if item.suffix == ".wav":
        item2 = pathlib.Path("assets","sounds","music",item.stem+".json")
        if item2.exists():
            common.MusicLibrary.update({item.stem:Music(item.stem,json.loads(item2.read_text()))})