## ###   Here, some questions to be answered for understanding the game:
#
#       Question: How is the fish rotation angle calculated?
#
#       If the fish's y velocity is 0, the the angle is 90°   
#       If the fish's y velocity is less than 0 (Going up), then the angle is the velocity is 90 divided by (velocity squared times ROTATION_SPEED), a cuadratic function where ROTATION_SPEED is the amplitude
#       If the fish's y velocity is more than 0 (Going down), then the angle is same formula from before plus 90°



#       Question: How does gravity work?
#
#       Each physics object (Objects from a PhysicsObject class' inherited class, which means they have speed, gravity and position)
#       Has a different speed and, depending on is class, different particular attributes.
#       The program takes each one of these objects and increases their y velocity as per their gravity attribute



#       Question: How do hitboxes work?
#
#       The three dimensional array of hitboxes stores a number of arrays
#       each one of these array store two more arrays (That's why it's "three dimensional")
#       these two arrays represent the coordinates of what are
#       -> The position of the top left corner of the hitbox
#       -> And ints size
#       Using this values, the game checks later on for each one of the moving objects on-screen and each one of the hitboxes if they have collided

# Imported required modules
from source.sources import *

# Simple keyboard layout:

KEYS = [
    pygame.K_UP,    #0 for jumping
    pygame.K_RIGHT, #1 for going right
    pygame.K_LEFT   #2 for going left
]



# Starting pygame
pygame.init()


# Basic constant for finding assets in the filesystem
# (while still keeping the code easy to read and modify)
MATERIALSDIR = "materiales/"





# These work very well for easily managing hitboxes
PELICAN_SIZE = [75, 59,4]
PELICAN_SIZE_COEFFICENT = PELICAN_SIZE[0]/48 # Because the sprite of the pelican is 48 pixels width
# Take into accout that the height of the pelican is 71,25
# This number was decided because the sprite has 38 pixels of height
# This is around 1 pixel of height for each 1,3 of width
# Same proportion is applied here.
# This is so that the pelican works in game as we intended it when using the sprite





## Here, the screen:

# Uncomment for a fullscreen window
#SCREEN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#SCREEN_SIZE = SCREEN.get_size()

# Uncomment for a window of half the screen width
#del SCREEN
#SCREEN = pygame.display.set_mode((SCREEN_SIZE[0]/2, SCREEN_SIZE[1]))
#del SCREEN_SIZE
#SCREEN_SIZE = SCREEN.get_size()

# Uncomment for a custom window size
#del SCREEN
SCREEN = pygame.display.set_mode((1000, 650))
#del SCREEN_SIZE
SCREEN_SIZE = SCREEN.get_size()

pygame.display.set_caption("Asfghjklñ")
pygame.display.set_icon(pygame.image.load(MATERIALSDIR+"image/pelican/0"))


## Hiding the mouse
pygame.mouse.set_visible(0)



## Defining here some constants:

# Physics:
GRAVITY = 0.6
PELICAN_JUMP = 10
FISH_JUMP = 20
PELICAN_SPEED = 6
ROTATION_SPEED = 0.02 # For fish, the only rotating objects



## Sizes:
BULLET_SIZE = 20
SEA_HEIGHT = 100


# We don't need to store boat's width since we won't need it for anything
BOAT_HEIGHT = 100



## Collision things
SEA_OFFSET = 20
Y_LIMIT = SCREEN_SIZE[1]-SEA_HEIGHT+SEA_OFFSET
PELICAN_HITBOXES = [
    [
        [1,   9], #< This is the position of the superior left corner of the hitbox relative to the pelican image
        [20, 10]  #< This is the width and height of the hitbox
    ],            
    [             # # # # # # # # # # # #    # # # # # # # # # # #   
        [15, 13], #  +-------+-----------+  # A rough representaion #  (*) 2 and 3 together work kind of how a circle would
        [25, 14]  #  |   1   | +-2----+  |  # of how the hitboxes   #
    ],            #  +-------+-|------|--+  #   would look like    # 
    [             #  |       | |      |  |    # # # # # # # # #   #  
        [21, 12], #  |       +-|------|3-+                      #  # 
        [14, 19]  #  +---------+------+--+                          #
    ]             # # # # # # # # # # # # # # # # # # # # # # #      
]
    # The hitboxes aren't defined within the Pelican class since the hitboxes are the same for all pelicans and this numbers are to be used several times in the code





