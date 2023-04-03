import random
import time
import pygame, sys
from pygame.locals import QUIT
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


pygame.init()
textfont = pygame.font.Font('freesansbold.ttf', 24)
menuTitle = pygame.font.Font('freesansbold.ttf', 50).render("Trivia game", True, WHITE)
pygame.mixer.music.load("tutorial.mp3")
pygame.mixer.music.play(-1)

menuTitleRect = menuTitle.get_rect()
menuTitleRect.center = (350, 200)
subTitle = textfont.render("Play game", True, BLACK)
subTitleRect = subTitle.get_rect()
subTitleRect.center = (350, 287.5)
retryButtonTitle = textfont.render("Return to menu", True, BLACK)
retryButtonTitleRect = retryButtonTitle.get_rect()
retryButtonTitleRect.center = (350, 287.5)

questions = [
    ['¿Quién pintó la obra "La Gioconda"?', "Leonardo da Vinci", "Pablo Picasso", "Miguel Ángel"],
    ['¿Cuál es la capital de España?', "Madrid", "Barcelona", "Valencia"],
    ['¿En qué año se inició la segunda guerra mundial?', "1914", "1918", "1920"],
    ['¿Cuál es el rio mas largo del mundo?', "Nilo", "Amazonas", "Yangtze"],
    ['¿Quén escribió "Cien Años de Soledad"?', "Gabriel García Márquez", "Mario Vargas Llosa", "Pablo Neruda"],
    ['¿Cuál es la moneda oficial de Japón?', "Yen", "Dólar", "Euro"],
    ['¿En qué pais se encuentra la Torre Eiffel?', "Francia", "Italia", "Inglaterra"],
    ['¿Quién es el autor de la teoría de la relatividad?', "Albert Einstein", "Isaac Newton", "Galileo Galilei"],
    ['¿En qué pais se encuentra el Machu Picchu?', "Perú", "Argentina", "Chile"],
    ['¿Cuál es la capital de Italia?', "Roma", "Milán", "Venecia"],
    ['¿Quién compuso la famosa novena sinfonía?', "Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johan Sebastian Bach"],
    ['¿Cuál es la capital de México?', "Ciudad de México", "Guadalajara", "Monterrey"],
    ['¿En qué país se encuentra la ciudad de Marrakech?', "Marruecos", "Túnez", "Argelia"],
    ['¿Quién escribió "El Quijote"?', "Miguel de Cervantes", "Federico García Lorca", "Lope de Vega"],
    ['¿En qué país se encuentra la estatua de la libertad?', "Estados unidos", "Inglaterra", "Francia"],
    ['¿Quién pintó "La noche estrellada"?', "Vincent van Gogh", "Pablo Picasso", "Claude Monet"],
    ['¿En qué país se encuentra el Coliseo Romano?', "Italia", "Grecia", "España"],
    ['¿Quién escribió "Don Juan Tenorio"?', "José Zorrilla", "Miguel de Cervantes", "Lope de Vega"],
    ['¿Cuál es la fórmula química del agua?', "H2O", "CO2", "O2"],
    ['¿Cuál es el país más grande del mundo por área?', "Rusia", "Canadá", "Estados Unidos"],
    ['¿En qué año comenzó la Segunda Guerra Mundial?', "1939", "1914", "1945"],
    ['¿Cuál es el océano más grande del mundo?', "Pacífico", "Atlántico", "Índico"],
    ['¿Quién escribió la obra "Hamlet"?', "William Shakespeare", "Charles Dickens", "Jane Austren"],
    ['¿Cuál es el país más poblado del mundo?', "China", "India", "Estados Unidos"],
    ['¿En qué continente se encuentra Egipto?', "África", "Asia", "Europa"],
    ['¿En qué ciudad se encuentra el Coliseo Romano?', "Roma", "Atenas", "Barcelona"],
    ['¿Cuál es la capital de Australia?', "Canberra", "Sídney", "Melbourne"],
    ['¿Cuál es el animal terrestre más grande del mundo?', "Elefante africano", "Ballena azul", "Jirafa"]
]
questions_number = 5# Number from 1 to len(questions)

questions_to_ask = []
for i in range(questions_number):
    question = questions[random.randint(0, len(questions)-1)]
    while question in questions_to_ask:
        question = questions[random.randint(0, len(questions)-1)]
    questions_to_ask.append(question)

screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Trivia game')
current_question = 0

squarescolor = [WHITE, WHITE, WHITE]

sleep = False
end_screen = False

