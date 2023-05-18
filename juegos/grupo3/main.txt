import pygame, sys
import time
import random
pygame.init()

# Creating the screen
display = pygame.display.set_mode((700, 500))
pygame.display.set_caption('STAR LABS')

# Defining the colors
COLORS = {}
COLORS["blue"] = (0, 0, 50)
COLORS["red"] = (75, 0, 0)
COLORS["green"] = (0, 75, 0)
COLORS["gray"] = (175, 175, 175)
option_colors = [COLORS["blue"], COLORS["blue"], COLORS["blue"]]

# Defining the fonts we will use and the create the texts with them
FONTS = {}
TEXT = {}
RECTS = {}

TEXT["menu"] = pygame.font.Font('font.ttf', 50).render("Trivia game", True, COLORS["gray"])
RECTS["menu"] = TEXT["menu"].get_rect()
RECTS["menu"].center = (350, 200)

FONTS["text"] = pygame.font.Font('font.ttf', 20)
TEXT["subtitle"] = FONTS["text"].render("Play", True, COLORS["gray"])
RECTS["subtitle"] = TEXT["subtitle"].get_rect()
RECTS["subtitle"].center = (350, 287.5)

TEXT["retry"] = FONTS["text"].render("Return to menu", True, COLORS["gray"])
RECTS["retry"] = TEXT["retry"].get_rect()
RECTS["retry"].center = (350, 287.5)

FONTS["stars"] = pygame.font.Font('font.ttf', 40)
TEXT["stars"] = FONTS["stars"].render("0", True, COLORS["gray"])


# Loading the images
background = pygame.transform.scale(pygame.image.load("background.jpg"), [700, 500])
astronaut = pygame.transform.scale(pygame.image.load("astronaut.png"), [250,249])
astronaut_waiting = pygame.transform.scale(pygame.image.load("astronaut_waiting.png"), [250,249])
star = pygame.transform.scale(pygame.image.load("star.png"), [50, 50])

# Definig initial values
trivia_length = 15
question = 0
sleep = False
menu = True
end_screen = False
check_question = False
stars = 0
options = [1, 2, 3]
random.shuffle(options)

# Defining the questions we will use
trivia = [
    ["How many bones does the human body have?", "208", "300", "206"],
    ["Which is the only mammal that can fly?", "bat", "pig", "elephant"],
    ["How many valves does the human heart have?", "four", "two", "three"],
    ["What is the process by which plants feed called?", "photosynthesis", "mitosis", "digestion"],
    ["Which is bigger an atom or a cell?", "cell", "atom", "the same"],
    ["How many hearts does an octopus have?", "three", "eight", "four"],
    ["How much is 9x6?", "54", "44", "68"],
    ["How much is 24/2?", "12", "3", "9"],
    ["What is the perimeter of a circle called?", "circumference", "radius", "diameter"],
    ["How much is 55/5?", "11", "10", "12"],
    ["What is the only number that is prime and even?", "2", "0", "4"],
    ["What is the triangle with three equal sides called?", "equilateral", "isosceles", "scalene"],
    ["How many sides does a heptagon have?", "7", "6", "8"],
    ["What are the three primary colors?", "yellow, blue, & red", "green, yellow, & red", "blue, red, & white"],
    ["Who painted The Last Supper?", "Leonardo da Vinci", "Vincent van Gogh", "Pablo Picasso"],
    ["What is the most-sold book in history?", "The Bible", "Don Quijote", "The Little Prince"],
    ["How many musical notes are there?", "12", "13", "16"],
    ["Who wrote One Hundred Years of Solitude?", "Gabriel García Márquez", "Rafael Pombo", "Álvaro Mutis"],
    ["How many rings are on the Olympic flag?", "five", "four", "six"],
    ["Who is the footballer with the most golden balls?", "Lionel Messi", "Cristiano Ronaldo", "Neymar"],
    ["What is the most popular sport in the world?", "Football", "Basketball", "Tennis"],
    ["Which football team has won the most World Cups?", "Brazil", "Germany", "Italy"],
    ["In what year did the Second World War end?", "1945", "1939", "1941"],
    ["Which are the largest and smallest countries?", "Russia and Vatican City", "Canada and Monaco", "China and Liechtenstein"],
    ["Which is the largest river in the world?", "Amazon River", "Nile River", "Mississippi River"],
    ["Which is the largest ocean in the world?", "Pacific Ocean", "Atlantic Ocean", "Indian Ocean"],
    ["In what year did the Berlin Wall fall?", "1989", "1991", "1987"],
    ["How long did the Hundred Years War last?", "116 years", "100 years", "85 years"],
    ["Which is the coldest place in the world?", "Antarctica", "Siberia", "Alaska"]
]