## Frames per second
FPS = 60
# In pixels per frame
BKG_SPEED = 1
SEA_SPEED = 2



# Waiting things
FISH_WAITING = 1 # (In seconds)
BOAT_APPEARANCE_WAIT= 0.5 # (In seconds)
FISH_APPEARANCE_WAIT = 0.5 # (In seconds)
TEXT_DISAPEARANCE_TIME = 1 # (In seconds)



#Probability things
BOAT_INITIAL_PROBABILITY = 50
FISH_INITIAL_PROBABILITY= 50
boat_probability = BOAT_INITIAL_PROBABILITY
fish_probability = FISH_INITIAL_PROBABILITY




# Font for text in our game
FONT = pygame.font.Font(MATERIALSDIR+"/font/font.otf", 32)


## ## Now, we must define our classes

## The size of the images are numbers we must always take into account

# Loading most of the images
class Sprite():
    def __init__(self, image_location, size, flip=False):
        image = pygame.image.load(MATERIALSDIR+"image/"+image_location)
        self.source_size = image.get_size()
        if flip:
            self.surface = pygame.transform.flip(pygame.transform.scale(image, [size[0], size[1]]), True, False)
        else:
            self.surface = pygame.transform.scale(image, [size[0], size[1]])


# Pelican frames organizing in an array with two sets (1 normal an another one flipped) of the several frames in the pelican animation
PELICAN_FRAMES = []
for frame in ls(MATERIALSDIR+"image/pelican"): # Appending every file in the pelican frames directory to the array
    PELICAN_FRAMES.append(Sprite("pelican/"+frame, [PELICAN_SIZE[0], PELICAN_SIZE[1]])) # Frames must be named in alphabetic order, and are foud with the os.listdir function (ls)

for frame in range(len(PELICAN_FRAMES)): # Now add another set of flipped surfaces
    PELICAN_FRAMES.append(Sprite("pelican/"+str(frame), [PELICAN_SIZE[0], PELICAN_SIZE[1]], True))


BACKGROUND_IMAGE    =    Sprite("background",           SCREEN_SIZE)
BULLET_IMAGE        =    Sprite("bullet",     [1    ,   2         ])
BOAT_IMAGE          =    Sprite("boat",       [168  ,   100       ])
BOAT_IMAGE_FLIPPED  =    Sprite("boat",       [168  ,   100       ], flip=True)
SEA_IMAGE           =    Sprite("sea",        [200  ,   SEA_HEIGHT])

## From this one we create fish species objects (not the fishes themselves) that store information about the fish
class defineNewSpecie():
    def __init__(self, name, value, size):
        self.value = value
        self.sprite = pygame.transform.scale(pygame.image.load(MATERIALSDIR+"/image/fish/"+name), size)
        self.size = size

        self.probability = None

## And now defining specifically each species so that we can apply this values in fish's constructor method

fish_species = [ # There is a total of 15 (and the erizo) species in the game

    defineNewSpecie(name="erizo", value=-1, size=[18, 36]),

    defineNewSpecie("clownfish",    1,    [18, 36]),
    defineNewSpecie("sargento",     2,    [18, 36]),
    defineNewSpecie("dory",         2,    [18, 36]),
    defineNewSpecie("cojinua",      6,    [18, 36]),
    defineNewSpecie("mojarra",      8,    [18, 36]),
    defineNewSpecie("palometa",     9,    [18, 36]),
    defineNewSpecie("caballa",     10,    [18, 36]),
    defineNewSpecie("dorado",      12,    [18, 36]),
    defineNewSpecie("atun",        13,    [18, 36]),
    defineNewSpecie("salmon",      14,    [18, 36]),
    defineNewSpecie("cusk",        16,    [18, 36]),
    defineNewSpecie("saithe",      17,    [18, 36]),
    defineNewSpecie("monkfish",    19,    [18, 36]),
    defineNewSpecie("cod",         21,    [18, 36]),
    defineNewSpecie("bigeye",      22,    [18, 36])
   
    # Ideally, the sum of all probabilities should be 100 (It's a percentage)
]

