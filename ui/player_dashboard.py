import os
import pygame

class PlayerPanel:
    PANEL_COLOR = (32, 38, 46)
    TEXT = (235, 235, 235)
    MUTED = (155, 165, 175)

    def __init__(self):
        self.asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        self.font = pygame.font.Font(None, 30)
        self.small = pygame.font.Font(None, 22)

    def get_image(self, piece_type, color):
        prefix = "b" if color == "black" else "w"
        image = pygame.image.load(os.path.join(self.asset_dir, f"{prefix}-{piece_type}.png")).convert_alpha()
        scale = min(.07, 42/max(image.get_width(), image.get_height()))
        return pygame.transform.smoothscale(image, (int(image.get_width()*scale), int(image.get_height()*scale)))

    def draw(self, screen, captured_black, captured_white, black_time=None, white_time=None, turn=None, dt=0):
        w,h=screen.get_size()
        left=pygame.Rect(0,0,250,h); right=pygame.Rect(w-250,0,250,h)
        pygame.draw.rect(screen,self.PANEL_COLOR,left); pygame.draw.rect(screen,self.PANEL_COLOR,right)
        self._player(screen,left,"BLACK",captured_white,black_time,turn=="black")
        self._player(screen,right,"WHITE",captured_black,white_time,turn=="white")

    def _player(self,screen,panel,name,captured,time_left,active):
        y=35
        label=self.font.render(name,True,self.TEXT)
        screen.blit(label,label.get_rect(centerx=panel.centerx,top=y)); y+=45
        status="YOUR TURN" if active else "WAITING"
        screen.blit(self.small.render(status,True,self.TEXT if active else self.MUTED),
                    (panel.left+25,y)); y+=35
        if time_left is not None:
            mins=int(time_left//60); secs=int(time_left%60)
            timer=self.font.render(f"{mins:02d}:{secs:02d}",True,self.TEXT)
            screen.blit(timer,timer.get_rect(centerx=panel.centerx,top=y)); y+=50
        screen.blit(self.small.render("Captured",True,self.MUTED),(panel.left+25,y)); y+=28
        for i,(ptype,_) in enumerate(captured):
            image=self.get_image(ptype,"black" if name=="WHITE" else "white")
            x=panel.left+20+(i%4)*48; yy=y+(i//4)*48
            screen.blit(image,image.get_rect(center=(x+20,yy+20)))
