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

window_width = 500
window_height = 560
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("The Great Block & The Sneaky Ball @Markus Halminen")

# Initialize the path to the current folder to find needed files
cd_dir = os.path.dirname(__file__)
path_assets = r'{}/assets'.format(cd_dir)

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

# Load the sound effects and make the music loop
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

# Set background to color white
background = (255, 255, 255)

# Set framerate
fps = 60

main_font = pygame.font.SysFont("comicsans", 30)
lose_font = pygame.font.SysFont("comicsans", 48)

lose_messages = ["You lost", "Game Over", "Better luck next time", "Git gud", "Too bad"]

def player_movement(keys, block, player_speed):
    if keys[pygame.K_LEFT] and block.x - player_speed > 0 - 0.5:
       block.x -= player_speed
    if keys[pygame.K_RIGHT] and block.x + player_speed + block.width < window_width:
        block.x += player_speed

# Draw the graphics to the window
def draw_window(block, ball, points):
        window.fill((background))
        window.blit(block_img, (block.x, block.y))
        window.blit(ball_img, (ball.x, ball.y))
        points_label = main_font.render("Points: " + str(points), 1, (0, 0, 0))
        window.blit(points_label, (10, 10))
        pygame.display.update()

# Draw a message to the window for four second when the player loses
def game_over(lose_text):
    draw_text = lose_font.render(lose_text, 1, (0, 0, 0))
    window.blit(draw_text, (window_width/2 - draw_text.get_width()/2, window_height/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

# Write the score to the text file when the game ends
def write_to_file (points):
    score = str(points)
    path_file = r'{}/scores.txt'.format(cd_dir)
    this_date = datetime.datetime.now()
    date_string = this_date.strftime("%d/%m/%Y %H:%M:%S")
    try:
        file = open(path_file, "a")
        file.write(date_string + " Score: " + score + "\n")
    except:
        print("\033[1;31;40m Failed to write scores into the file \033[0m")
        pass
    finally:
        file.close()

def main():
    ball_directions = [3, -3]
    lose_text = random.choice(lose_messages)
    # Set rectancles for the block and the ball for movement
    block = pygame.Rect(window_width / 2, window_height - 20 , 125, 20)
    ball = pygame.Rect(window_width / 2, 30, 40, 40)
    player_speed = 10
    # Set the direction for the ball randomly
    ball_speed_x = random.choice(ball_directions)
    ball_speed_y = 3
    points = 0

    # Define the main loop which controls the game
    while True:
        # Set the framerate of the game so that it does not exceed the amount of the fps variable
        pygame.time.Clock().tick(fps)
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
        
        # Set a Pygame event for pressing buttons and give those to the
        # function that determines the movement of the player
        keys = pygame.key.get_pressed()
        player_movement(keys, block, player_speed)
    
        # Define the ball's movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        # Change the ball's direction when it hits the sides of the window
        if ball.top <= 0:
            ball_speed_y *= -1
        if ball.left <= 0 or ball.right >= window_width:
            ball_speed_x *= -1
        # Change the ball's direction and give it more speed when it hits the player
        if ball.colliderect(block):
            ball_speed_y *= -1.1
            ball_speed_x *= 1.1
            points += 1
            ball_hit_sound.play()
            ball.bottom = block.y
        # Loop ends when the ball drops from the bottom of the screen
        if ball.top > window_height:
            write_to_file(points)
            game_over(lose_text)
            break

        # Draw the graphics to the window each round of the loop
        draw_window(block, ball, points)

    #  Call the main function again when the player loses
    main()

main()