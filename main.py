import random
import time
import pygame, sys
from pygame.locals import QUIT
pygame.init()

# Start the music to repeat forever:
pygame.mixer.music.load("musica.mp3")
pygame.mixer.music.play(-1)

# Colors:
WHITE = (255, 255, 255) # Color of the buttons
RED = (255, 0, 0) # Color for wrong answers
GREEN = (0, 255, 0) # Color for right answers
BLACK = (0, 0, 0) # Color for text and buttons' outlines
TITLE = (255, 255, 255) # Color of text outside buttons

# The font used for most text in the game:
textfont = pygame.font.Font('freesansbold.ttf', 24)
# The font used for the title in the main menu:
menuTitle = pygame.font.Font('freesansbold.ttf', 50).render("Juego de trivia", True, TITLE)

# Position of the main menu title
menuTitleRect = menuTitle.get_rect()
menuTitleRect.center = (350, 200)

# Text in the Play game button
subTitle = textfont.render("Jugar", True, BLACK)
subTitleRect = subTitle.get_rect()
subTitleRect.center = (350, 287.5)

# Text in the Retry button at the eng of the game
retryButtonTitle = textfont.render("Volver al menú", True, BLACK)
retryButtonTitleRect = retryButtonTitle.get_rect()
retryButtonTitleRect.center = (350, 287.5)


# Each question has 3 possible anwers, in the array, the first element is always the question and the following one is the correct answer, followed by two other possible answers
questions = [
    ['¿Quién pintó la obra "La Gioconda"?', "Leonardo da Vinci", "Pablo Picasso", "Miguel Ángel"],
    ['¿Cuál es la capital de España?', "Madrid", "Barcelona", "Valencia"],
    ['¿En qué año se inició la primera guerra mundial?', "1914", "1918", "1920"],
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
    ['¿Cuál es el animal terrestre más grande del mundo?', "Elefante africano", "Ballena azul", "Jirafa"],
]
questions_number = 5 # The number of questions that you will be asked

# Select from all the possible answers the ones that you will be asked using the for loop
questions_to_ask = []
for i in range(questions_number):
    question = questions[random.randint(0, len(questions)-1)]

    # This section makes sure all the questions are different by selecting again a random answer until the one selected isn't repeated at all in the questions to ask array
    while question in questions_to_ask:
        question = questions[random.randint(0, len(questions)-1)]
    
    questions_to_ask.append(question)

# Setting up the window:
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption('Juego')

# Setting up some default values:
# To let the game know on which question of all the questions in the questions to ask array are you, where 1 is the first one
current_question = 0
# The color of each one of the three squares with answers in the main game
squarescolor = [WHITE, WHITE, WHITE]
# When it is True the game will stop for 0.5 seconds
sleep = False
# When it is true the menu will be displayed
menu = True
# When it is true the end screen will be displayed
end_screen = False
#* if none of above are True then the main game will be displayed until end_screen is True
# If you choose an answer this one will be True and the game will check wether it is correct or not
question_answered = False
# Setting score as 0 at the beggining of the game
score = 0
# Loading the background, scaled to fill the screen
background = pygame.transform.scale(pygame.image.load("background.jpg"), [700, 500])

# An array with three numbers randomly organized. The position of these numbers will decide the order of the answers. Each time question answered is True this array will be randomly arranged again
answers = []
for i in range(3):
    answer = random.randint(1, 3)
    while answer in answers:
        answer = random.randint(1, 3)
    answers.append(answer)

