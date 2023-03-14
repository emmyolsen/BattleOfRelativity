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


#finner font på maskinen som matcher best med navnet "arial" 
font_name = pg.font.match_font('arial') 

# Variabler som styrer tid og nedtelling
year = 365
seconds = 1
start_time = None


# Initierer pygame og mixer
pg.init()
pg.mixer.init()

# musikk og sounds
background_music = pg.mixer.music.load('Medier/BakgrunnsMusikk.mp3')
win_sound = pg.mixer.Sound('Medier/Won!.wav')

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()



# Klasse for planetene
class Planet:
    def __init__(self, x, y, planet_img):
        self.x = x 
        self.y = y
        self.planet_img = planet_img
        
        self.h = 80
        self.w = 80
        self.r = self.h/2 - 10 #lager en radius som senere skal brukes til kollisjoner
        self.cake = False #styrer om kaken finnes på denne planeten
        
        # skalerer bildet etter oppgitt høyde og bredde
        self.scaled = pg.transform.scale(self.planet_img, (self.h, self.w))
        
    # metode som tegner planeten til skjermen
    def draw(self):
        surface.blit(self.scaled, (self.x, self.y))
        
        
        
# klasse Earth for jorden (arver fra planet)       
class Earth(Planet):
    def __init__(self, x, y, planet_img):
        super().__init__(x, y, planet_img)
        
        # skalerer bildet
        self.scaled = pg.transform.scale(self.planet_img, (400,400))
        
        self.r = 150 #lager en radius som senere skal brukes til kollisjon
        
        # definerer et sentrum for planeten som senere brukes til kollisjon
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
    
# metode som tegner spaceshipet til skjermen  
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
            
    # metode som beveger spaceshipet
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

# planet-objekter
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

# liste med planeter
planet_list = [planet1, planet2, planet3, planet4, planet5, planet6, planet7, planet8, planet9, planet10]

earth = Earth(350, 500, earth_img)

spaceship = Spaceship(520, 485, spaceship_img)

# skalerer bilde av kaken
cake_scaled = pg.transform.scale(cake_img, (100, 100))

cake_index = 0
    
# funksjon som plasserer planeten på en tifeldig planet
def place_cake(planet_list):
    global cake_index
    
    for planet in planet_list:
        planet.cake = False
    
    cake_index = random.randint(0,9)
    
    planet_list[cake_index].cake = True
    #for planet in planet_list:
        #print(planet.cake)
    
    for planet in planet_list:
        print(planet.cake)

# funksjon som sjekker kollisjon mellom spaceship og planet
def collision(spaceship, planet):
    # henter globale variabler
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
            #print("Kollisjon fra venstre")
        elif spaceship_center_x > planet_center_x:
            spaceship.x += 10
            #print("Kollisjon fra høyre")
        elif spaceship_center_y > planet_center_y:
            spaceship.y += 10
            #print("Kollisjon fra bunn")
        elif spaceship_center_y < planet_center_y:
            spaceship.y -= 10
            #print("Kollisjon fra topp")
            
        # sjekker om det finnes en kake på planeten    
        if planet.cake == True:
            cake_exists = True
            cake_found = True
            game_active = False
        else:
            cake_none = True
            game_active = False
            
# funksjon som sjekker kollisjon med spaceship og jorda            
def collision_earth(spaceship, earth):
    
    # henter globale variabler
    global win
    global game_active
    
    # sjekker om kaken er funnet
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
            pg.mixer.music.pause()

# funskjon som viser skjerm når kaken er funnet
def show_cake_screen():
    
    # henter globale variabler
    global game_over
    global game_active
    
    # tegner tekst
    drawText(surface, "YOU FOUND THE CAKE!", 30, WIDTH/2, HEIGHT/2 + 20)
    drawText(surface, "Return to earth to surprise your bff<3!", 25, WIDTH/2, HEIGHT*2/3 + 20)

    # tegner kake
    surface.blit(cake_scaled, (500, 250))
    
    # pauser bakgrunnsmusikk og spiller av vinne-lyd
    pg.mixer.music.pause()
    pg.mixer.Sound.play(win_sound)
    
    # når space trykkes på skal man kunne fortsette spillet
    keys = pg.key.get_pressed()
    
    if keys[pg.K_SPACE]:
        collision_variable = False
        game_over = False
        game_active = True
        pg.mixer.music.unpause()


# funskjon som viser skjerm når kaken ikke finnes
def show_empty_screen():
    
    # henter globale variabler
    global game_over
    global game_active
    
    # tegner "planet" i bakgrunnen
    pg.draw.circle(surface, BLUE, (550, 350), 400)
    
    # tegner tekst
    drawText(surface, "NO CAKE!", 30, WIDTH/2, HEIGHT/3)
    drawText(surface, "Press space to keep looking!", 25, WIDTH/2, HEIGHT*2/3 + 20)    

    # spillet fortsetter når space trykkes på
    keys = pg.key.get_pressed()
    
    if keys[pg.K_SPACE]:
        collision_variable = False
        game_over = False
        game_active = True
        
    
