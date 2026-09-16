import pygame
from .base_screen import BaseScreen
from ui.components import Button

class GameSetup(BaseScreen):
    def __init__(self, screen, screen_manager):
        super().__init__(screen); self.screen_manager=screen_manager
        self.width=screen.get_width(); self.height=screen.get_height()
        self.title_font=pygame.font.Font(None,70); self.font=pygame.font.Font(None,32)
        self.selected_color="white"; self.selected_difficulty="medium"; self.selected_mode="casual"
        self.create_buttons()

    def create_buttons(self):
        cx=self.width//2
        self.white_button=Button((cx-260,190,220,55),"WHITE",self.font,lambda:self.select_color("white"))
        self.black_button=Button((cx+40,190,220,55),"BLACK",self.font,lambda:self.select_color("black"))
        self.easy_button=Button((cx-330,315,200,55),"EASY",self.font,lambda:self.select_difficulty("easy"))
        self.medium_button=Button((cx-100,315,200,55),"MEDIUM",self.font,lambda:self.select_difficulty("medium"))
        self.hard_button=Button((cx+130,315,200,55),"HARD",self.font,lambda:self.select_difficulty("hard"))
        self.casual_button=Button((cx-230,440,210,55),"CASUAL",self.font,lambda:self.select_mode("casual"))
        self.competitive_button=Button((cx+20,440,210,55),"COMPETITIVE",self.font,lambda:self.select_mode("competitive"))
        self.start_button=Button((cx-150,550,300,60),"START GAME",self.font,self.start_game)
        self.back_button=Button((cx-100,625,200,45),"BACK",self.font,self.go_back)
        self.buttons=[self.white_button,self.black_button,self.easy_button,self.medium_button,self.hard_button,
                      self.casual_button,self.competitive_button,self.start_button,self.back_button]

    def select_color(self,v): 
        self.selected_color=v

    def select_difficulty(self,v): 
        self.selected_difficulty=v

    def select_mode(self,v): 
        self.selected_mode=v

    def start_game(self): 
        self.screen_manager.start_game(self.selected_color,self.selected_difficulty,self.selected_mode)


    def go_back(self): 
        self.screen_manager.show_main_menu()


    def handle_event(self,event):
        for b in self.buttons: 
            b.handle_event(event)

    def update(self): 
        pass

    def draw(self):
        self.screen.fill((24,29,35))
        title=self.title_font.render("NEW GAME",True,(240,240,240))
        self.screen.blit(title,title.get_rect(center=(self.width//2,80)))
        for text,y in [("COLOR",150),("DIFFICULTY",275),("MODE",400)]:
            t=self.font.render(text,True,(190,200,210)); self.screen.blit(t,t.get_rect(center=(self.width//2,y)))
        for b in self.buttons: b.draw(self.screen)
