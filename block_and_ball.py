try:
    import pygame
except ModuleNotFoundError:
    print("\033[1;31;40m You will need to install Python's Pygame module in order play this game \033[0m")
    exit()
except ImportError:
    print("\033[1;31;40m The game encountered a problem when trying to import the Pygame module \033[0m")
    exit()
except:
    print("\033[1;31;40m Something went wrong with Pygame module +358 45 322 7595 \033[0m")
    exit()

import os
import random
import datetime
pygame.font.init()
pygame.mixer.init()

# Määritetään ikkunan kooksi 500x560 ja ikkunaan kuvateksti
window_width = 500
window_height = 560
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("The Great Block & The Sneaky Ball @Markus Halminen")

# Määritetään polku pelin nykyiseen kansioon tiedostojen löytämistä/tallentamista varten
cd_dir = os.path.dirname(__file__)

# Määritetään polku assets-kansioon, jotta ohjelma löytää tiedostot myös muilla koneilla
path_assets = r'{}/assets'.format(cd_dir)

# Ladataan grafiikat palikalle ja pallolle sekä muutetaan niidet koot sopivaksi
try:
    block_img = pygame.transform.scale(pygame.image.load(os.path.join(path_assets, "block.png")), (125, 20))
    ball_img = pygame.transform.scale(pygame.image.load(os.path.join(path_assets, "ball.png")), (40, 40))
except FileNotFoundError:
    print("\033[1;31;40m Could not find images in the assets folder \033[0m")
    pygame.quit()
    exit()
except:
    print("\033[1;31;40m Something went wrong when trying to load images \033[0m")
    pygame.quit()
    exit()

# Ladataan taustamusiikki ja äänitehoste pallon ja palikan yhteentörmäykselle
# Asetetaan niiden äänenvoimakkuus sekä musiikki jatkuvalle toistolle
try:
    ball_hit_sound = pygame.mixer.Sound(os.path.join(path_assets, "boing.wav"))
    ball_hit_sound.set_volume(1)
    pygame.mixer.music.load(os.path.join(path_assets, "waves.mp3"))
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play(-1,0.0)
except FileNotFoundError:
    print("\033[1;31;40m Could not find sound effects in the assets folder \033[0m")
    pass
except:
    print("\033[1;31;40m Something went wrong when trying to load sound effects \033[0m")
    pass

# Määritetään taustan väriksi valkoinen
background = (255, 255, 255)

# Määritetään ruudunpäivitykseksi 60 kuvaa sekunnissa
fps = 60

# Määritetään pelin tarvitsemat fontit ja niiden koko Pygamen kirjastosta
main_font = pygame.font.SysFont("comicsans", 30)
lose_font = pygame.font.SysFont("comicsans", 48)

# Listataan eri viestit, jotka näytetään kun pelaaja häviää
lose_messages = ["You lost", "Game Over", "Better luck next time", "Git gud", "Too bad"]

# Määritetään pelaajan liike funktion avulla
def player_movement(keys, block, player_speed):
    if keys[pygame.K_LEFT] and block.x - player_speed > 0 - 0.5: # palikka liikkuu vasemmalle
       block.x -= player_speed
    if keys[pygame.K_RIGHT] and block.x + player_speed + block.width < window_width: # palikka liikkuu oikealle
        block.x += player_speed

# Määritetään funktio, joka piirtää grafiikat ikkunaan
def draw_window(block, ball, points):
        window.fill((background))
        window.blit(block_img, (block.x, block.y))
        window.blit(ball_img, (ball.x, ball.y))
        points_label = main_font.render("Points: " + str(points), 1, (0, 0, 0))
        window.blit(points_label, (10, 10))
        pygame.display.update()

# Määritetään funktio, joka piirtää häviötekstin ruudulle neljäksi sekunniksi
def game_over(lose_text):
    draw_text = lose_font.render(lose_text, 1, (0, 0, 0))
    window.blit(draw_text, (window_width/2 - draw_text.get_width()/2, window_height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

# Määritetään funktio, jolla pisteet tallennetaan tekstitiedostoon.
def write_to_file (points):
    score = str(points)
    # Määritetään polku tiedostolle, johon pisteet tallennetaan
    path_file = r'{}/highscores.txt'.format(cd_dir)
    this_date = datetime.datetime.now()
    date_string = this_date.strftime("%d/%m/%Y %H:%M:%S")
    try:
        file = open(path_file, "a")
        file.write(date_string + " Highscore: " + score + "\n")
    except:
        print("\033[1;31;40m Failed to write highscores into the file \033[0m")
        pass
    finally:
        file.close()

# Määritetään pelin pää-funktio
def main():
    ball_directions = [3, -3]
    lose_text = random.choice(lose_messages)
    # Määritetään palikalle ja pallolle suorakulmiot niiden liikettä varten
    block = pygame.Rect(window_width / 2, window_height - 20 , 125, 20)
    ball = pygame.Rect(window_width / 2, 30, 40, 40)
    player_speed = 10
    # Määritetään pallon liikkeen suunta sattumanvaraisesti pelin alkaessa
    ball_speed_x = random.choice(ball_directions)
    ball_speed_y = 3
    points = 0

    run = True
    clock = pygame.time.Clock()

    # Määritetään while-loop, joka pyörittää peliä ja tarvittaessa lopettaa sen
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                print("\033[1;32;40m \nThanks for playing! \033[0m")
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    print("\033[1;32;40m \nThanks for playing! \033[0m")
                    exit()
        
        # Määritetään ensin Pygame-tapahtuma näppäimien painamista varten
        # ja kutsutaan sitten funktio, joka määrittää palikan liikkeen
        keys = pygame.key.get_pressed()
        player_movement(keys, block, player_speed)
    
        # Määritetään pallon liike
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        # Pallon suunta muuttuu jos se osuu ikkunan ylä- tai sivureunoihin
        if ball.top <= 0:
            ball_speed_y *= -1
        if ball.left <= 0 or ball.right >= window_width:
            ball_speed_x *= -1
        # Pallon osuessa palikkaan se vaihtaa suuntaansa ja kiihdyttää vauhtiaan
        # Törmäys aktivoi äänitehosteen ja antaa pelaajalle pisteen
        if ball.colliderect(block):
            ball_speed_y *= -1.1
            ball_speed_x *= 1.1
            points += 1
            ball_hit_sound.play()
            ball.bottom = block.y
        # Pallon tippuessa ikkunan alakulmasta pistemäärä tallennetaan tiedostoon
        # Näytetään häviöteksti ja pelikierros lopetetaan
        if ball.top > window_height:
            write_to_file(points)
            game_over(lose_text)
            break

        # Kutsutaan funktio piirtämään grafiikat näytölle loopin joka kierroksella
        draw_window(block, ball, points)

    # Aloitetaan main-funktio uudestaan kun while-loop katkeaa pelaajan hävitessä
    main()

main()