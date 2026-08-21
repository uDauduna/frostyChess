import pygame

class PlayerPanel:
    def __init__(self):
        self.pieces_captured_by_black = []
        self.pieces_captured_by_white = []
        self.hourglass_frames = []
        self.hourglass_frame_count = 15
        self.white_hourglass_frame = 0
        self.black_hourglass_frame = 0
        self.white_hourglass_time = 0
        self.black_hourglass_time = 0
        self.hourglass_speed = 0.08
        self.load_hourglass()
        self.PANEL_COLOR = (190, 220, 204)

    def black_pieces(self, piece):
        self.pieces_captured_by_black.append(piece)

    def white_pieces(self, piece):
        self.pieces_captured_by_white.append(piece)

    def get_image(self, piece_type, color):
        prefix = "b" if color == "black" else "w"
        path = f"./assets/{prefix}-{piece_type}.png"
        image = pygame.image.load(path).convert_alpha()
        width = int(image.get_width() * 0.125)
        height = int(image.get_height() * 0.125)
        return pygame.transform.scale(image,(width, height),)

    def load_hourglass(self):
        sheet = pygame.image.load("./assets/hourglass.png").convert_alpha()
        frame_width = sheet.get_width() // self.hourglass_frame_count
        frame_height = sheet.get_height()
        for index in range(self.hourglass_frame_count):
            frame = sheet.subsurface((index * frame_width,0,frame_width,frame_height)).copy()
            width = int(frame.get_width() * 0.5)
            height = int(frame.get_height() * 0.5)
            frame = pygame.transform.scale(frame,(width,height))
            self.hourglass_frames.append(frame)

    def update_hourglass(self, color, active, dt):
        if not active:
            return
        if color == "white":
            self.white_hourglass_time += dt
            if self.white_hourglass_time >= self.hourglass_speed:
                self.white_hourglass_time = 0
                self.white_hourglass_frame = (self.white_hourglass_frame + 1) % len(self.hourglass_frames)
        else:
            self.black_hourglass_time += dt
            if self.black_hourglass_time >= self.hourglass_speed:
                self.black_hourglass_time = 0
                self.black_hourglass_frame = (self.black_hourglass_frame + 1) % len(self.hourglass_frames)

    def draw_hourglass(self, screen, panel, color, active):
        if len(self.hourglass_frames) == 0:
            return
        if color == "white":
            image = self.hourglass_frames[self.white_hourglass_frame]
        else:
            image = self.hourglass_frames[self.black_hourglass_frame]
        image = image.copy()
        rect = image.get_rect()
        rect.centerx = panel.centerx
        rect.bottom = screen.get_height() - 120
        if not active:
            image.set_alpha(100)
        else:
            image.set_alpha(255)
        screen.blit(image,rect)

    def draw_captured_pieces(self, screen,pieces_captured_by_black, pieces_captured_by_white):
        black_panel = pygame.Rect(0,0,250,screen.get_height())
        white_panel = pygame.Rect(screen.get_width() - 250,0,250,screen.get_height())
        pygame.draw.rect(screen,self.PANEL_COLOR,black_panel)
        pygame.draw.rect(screen,self.PANEL_COLOR,white_panel)
        self.draw_spoil_header(screen,white_panel,"white")
        self.draw_spoil_header(screen,black_panel,"black")
        self.draw_piece_list(screen,pieces_captured_by_white,white_panel,"black")
        self.draw_piece_list(screen,pieces_captured_by_black,black_panel,"white")

    def draw_spoil_header(self, screen, panel, color):
        king = self.get_image("king",color)
        king_rect = king.get_rect()
        king_rect.centerx = panel.centerx
        king_rect.top = 15
        screen.blit(king,king_rect)
        font = pygame.font.Font(None,32)
        title = font.render(f"{color.capitalize()}'s Spoil",True,(255,255,255))
        title_rect = title.get_rect()
        title_rect.centerx = panel.centerx
        title_rect.top = king_rect.bottom + 5
        screen.blit(title,title_rect)

    def draw_piece_list(self, screen, pieces, panel, color):
        x = panel.left + 20
        y = 90
        spacing = 45
        for index, piece in enumerate(pieces):
            piece_type = piece[0]
            image = self.get_image(piece_type,color)
            rect = image.get_rect()
            rect.topleft = (x + (index % 4) * spacing,y + (index // 4) * spacing)
            screen.blit(image,rect)

    def draw_timer(self, screen, panel, time_left, active):
        font = pygame.font.Font(None,48)
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        text = f"{minutes:02d}:{seconds:02d}"
        if active:
            timer = font.render(text,True,(255,255,255))
        else:
            timer = font.render(text,True,(150,150,150))
        rect = timer.get_rect()
        rect.centerx = panel.centerx
        rect.bottom = screen.get_height() - 70
        screen.blit(timer,rect)

    def draw_turn(self, screen, panel, color):
        font = pygame.font.Font(None,30)
        if color == "black":
            text = "Black's Turn"
        else:
            text = "White's Turn"
        turn = font.render(text,True,(255,255,255))
        rect = turn.get_rect()
        rect.centerx = panel.centerx
        rect.bottom = screen.get_height() - 30
        screen.blit(turn,rect)

    def draw(self,screen, pieces_captured_by_black, pieces_captured_by_white,black_time=None, white_time=None, turn=None, dt=0):
        self.draw_captured_pieces(screen, pieces_captured_by_black, pieces_captured_by_white)
        black_panel = pygame.Rect(0,0,250,screen.get_height())
        white_panel = pygame.Rect(screen.get_width() - 250,0,250,screen.get_height())
        self.update_hourglass("black",turn == "black",dt)
        self.update_hourglass("white",turn == "white",dt)
        self.draw_hourglass(screen,black_panel,"black",turn == "black")
        self.draw_hourglass(screen,white_panel,"white",turn == "white")
        if black_time is not None:
            self.draw_timer(screen,black_panel,black_time,turn == "black")
        if white_time is not None:
            self.draw_timer(screen,white_panel,white_time,turn == "white")
        if turn is not None:
            if turn == "black":
                self.draw_turn(screen,black_panel,"black")
            else:
                self.draw_turn(screen,white_panel,"white")
    