answers = []
for i in range(3):
    answer = random.randint(1, 3)
    while answer in answers:
        answer = random.randint(1, 3)
    answers.append(answer)
current_question += 1
question_answered = False


menu = True
score = 0

background = pygame.image.load("background.jpg")
while True:
    returnToMenu = False
    pressed_button = 0
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if menu or end_screen:
                if mouse_pos[0] >= 220 and mouse_pos[0] <= 480 and mouse_pos[1] >= 250 and mouse_pos[1] <= 325:
                    menu = False
                    returnToMenu = True
            elif mouse_pos[0] >= 50 and mouse_pos[0] <= 650 and mouse_pos[1] >= 200 and mouse_pos[1] <= 445:
                if mouse_pos[1] <= 275:
                    pressed_button = 1
                elif mouse_pos[1] >= 285 and mouse_pos[1] <= 360:
                    pressed_button = 2
                elif mouse_pos[1] >= 370:
                    pressed_button = 3

    if menu:
        pygame.draw.rect(screen, BLACK, (220, 250, 260, 80), border_radius=5)
        pygame.draw.rect(screen, WHITE, (225, 255, 250, 65), border_radius=5)

        screen.blit(menuTitle, menuTitleRect)
        screen.blit(subTitle, subTitleRect)

    elif end_screen:

        pygame.draw.rect(screen, BLACK, (220, 250, 260, 80), border_radius=5)
        pygame.draw.rect(screen, WHITE, (225, 255, 250, 65), border_radius=5)

        if score >= questions_number-(questions_number/3):
            scoreprompt = "¡Tu puntaje fue de "+str(score)+"/"+str(questions_number)+"!"
        elif score >= questions_number-(questions_number/2):
            scoreprompt = "Tu puntaje fue de "+str(score)+"/"+str(questions_number)+"."
        else:
            scoreprompt = "Tu puntaje fue de "+str(score)+"/"+str(questions_number)+". Intenta de nuevo"
        Text = textfont.render(scoreprompt, True, WHITE)
        TextRect = Text.get_rect()
        TextRect.center = (350, 187.5)

        if returnToMenu:
            menu = True
            end_screen = False
            current_question = 1
            score = 0
            questions_to_ask = []
            for i in range(questions_number):
                question = questions[random.randint(0, len(questions)-1)]
                while question in questions_to_ask:
                    question = questions[random.randint(0, len(questions)-1)]
                questions_to_ask.append(question)
            question_answered = False

        screen.blit(Text, TextRect)
        screen.blit(retryButtonTitle, retryButtonTitleRect)

    else:

        if pressed_button > 0:
            squarescolor[answers.index(1)] = GREEN
            if questions_to_ask[current_question-1][1] == questions_to_ask[current_question-1][answers[pressed_button-1]]:
                score += 1
            else:
                squarescolor[pressed_button-1] = RED
            sleep = True
            question_answered = True


        pygame.draw.rect(screen, BLACK, (30, 50, 640, 105), border_radius=5)
        pygame.draw.rect(screen, WHITE, (35, 55, 630, 90), border_radius=5)


        pygame.draw.rect(screen, BLACK, (50, 200, 600, 80), border_radius=5)
        pygame.draw.rect(screen, squarescolor[0], (55, 205, 590, 65), border_radius=5)

        pygame.draw.rect(screen, BLACK, (50, 285, 600, 80), border_radius=5)
        pygame.draw.rect(screen, squarescolor[1], (55, 290, 590, 65), border_radius=5)

        pygame.draw.rect(screen, BLACK, (50, 370, 600, 80), border_radius=5)
        pygame.draw.rect(screen, squarescolor[2], (55, 375, 590, 65), border_radius=5)

        Title = textfont.render(questions_to_ask[current_question-1][0], True, BLACK)
        TitleRect = Title.get_rect()
        TitleRect.center = (350, 100)

        screen.blit(Title, TitleRect)


        if len(questions_to_ask) >= current_question:
            for i in range(3):
                Text = textfont.render(questions_to_ask[current_question-1][answers[i]], True, BLACK)
                TextRect = Text.get_rect()
                TextRect.center = (350, 237.5+(i)*85)
                screen.blit(Text, TextRect)
        
        if question_answered:
            answers = []
            for i in range(3):
                answer = random.randint(1, 3)
                while answer in answers:
                    answer = random.randint(1, 3)
                answers.append(answer)

            current_question += 1

            question_answered = False
            if current_question > questions_number:
                end_screen = True

    pygame.display.update()
    if sleep:
        time.sleep(0.5)
        squarescolor = [WHITE, WHITE, WHITE]
        sleep = False