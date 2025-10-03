'''
Ashley Im
A3
'''

import pygame, sys, math, random

# Test if two sprite masks overlap
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    if overlap:
        return True
    else:
        return False

# A basic Sprite class that can draw itself, move, and test collisions. Basically the same as
# the Character example from class.
class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)

class Enemy:
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

        # 1. Set the rectangle center to a random x and y based
        #    on the screen width and height
        # 2. Set a speed instance variable that holds a tuple (vx, vy)
        #    which specifies how much the rectangle moves each time.
        #    vx means "velocity in x". Make the vx and vy random (with
        #    possible negative and positive values. Experiment so the
        #    speeds are not too fast.
        self.vx = random.randint(-5,5)
        if self.vx == 0:
            self.vx = 1
        self.vy = random.randint(-5,5)
        if self.vy == 0:
            self.vy = 1

    def move(self):
        # Add code to move the rectangle instance variable in x by
        # the speed vx and in y by speed vy. The vx and vy are the
        # components of the speed instance variable tuple.
        # A useful method of rectangle is pygame's move_ip method.
        # Research how to use it for this task.
        self.rectangle.move_ip(self.vx, self.vy)

    def bounce(self, width, height):
        # This method makes the enemy bounce off of the top/left/right/bottom
        # of the screen. For example, if you want to check if the object is
        # hitting the left side, you can test
        # if self.rectangle.left < 0:
        # The rectangle.left tests the left side of the rectangle. You will
        # want to use .right .top .bottom for the other sides.
        # The height and width parameters gives the screen boundaries.
        # If a hit of the edge of the screen is detected on the top or bottom
        # you want to negate (multiply by -1) the vy component of the speed instance
        # variable. If a hit is detected on the left or right of the screen, you
        # want to negate the vx component of the speed.
        # Make sure the speed instance variable is updated as needed.
        if self.rectangle.left < 0:
            self.vx = self.vx * -1
        if self.rectangle.right > width:
            self.vx = self.vx * -1
        if self.rectangle.top < 0:
            self.vy = self.vy * -1
        if self.rectangle.bottom > height:
            self.vy = self.vy * -1

    def draw(self, screen):
        # Same draw as Sprite
        screen.blit(self.image, self.rectangle)

class PowerUp:
    def __init__(self, image, width, height):
        # Set the PowerUp position randomly like is done for the Enemy class.
        # There is no speed for this object as it does not move.
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()

        x = random.randint(0, width)
        y = random.randint(0, height)
        self.rectangle.center = (x,y)

    def draw(self, screen):
        # Same as Sprite
        screen.blit(self.image, self.rectangle)

def main():
    # Setup pygame
    pygame.init()

    # Get a font for printing the lives left on the screen.
    myfont = pygame.font.SysFont('monospace', 24)

    # Define the screen
    width, height = 600, 400
    size = width, height
    screen = pygame.display.set_mode((width, height))

    background = pygame.image.load("background.png").convert_alpha()
    background= pygame.transform.scale(background, (width,height))

    # Load image assets
    # Choose your own image
    enemy = pygame.image.load("S.gif").convert_alpha()
    # Here is an example of scaling it to fit a 50x50 pixel size.
    enemy_image = pygame.transform.smoothscale(enemy, (50, 50))

    enemy_sprites = []
    for i in range(10):
        enemy_sprites.append(Enemy(enemy_image, width, height))
    # Make some number of enemies that will bounce around the screen.
    # Make a new Enemy instance each loop and add it to enemy_sprites.

    # This is the character you control. Choose your image.
    player_image = pygame.image.load("squid.gif").convert_alpha()
    player_sprite = Sprite(player_image)
    life = 3

    # This is the powerup image. Choose your image.
    powerup_image = pygame.image.load("burger.png").convert_alpha()
    powerup_image = pygame.transform.smoothscale(powerup_image, (50, 50))
    # Start with an empty list of powerups and add them as the game runs.
    powerups = []

    # Main part of the game
    is_playing = True
    # while loop
    while is_playing:# while is_playing is True, repeat
        if life <= 0:
             is_playing = False
    # Modify the loop to stop when life is <= to 0.

        # Check for events
        for event in pygame.event.get():
            # Stop loop if click on window close button
            if event.type == pygame.QUIT:
                is_playing = False

        # Make the player follow the mouse
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        # Loop over the enemy sprites. If the player sprite is
        # colliding with an enemy, deduct from the life variable.
        # A player is likely to overlap an enemy for a few iterations
        # of the game loop - experiment to find a small value to deduct that
        # makes the game challenging but not frustrating.

        for enemy_sprite in enemy_sprites:
            if player_sprite.is_colliding(enemy_sprite):
                life -= 0.3

        # Loop over the powerups. If the player sprite is colliding, add
        # 1 to the life.
        for powerup_sprite in powerups:
            if player_sprite.is_colliding(powerup_sprite):
                life += 1

        # Make a list comprehension that removes powerups that are colliding with
        # the player sprite.
        powerups = [p for p in powerups if not player_sprite.is_colliding(p)]

        # Loop over the enemy_sprites. Each enemy should call move and bounce.
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width, height)

        # Choose a random number. Use the random number to decide to add a new
        # powerup to the powerups list. Experiment to make them appear not too
        # often, so the game is challenging.
        if random.randint(1,100) ==1:
            powerups.append(PowerUp(powerup_image, width, height))

        # Erase the screen with a background color
        screen.blit(background,(0,0))

        # Draw the characters
        for enemy_sprite in enemy_sprites:
            enemy_sprite.draw(screen)
        for powerup_sprite in powerups:
            powerup_sprite.draw(screen)

        player_sprite.draw(screen)

        # Write the life to the screen.
        text = "Life: " + str('%.1f'%life)
        life_banner = myfont.render(text, True, (255, 255, 0))
        screen.blit(life_banner, (20, 20))

        # Bring all the changes to the screen into view
        pygame.display.update()
        # Pause for a few milliseconds
        pygame.time.wait(20)

    #if the game loop is done, show GameOver, and close the window and quit.
    if life <= 0:
        screen.blit(background, (0, 0))
        game_over_text = myfont.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.update()
        pygame.time.wait(1000)

    # Once the game loop is done, pause, close the window and quit.
    # Pause for a few seconds
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