while True:
    # returnToMenu can only be True during one whole frame, at the beggining of the next one it will be turned to False again
    returnToMenu = False
    # 0 Means no button was pressed, 1-3 indicates an answer was chosen
    pressed_button = 0
    # Display the background
    screen.blit(background, (0, 0))

    # Events:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # If any mouse button is pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos() # an array with x and y position
            # Since the position for the Retry and Start game in both Main menu and End Screen is the same
            if menu or end_screen:
                if mouse_pos[0] >= 220 and mouse_pos[0] <= 480 and mouse_pos[1] >= 250 and mouse_pos[1] <= 325:
                    menu = False # Exit the menu in case you are in the menu
                    returnToMenu = True # This will be True for the rest of the current frame

            # If we are in the main game compare the position of the mouse with the position and size of each of the 3 answer buttons
            elif mouse_pos[0] >= 50 and mouse_pos[0] <= 650 and mouse_pos[1] >= 200 and mouse_pos[1] <= 445:
                if mouse_pos[1] <= 275:
                    pressed_button = 1

                elif mouse_pos[1] >= 285 and mouse_pos[1] <= 360:
                    pressed_button = 2

                elif mouse_pos[1] >= 370:
                    pressed_button = 3

    if menu: # The menu is very simple:
        # Draw a big black square and a white one on top of it to illustrate a button, this will be repeated for all buttons in the game
        pygame.draw.rect(screen, BLACK, (220, 250, 260, 80), border_radius=5)
        pygame.draw.rect(screen, WHITE, (225, 255, 250, 65), border_radius=5)

        # Show the "Juego de trivia" text
        screen.blit(menuTitle, menuTitleRect)
        # Show the "Jugar" text
        screen.blit(subTitle, subTitleRect)

    elif end_screen:
        # Create a button identical to the one seen in the menu screen
        pygame.draw.rect(screen, BLACK, (220, 250, 260, 80), border_radius=5)
        pygame.draw.rect(screen, WHITE, (225, 255, 250, 65), border_radius=5)

        # This code here decides if the score was high, regular or low compared to the questions number
        if score >= questions_number-(questions_number/3):
            scoreprompt = f"¡Tu puntaje fue de {score}/{questions_number}!"
        elif score >= questions_number-(questions_number/2):
            scoreprompt = f"Tu puntaje fue de {score}/{questions_number}."
        else:
            scoreprompt = f"Tu puntaje fue de {score}/{questions_number}. Intenta de nuevo"

        # The text to be shown here is decided by the code above, with three posibilities, it is displayed on top of the button drawn before
        Text = textfont.render(scoreprompt, True, TITLE)
        TextRect = Text.get_rect()
        TextRect.center = (350, 187.5)

        # If the button has been clicked
        if returnToMenu:
            menu = True # Turn it back to true since this variable is False during the whole main game and end screen
            end_screen = False
            current_question = 0 # Each time we answer a question this variable increases, so set it up to its initial value
            score = 0 # Reset the score

            # Decide again which questions to ask
            questions_to_ask = []
            for i in range(questions_number):
                question = questions[random.randint(0, len(questions)-1)]
                while question in questions_to_ask:
                    question = questions[random.randint(0, len(questions)-1)]
                questions_to_ask.append(question)
            question_answered = False

        screen.blit(Text, TextRect)
        screen.blit(retryButtonTitle, retryButtonTitleRect)

    else: # If we are not in the menu nor in the end screen, we are playing the main game
        # If a button has been pressed
        if pressed_button > 0:
            squarescolor[answers.index(1)] = GREEN # Color the right answer whith green (the element in the answers array whose value (1) corresponds to the index of the right answer of the question, remember the answers array is randomly organized so it could be [1, 2, 3], [3, 1, 2], and so on)
            if questions_to_ask[current_question][1] == questions_to_ask[current_question][answers[pressed_button-1]]:
                score += 1
                # If the answer we chose is the right answer increase our score
            else:
                squarescolor[pressed_button-1] = RED
                # Otherwise color the answer we wrote with red
            # Sleep for 0.5 seconds
            sleep = True
            # This indicates the game to do several thing we will see further on
            question_answered = True

        # Draw the Question's button (which is not clickable at all)
        pygame.draw.rect(screen, BLACK, (30, 50, 640, 105), border_radius=5)
        pygame.draw.rect(screen, WHITE, (35, 55, 630, 90), border_radius=5)

        # Draw the first option button
        pygame.draw.rect(screen, BLACK, (50, 200, 600, 80), border_radius=5)
        pygame.draw.rect(screen, squarescolor[0], (55, 205, 590, 65), border_radius=5)

        # Draw the second option button
        pygame.draw.rect(screen, BLACK, (50, 285, 600, 80), border_radius=5)
        pygame.draw.rect(screen, squarescolor[1], (55, 290, 590, 65), border_radius=5)

        # Draw the third option button
        pygame.draw.rect(screen, BLACK, (50, 370, 600, 80), border_radius=5)
        pygame.draw.rect(screen, squarescolor[2], (55, 375, 590, 65), border_radius=5)

        # Display a text with the question in it on screen
        Title = textfont.render(questions_to_ask[current_question][0], True, BLACK)
        TitleRect = Title.get_rect()
        TitleRect.center = (350, 100)
        screen.blit(Title, TitleRect)

        # Display the 3 answers of the current question on screen in the order indicated by the answers array
        for i in range(3):
            Text = textfont.render(questions_to_ask[current_question][answers[i]], True, BLACK)
            TextRect = Text.get_rect()
            TextRect.center = (350, 237.5+(i)*85)
            screen.blit(Text, TextRect)
        
        if question_answered:

            # Reorder the answers array again so that the correct answer of the next question isn't at the same position than the one before
            answers = []
            for i in range(3):
                answer = random.randint(1, 3)
                while answer in answers:
                    answer = random.randint(1, 3)
                answers.append(answer)

            # For changing the question
            current_question += 1

            # If there are no more answers, then we have reached the end and should go to the end screen on the next frame
            if current_question > questions_number-1:
                end_screen = True

            # Returning to False so this doesn't repeats until we answer another question
            question_answered = False

    # Updating the screen
    pygame.display.update()

    # This should be done here so that screen is updated before sleeping, also, here we set all squares' color back to white after sleeping
    if sleep:
        time.sleep(0.5)
        squarescolor = [WHITE, WHITE, WHITE]
        sleep = False