# funksjon som tegner tekst til skjermen   
def drawText(surface, text, size, x, y):
    font = pg.font.Font(font_name, size) #lager et font-objekt
    text_surface = font.render(text, True, WHITE) #true gir anti-aliased font som er "smoothere"
    text_rect = text_surface.get_rect() # lager et rect
    text_rect.midtop = (x,y) # setter midtop til referansepunkt
    surface.blit(text_surface, text_rect) # tegner til skjermen
  
  
# funskjon som viser start-skjerm
def show_start_screen():
    
    # henter globale variabler
    global game_over
    global game_active
    global start_time
    global year
    
    # tegner tekst
    drawText(surface, "The Battle of Relativity!", 64, WIDTH/2, HEIGHT/4)
    drawText(surface, "In 365 days your best friend is celebrating her birthday! She wants a spacecake!", 25, WIDTH/2, HEIGHT*3/7)
    drawText(surface, "But here's the problem: you don't know which planet the cake is on...", 25, WIDTH/2, HEIGHT*3/7 +30)    
    drawText(surface, "Use the arrows to move around in space and find the cake before 365 days have passed!", 25, WIDTH/2, HEIGHT*3/7 + 60)
    drawText(surface, "Press space to begin!", 30, WIDTH/2, HEIGHT*3/7 + 100)
    
    # plasserer spaceshipet
    spaceship.x = 520
    spaceship.y = 485
    
    # når space trykkes på starter spillet på nytt
    keys = pg.key.get_pressed()
    
    if keys[pg.K_SPACE]:
        game_over = False
        game_active = True
        start_time = pg.time.get_ticks()
        year = 365
        seconds = 1
        
        # spiller musikk
        pg.mixer.music.play()

# funksjon som lager nedtelling              
def show_timer():
    
    # henter globale variabler
    global year
    global start_time
    global seconds
    global game_active
    global game_over
    
    # definerer nåtid
    real_time = pg.time.get_ticks()
    
    # regner ut tid siden spillet begynte
    time = real_time - start_time
    
    # variabel som gjør det mulig å nullstille tiden ved nytt spill
    change_time = False
    
    # tegner klokken
    drawText(surface, f"Days left until birthday: {year}", 30, 200, 20)

    # endrer tid
    if time >= 125 * seconds:
        change_time = True
        seconds += 1
        
    if change_time == True:
        year -= 1
    
    # sjekker om tiden er ute
    if year == 0:
        game_active = False
        game_over = True
        
        
# funskjon som viser skjerm ved vunnet spill
def show_win_screen():
    
    # henter globale variabler
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
    
    # tegner tekst
    drawText(surface, "The Battle of Relativity!", 64, WIDTH/2, HEIGHT/4)    
    drawText(surface, "You won! Your bestfriend is super happy and you are the best friend ever <3", 25, WIDTH/2, HEIGHT*3/7)
    
    # setter bakgrunnsmusikk på pause og spiller av vinne-lyd
    pg.mixer.music.pause()
    pg.mixer.Sound.play(win_sound)
    
    # når space trykkes på skal spillet starte på nytt
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
        
        # spiller musikk
        pg.mixer.music.play()
    

               
    
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
    
    # sjekker om spillet skal runne
    if game_active:
        # viser nedtelling
        show_timer()
        
        # sjekker om kaken er plassert. hvis den ikke er det kalles funksjon som plasserer kaken.
        if cake_placed == False:
            place_cake(planet_list)
            cake_placed = True
            
        # tegner alle planetene og sjekker kollisjon
        for planet in planet_list:
            planet.draw()
            collision(spaceship, planet)
        
        # sjekker kollisjon med spaceship og jorda
        collision_earth(spaceship, earth)
        
        # tegner jorda og spaceship og oppdaterer spaceshipets posisjon
        earth.draw() 
        spaceship.draw()
        spaceship.update()
        spaceship.move()
        
    # sjekker om gameover er true
    elif game_over:
        # viser startskjerm
        show_start_screen()
        
    # sjekker om spillet er vunnet       
    elif win:
        show_win_screen()
    
    # sjekker om kollisjons-skjerm skal vises og viser riktig skjerm
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


"""
Prestentasjon:
- vi lærte fra Philip sin presentasjon at det hadde vært bedre å ha en status = fremfor å ha tusen forskjellige variabler som er true or false


ekstra hvis vi får tid:
- Legge til år/liv og eventuell "prøv igjen neste år skjerm"
- flamme bak romskip + kake oppå romskip når du har funnet den
- powerups? så farten går fortere


KILDER:
inspirasjon til gameoverscreen:
https://www.youtube.com/watch?v=Z2K2Yttvr5g&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw&index=18

won-sound:
spuispuin, https://opengameart.org/content/won-orchestral-winning-jingle

"""
