import pygame as pg
import math
import random

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
backgroundImg = pg.image.load('Medier/bakgrunn.png')

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

cake_img = pg.image.load('Medier/cake.png')

#backgroundSound = pg.mixer.Sound('Medier/Bakgrunnsmusikk2.ogg')

#finner font på maskinen som matcher best med navnet "arial" 
font_name = pg.font.match_font('arial') 

# Variabler som styrer tid og nedtelling
year = 365
seconds = 1
start_time = None


# Initierer pygame
pg.init()
pg.mixer.init()

background_music = pg.mixer.music.load('Medier/BakgrunnsMusikk.mp3')
win_sound = pg.mixer.Sound('Medier/Won!.wav')

#pg.mixer.music.load('Medier/BakgrunnsMusikk.mp3')
#pg.mixer.music.load('Medier/Won!.wav')


# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()



# Klasse for planetene
class Planet:
    def __init__(self, x, y, planet_img):
        self.x = x 
        self.y = y
        self.h = 80
        self.w = 80
        self.r = self.h/2 - 10
        self.planet_img = planet_img
        self.cake = False #styrer om kaken finnes på denne planeten
        
        # skalerer bildet etter oppgitt høyde og bredde
        self.scaled = pg.transform.scale(self.planet_img, (self.h, self.w))
        
    # metode som tegner planeten til skjermen
    def draw(self):
        surface.blit(self.scaled, (self.x, self.y))
        
# klasse Earth for jorden        
class Earth(Planet):
    def __init__(self, x, y, planet_img):
        super().__init__(x, y, planet_img)
            
        self.scaled = pg.transform.scale(self.planet_img, (400,400))
        
        self.r = 150

        self.center_x = self.x + 200
        self.center_y = self.y + 200
        
    
# Klasse for Spaceship        
class Spaceship:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        
        self.w = 60
        self.h = 60
        
        self.speed = 1
        self.vx = 0
        self.vy = 0
        
        # definerer en radius så vi kan tenke på spaceshipet som en sirkel senere (hitbox)
        self.r = self.w / 2 - 10
        
        # skalerer bildet etter oppgitt høyde og bredde
        self.scaled = pg.transform.scale(self.img, (self.w,self.h))
    
        
       
    def draw(self):
        surface.blit(self.scaled, (self.x, self.y))
    
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


planet1 = Planet(200, 50, planet1_img)
planet2 = Planet(450, 100, planet2_img)
planet3 = Planet(950, 100, planet3_img)
planet4 = Planet(50, 200, planet4_img)
planet5 = Planet(400, 300, planet5_img)
planet6 = Planet(700, 200, planet6_img)
planet7 = Planet(75, 550, planet7_img)
planet8 = Planet(770, 370, planet8_img)
planet9 = Planet(250, 430, planet9_img)
planet10 = Planet(930, 505, planet10_img)

planet_list = [planet1, planet2, planet3, planet4, planet5, planet6, planet7, planet8, planet9, planet10]

earth = Earth(350, 500, earth_img)

spaceship = Spaceship(520, 485, spaceship_img)

cake_scaled = pg.transform.scale(cake_img, (100, 100))

# variabel som forteller hvilket index i planetlisten kaken befinner seg
cake_index = 0

def place_cake(planet_list):
    global cake_index
    
    for planet in planet_list:
        planet.cake = False
        
    cake_index = random.randint(0,9)
    planet_list[cake_index].cake = True

    for planet in planet_list:
        print(planet.cake)

def collision(spaceship, planet):
    global collision_variable
    global cake_exists
    global cake_none
    global game_active
    global cake_found
    
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
        # setter kollisjonsvariabel til sann
        collision_variable = True
        # sjekker fra hvilken side spaceshipet kommer fra og flytter det deretter
        
        if spaceship_center_x < planet_center_x:
            spaceship.x -= 10
            print("Kollisjon fra venstre")
        elif spaceship_center_x > planet_center_x:
            spaceship.x += 10
            print("Kollisjon fra høyre")
        elif spaceship_center_y > planet_center_y:
            spaceship.y += 10
            print("Kollisjon fra bunn")
        elif spaceship_center_y < planet_center_y:
            spaceship.y -= 10
            print("Kollisjon fra topp")
            
            
        if planet.cake == True:
            cake_exists = True
            cake_found = True
            game_active = False
            pg.mixer.Sound.play(win_sound)
            pg.mixer.music.stop()
            #background_music.pause()
            #win_sound.play()
            #pg.mixer.music.pause(background_music)
            #pg.mixer.music.play(win_sound)

            
        else:
            cake_none = True
            game_active = False
            
            
def collision_earth(spaceship, earth):
    global win
    global game_active
    
    if cake_found:
        # definerer sentrum av spaceship
        spaceship_center_x = spaceship.x + (spaceship.w/2)
        spaceship_center_y = spaceship.y + (spaceship.w/2)
        
        # avstand mellom sentrum av jorda og sentrum av spaceship
        dist2 = (earth.center_x - spaceship_center_x)**2 + (earth.center_y - spaceship_center_y)**2
        dist = math.sqrt(dist2)
        
        # dersom avstanden mellom sentrum av planet og spaceship er mindre enn summen av de to radiusene får vi kollisjon
        if dist <= earth.r + spaceship.r:
            win = True
            game_active = False
            #background_music.pause()
            pg.mixer.music.pause()
            #pg.mixer.music.pause(background_music)
            
