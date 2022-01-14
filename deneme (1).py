from ast import Str
import sys, pygame, time, random
pygame.init()
pygame.font.init()


class Game_Launcher:
    CAR_IMAGE = pygame.image.load("greencar.png")
    COIN_IMAGE = pygame.image.load("coin.png")
    HOLE_IMAGE = pygame.image.load("hole.png")
    size = width, height = 1000, 780
    screen = pygame.display.set_mode(size)
    background = pygame.transform.scale(pygame.image.load("asphalt.jpg"), size)

    posx_list = [75,275,475,675]
    lane_posx_list = [75,275,475,675]
    list = [1, 2, 3, 4]

    CAR = []
    STRIPS = []
    OBJECTS = []
    

    def __init__(self, value):
        self._bool = value

    def create_objects(self):
        car = Car(450, 450)
        Game_Launcher.CAR.append(car)
        strip1 = Strip(195, 0, 1, Game_Launcher.screen)
        strip2 = Strip(395, 0, 1, Game_Launcher.screen)
        strip3 = Strip(595, 0, 1, Game_Launcher.screen)
        strip_4 = Strip(195,260, 1, Game_Launcher.screen)
        strip_5 = Strip(395,260, 1, Game_Launcher.screen)
        strip_6 = Strip(595,260, 1, Game_Launcher.screen)
        strip_7 = Strip(195,520, 1, Game_Launcher.screen)
        strip_8 = Strip(395,520, 1, Game_Launcher.screen)
        strip_9 = Strip(595,520, 1, Game_Launcher.screen)
        Game_Launcher.STRIPS.extend([strip1, strip2, strip3, strip_4, strip_5, strip_6, strip_7, strip_8, strip_9])
        coin = Coin(0, Game_Launcher.COIN_IMAGE, Game_Launcher.list, 1, Game_Launcher.screen)
        Game_Launcher.OBJECTS.append(coin)


    def working(self):
        self._bool = True

    def not_working(self):
        self._bool = False
        
    def move_car_left(self):
        for car in Game_Launcher.CAR:
            car.move_left()

    def move_car_right(self):
        for car in Game_Launcher.CAR:
            car.move_right()

    def blit_window(self):

        FPS = 60  # shows 60 frames per second
        level = 1
        health = 10
        fuel = 20
        main_font = pygame.font.SysFont("timesnewroman", 30)

        clock = pygame.time.Clock()
        Game_Launcher.screen.blit(Game_Launcher.background, (0,0))
        health_label = main_font.render(f"Health: {health}", 1, (255,255,255))
        fuel_label = main_font.render(f"Fuel: {fuel}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        Game_Launcher.screen.blit(health_label,(10,10))
        Game_Launcher.screen.blit(fuel_label,(680,10))
        Game_Launcher.screen.blit(level_label,(350,10))

        for car in Game_Launcher.CAR:
            car.show(Game_Launcher.screen, pygame.transform.smoothscale(Game_Launcher.CAR_IMAGE, (100,200)))
        for item in Game_Launcher.STRIPS:
            item.show()
            item.move()
        for object in Game_Launcher.OBJECTS:
            object.move()
            object.show()
        pygame.display.update()


class Car:
    def __init__(self, x, y, health =100):
        self._posx = x
        self._posy = y
        self._health = health
        self._image = None
        self._sized_image = None
        self._lane = 3

    def show(self, screen,  image):
        screen.blit(image, (self._posx, self._posy))

    def give_posx(self):
        return self._posx

    def move_left(self):
        if self._posx -200 > 0:
            self._posx -= 200
            self._lane -= 1
        else:
            pass
        return self._posx
    
    def move_right(self):
        if self._posx + 200 < 800:
            self._posx += 200
            self._lane += 1
        else:
            pass

class Strip:
    def __init__(self, x, y, speed, screen):
        self._posx = x
        self._posy = y
        self._speedy = speed
        self._screen = screen

    def show(self):
        pygame.draw.rect(self._screen, (255,255,255), (self._posx, self._posy,10,50))

    def move(self):
        self._posy += self._speedy
        if self._posy == 780:
            self._posy = 0

class Objects:
    def __init__(self, y, image, list, speed, screen):
        self._posy = y
        self._image = image
        self._scaled = pygame.transform.smoothscale(self._image, (50,50))
        self._screen = screen
        self._possible_posx = [75,275,475,675]
        self._lane_list = list
        self._speedy = speed

    def move(self):
        self._posy += self._speedy
        if self._posy == 780:
            self._posy = 0

    #def select_lane(self):
     #   self._lane = self._possible_posx.index(self._posx) + 1

    #def change_lane(self, list):
    #    self._posx = list[0]

    def show(self):
        self._screen.blit(self._scaled, (self._posx, self._posy))

    def hide_self(self):   # objects will disappear when car hits them
        pass

class Coin(Objects):
    def __init__(self, y, image, list, speed, screen):
        super().__init__(y, image, list, speed, screen)
        self._posx = self._lane_list[0]
        #self.select_lane()

    def change_lane(self, list):
        self._posx = list[0]

playing = Game_Launcher(False)

while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                playing.create_objects()
                playing.working()

            if event.key == pygame.K_a:
                playing.move_car_left()

            if event.key == pygame.K_d:
                playing.move_car_right()

    if playing._bool:  
        playing.blit_window()

    pygame.display.update()
