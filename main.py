# Kolejne kroki tworzenia gry:
#
# Po zaimportowaniu biblioteki Pygame, określamy rozmiar okna gry i kolory, tworzymy okno i wczytujemy grafiki postaci,
# pocisków i serduszek. Ustawiamy również pozycję początkową postaci i pocisku oraz inicjujemy zmienne wyniku i ilości żyć.
# Następnie definiujemy funkcje rysującą postać i pociski na ekranie oraz aktualizującą pozycję pocisków.
# Sprawdzamy również kolizje postaci z pociskami za pomocą masek.Dzięki czemu jako pole kolizji uzyskujemy dokładny kształt modelu postaci.
# W pętli głównej obsługujemy zdarzenia Pygame, aktualizujemy pozycję pocisków i sprawdzamy kolizje, rysujemy obiekty, wyświetlamy wynik i liczby żyć,
# a także obsługujemy skok postaci i opadanie.
#

import pygame
import random


# inicjalizacja Pygame
pygame.init()

# rozmiar okna gry
window_width = 1000
window_height = 800

# kolory
white = (255, 255, 255)
black = (0, 0, 0)

# utworzenie okna
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Bullet wind")

# wczytanie grafiki postaci i pocisków

player_img = pygame.image.load("player_1.png").convert_alpha()

bullet_img = pygame.image.load("bullet1.png").convert_alpha()

heart_img = pygame.image.load("heart.png").convert_alpha()

player_mask = pygame.mask.from_surface(player_img)
bullet_mask = pygame.mask.from_surface(bullet_img)

player_width = 150
player_height = 150
bullet_width = 134
bullet_height = 100
heart_width = 115
heart_height = 81

# pozycja początkowa postaci
player_x = 50
player_y = window_height - player_height - 50

#pozycja poczatkowa pocisku
bullet_x = window_width
bullet_y = random.randint(0, window_height - bullet_height)


# czas trwania gry
game_time = 0

# wynik gracza
score = 0

# życia gracza
lives = 1
hearts = [True] * lives

#podwójny skok
can_double_jump = True


# funkcja rysująca postać i pociski na ekranie
def draw_objects():
    # rysowanie postaci
    window.blit(player_img, (player_x, player_y))
    # rysowanie pocisku
    window.blit(bullet_img, (bullet_x, bullet_y))
    # rysowanie serduszek
    for i in range(lives):
        if hearts[i]:
            window.blit(heart_img, (window_width - (i + 1) * heart_width, 10))

# funkcja aktualizująca pozycje pocisków
def update_bullet():
    global bullet_x, bullet_y
    bullet_x -= 3 + (score // 20)

    # zmiana kierunku pocisku, jeśli ten dotrze do końca ekranu
    if bullet_x < 0:
        bullet_x = window_width
        bullet_y = random.randint(0, window_height - bullet_height)

def check_collisions_mask():
    global hearts, lives
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_width, bullet_height)

    # utwórz maski
    player_mask = pygame.mask.from_surface(player_img)
    bullet_mask = pygame.mask.from_surface(bullet_img)

    # sprawdź kolizję z maskami
    if player_rect.colliderect(bullet_rect):
        # kolizja z pociskiem
        if player_mask.overlap(bullet_mask, (bullet_rect.left - player_rect.left, bullet_rect.top - player_rect.top)):
            lives -= 1
            if lives < 1:
                return False



# pętla główna gry
game_running = True
while game_running:
    # obsługa zdarzeń Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y == window_height - player_height:
                # skok postaci
                player_y -= 150




    # aktualizacja pozycji pocisków
    update_bullet()

    # sprawdzenie kolizji postaci z pociskami
    check_collisions_mask()

    # rysowanie obiektów na ekranie
    window.fill(white)
    draw_objects()

    # wyświetlenie wyniku i liczby żyć
    font = pygame.font.Font(None, 30)
    score_text = font.render("Wynik: " + str(score), True, black)
    lives_text = font.render("Życia: " + str(lives), True, black)
    window.blit(score_text, (10, 10))
    window.blit(lives_text, (10, 40))
    # aktualizacja czasu gry i wyniku
    game_time += 1
    score = game_time // 60

    #jeśli gracz stracił wszystkie życia, koniec gry
    if lives == 0:
        game_running = False

    # obsługa skoku postaci
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if player_y == window_height - player_height:
            # pierwszy skok
            player_y -= 150
        elif player_y == window_height - player_height - 150:
            # drugi skok
            player_y -= 150

    # opadanie postaci po skoku
    if player_y < window_height - player_height:
        player_y += 2
     # wyświetlenie zmian na ekranie
    pygame.display.update()



# wyświetlenie końcowego wyniku
window.fill(white)
font = pygame.font.Font(None, 50)
game_over_text = font.render("GAME OVER", True, black)
score_text = font.render("Wynik: " + str(score), True, black)
window.blit(game_over_text, (window_width // 2 - 100, window_height // 2 - 50))
window.blit(score_text, (window_width // 2 - 75, window_height // 2))
pygame.display.update()

# oczekiwanie na zamknięcie okna
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