def show_cake_screen():
    global game_over
    global game_active
    
    drawText(surface, "YOU FOUND THE CAKE!", 30, WIDTH/2, HEIGHT/2 + 20)
    drawText(surface, "Return to earth to surprise your bff<3!", 25, WIDTH/2, HEIGHT*2/3 + 20)    

    surface.blit(cake_scaled, (500, 250))
    
    keys = pg.key.get_pressed()
    
    if keys[pg.K_SPACE]:
        collision_variable = False
        game_over = False
        game_active = True



def show_empty_screen():
    global game_over
    global game_active
    drawText(surface, "NO CAKE!", 30, WIDTH/2, HEIGHT/3)
    
    keys = pg.key.get_pressed()
    
    if keys[pg.K_SPACE]:
        collision_variable = False
        game_over = False
        game_active = True



        
    
# funksjon som tegner tekst til skjermen   
def drawText(surface, text, size, x, y):
    font = pg.font.Font(font_name, size) #lager et font-objekt
    text_surface = font.render(text, True, WHITE) #true gir anti-aliased font som er "smoothere"
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)
    

def show_start_screen():
    
    global game_over
    global game_active
    global start_time
    global year
    
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
        game_active = True
        start_time = pg.time.get_ticks()
        year = 365
        seconds = 1
        #pg.mixer.music.play(background_music)
        #background_music.play()
        pg.mixer.music.unpause()

    

                 
def show_timer():
    global year
    global start_time
    global seconds
    global game_active
    global game_over
    real_time = pg.time.get_ticks()
    time = real_time - start_time
    change_time = False
        
    drawText(surface, f"Days left until birthday: {year}", 30, 200, 20)

    
    if time >= 125 * seconds:
        change_time = True
        seconds += 1
        
    if change_time == True:
        year -= 1
        
    if year == 0:
        game_active = False
        game_over = True
        
def show_win_screen():
    global game_over
    global game_active
    global cake_placed
    global cake_exists
    global cake_none
    global cake_found
    global win
    
    global start_time 
    global year
    global seconds
    
    drawText(surface, "The Battle of Relativity!", 64, WIDTH/2, HEIGHT/4)    
    drawText(surface, "Du vant bestevennen din er dritglad du er best!", 25, WIDTH/2, HEIGHT*3/7)
    
    keys = pg.key.get_pressed()
    
    if keys[pg.K_SPACE]:
        game_over = False
        game_active = True
        cake_placed = False
        cake_exists = False
        cake_none = False
        cake_found = False 
        win = False
        
        start_time = pg.time.get_ticks()
        year = 365
        seconds = 1
        
        #pg.mixer.music.play(background_music)
        #background_music.play()

               
    
# Variabel som styrer om spillet skal kjøres
run = True

# variabel som styrer om gave_over skjerm skal vises
game_over = True

# variabel som styrer som spillet skal kjøres / om spill-skjerm skal vises
game_active = False

# variabel som styrer om kaken skal plasseres på nytt
cake_placed = False

# variabel som styrer om kollisjonsskjerm skal vises
collision_variable = False

# variabler som forteller om hvor vidt kaken er på planeten eller ikke
cake_exists = False
cake_none = False

# variabel som styrer om kaken er funnet eller ikke
cake_found = False

# Variabel som styrer som spilleren har vunnet
win = False



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
    

    if game_active:
        show_timer()
        
        # sjekker om kaken er plassert. hvis den ikke er det kalles funksjon som plasserer kaken.
        if cake_placed == False:
            place_cake(planet_list)
            cake_placed = True
            
        for planet in planet_list:
            planet.draw()
            collision(spaceship, planet)
         
        collision_earth(spaceship, earth)
        earth.draw() 
        spaceship.draw()
        spaceship.update()
        spaceship.move()
        
    elif game_over:
        show_start_screen()
            
    elif win:
        show_win_screen()
        
    elif collision_variable:
        if cake_exists:
            show_cake_screen()
        elif cake_none:
            show_empty_screen()
                                
    
    # Skalerer bakgrunnsbilde
    backgroundImg = pg.transform.scale(backgroundImg, SIZE)

    # Etter vi har tegner alt, "flipper" vi displayet
    pg.display.flip()

# Avslutter pygame
pg.quit()

#https://www.youtube.com/watch?v=Z2K2Yttvr5g&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=17

"""
PLAN:
- fikse lyd!
- ulm diagram
- kommentere koden

ekstra hvis vi får tid:
- Legge til år/liv og eventuell "prøv igjen neste år skjerm"
- flamme bak romskip + kake oppå romskip når du har funnet den
- powerups? så farten går fortere
"""
