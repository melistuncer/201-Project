from os import replace, spawnl
import random
import sys, pygame
from pygame.event import get
from pygame.time import Clock, get_ticks
from pygame.transform import scale
import time
from pygame import mixer
pygame.init()
random.seed()
clock = pygame.time.Clock

black = 0, 0, 0
white = 255, 255, 255
size = width, height = 1000, 780
screen = pygame.display.set_mode(size)
mixer.music.load("backgroundMusic.mp3")
mixer.music.play(-1)
speed = 1

posx_list = [75,275,475,675]
lane_posx_list = [75,275,475,675]
list = []

def random_picker():
    while len(list) < 4:
        item = random.choice(posx_list)
        list.append(item)
        posx_list.remove(item)
    return list

random_picker()

class Game_Launcher:

    def __init__(self, value):
        self._bool = value
    
    def game_working(self):
        screen.fill(black)
        for i in my_strips:
            i.move()
            i.show()
        for i in game_objects:
            i.move()
            i.show()
        tree.lose_health()
        hole.lose_health()
        coin.get_score()
        health.show()
        score.show()
        gas.lose_fuel()
        fuel.full()
        gas.show()
        if coin._posy < 780 and coin._posy > 774:
            posx_list.append(75)
            posx_list.append(275)
            posx_list.append(475)
            posx_list.append(675)
            list.clear()
            random_picker()
            coin._posx = list[0]
            fuel._posx = list[1]
            tree._posx = list[2]
            hole._posx = list[3]
            coin.selectlane()
            fuel.selectlane()
            tree.selectlane()
            hole.selectlane()
            
class Grass():
    def __init__(self):
        self._image = pygame.image.load("grass.jpeg")
        self._sized = pygame.transform.smoothscale(self._image, (200,1560))
        self._screen = screen
        self._posx = 800
        self._posy = -780
        self._speedy= speed
    
    def show(self):
        screen.blit(self._sized, (self._posx, self._posy))
    
    def move(self):
        self._posy += self._speedy
        if self._posy == 0:
            self._posy = -780

class Strip():
    def __init__(self, posx, posy):
        self._screen = screen
        self._posx = posx
        self._posy = posy
        self._speedy = speed
        self.show()
        self.move()
           
    def show(self):
        pygame.draw.rect(self._screen, (255,255,255), (self._posx, self._posy,10,50))
    
    def move(self):
        self._posy += self._speedy
        if self._posy == 780:
            self._posy = 0

class Car():
    def __init__(self, posx, posy):
        self._image = pygame.image.load("car.png")
        self._sized = pygame.transform.smoothscale(self._image, (100,200))
        self._screen = screen
        self._posy = posy
        self._posx = posx
        self.show()
        self._state = 'straight'
        self.move()
        self._lane = 3

    def show(self):
        screen.blit(self._sized, (self._posx, self._posy))

    def move(self):
        if self._state == 'right':
            self._posx += 200
        elif self._state == 'left':
            self._posx -= 200
    
class Health():
    def __init__(self):
        self._image = pygame.image.load("heart1.png")
        self._sized = pygame.transform.smoothscale(self._image, (50,50))
        self._amount = 3
    
    def show(self):
        if self._amount == 3:
            screen.blit(self._sized, (800, 100))
            screen.blit(self._sized, (860, 100))
            screen.blit(self._sized, (920, 100))
        elif self._amount == 2:
            screen.blit(self._sized, (800, 100))
            screen.blit(self._sized, (860, 100))
        elif self._amount == 1:
            screen.blit(self._sized, (800, 100))

class Score():
    def __init__(self):
        self._posx = 100
        self._posy = 100
        self._score = 0

    def show(self):
        font = pygame.font.Font('freesansbold.ttf', 32)
        score = str(self._score)
        text = font.render(score, True, white)
        screen.blit(text, (900, 50))