stages = [
    { # Stage 1
        "name"      : "Reef",
        "max score" : 35,

        "sargento"  : 40,
        "clownfish" : 30,
        "dory"      : 25,
        "erizo"     : 5,
        "boats"     : 0
    },

    { # Stage 2
        "name" : "Shore",
        "max score" : 180,

        "cojinua"   : 25,
        "mojarra"   : 25,
        "palometa"  : 25,
        "erizo"     : 15,
        "boats"     : 10
    },

    { # Stage 3
        "name" : "Warm Ocean",
        "max score" : 450,

        "caballa"   : 20,
        "dorado"    : 20,
        "atun"      : 20,
        "erizo"     : 20,
        "boats"     : 20
    },

    { # Stage 4
        "name" : "Cold Ocean",
        "max score" : 450,

        "salmon"    : 15,
        "cusk"      : 15,
        "saithe"    : 15,
        "erizo"     : 30,
        "boats"     : 25
    },

    { # Stage 5
        "name" : "Deep Cold Ocean",
        "max score" : 450,

        "monkfish"  : 10,
        "cod"       : 10,
        "bigeye"    :  5,
        "erizo"     : 40,
        "boats"     : 35
    },
]

stage = 0

def ChangeStage():
    for specie in fish_species:
        if specie.name in stages[stage]:
            specie.probability = stages[stage][specie.name]
        else:
            specie.probability = 0
    boat_probability = stages[stage]["boats"]

## This class makes it easier to work with objects that move along the screen
class PhysicsObject():
    velocity = [0, 0]   # These are the attributes each instance of an inherited class is supposed to be assigned
    position = None     #
    # The velocity is a two elemt array, since objects move in a two dimensional space.
    # [Xspeed, Yspeed]

    gravity = GRAVITY # If needed, this value will be set to 0 in inherited classes

    # A physicsObject should have no more attributes by itself
    # I am not taking into account any kind of interaction between objects

    # Now a method for moving the object:

def move(obj):
    obj.velocity[1] += obj.gravity
    obj.position[0] += obj.velocity[0]
    obj.position[1] += obj.velocity[1]



## Score texts are also objects who moves trough screen, with an alpha value and a surface with text
class ScoreText(PhysicsObject):
    velocity = [0, -5]
    gravity = 0 # It will just go upwards
    alpha = 255
    def __init__(self, text, position, color, outline):
        self.text = render(text, FONT, color, outline)
        self.position = position



class Boat(PhysicsObject):
    def __init__(self):
        self.position = [[-BOAT_IMAGE.surface.get_width(), SCREEN_SIZE[0]][random(0, 1)], Y_LIMIT-BOAT_IMAGE.surface.get_height()]
        self.gravity = 0
        if self.position[0] == -BOAT_IMAGE.surface.get_width(): # Which means the boat starts from the left of the screen
            self.velocity = [6, 0]
        else:
            self.velocity = [-6, 0]
        self.bulletpoint = random(0, SCREEN_SIZE[0]-BOAT_IMAGE.surface.get_width())



