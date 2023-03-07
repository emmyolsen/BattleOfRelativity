import pygame as pg
import math

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


spaceship_img = pg.image.load('Medier/romskip.png')

#finner font på maskinen som matcher best med navnet "arial" 
font_name = pg.font.match_font('arial') 



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
        self.h = 80
        self.w = 80
        self.r = self.h/2
        self.planet_img = planet_img
        
        self.surface = pg.transform.scale(self.planet_img, (self.h, self.w))
        
    
    def draw(self):
        surface.blit(self.surface, (self.x, self.y))
        
        
class Earth(Planet):
    def __init__(self, x, y, planet_img):
        super().__init__(x, y, planet_img)
            
        self.surface = pg.transform.scale(self.planet_img, (400,400))

    
        
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
        # definerer en radius så vi kan tenke på spaceshipet som en sirkel senere (hitbox)
        self.r = self.w / 2 - 10
    
        
       
    def draw(self):
        surface.blit(self.surface, (self.x, self.y))
    
    def update(self):
        # sjekker om spaceship kolliderer med vegg. Hvis den gjør det endres posisjon.
        
        # Kollisjon topp
        if self.x >= 0:
            self.x += self.vx
        else:
            game_over = True
            self.x = 1
            
        # Kollisjon bunn 
        if self.x + self.w <= WIDTH:
            self.x += self.vx
        else:
            self.x = 1099 - self.w
        
        # Kollisjon venstre vegg
        if self.y >= 0:  
            self.y += self.vy
        else:
            self.y = 1
        
        # Kollisjon høyre vegg 
        if self.y + self.h <= HEIGHT:
            self.y += self.vy

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
                
        

planet1 = Planet(160, 50, planet1_img)
planet2 = Planet(550, 100, planet2_img)
planet3 = Planet(1220, 90, planet3_img)
planet4 = Planet(80, 200, planet4_img)
planet5 = Planet(410, 300, planet5_img)
planet6 = Planet(700, 200, planet6_img)
planet7 = Planet(175, 580, planet7_img)
planet8 = Planet(700, 450, planet8_img)
planet9 = Planet(250, 420, planet9_img)
planet10 = Planet(900, 735, planet10_img)

planet_list = [planet1, planet2, planet3, planet4, planet5, planet6, planet7, planet8, planet9, planet10]

earth = Earth(350, 500, earth_img)

spaceship = Spaceship(520, 485, spaceship_img) 

def collision(spaceship, planet):
    global game_over
    # definerer sentrum for planet og sirkel
    planet_center_x = planet.x + planet.r
    planet_center_y = planet.y + planet.r
    spaceship_center_x = spaceship.x + (spaceship.w/2)
    spaceship_center_y = spaceship.y + (spaceship.w/2)
    
    # avstand mellom sentrum av planet og sentrum av spaceship
    dist2 = (planet_center_x - spaceship_center_x)**2 + (planet_center_y - spaceship_center_y)**2
    dist = math.sqrt(dist2)
    
    # dersom avstanden mellom sentrum av planet og spaceship er mindre enn summen av de to radiusene får vi kollisjon
    if dist <= planet.r + spaceship.r:
        game_over = True
        
        
    
# funksjon som tegner tekst til skjermen   
def drawText(surface, text, size, x, y):
    font = pg.font.Font(font_name, size) #lager et font-objekt
    text_surface = font.render(text, True, WHITE) #true gir anti-aliased font som er "smoothere"
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)
    

def show_start_screen():
    
    global game_over
    
    drawText(surface, "The Battle of Relativity!", 64, WIDTH/2, HEIGHT/4)    
    drawText(surface, "Bestevennen din har bursdag om 365 dager og ønsker seg en kake fra verdensrommet!", 25, WIDTH/2, HEIGHT*3/7)    
    drawText(surface, "Finn kaken på en av planetene innen det har gått 365 dager.", 25, WIDTH/2, HEIGHT*3/7 +30)    
    drawText(surface, "Du beveger deg ved hjelp av piltastene.", 25, WIDTH/2, HEIGHT*3/7 + 60)
    
    drawText(surface, "Trykk på mellomrom for å begynne!", 30, WIDTH/2, HEIGHT*3/7 + 100)
    
    spaceship.x = 520
    spaceship.y = 485
    
    keys = pg.key.get_pressed()
    
    if keys[pg.K_SPACE]:
        game_over = False



# Variabel som styrer om spillet skal kjøres
run = True

# variabel som styrer om gave_over skjerm skal vises
game_over = True

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
    
    if game_over:
        show_start_screen()
    
    else:        
        for planet in planet_list:
            planet.draw()
            collision(spaceship, planet)
            
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