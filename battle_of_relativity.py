import pygame as pg
import os

WIDTH = 1100  # bredden av vinduet
HEIGHT = 700 # høyden til vinduet
SIZE = (WIDTH, HEIGHT) # størrelsen til vinduet

FPS = 60 # frames per second (bilder per sekund)

# Farger (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Medier
planet1_img = pg.image.load('Medier/planets/planet1.png')
planet2_img = pg.image.load('Medier/planets/planet2.png')
planet3_img = pg.image.load('Medier/planets/planet3.png')
planet4_img = pg.image.load('Medier/planets/planet4.png')
planet5_img = pg.image.load('Medier/planets/planet5.png')
planet6_img = pg.image.load('Medier/planets/planet6.png')
planet7_img = pg.image.load('Medier/planets/planet7.png')
planet8_img = pg.image.load('Medier/planets/planet8.png')
planet9_img = pg.image.load('Medier/planets/planet9.png')
planet10_img = pg.image.load('Medier/planets/planet10.png')
earth_img = pg.image.load('Medier/jorda.png')

planet_size = (80,80)

spaceship_img = pg.image.load('Medier/romskip.png')



# Initiere pygame
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()

# Henter inn bakgrunnsbilde
backgroundImg = pg.image.load('Medier/bakgrunn.png')



# Klasse for planetene
class Planet:
    def __init__(self, x, y, planet_img):
        self.x = x
        self.y = y
        #self.center = (self.x
        self.planet_img = planet_img
        
        self.surface = pg.transform.scale(self.planet_img, planet_size)
        
        self.rect = self.surface.get_rect(center=(self.x,self.y))
    
    def draw(self):
        surface.blit(self.surface, self.rect)
        
        
class Earth(Planet):
    def __init__(self, x, y, planet_img):
        super().__init__(x, y, planet_img)
            
        self.surface = pg.transform.scale(self.planet_img, (400,400))
        self.rect = self.surface.get_rect(center=(self.x,self.y))

    
        
class Spaceship:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
        self.w = 60
        self.h = 60
        self.surface = pg.transform.scale(self.img, (self.w,self.h))
        self.speed = 1
        self.vx = 0
        self.vy = 0
        
        self.rect = self.surface.get_rect(center=(self.x,self.y))

    
        
       
    def draw(self):
        surface.blit(self.surface, self.rect)
    
    def update(self):
        # sjekker om spaceship kolliderer med vegg. Hvis den gjør det endres posisjon.
        
        # Kollisjon topp
        if self.x >= 0:
            self.rect.x += self.vx
        else:
            self.x = 1
            
        # Kollisjon bunn 
        if self.rect.x + self.w <= WIDTH:
            self.x += self.vx
        else:
            self.x = 1099 - self.w
        
        # Kollisjon venstre vegg
        if self.y >= 0:  
            self.rect.y += self.vy
        else:
            self.y = 1
        
        # Kollisjon høyre vegg 
        if self.y + self.h <= HEIGHT:
            self.rect.y += self.vy

        else:
            self.y = 699 - self.h
            

    def move(self):
        self.vy = 0
        self.vx = 0
        
        keys = pg.key.get_pressed()
        
        if keys[pg.K_UP]:
            self.vy = -self.speed
            
        if keys[pg.K_DOWN]:
            self.vy = self.speed
        
        if keys[pg.K_RIGHT]:
            self.vx = self.speed
            
        if keys[pg.K_LEFT]:
            self.vx = -self.speed
                
        

planet1 = Planet(240, 90, planet1_img)
planet2 = Planet(490, 140, planet2_img)
planet3 = Planet(990, 140, planet3_img)
planet4 = Planet(90, 240, planet4_img)
planet5 = Planet(530, 340, planet5_img)
planet6 = Planet(740, 240, planet6_img)
planet7 = Planet(115, 590, planet7_img)
planet8 = Planet(740, 490, planet8_img)
planet9 = Planet(290, 470, planet9_img)
planet10 = Planet(940, 515, planet10_img)

planet_list = [planet1, planet2, planet3, planet4, planet5, planet6, planet7, planet8, planet9, planet10]

earth = Earth(550, 700, earth_img)

spaceship = Spaceship(550, 520, spaceship_img) 



def collision(spaceship, planet):
    
    
    
    





# Variabel som styrer om spillet skal kjøres
run = True

# Spill-løkken
while run:
    # Løkken kjører i korrekt hastighet
    clock.tick(FPS)
    
    # Går gjennom hendelser (events)
    for event in pg.event.get():
        # Sjekket om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            run = False # Spillet skal avsluttes
    
    
    # Legger til bakgrunnsbilde på skjermen
    surface.blit(backgroundImg, (0,0))
    
    #surface.blit(planet1,(planet1.x, planet1.y))
    
    for planet in planet_list:
        planet.draw()
        
    earth.draw()
    
    spaceship.draw()
    spaceship.update()
    spaceship.move()

    # Skalerer bakgrunnsbilde
    backgroundImg = pg.transform.scale(backgroundImg, SIZE)

    # Etter vi har tegner alt, "flipper" vi displayet
    pg.display.flip()

# Avslutter pygame
pg.quit()

#https://www.youtube.com/watch?v=Z2K2Yttvr5g&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=17