class Gas():
    def __init__(self):
        self._posx = 100
        self._posy = 100
        self._amount = 100

    def show(self):
        font = pygame.font.Font('freesansbold.ttf', 22)
        fuel_left = str("%.2f" % self._amount)
        text1 = font.render("Remaining fuel: ", True, white)
        text = font.render(fuel_left, True, white)
        screen.blit(text1, (810, 700))
        screen.blit(text, (870, 740))

    def lose_fuel(self):
        self._amount -= (100) * (start - finish)

class Objects():
    def __init__(self):
        self._screen = screen
        self._posy = 0
        self._speedy = speed
        self._possible_posx = [75,275,475,675]
        self._list = list

    def move(self):
        self._posy += self._speedy
        if self._posy == 780:
            self._posy = 0
    
    def selectlane(self):
        self._lane = self._possible_posx.index(self._posx) + 1

class Coin(Objects):
    def __init__(self):
        super().__init__()
        self._image = pygame.image.load("coin.png")
        self._scaled = pygame.transform.smoothscale(self._image, (50,50))
        self._posx = self._list[0]
        self.selectlane()
    
    def show(self):
        screen.blit(self._scaled, (self._posx, self._posy))

    def get_score(self):
        if self._posy == car._posy:
            if car._lane == self._lane:
                score._score += 1

class Fuel(Objects):
    def __init__(self):
        super().__init__()
        self._image = pygame.image.load("fuel.png")
        self._scaled = pygame.transform.smoothscale(self._image, (50,50))
        self._posx = self._list[1]
        self.selectlane()

    def show(self):
        screen.blit(self._scaled, (self._posx, self._posy))

    def full(self):
        if self._posy == car._posy:
            if car._lane == self._lane:
                gas._amount = 100

class Obstacles(Objects):
    def __init__(self):
        super().__init__()
    
    def lose_health(self):
        if self._posy == car._posy:
            if car._lane == self._lane:
                health._amount -= 1
        
class Tree(Obstacles):
    def __init__(self):
        super().__init__()
        self._image = pygame.image.load("tree.png")
        self._scaled = pygame.transform.smoothscale(self._image, (50,50))
        self._posx = self._list[2]
        self.selectlane()

    def show(self):
        screen.blit(self._scaled, (self._posx, self._posy))

class Hole(Obstacles):
    def __init__(self):
        super().__init__()
        self._image = pygame.image.load("hole.png")
        self._scaled = pygame.transform.smoothscale(self._image, (50,50))
        self._posx = self._list[3]
        self.selectlane()

    def show(self):
        screen.blit(self._scaled, (self._posx, self._posy))
    
#road cars
strip_1 = Strip(195,0)
strip_2 = Strip(395,0)
strip_3 = Strip(595,0)
strip_4 = Strip(195,260)
strip_5 = Strip(395,260)
strip_6 = Strip(595,260)
strip_7 = Strip(195,520)
strip_8 = Strip(395,520)
strip_9 = Strip(595,520)
my_strips = [strip_1, strip_2, strip_3, strip_4, strip_5, strip_6, strip_7, strip_8, strip_9]
#car
car = Car(450, 450)
health = Health()
score = Score()
gas = Gas()
#interrection
coin = Coin()
fuel = Fuel()
hole = Hole()
tree = Tree()
#decorations
grass = Grass()
game_objects = [grass, car, fuel, coin, tree, hole]
playing = Game_Launcher(False)

def lose_game():
    pygame.draw.rect(screen, white, (500,500,300,300))
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render("u suck", True, white)
    screen.blit(text, (150, 150))


while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                playing._bool = True

            if event.key == pygame.K_a:
                if car._posx -200 > 0:
                    car._posx -= 200
                    car._lane -= 1
                else:
                    pass

            if event.key == pygame.K_d:
                if car._posx + 200 < 800:
                    car._posx += 200
                    car._lane += 1
                else:
                    pass

    if health._amount == 0:
        lose_game()
        playing._bool = False
    
    if gas._amount <= 0:
        lose_game()
        playing._bool = False

    start = time.time()
    if playing._bool:  
        playing.game_working()
    finish = time.time()

    pygame.display.update()