#Selecting five random questions
random.shuffle(trivia)
questions = trivia[:trivia_length]

while True:
    retry = False
    election = 0
    display.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.mouse.get_pos() 
            if menu or end_screen:
                if click[0] >= 220 and click[0] <= 480 and click[1] >= 250 and click[1] <= 325:
                    menu = False 
                    retry = True
            elif 30 <= click[0] <= 370 and 200 <= click[1] <= 450:
                if click[1] <= 275:
                    election = 1
                elif click[1] >= 285 and click[1] <= 360:
                    election = 2
                elif click[1] >= 370:
                    election = 3
    if menu: 
        pygame.draw.rect(display, COLORS["gray"], (220, 250, 260, 80), border_radius=90)
        pygame.draw.rect(display, COLORS["blue"], (225, 255, 250, 70), border_radius=90)
        display.blit(TEXT["menu"], RECTS["menu"])
        display.blit(TEXT["subtitle"], RECTS["subtitle"])
    
    elif not end_screen: 
        if election > 0:
            option_colors[options.index(1)] = COLORS["green"] 
            if questions[question][1] == questions[question][options[election-1]]:
                stars += 1
                TEXT["stars"] = FONTS["stars"].render(str(stars), True, COLORS["gray"])
                display.blit(astronaut, (60+340, 200))
            else:
                option_colors[election-1] = COLORS["red"]
                display.blit(astronaut_waiting, (60+340, 200))
            sleep = True
            check_question = True
        else:
            display.blit(astronaut_waiting, (60+340, 200))
        pygame.draw.rect(display, COLORS["gray"], (30, 50, 640, 105), border_radius=35)
        pygame.draw.rect(display, COLORS["blue"], (35, 55, 630, 95), border_radius=35)
        pygame.draw.rect(display, COLORS["gray"], (30, 200, 340, 80), border_radius=90)
        pygame.draw.rect(display, option_colors[0], (35, 205, 330, 70), border_radius=90)
        pygame.draw.rect(display, COLORS["gray"], (30, 285, 340, 80), border_radius=90)
        pygame.draw.rect(display, option_colors[1], (35, 290, 330, 70), border_radius=90)
        pygame.draw.rect(display, COLORS["gray"], (30, 370, 340, 80), border_radius=90)
        pygame.draw.rect(display, option_colors[2], (35, 375, 330, 70), border_radius=90)
        Title = FONTS["text"].render(questions[question][0], True, COLORS["gray"])
        TitleRect = Title.get_rect()
        TitleRect.center = (350, 100)
        display.blit(Title, TitleRect)
        for i in range(3):
            Text = FONTS["text"].render(questions[question][options[i]], True, COLORS["gray"])
            TextRect = Text.get_rect()
            TextRect.center = (200, 237.5+(i)*85)
            display.blit(Text, TextRect)
        if check_question:
            random.shuffle(options)
            question += 1
            if question > trivia_length-1:
                end_screen = True
            check_question = False
        display.blit(TEXT["stars"], (display.get_width()-TEXT["stars"].get_width()-star.get_width(), display.get_height()-TEXT["stars"].get_height()))
        display.blit(star, (display.get_width()-star.get_width(), display.get_height()-star.get_height()))
        if sleep:
            pygame.display.update()
            time.sleep(0.5)
            option_colors = [COLORS["blue"], COLORS["blue"], COLORS["blue"]]
            sleep = False
    else:
        pygame.draw.rect(display, COLORS["gray"], (220, 250, 260, 80), border_radius=90)
        pygame.draw.rect(display, COLORS["blue"], (225, 255, 250, 70), border_radius=90)
        scoreprompt = f"Your score was {stars}/{trivia_length}."
        Text = FONTS["text"].render(scoreprompt, True, COLORS["gray"])
        TextRect = Text.get_rect()
        TextRect.center = (350, 187.5)
        if retry:
            menu = True 
            end_screen = False
            question = 0 
            stars = 0
            TEXT["stars"] = FONTS["stars"].render("0", True, COLORS["gray"])
            random.shuffle(trivia)
            questions = trivia[:trivia_length]
        display.blit(Text, TextRect)
        display.blit(TEXT["retry"], RECTS["retry"])
    pygame.display.update()
