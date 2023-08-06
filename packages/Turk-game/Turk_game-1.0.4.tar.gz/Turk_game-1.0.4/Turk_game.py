from collections.abc import Callable, Iterable, Mapping
from typing import Any, Optional
import pygame as pg
import threading as th
import keyboard as ky
import sys, os , time , random






pg.init()
pg.font.init()



def rastgele(ilk,son,ondalik = False):
    if ondalik:
        return random.uniform(ilk,son)
    else:
        return random.randint(ilk,son)


class is_parcasi(th.Thread):
    def __init__(self, group: None = None, target: Callable[..., object] | None = None, name: str | None = None, args: Iterable[Any] = ..., kwargs: Mapping[str, Any] | None = None, *, daemon: bool | None = None) -> None:
        super().__init__(group, target, name, args, kwargs, daemon=daemon)



class yazi:
    def __init__(self,text="Made by Turk-game",pixel=1):
        self.yazi = pg.font.Font.render(text=text,antialias=pixel)
    def guncelle(self,text,pixel):
        self.yazi =  pg.font.Font.render(text=text,antialias=pixel)



def Vektor2_yap(konum):
    return pg.Vector2(konum)



def normalize_et(nesne:pg.Vector2):
    return nesne.normalize()



def bekle(sure):
    time.sleep(sure)



def basildi(tus:str):
    return ky.is_pressed(tus)



def carpma_listesi(nesne,diger):

    x = nesne.collidelist(diger)
    if x != -1:
        return 1
    else:    
        return 0



def dikdortgen_carp(nesne,diger):
    
    return pg.Rect.colliderect(nesne,diger)



def ses_yukle(ses):
    pg.mixer.music.load(ses)



def ses_cal():
    pg.mixer.music.play()



def s_duraklat():
    pg.mixer.music.pause()



def s_devam():
    pg.mixer.music.unpause()



def s_durdur():
    pg.mixer.stop()



class dikdortgen():
    def __init__(self,konum:list or pg.Vector2,boyut:list):
        self.rect = pg.rect.Rect(konum,boyut)
    
    def carp(self,diger,carpma_tip):
        return carpma_tip(self.rect,diger)
            
    def guncelle(self,konum:list or pg.Vector2,boyut:list):
        self.rect = pg.rect.Rect(konum,boyut)



class resim():
    def __init__(self,resim,boyut:list):
        self.resim = pg.transform.scale(pg.image.load(resim),boyut)
    def guncelle(self,resim,boyut:list):
        self.resim = pg.transform.scale(pg.image.load(resim),boyut)
        

    
class EKRAN:
    def __init__(self,x:int,y:int,baslik:str,ikon:str):
        if not ikon == "":
            self.ikon = pg.transform.scale(pg.image.load(ikon),(320,320))
            pg.display.set_icon(self.ikon)
        pg.display.set_caption(str(baslik))
        self.___ekran___ = pg.display.set_mode((x,y))
        self.running = True  # running özelliğini tanımla
        #self.dongu(normal_islem,event_islem,kapandi_islem,yenileme_cesidi)

    def yerlestir(self,nesne,konum):
        if type(nesne) == resim:
            self.___ekran___.blit(nesne.resim,konum)
        elif type(nesne) == yazi:
            self.___ekran___.blit(nesne.yazi,konum)
        else:
            self.___ekran___.blit(nesne,konum)

    def ciz(self,nesne:dikdortgen,renk):
        pg.draw.rect(self.___ekran___,renk,nesne.rect)

    def update(self):
        pg.display.update()

    def flip(self):
        pg.display.flip()
        
    def dongu(self,normal_islem,event_islem,kapandi_islem,yenileme_cesidi):
        self.running = True
        while self.running:  # self.running özelliğini kullan
            self.events = pg.event.get()
            for self.event in self.events:
                if self.event.type == pg.QUIT:
                    kapandi_islem()
                    self.running = False

                event_islem()
            
            normal_islem()
            yenileme_cesidi()

        pg.quit()
        sys.exit()