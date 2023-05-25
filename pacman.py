# Pacman in Python with PyGame
# https://github.com/hbokmann/Pacman

# Changed to Vax-Man 
# # Modified by Alex Falkowski for EA Virtual Internship
# # # You may change the number of ghosts and multiply time in the Ghost Class
# # # Ghosts no longer have hard-coded paths, instead they are chosen randomly

import pygame
import random

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
purple = (255,0,255)
yellow = (255,255,0)

# Sets the Window icon displayed in the top-left
Trollicon = pygame.image.load('images/Trollman.png')
pygame.display.set_icon(Trollicon)

# # # (MUSIC CURRENTLY DISABLED) # # #
# Add music 
# pygame.mixer.init()
# pygame.mixer.music.load('vaxman.mp3')
# pygame.mixer.music.play(-1, 0.0)
# # # # # # # # # # # # # # # # # # # #

# This class represents the bar at the bottom that the player controls
class Wall(pygame.sprite.Sprite):
    # Constructor function
    def __init__(self,x, y, width, height, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
  
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
  
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


# This creates all the walls in room 1
def setupRoomOne(all_sprites_list):
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.RenderPlain()
     
    # This is a list of walls. Each is in the form [x, y, width, height]
    walls = [ 
            [0,0,6,600], # Entire Left Blue Wall
            [0,0,600,6], # Entire Top Blue Wall
            [0,600,606,6], # Entire Bot Blue Wall
            [600,0,6,606], # Entire Right Blue Wall
            [300,0,6,66],
            [60,60,186,6],
            [360,60,186,6],
            [60,120,66,6],
            [60,120,6,126],
            [180,120,246,6],
            [300,120,6,66],
            [480,120,66,6],
            [540,120,6,126],
            [120,180,126,6],
            [120,180,6,126],
            [360,180,126,6],
            [480,180,6,126],
            [180,240,6,126],
            [180,360,246,6],
            [420,240,6,126],
            [240,240,42,6],
            [324,240,42,6],
            [240,240,6,66],
            [240,300,126,6],
            [360,240,6,66],
            [0,300,66,6],
            [540,300,66,6],
            [60,360,66,6],
            [60,360,6,186],
            [480,360,66,6],
            [540,360,6,186],
            [120,420,366,6],
            [120,420,6,66],
            [480,420,6,66],
            [180,480,246,6],
            [300,480,6,66],
            [120,540,126,6],
            [360,540,126,6]
            ] 
    
    # Loop through the list. Create the wall, add it to the list
    for item in walls:
        wall=Wall(item[0], item[1], item[2], item[3], blue)
        wall_list.add(wall)
        all_sprites_list.add(wall)  
    
    # return our new list
    return wall_list

def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, white))
    all_sprites_list.add(gate)
    return gate

