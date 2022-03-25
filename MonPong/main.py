import pygame, sys, random, time


#pause when on a player wins
def pause(var):
    paused = True
    while paused:
        screen.fill(bg_color)
        machine_text = game_font.render(f"{var} WiN(s) \n press 'c' to continue.", False, light_grey)
        screen.blit(machine_text, (screen_width // 2 - 400, screen_height // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False

        pygame.display.update()


#sound when player wins
def applaudir():
   score = pygame.mixer.Sound("applause.wav")
   pygame.mixer.Sound.play(score)


def score_sound():
    score = pygame.mixer.Sound("score.wav")
    pygame.mixer.Sound.play(score)

#sound when ball touch the paddle , top and laterals
def paddle_hit():
    score = pygame.mixer.Sound("paddle_hit.wav")
    pygame.mixer.Sound.play(score)


#delay when ball touch the bottom
def game_delay(i=3):
    time.sleep(i)

#animate the ball
def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, machine_score
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0:
        ball_speed_y *= -1
        paddle_hit()

    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
        paddle_hit()

    # decrease player point
    if ball.bottom >= screen_height:
        if player_score >=5:
            machine_score += 5
            player_score -= 5
            score_sound()
            time.sleep(1)
        ball_restart()

        #Display the winner
        if machine_score == 100:
             pause("Machine")
             player_score = 50
             machine_score = 50

    # increase the score when ball touch the paddle
    if ball.colliderect(player):
        ball_speed_y *= -1
        if machine_score > 5 or player_score < 100:
            machine_score -= 5
            player_score += 5
            paddle_hit()


    if player_score == 100:

        applaudir()
        pause("You")
        player_score  = 50
        machine_score = 50

# animate the paddle
def player_animation():
    player.x += player_speed
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

#function to restart the ball
def ball_restart():
    global ball_speed_x
    global ball_speed_y
    ball.center = (screen_width // 2, screen_height // 2)
    ball_speed_y *= random.choice((1, -1))
    ball_speed_x *= random.choice((1, -1))

pygame.init()
clock = pygame.time.Clock()

#screen size
screen_width  = 900
screen_height = 700

#font
game_font = pygame.font.Font("BOUNCY.ttf", 60)

#screen display and title
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("PONG")

#my icon
programIcon = pygame.image.load('racket.png')
pygame.display.set_icon(programIcon)

#ball and player postion initial postion
ball = pygame.Rect(screen_width//2 -11, screen_height//2 - 11, 22,22)
player = pygame.Rect(screen_width//4 - 20, screen_height -15, 180, 10)

#colors
bg_color = pygame.Color(0,150,60)
light_grey =(200, 200, 200)
black =(0,0,0)

#ball speed and player speed
ball_speed_x = 5
ball_speed_y = 5
player_speed = 0

#initial scores
player_score  =  50
machine_score =  50



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                    player_speed += 7
            if event.key == pygame.K_LEFT:
                    player_speed -= 7

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_speed -= 7
            if event.key == pygame.K_LEFT:
                player_speed += 7

    ball_animation()

    player_animation()
    player.x += player_speed


    screen.fill(bg_color)
    pygame.draw.rect(screen,light_grey, player)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen, light_grey,(screen_width/2,0),(screen_width/2,screen_height))


    #Player score
    player_text = game_font.render(f"Player", False, light_grey)
    screen.blit(player_text, (screen_width // 2 + 20, screen_height // 2 - 50))

    player_text = game_font.render(f"{player_score}",False,light_grey)
    screen.blit(player_text,(screen_width//2+90,screen_height//2))


    #machine score
    machine_text = game_font.render(f"Computer", False, light_grey)
    screen.blit(machine_text, (screen_width // 2 - 240, screen_height // 2 -50))

    machine_text = game_font.render(f"{machine_score}", False, light_grey)
    screen.blit(machine_text, (screen_width // 2 -150, screen_height // 2))


    pygame.display.flip()
    clock.tick(60)