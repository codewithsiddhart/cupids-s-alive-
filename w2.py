import pygame
import random
import time
import os

pygame.init()

WIDTH = 900
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flower Hunter Deluxe")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial",30)
big = pygame.font.SysFont("Arial",70)

# basket
basket_x = 400
basket_y = 550
basket_w = 120
basket_h = 20

flowers = []
particles = []

score = 0
lives = 3
multiplier = 1

state = "splash"

# leaderboard
if not os.path.exists("scores.txt"):
    with open("scores.txt","w") as f:
        f.write("")

def load_scores():
    with open("scores.txt","r") as f:
        scores = f.readlines()
    return [int(s.strip()) for s in scores]

def save_score(s):
    scores = load_scores()
    scores.append(s)
    scores = sorted(scores,reverse=True)[:5]
    with open("scores.txt","w") as f:
        for sc in scores:
            f.write(str(sc)+"\n")

start_time = time.time()

running = True

while running:

    screen.fill((15,20,40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    state = "game"
                if event.key == pygame.K_2:
                    state = "leaderboard"

        if state == "gameover":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    score = 0
                    lives = 3
                    multiplier = 1
                    flowers.clear()
                    particles.clear()
                    state = "menu"

        if state == "leaderboard":
            if event.type == pygame.KEYDOWN:
                state = "menu"

    # SPLASH SCREEN
    if state == "splash":

        title = big.render("Flower Hunter",True,(255,200,255))
        screen.blit(title,(250,250))

        if time.time() - start_time > 2:
            state = "menu"

    # MENU
    elif state == "menu":

        title = big.render("Flower Hunter",True,(255,150,200))
        screen.blit(title,(250,200))

        t1 = font.render("1 - Start Game",True,(255,255,255))
        t2 = font.render("2 - Leaderboard",True,(255,255,255))

        screen.blit(t1,(350,350))
        screen.blit(t2,(350,400))

    # GAMEPLAY
    elif state == "game":

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            basket_x -= 8
        if keys[pygame.K_RIGHT]:
            basket_x += 8

        if random.randint(1,25) == 1:

            flower_type = random.choice(
                ["normal","normal","gold","poison","diamond"]
            )

            flowers.append([
                random.randint(20,WIDTH-20),
                0,
                random.uniform(-2,2),
                flower_type
            ])

        for f in flowers[:]:

            f[0] += f[2]
            f[1] += 5 + score/200

            if f[3] == "normal":
                color = (255,120,200)
                value = 10
                size = 10

            elif f[3] == "gold":
                color = (255,215,0)
                value = 50
                size = 12

            elif f[3] == "diamond":
                color = (80,200,255)
                value = 200
                size = 14

            else:
                color = (200,50,50)
                value = -1
                size = 10

            pygame.draw.circle(screen,color,(int(f[0]),int(f[1])),size)

            if basket_x < f[0] < basket_x + basket_w and basket_y < f[1] < basket_y + basket_h:

                if f[3] == "poison":
                    lives -= 1
                    multiplier = 1
                else:
                    score += value * multiplier
                    multiplier += 0.1

                for i in range(15):
                    particles.append([
                        f[0],
                        f[1],
                        random.uniform(-4,4),
                        random.uniform(-4,4),
                        random.randint(4,7)
                    ])

                flowers.remove(f)

            elif f[1] > HEIGHT:
                flowers.remove(f)

        # particles
        for p in particles[:]:

            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 0.3

            pygame.draw.circle(screen,(255,200,255),(int(p[0]),int(p[1])),int(p[4]))

            if p[4] <= 0:
                particles.remove(p)

        pygame.draw.rect(screen,(255,200,0),(basket_x,basket_y,basket_w,basket_h))

        score_t = font.render("Score: "+str(int(score)),True,(255,255,255))
        lives_t = font.render("Lives: "+str(lives),True,(255,255,255))
        mult_t = font.render("Combo: x"+str(round(multiplier,1)),True,(255,255,255))

        screen.blit(score_t,(10,10))
        screen.blit(lives_t,(750,10))
        screen.blit(mult_t,(400,10))

        if lives <= 0:
            save_score(int(score))
            state = "gameover"

    # GAME OVER
    elif state == "gameover":

        t = big.render("GAME OVER",True,(255,80,80))
        screen.blit(t,(280,250))

        s = font.render("Score: "+str(int(score)),True,(255,255,255))
        screen.blit(s,(400,350))

        r = font.render("Press R to return to menu",True,(255,255,255))
        screen.blit(r,(320,400))

    # LEADERBOARD
    elif state == "leaderboard":

        title = big.render("Leaderboard",True,(255,200,255))
        screen.blit(title,(300,150))

        scores = load_scores()

        for i,s in enumerate(scores):
            t = font.render(str(i+1)+". "+str(s),True,(255,255,255))
            screen.blit(t,(420,250+i*40))

        back = font.render("Press any key to return",True,(255,255,255))
        screen.blit(back,(330,500))

    pygame.display.update()
    clock.tick(60)

pygame.quit()