# This class represents the ball        
# It derives from the "Sprite" class in Pygame
class Dot(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the dot, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
 
        # Create an image of the dot, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect() 


# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):

    # Constructor function
    def __init__(self, x, y, filename):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.first_run = True

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

        # Set speed vector
        self.change_x = 0
        self.change_y = 0

    # Clear the speed of the player
    def prevdirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Find a new position for the player
    def update(self, walls, gate):
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y

        # Did this update cause us to hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        
        if x_collide:
            # Whoops, hit a wall. Go back to the old position
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            # Did this update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            
            if y_collide:
                # Whoops, hit a wall. Go back to the old position
                self.rect.top = old_y

        if gate != False:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


class Ghost(Player):
    # Adjustable Values
    start_amount = 4 # Number of starting ghosts
    ghost_count = start_amount 
    time_until_multiply = 3 # Time until ghosts multiply (seconds).
    
    # Do not adjust values, variables used in ghost multiplying
    all_ghosts = list()
    clone_timer = int()
    first_time = True
    copies = 0
    
    # Constructor function
    def __init__(self, x, y, filepath, direction, color):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.first_run = True

        # Set height, width
        self.image = pygame.image.load(filepath).convert()

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x

        self.prev_x = x
        self.prev_y = y

        self.color = color
        
        self.reverseDirection = str()
        self.currentDirection = direction
        self.lastDirection = str()

        self.filepath = filepath

        Ghost.all_ghosts.append(self)

        # Set speed vector
        self.change_x = 0
        self.change_y = 0

    def stopMoving(self):
        self.change_x = 0
        self.change_y = 0
        # Ghost Stop

    def getReverseDirection(self, x, y):
        # (U)p, (R)ight, (D)own, (L)eft
        if x > 0:
            reverseDirection = 'L'
        elif x < 0:
            reverseDirection = 'R'
        elif y > 0:
            reverseDirection = 'U'
        elif y < 0:
            reverseDirection = 'D'
        return reverseDirection

    def changespeed(self, x, y):
        self.lastDirection = self.currentDirection
        self.stopMoving()

        self.reverseDirection = self.getReverseDirection(x, y)

        # Set ghost's new speed
        self.change_x += x
        self.change_y += y

        # Save ghost's current direction
        # (U)p, (R)ight, (D)own, (L)eft
        if self.currentDirection != 'UR' or self.currentDirection != 'UL':
            if x < 0:
                self.currentDirection = 'L'
            elif x > 0:
                self.currentDirection = 'R'
            elif y < 0:
                self.currentDirection = 'U'
            elif y > 0:
                self.currentDirection = 'D'
            else:
                # No currentDirection change
                pass
        else:
            pass

    # List of valid directions at each map cell for Ghost AI
    def getValidDirections(self, coords:tuple):
        # Valid Directions (U)p, (R)ight, (D)own, (L)eft]
        valid_directions_dict = {
                                (20,559) : ('U','R'),
                                (20,499) : ('U','D'),
                                (20,439) : ('U','D'),
                                (20,379) : ('U','D'),
                                (20,319) : ('R','D'),
                                (20,259) : ('U','R'),
                                (20,199) : ('U','D'),
                                (20,139) : ('U','D'),
                                (20,79) : ('U','R','D'),
                                (20,19) : ('R','D'),
                                (80,559) : ('U','R','L'),
                                (80,499) : ('U','R','D'),
                                (80,439) : ('U','D'),
                                (80,379) : ('R','D'),
                                (80,319) : ('U','R','L'),
                                (80,259) : ('U','D','L'),
                                (80,199) : ('U','D'),
                                (80,139) : ('R','D'),
                                (80,79) : ('R','L'),
                                (80,19) : ('R','L'),
                                (140,559) : ('R','L'),
                                (140,499) : ('U','R','L'),
                                (140,439) : ('R','D'),
                                (140,379) : ('U','R','L'),
                                (140,319) : ('U','D','L'),
                                (140,259) : ('U','D'),
                                (140,199) : ('R','D'),
                                (140,139) : ('U','R','L'),
                                (140,79) : ('R','D','L'),
                                (140,19) : ('R','L'),
                                (200,559) : ('R','L'),
                                (200,499) : ('R','L'),
                                (200,439) : ('R','L'),
                                (200,379) : ('R','L'),
                                (200,319) : ('R','U'),
                                (200,259) : ('U','D'),
                                (200,199) : ('R','D','L'),
                                (200,139) : ('R','L'),
                                (200,79) : ('R','L'),
                                (200,19) : ('R','L'),
                                (260,559) : ('U','R','L'),
                                (260,499) : ('D','L'),
                                (260,439) : ('R','L'),
                                (260,379) : ('R','L'),
                                (260,319) : ('R','L'),
                                (260,259) : ('UR'), # Box Left
                                (260,199) : ('U','R','L'),
                                (260,139) : ('D','L'),
                                (260,79) : ('U','R','L'),
                                (260,19) : ('D','L'),
                                (290,259) : ('UU'), # Box Mid
                                (290,199) : ('RR', 'LL'), # Above Gate
                                (320,559) : ('U','R','L'),
                                (320,499) : ('R','D'),
                                (320,439) : ('R','L'),
                                (320,379) : ('R','L'),
                                (320,319) : ('R','L'),
                                (320,259) : ('UL'), # Box Right
                                (320,199) : ('U','R','L'),
                                (320,139) : ('R','D'),
                                (320,79) : ('U','R','L'),
                                (320,19) : ('R','D'),
                                (380,559) : ('R','L'),
                                (380,499) : ('R','L'),
                                (380,439) : ('R','L'),
                                (380,379) : ('R','L'),
                                (380,319) : ('U','L'),
                                (380,259) : ('U','D'),
                                (380,199) : ('R','D','L'),
                                (380,139) : ('R','L'),
                                (380,79) : ('R','L'),
                                (380,19) : ('R','L'),
                                (440,559) : ('R','L'),
                                (440,499) : ('U','R','L'),
                                (440,439) : ('D','L'),
                                (440,379) : ('U','R','L'),
                                (440,319) : ('U','R','D'),
                                (440,259) : ('U','D'),
                                (440,199) : ('D','L'),
                                (440,139) : ('U','R','L'),
                                (440,79) : ('R','D','L'),
                                (440,19) : ('R','L'),
                                (500,559) : ('U','R','L'),
                                (500,499) : ('U','D','L'),
                                (500,439) : ('U','D'),
                                (500,379) : ('D','L'),
                                (500,319) : ('U','R','L'),
                                (500,259) : ('U','R','D'),
                                (500,199) : ('U','D'),
                                (500,139) : ('D','L'),
                                (500,79) : ('R','L'),
                                (500,19) : ('R','L'),
                                (560,559) : ('U','L'),
                                (560,499) : ('U','D'),
                                (560,439) : ('U','D'),
                                (560,379) : ('U','D'),
                                (560,319) : ('D','L'),
                                (560,259) : ('U','L'),
                                (560,199) : ('U','D'),
                                (560,139) : ('U','D'),
                                (560,79) : ('U','D','L'),
                                (560,19) : ('D','L')
                                }
        try:
            return(valid_directions_dict[(coords)])
        except:
            # coordinates not found, return currentDirection
            return(False)
        
    # Returns a new Ghost direction as a string
    def getNewDirection(self, coords:tuple):
        directions = self.getValidDirections((coords))

        if directions == False:
            directions_list = [self.currentDirection]
        else:
            directions_list = list(directions)

        try:
            directions_list.remove(self.reverseDirection)
        except:
            pass
            
        # Of remaining valid directions, return random choice
        if self.currentDirection != 'UR' and self.currentDirection != 'UL':
            try:
                return(random.choice(directions_list))
            except:
                return(self.currentDirection)
        else:
            return self.currentDirection

    def move(self, old_x:int, old_y:int, move_direction:str):
        if move_direction == 'U':
            self.changespeed(0, -15)
            new_y = old_y + self.change_y
            self.rect.top = new_y
        elif move_direction == 'D':
            self.changespeed(0, 15)
            new_y = old_y + self.change_y
            self.rect.top = new_y
        elif move_direction == 'L':
            self.changespeed(-15, 0)
            new_x = old_x + self.change_x
            self.rect.left = new_x
        elif move_direction == 'R':
            self.changespeed(15, 0)
            new_x = old_x + self.change_x
            self.rect.left = new_x
        elif move_direction == 'UL': # Box Right
            self.changespeed(-30, 0)
            new_x = old_x + self.change_x
            self.rect.left = new_x
        elif move_direction == 'UR': # Box Left
            self.changespeed(15, 0)
            new_x = old_x + self.change_x
            self.rect.left = new_x
        elif move_direction == 'UU': # Box Mid
            self.changespeed(0, -60)
            new_y = old_y + self.change_y
            self.rect.top = new_y
        elif move_direction == 'LL': # Above Gate
            self.currentDirection = 'L'
            self.reverseDirection = 'R'
            self.changespeed(-15, 0)
            new_x = old_x + self.change_x
            self.rect.left = new_x
        elif move_direction == 'RR': # Above Gate
            self.currentDirection = 'R'
            self.reverseDirection = 'L'
            self.changespeed(15, 0)
            new_x = old_x + self.change_x
            self.rect.left = new_x
        else:
            self.stopMoving()

    # Change the speed of the ghost
    def update(self, current_time):
        # Sets initial Ghost speed and direction (velocity)
        if Ghost.first_time:
            self.first_run = True

        if self.first_run == True:
            Ghost.clone_timer = current_time + Ghost.time_until_multiply
            self.first_run = False
        
        x = self.rect.left
        y = self.rect.top
        
        coords = (self.rect.left, self.rect.top)

        check_list = [
            (290, 199), # Above Gate
            (260, 259), # Box Left
            (320, 259), # Box Right
            (290, 259)  # Box Mid
            ]
        
        # Additional coordinates that require a new direction because they
        # are not in the valid_directions_dict. Used to navigate ghost out 
        # of gated box in center of the map at start of game.
        if coords in check_list:
            move_direction = self.getNewDirection(coords)
        # Coordinates are stored in valid_directions_dict
        elif self.rect.left % 20 == 0 and self.rect.top % 20 == 19:
            move_direction = self.getNewDirection(coords)
        # Keep moving in same direction until coordinates are found in dict
        else:
            move_direction = self.currentDirection

        self.move(x, y, move_direction)

        
        countdown = current_time - Ghost.clone_timer
        
        # Ghost does multiply
        if countdown == 0 and Ghost.copies < Ghost.ghost_count and not Ghost.first_time:
            Ghost.copies += 1
            return [
                    self.rect.left, 
                    self.rect.top,
                    self.filepath,
                    self.reverseDirection, 
                    self.color,
                    ]
        # Ghost does not multiply
        else:
            if Ghost.copies == Ghost.ghost_count:
                Ghost.clone_timer += Ghost.time_until_multiply
                Ghost.copies = 0
                Ghost.ghost_count += Ghost.ghost_count
            if current_time > 1:
                Ghost.first_time = False
            return []
        

# Call this function so the Pygame library can initialize itself
pygame.init()
  
# Create an 606x656 sized screen
screen = pygame.display.set_mode([606, 656])

# This is a list of 'sprites.' Each dot in the program is
# added to this list. The list is managed by a class called 'RenderPlain.'

# Set the title of the window
pygame.display.set_caption('Vax-Man')

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Used for converting color maps and such
background = background.convert()
  
# Fill the screen with a black background
background.fill(black)

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

def startGame():
    current_time = 0

    all_sprites_list = pygame.sprite.RenderPlain()
    
    dot_list = pygame.sprite.RenderPlain()

    ghost_list = pygame.sprite.RenderPlain()

    vaxman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)

    gate = setupGate(all_sprites_list)

    # Create the player paddle object
    
    # Default Vax-man location and image filepath
    Vaxman = Player(287, 439, "images/pacman.png")

    all_sprites_list.add(Vaxman)
    vaxman_collide.add(Vaxman)

    # default locations & filepaths for ghost types
    ghost_template_dict = {
        "Blinky": { 
            "x" : 260, # 287
            "y" : 199, # 199
            "filepath" : "images/Blinky.png",
            "color" : 'RED'
        },
        "Pinky": {
            "x" : 290, # 287
            "y" : 259, # 259
            "filepath" : "images/Pinky.png",
            "color" : 'PINK'
        },
        "Inky": {
            "x" : 260, # 260
            "y" : 259, # 259
            "filepath" : "images/Inky.png",
            "color" : 'BLUE'
        },
        "Clyde": {
            "x" : 320, # 320
            "y" : 259, # 259
            "filepath" : "images/Clyde.png",
            "color" : 'YELLOW'
        }
    }

    ghost_init_list = list(ghost_template_dict)
    ghost_index = 0
    i = 0

    while i != Ghost.start_amount:
        ghost_name = ghost_init_list[ghost_index]
        
        x = ghost_template_dict[ghost_name]['x']
        y = ghost_template_dict[ghost_name]['y']
        filepath = ghost_template_dict[ghost_name]['filepath']
        color = ghost_template_dict[ghost_name]['color']
        
        ghost_index += 1

        if ghost_name == "Blinky":
            Blinky = Ghost(x, y, filepath, 'U', color)
            ghost_list.add(Blinky)
            all_sprites_list.add(Blinky)
        
        if ghost_name == "Pinky":
            Pinky = Ghost(x, y, filepath, 'UU', color)
            ghost_list.add(Pinky)
            all_sprites_list.add(Pinky)

        if ghost_name == "Inky":
            Inky = Ghost(x, y, filepath, 'UR', color)
            ghost_list.add(Inky)
            all_sprites_list.add(Inky)

        if ghost_name == "Clyde":
            Clyde = Ghost(x, y, filepath, 'UL', color)
            ghost_list.add(Clyde)
            all_sprites_list.add(Clyde)
        
        if ghost_index == 4:
            ghost_index = 0

        i += 1

    # Draw the grid
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                dot = Dot(yellow, 4, 4)

                # Set a random location for the dot
                dot.rect.x = (30 * column + 6) + 26
                dot.rect.y = (30 * row + 6) + 26

                b_collide = pygame.sprite.spritecollide(dot, wall_list, False)
                p_collide = pygame.sprite.spritecollide(dot, vaxman_collide, False)
                
                if b_collide:
                    continue
                elif p_collide:
                    continue
                else:
                    # Add the dot to the list of objects
                    dot_list.add(dot)
                    all_sprites_list.add(dot)

    bll = len(dot_list)
    score = 0
    done = False
    i = 0

    while done == False:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Vaxman.changespeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Vaxman.changespeed(30, 0)
                if event.key == pygame.K_UP:
                    Vaxman.changespeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Vaxman.changespeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Vaxman.changespeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Vaxman.changespeed(-30, 0)
                if event.key == pygame.K_UP:
                    Vaxman.changespeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Vaxman.changespeed(0, -30)
          
        # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
    
        # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
        
        Vaxman.update(wall_list, gate)

        for ghost in ghost_list:
            ghost_info = ghost.update(current_time)
            if ghost_info != []:
                x = ghost_info[0]
                y = ghost_info[1]
                filepath = ghost_info[2]
                direction = ghost_info[3]
                new_ghost = Ghost( x, y, filepath, direction, color )
                new_ghost.reverseDirection = new_ghost.getReverseDirection(x, y)
                ghost_list.add(new_ghost)
                all_sprites_list.add(new_ghost)
            else:
                pass

        # See if the Vax-man dot has collided with anything.
        dots_hit_list = pygame.sprite.spritecollide(Vaxman, dot_list, True)
        
        # Check the list of collisions.
        if len(dots_hit_list) > 0:
            score += len(dots_hit_list)

        # # # # #  COMMENT BLOCK, TO DISABLE PACMAN KILLING GHOSTS # # # # # 
        ghost_hit_list = pygame.sprite.spritecollide(Vaxman, ghost_list, True)
        if ghost_hit_list:
            ghost_list.remove(ghost_hit_list)
            Ghost.ghost_count -= 1
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
        
        # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
    
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        screen.fill(black)
            
        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        ghost_list.draw(screen)

        font = pygame.font.Font(None,30) 

        dot_score_text = font.render(f"Score: {score}/{bll}", True, green)
        screen.blit(dot_score_text, [20, 622])

        ghost_score_text = font.render(f"Ghosts: {len(ghost_list)}/{32 * Ghost.start_amount}", True, red)
        # Adjust X spacing of Ghost score to keep text 'in place' as number grows
        if len(ghost_list) < 10:
            screen.blit(ghost_score_text, [453, 622])
        elif len(ghost_list) < 100:
            screen.blit(ghost_score_text, [442, 622])
        else:
            screen.blit(ghost_score_text, [429, 622])

        countdown_text = font.render(f"{abs(current_time - Ghost.clone_timer)}", True, white)
        screen.blit(countdown_text, [290, 622])

        # Win Condition
        # # Player (Vax-Man) collects all the dots
        if score == bll:
            doNext("Congratulations, you won!", 145, all_sprites_list, dot_list, ghost_list, vaxman_collide, wall_list, gate)

        # Loss Condition
        # # When number of ghosts grows to 32 times the original number
        if len(ghost_list) >= (32 * Ghost.start_amount):
            doNext("Game Over", 235, all_sprites_list, dot_list, ghost_list, vaxman_collide, wall_list, gate)
      
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        
        pygame.display.flip()
        
        clock.tick(10)

        current_time = int(pygame.time.get_ticks() / 1000)

