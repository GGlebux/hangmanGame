import sys
import pygame
from random import choice
import math
import os


pygame.init()



# Настройка дисплея
WIDTH = 1000
HEIGHT = 1000
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Hangman game')
pygame.display.set_icon(pygame.image.load('images/hangman_logo.jpg'))
back_ground = pygame.image.load('images/hangman_logo.jpg')
lose_screen = pygame.image.load('images/Anime_black.png')
win_screen = pygame.image.load('images/Anime_white.png')

# Установка шрифта и текстов
my_font = pygame.font.Font('fonts/AniMeMatrix-MB_EN.ttf', 20)
word_font = pygame.font.Font('fonts/AniMeMatrix-MB_EN.ttf', 50)
congrat = pygame.font.Font('fonts/AniMeMatrix-MB_EN.ttf', 70)
welcome_text = my_font.render('Welcome To Hangman', True, (115, 5, 5))

# Установка звуков
sound_win = pygame.mixer.Sound('sounds/laugh-girl.mp3')
sound_lost = pygame.mixer.Sound('sounds/suffocation.mp3')
sound_right = pygame.mixer.Sound('sounds/light_exhalation.mp3')
sound_wrong = pygame.mixer.Sound('sounds/wrong.mp3')
back_ground_sounds = pygame.mixer.Sound('sounds/back_ground.mp3')
back_ground_sounds.play()

# Загрузка картинок
hangman_pic = [
    pygame.image.load('images/hangman/hangman_logo0.png'),
    pygame.image.load('images/hangman/hangman_logo1.png'),
    pygame.image.load('images/hangman/hangman_logo2.png'),
    pygame.image.load('images/hangman/hangman_logo3.png'),
    pygame.image.load('images/hangman/hangman_logo4.png'),
    pygame.image.load('images/hangman/hangman_logo5.png'),
    pygame.image.load('images/hangman/hangman_logo6.png')
]

class Pass():
    pass

def select_word():
    with open('texts/words.txt') as wordd:
        words_list = wordd.readlines()
    return choice(words_list).strip()


# Игровые переменные
hangman_pic_count = 0
word = select_word().upper()
guessed = []

# Переменные кнопок
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 850
A = 65
for i in range(26):
    x = startx + GAP * 2 + (RADIUS * 2 + GAP) * (i % 13)
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])


def draw():
    screen.blit(hangman_pic[hangman_pic_count], (0, 0))
    screen.blit(welcome_text, (10, 10))
    # Отображение слова
    display_word = ''
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
    text = word_font.render(display_word, 1, ((115, 5, 5)))
    screen.blit(text, (400, 100))
    # Отображение кнопок
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), RADIUS, 1)
            text = my_font.render(ltr, True, (115, 5, 5))
            screen.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

    pygame.display.update()


def display_message(message, won=True):
    pygame.time.delay(1000)
    screen.fill('Black')
    text = congrat.render(message, 1, (115, 5, 5))
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 200))
    if won:
        screen.blit(win_screen, (WIDTH / 2 - win_screen.get_width() / 2, 450))
    else:
        screen.blit(lose_screen, (WIDTH / 2 - win_screen.get_width() / 2, 450))
    pygame.display.update()
    pygame.time.delay(4000)


def main():
    global hangman_pic_count
    # Установка игрового цикла
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    clock.tick(FPS)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_pic_count += 1
                                sound_wrong.play()
                            else:
                                sound_right.play()
        draw()
        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break
        if won:
            sound_win.play()
            display_message('!You SURVIVED!')
            break
        if hangman_pic_count == 6:
            sound_lost.play()
            display_message('): You DIED :(', False)
            break


main()
pygame.quit()
sys.exit()