import asyncio
import random
import pygame
from pygame import *
pygame.mixer.init()

plat_colour = (160, 160, 160)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black = (0, 0, 0)

FPS = 40
height = 1000
width = 800

vector = pygame.math.Vector2

class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((width, height))
        self.bg_img1 = pygame.image.load('Images/background.png').convert_alpha()
        self.bg_img2 = pygame.image.load('Images/background.png').convert_alpha()
        pygame.display.set_caption("Globe Hopper")
        self.running = True

    def newgame(self):
        self.bg_y1 = -4267 + height
        self.bg_y2 = -8534 + height
        self.tourist = Tourist(self)
        self.platforms = pygame.sprite.Group()
        self.mosquitos = pygame.sprite.Group()
        self.gamesprites = pygame.sprite.Group()
        self.gamesprites.add(self.tourist)
        platarray = [(0, height - 50, width, 50),
                    (40, height - 200, 200, 30),
                    (300, height - 500, 200, 30),
                    (200, height - 800, 200, 30)]
        for plat in platarray:
            platform = Platform(*plat)
            self.gamesprites.add(platform)
            self.platforms.add(platform)
        pygame.mixer.music.load('Sounds/Ancient Ruins - Loopable.ogg')
        pygame.mixer.music.play(20)
        self.mosquito_timer = 0
    
    def gameloop(self):
        self.playgame = True
        while self.playgame == True:
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()
    
    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playgame = False
                self.running = False
                pygame.quit()

    def update(self):
        self.gamesprites.update()

        now = pygame.time.get_ticks()
        if now - self.mosquito_timer > 5000 + random.choice([-2000, -1500,-1000, -500, 0, 500, 1000]):
            self.mosquito_timer = now
            mosquito = Mosquito(self)
            self.mosquitos.add(mosquito)
            self.gamesprites.add(mosquito)

        mosquito_collision = pygame.sprite.spritecollide(self.tourist, self.mosquitos, False)
        if mosquito_collision:
            self.playgame = False

        if self.tourist.vel.y > 0:
            collide = pygame.sprite.spritecollide(self.tourist, self.platforms, False)
            if collide:
                if self.tourist.coord.y < collide[0].rect.bottom:
                    self.tourist.coord.y = collide[0].rect.top
                    self.tourist.vel.y = 0

        if self.tourist.rect.top <= height * 0.25:
            self.bg_y1 += -0.5 * self.tourist.vel.y  # Increased scroll speed
            self.bg_y2 += -0.5 * self.tourist.vel.y  # Increased scroll speed

            if self.bg_y1 >= height:
                self.bg_y1 = -4267 + height

            if self.bg_y2 >= height:
                self.bg_y2 = -4267 + height

            self.tourist.coord.y += -1 * self.tourist.vel.y
            for platform in self.platforms:
                platform.rect.y += -1 * self.tourist.vel.y
                if platform.rect.top >= height:
                    platform.kill()
                    self.tourist.score += 10
            for mosquito in self.mosquitos:
                mosquito.rect.y += -1 * self.tourist.vel.y

        if self.tourist.rect.bottom > height:
            self.playgame = False 
        
        if len(self.platforms) < 4:
            platwidth = random.randint(100, 250)
            platheight = 30
            platx = random.randint(0, width - 200)
            platy = random.randint(-50, -20)
            platform = Platform(platx, platy, platwidth, platheight)
            self.platforms.add(platform)
            self.gamesprites.add(platform)
        
    def draw(self):
        self.display.blit(self.bg_img1, (0, self.bg_y1))
        self.display.blit(self.bg_img2, (0, self.bg_y2))
        self.gamesprites.draw(self.display)
        self.printtext(str(self.tourist.score), 22, yellow, width / 2, 15)
        for platform in self.platforms:
            pygame.draw.rect(self.display, yellow, platform.rect, 2)
        pygame.display.flip()

    def startscreen(self):
        start_bg = pygame.image.load("Images/start_background.png")
        start_bg = pygame.transform.scale(start_bg, (width, height))
        self.display.blit(start_bg, (0,0))
        self.printtext("GLOBE HOPPER!", 96, red, width/2, height/5)
        self.printtext("GLOBE HOPPER!", 96, yellow, width/2 + 5, height/5)
        self.printtext("Up arrow to jump", 30, red, width/2, height - 500)
        self.printtext("Up arrow to jump", 30, yellow, width/2 + 2, height - 500)
        self.printtext("Right and left arrows to strafe", 30, red, width/2, height - 450)
        self.printtext("Right and left arrows to strafe", 30, yellow, width/2 + 2, height - 450)
        self.printtext("Esc to pause", 30, red, width/2, height - 400)
        self.printtext("Esc to pause", 30, yellow, width/2 + 2, height - 400)
        self.printtext("Press enter to play!", 30, red, width/2, height - 350)
        self.printtext("Press enter to play!", 30, yellow, width/2 + 2, height - 350)
        pygame.display.flip()
        self.keypress()

    def gameoverscreen(self):
        self.display.fill(red)
        self.gameovertone = mixer.Sound('Sounds/game_over_tone.WAV')
        self.gameovertone.play()
        self.printtext("GAME OVER!", 96, black, width/2 + 5, height/5)
        self.printtext("GAME OVER!", 96, white, width/2, height/5 - 4)
        self.printtext("Score: "+ str(self.tourist.score), 30, black, width/2 + 2, height - 400)
        self.printtext("Score: "+ str(self.tourist.score), 30, white, width/2, height - 402)
        self.printtext("Press enter to play again", 30, black, width/2 + 2, height - 350)
        self.printtext("Press enter to play again", 30, white, width/2, height - 352)
        skull_img = pygame.image.load('Images/skull.png')
        skull_img = pygame.transform.scale(skull_img, (250, 250))
        self.display.blit(skull_img, (width/2 - 125, height - 670))
        pygame.display.flip()
        self.keypress()
    
    def printtext(self, text, size, colour, x, y):
        font = pygame.font.Font('VCR_OSD_MONO.ttf', size)
        textsurface = font.render(text, True, colour)
        textrect = textsurface.get_rect()
        textrect.midtop = (x, y)
        self.display.blit(textsurface, textrect)

    def keypress(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
            keypressed = pygame.key.get_pressed()
            if keypressed[pygame.K_RETURN]:
                waiting = False

class Tourist(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.img = pygame.image.load('Images/tourist.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (60, 60))
        self.image = self.img
        self.x = width/2
        self.y = height - 50
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.coord = vector(self.x, self.y)
        self.acc = vector(0, 0)
        self.vel = vector(0, 0)
        self.score = 0

    def jump(self):
        if self.vel.y >= 0:
            collide = pygame.sprite.spritecollide(self, self.game.platforms, False)
            if collide:
                self.jumptone = mixer.Sound('Sounds/jump_tone.WAV')
                self.jumptone.play()
                self.vel.y = -24 
    
    def update(self):
        self.acc = vector(0, 0.8)

        keypressed = pygame.key.get_pressed()
        if keypressed[pygame.K_RIGHT]:
            self.acc.x = 1.0  
        if keypressed[pygame.K_LEFT]:
            self.acc.x = -1.0 
        if keypressed[pygame.K_UP]:
            self.jump()

        self.acc.x += self.vel.x * -0.1 
        
        self.vel += self.acc
        self.coord += (self.acc * 0.5) + self.vel
        
        if self.coord.x > width:
            self.coord.x = 0
        if self.coord.x < 0:
            self.coord.x = width
        self.rect.midbottom = self.coord

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, plat_width, plat_height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((plat_width, plat_height))
        self.image.fill(plat_colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Mosquito(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.img = pygame.image.load('Images/mosquito.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (75, 75))
        self.image = self.img
        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice([76, width - 76])
        self.x_vel = random.randint(4, 7) 
        self.y_vel = 0
        self.rect.y = random.randint(-50, 0)

    def update(self):
        self.rect.x += self.x_vel
        center = self.rect.center
        if self.rect.left >= width or self.rect.right <= 0:
            self.x_vel *= -1
        if self.rect.top >= height:
            self.kill()

async def main():
    game = Game()
    game.startscreen()
    while game.running:
        game.newgame()
        game.gameloop()
        game.gameoverscreen()
        await asyncio.sleep(0)

asyncio.run(main())