def doNext(message, left, all_sprites_list, dot_list, ghost_list, vaxman_collide, wall_list, gate):
    while True:
        # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_RETURN:
                    del all_sprites_list
                    del dot_list
                    del ghost_list
                    del vaxman_collide
                    del wall_list
                    del gate
                    Ghost.time_until_multiply = 30
                    Ghost.copies = 0
                    Ghost.ghost_count = Ghost.start_amount
                    Ghost.first_time = True
                    Ghost.all_ghosts.clear()
                    startGame()
                if event.key == pygame.K_BACKSPACE:
                    del all_sprites_list
                    del dot_list
                    del ghost_list
                    del vaxman_collide
                    del wall_list
                    del gate
                    Ghost.time_until_multiply = 4
                    Ghost.copies = 0
                    Ghost.ghost_count = Ghost.start_amount
                    Ghost.first_time = True
                    Ghost.all_ghosts.clear()
                    startGame()

        # Grey background
        w = pygame.Surface((400, 230))  # the size of your rect
        w.set_alpha(150)                # alpha level
        w.fill((10, 10, 10))           # this fills the entire surface
        screen.blit(w, (100, 200))    # (0,0) are the top-left coordinates

        # Won or Lost
        font = pygame.font.Font(None, 30)
        text1 = font.render(message, True, white)
        screen.blit(text1, [left, 233])

        text2 = font.render("Easy - ENTER", True, green)
        screen.blit(text2, [215, 303])
        
        text3 = font.render("Hard - BACKSPACE", True, red)
        screen.blit(text3, [215, 333])

        text4 = font.render("Quit  - ESCAPE", True, white)
        screen.blit(text4, [215, 363])

        pygame.display.flip()

        clock.tick(10)

startGame()

pygame.quit()