class Fish(PhysicsObject):

    specie = None

    def __init__(self):
        self.velocity = [0, 0]
        self.gravity = 0
        self.wait = 0
        self.waiting = True

        _random = random(0, 100)
        probability = 0

        for specie in fish_species:
            probability += specie.probability

            if _random <= probability:
                self.specie = specie
                break
        
        self.position = [random(0, SCREEN_SIZE[0]-self.specie.size[0]), Y_LIMIT-self.specie.size[0]/5*6]

    def angle(self):
        if self.waiting          : return 0
        if self.velocity[1] <  0 : return 90/(ROTATION_SPEED * self.velocity[1]**2+1)
        if self.velocity[1] == 0 : return 90
        if self.velocity[1]  > 0 : return 180-90/(ROTATION_SPEED*self.velocity[1]**2+1)




class Bullet(PhysicsObject):
    def __init__(self, position, pelican): # Initial position is only one value since all boats are at the same height of the screen, only thing that varies is x position
        self.gravity = 0
        self.position = [position+21,Y_LIMIT-50] # The additions are in order to position the bullet at the center of the boat and its objective at the center of the pelican

        # The following code calculates the x and y velocity so that the sum of both is 7 and direction is the same
        difference = [abs((pelican.position[0]+PELICAN_SIZE[0]/2) - (position+21)), abs((pelican.position[1]+PELICAN_SIZE[1]/2) - (Y_LIMIT+50))]
        lack = 7*sqrt(difference[0]**2 + difference[1]**2)/(difference[0]**2 + difference[1]**2)
        lack = [lack*difference[0], lack*difference[0]]
        self.velocity = lack



### And finally, here we got the pelican
class Pelican(PhysicsObject):

    animation_speed = 5 # In frames per second

    current_frame = 0 # Initial frame

    looking_right = False # By default the sprite is looking left, so with this we can know when to flip it

    position = [(SCREEN_SIZE[0]/2 - PELICAN_SIZE[0]/2), (SCREEN_SIZE[1]/3-PELICAN_SIZE[0]/2)]# Initial position





def findHitboxes(pelican):
    hitboxes = []
    for hitbox in PELICAN_HITBOXES:
        global_size = [hitbox[1][0]*PELICAN_SIZE_COEFFICENT, hitbox[1][1]*PELICAN_SIZE_COEFFICENT]
        if  pelican.looking_right:
            center = [PELICAN_SIZE[0] - hitbox[0][0]*PELICAN_SIZE_COEFFICENT - global_size[0]/2 + pelican.position[0], hitbox[0][1]*PELICAN_SIZE_COEFFICENT+pelican.position[1] + global_size[1]/2]
        else:
            center = [hitbox[0][0]*PELICAN_SIZE_COEFFICENT+pelican.position[0] + global_size[0]/2, hitbox[0][1]*PELICAN_SIZE_COEFFICENT+pelican.position[1] + global_size[1]/2]
        hitboxes.append([center, global_size])

    return hitboxes # This function takes the current pelican object as an argument (so that later on multiple pelican objects can be created at once) and returns the position and size of each hitbox NOT relative to the pelican sprite but relative to the top left corner of the window
    # also, if the pelican is looking right, the hitboxes are flipped with it

# This function takes an object's position and size and compares it with the pelican's hitboxes
hasCollidedWithPelican = lambda hitbox, position, size : abs(position[0]+size[0]/2 - hitbox[0][0]) < hitbox[1][0] and abs(position[1]+size[1]/2 - hitbox[0][1]) < hitbox[1][1]



## Finally, and with everything configured, we must set up the constants for displaying images on screen the corresponding oreder:


DRAWSURFACES = {
    "Pelican"         : [],
    "Boats"           : [],
    "Fish"            : [],
    "Background"      : [],
    "Clouds"          : [],
    "Sea"             : [],
    "Bullets"         : [],
    "Text"            : [],
    "Titles"          : []
}   # Each one of this values will be altered by adding a surface
    # For example, for each bullet on screen an array with a surface and coordinates will be added to the "Bullets" key
    # For each element in each one of these arrays, each surface will be drawn


def addObject(obj, section):
    objects_in_game[section].append(obj)


def game():

    ChangeStage()

    global objects_in_game
    objects_in_game= {
        "Pelican" : [],
        "Fish"    : [],
        "Boats"   : []
    }

    # Adding the pelican on its initial position
    addObject(Pelican(), "Pelican")


    # The score must be 0 at the beginning, obviously
    score = 0

    # For scrolling
    SEA_WIDTH = SEA_IMAGE.surface.get_width()
    BKG_WIDTH = BACKGROUND_IMAGE.surface.get_width()
    
    # Initializing variables we will need:
    fish_waiting_tick = 0
    boat_waiting_tick = 0
    # Scroll, variabiles that define the offset of scrolling images from original position
    sea_scroll = 0
    bkg_scroll = 0

    while True:

        #SCREEN = pygame.display.set_mode(SCREEN_SIZE[0], SCREEN_SIZE[1])

        # For testing fish:
        #addObject(Fish(50), "Fish")



        # Calculating position of each hitbox
        hitboxes = findHitboxes(objects_in_game["Pelican"][0])


        # Remove surfaces from preceding frame
        DRAWSURFACES = {
                "Pelican"    :       [],
                "Boats"      :       [],
                "Fish"       :       [],
                "Background" :       [],
                "Clouds"     :       [],
                "Sea"        :       [],
                "Bullets"    :       [],
                "Text"       :       [],
                "Titles"     :       []
        }

        # Checking input

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                wexit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    wexit()
                elif event.key == pygame.K_UP:
                    objects_in_game["Pelican"][0].velocity[1] = -PELICAN_JUMP


        # This is for checking keys specifically in the KEYS dictionary
        # This are keys to be held by the user for a continuous output
        for key in KEYS:
            if pygame.key.get_pressed()[key]:
                if key == pygame.K_RIGHT:
                    objects_in_game["Pelican"][0].velocity[0] = PELICAN_SPEED
                    objects_in_game["Pelican"][0].looking_right = True
                elif key == pygame.K_LEFT:
                    objects_in_game["Pelican"][0].velocity[0] = -PELICAN_SPEED
                    objects_in_game["Pelican"][0].looking_right = False


        # Checking the current state of the game

        # Checking if it is moment to create a new fish

        if fish_waiting_tick == FISH_APPEARANCE_WAIT*FPS:

            if random(0, 100) <= fish_probability:

                addObject(Fish(), "Fish")

            fish_waiting_tick = 0
        
        else: fish_waiting_tick += 1

        # Checking if it is moment to create a new boat

        if boat_waiting_tick == BOAT_APPEARANCE_WAIT*FPS:

            if random(0, 100) <= boat_probability:

                addObject(Boat(), "Boats")
            
            boat_waiting_tick = 0
        
        else: boat_waiting_tick += 1


        # Checking fish's state

        deleted_items = 0
        for index in range(0, len(objects_in_game["Fish"])):

            index -= deleted_items


            if objects_in_game["Fish"][index].wait >= FISH_WAITING*FPS and objects_in_game["Fish"][index].waiting:
                objects_in_game["Fish"][index].gravity = GRAVITY
                objects_in_game["Fish"][index].velocity = [0, -FISH_JUMP]
                objects_in_game["Fish"][index].waiting = False
            elif objects_in_game["Fish"][index].position[1] >= Y_LIMIT:
                del objects_in_game["Fish"][index]
                deleted_items += 1
                continue
            elif objects_in_game["Fish"][index].waiting: objects_in_game["Fish"][index].wait += 1


            for hitbox in hitboxes:

                if hasCollidedWithPelican(hitbox, objects_in_game["Fish"][index].position, objects_in_game["Fish"][index].specie.size):

                    if  objects_in_game["Fish"][index].specie.value >= 0:
                        score += objects_in_game["Fish"][index].specie.value
                    else:
                        die()
                    del objects_in_game["Fish"][index]
                    deleted_items += 1

                    # Here we check if we must pass to the next stage
                    if score >= stages[stage]["max score"]:
                        stages += 1
                        if stages > len(stages):
                            pass # You won the game
                        ChangeStage()



                    break
            
        # Checking boats' state

        deleted_items = 0
        for index in range(0, len(objects_in_game["Boats"])):

            index -= deleted_items

            if objects_in_game["Boats"][index].position[0] < -BOAT_IMAGE.surface.get_width() or objects_in_game["Boats"][index].position[0] > SCREEN_SIZE[0]:
                del objects_in_game["Boats"][index]
                print
                deleted_items += 1
                continue


            for hitbox in hitboxes:

                if hasCollidedWithPelican(hitbox, objects_in_game["Boats"][index].position, BOAT_IMAGE.surface.get_size()):

                    # We die here
                    die()



        # Moving every object

        for obj in objects_in_game:
            for body in objects_in_game[obj]:
                move(body)


        # Appending surfaces to DRAWSURFACES

        # Pelican surfaces
        if objects_in_game["Pelican"][0].looking_right:
            DRAWSURFACES["Pelican"].append([PELICAN_FRAMES[objects_in_game["Pelican"][0].current_frame+int(len(PELICAN_FRAMES)/2)].surface, objects_in_game["Pelican"][0].position])
        else:
            DRAWSURFACES["Pelican"].append([PELICAN_FRAMES[objects_in_game["Pelican"][0].current_frame].surface, objects_in_game["Pelican"][0].position])

        # Fish surfaces
        for fish in objects_in_game["Fish"]:
            DRAWSURFACES["Fish"].append([pygame.transform.rotate(fish.specie.sprite, fish.angle()), fish.position])
        
        # Boat surfaces
        for boat in objects_in_game["Boats"]:
            if boat.velocity[0] > 0: DRAWSURFACES["Boats"].append([BOAT_IMAGE_FLIPPED.surface, boat.position])
            else: DRAWSURFACES["Boats"].append([BOAT_IMAGE.surface, boat.position])
        




        ## Drawing background layers:

        # Sea
        if -sea_scroll > SEA_WIDTH: sea_scroll = 0

        for offset in range(int(round(SCREEN_SIZE[0]/SEA_WIDTH, 0))+2):
            DRAWSURFACES["Sea"].append([SEA_IMAGE.surface, [offset*SEA_WIDTH+sea_scroll, Y_LIMIT-SEA_OFFSET]])
        
        sea_scroll -= SEA_SPEED


        # Background
        if -bkg_scroll > BKG_WIDTH: bkg_scroll = 0

        for offset in range(int(round(SCREEN_SIZE[0]/BKG_WIDTH, 0))+2):
            DRAWSURFACES["Background"].append([BACKGROUND_IMAGE.surface, [offset*BKG_WIDTH+bkg_scroll, 0]])

        bkg_scroll -= BKG_SPEED




        objects_in_game["Pelican"][0].velocity[0] = 0


        DRAWORDER = [
            DRAWSURFACES[   "Background"   ],
            DRAWSURFACES[     "Clouds"     ],
            DRAWSURFACES[      "Fish"      ],
            DRAWSURFACES[     "Bullets"    ],
            DRAWSURFACES[     "Pelican"    ],
            DRAWSURFACES[      "Boats"     ],
            DRAWSURFACES[      "Text"      ],
            DRAWSURFACES[     "Titles"     ],
            DRAWSURFACES[       "Sea"      ]
        ]

        for objects in DRAWORDER:
            for surface in objects:
                SCREEN.blit(surface[0], surface[1])

        #hitboxes = findHitboxes(objects_in_game["Pelican"][0])
        #for hitbox in hitboxes:
        #    pygame.draw.rect(SCREEN, (255, 0, 0), pygame.Rect(hitbox[0][0]-hitbox[1][0]/2, hitbox[0][1]-hitbox[1][1]/2, hitbox[1][0], hitbox[1][1]))

        pygame.display.update()
        pygame.time.Clock().tick(FPS)








while True:

    #menu()

    game()
