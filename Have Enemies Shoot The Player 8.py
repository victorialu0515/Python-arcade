"""
Show how to have enemies shoot bullets aimed at the player.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_bullets_enemy_aims
"""

import arcade
import math
import os
import random
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprites and Bullets Enemy Aims Example"
BULLET_SPEED = 4 #bullet travel speed
ENEMY_SPEED = 2 #enemy movement speed
FIRE_RATE = 30 #the enemy will shoot a bullet every this many frames
BULLET_OFFSET_DISTANCE = 50 #offset the bullet from the enemy when it's firing to avoid collision with itself upon firing
PLAYER_SPEED = 10
INITIAL_AMMO = 10


class InstructionView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        texture = arcade.load_texture("Instructions page-2.jpg")
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, texture)
        # arcade.draw_text("Menu Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
        #                  arcade.color.BLACK, font_size=50, anchor_x="center")
        # arcade.draw_text("Click to start", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 75,
        #                  arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.frame_count = 0
        self.score = 0
        self.hit = 0
        self.health = 10
        self.timer = 0
        self.background_y = 0
        self.ammo = INITIAL_AMMO

        self.enemy_list = None
        self.bullet_list = None
        self.player_list = None
        self.player = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.space_pressed = False

        self.background = None
        self.PowerUpBool = False
        self.setup()

    def setup(self):
        self.enemy_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # this code modifies the arcade.Sprite class by adding a new attribute called "moving_down"
        setattr(arcade.Sprite, "moving_down", True)  # initial memory of the movement direction
        setattr(arcade.Sprite, "moving_right", True)
        setattr(arcade.Sprite, "description", None)

        # Add player ship
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
        self.player.center_x = SCREEN_WIDTH / 2
        self.player.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player)

        self.hit = 0
        self.elapsed = 0

        self.background_y = 0

        # Add top-left enemy ship
        # enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        # enemy.center_x = random.randint(1, SCREEN_WIDTH)
        # enemy.center_y = random.randint(1, SCREEN_HEIGHT)
        # enemy.angle = 180
        # self.enemy_list.append(enemy)
        #
        # # Add top-right enemy ship
        # enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        # enemy.center_x = random.randint(1, SCREEN_WIDTH)
        # enemy.center_y = random.randint(1, SCREEN_HEIGHT)
        # enemy.angle = 180
        # print("enemy.moving down:", enemy.moving_down)
        # self.enemy_list.append(enemy)

        for i in range(1):
            self.spawn_enemy()

        self.start = time.time()


    def on_draw(self):
        """Render the screen. """

        arcade.start_render()
        #texture = arcade.load_texture("photo-1475274047050-1d0c0975c63e.jpeg")
        texture = arcade.load_texture("spacebg.jpg")
        self.background_y -= 2
        arcade.draw_lrwh_rectangle_textured(0, self.background_y, SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2, texture)
        arcade.draw_lrwh_rectangle_textured(0, self.background_y + 1200, SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2, texture)
        if (self.background_y <= -1200):
            self.background_y = 0

        output_total = f"Enemies hit: {self.window.total_score}"
        arcade.draw_text(output_total, 10, 10, arcade.color.WHITE, 14)
        # Tells you how many times you've been hit
        output = f"Hit: {self.hit}"
        timeOutput = f"Time passed: {self.elapsed}"
        arcade.draw_text(output, 10, 50, arcade.color.FERRARI_RED, 25)
        arcade.draw_text(timeOutput, 10, 20, arcade.color.BABY_BLUE, 20)

        output = f"Ammo: {self.ammo}"
        arcade.draw_text(output, self.player.center_x, self.player.center_y - 30, arcade.color.GRAY, 10,
                         anchor_x="center")
        # Tells you to reload when you have 0 ammo
        if self.ammo == 0:
            output = "Press R to reload"
            arcade.draw_text(output, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.AERO_BLUE, 25, anchor_x="center")

        # Tells you how many lives you have (self.health equals to 10)
        output = (self.health - self.hit) * '|'
        arcade.draw_text(output, self.player.center_x, self.player.center_y - 60, arcade.color.RED_VIOLET, 20, anchor_x="center")

        print()

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here. """
        self.elapsed = round(time.time() - self.start, 2);

        self.player.change_x = 0
        self.player.change_y = 0
        # move the ship by keyboard
        if self.up_pressed and not self.down_pressed:
            self.player.change_y = PLAYER_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player.change_y = -PLAYER_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_SPEED

        # Check for out-of-bounds
        if self.player.center_x < 0:
            self.player.center_x = 0
        elif self.player.center_x > SCREEN_WIDTH - 1:
            self.player.center_x = SCREEN_WIDTH - 1

        if self.player.center_y < 0:
            self.player.center_y = 0
        elif self.player.center_y > SCREEN_HEIGHT - 1:
            self.player.center_y = SCREEN_HEIGHT - 1

        self.frame_count += 1
        textures = [
            ":resources:images/enemies/frog.png",
            ":resources:images/topdown_tanks/tankBody_blue_outline.png",
            ":resources:images/enemies/ladybug.png",
            ":resources:images/space_shooter/playerShip3_orange.png",
            ":resources:images/space_shooter/playerShip2_orange.png",
            ":resources:images/space_shooter/playerLife1_orange.png"
        ]
        if self.frame_count % 50 == 0 and len(self.enemy_list) < 100:  # spawn 1 enemy every 5 seconds
            self.spawn_enemy(texture=random.choice(textures))

        # Hit detection
        for enemy in self.enemy_list:
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, self.enemy_list) #check if an enemy has collided with another enemy
            enemyCollideBullet = arcade.check_for_collision_with_list(enemy, self.bullet_list) #check if an enemy has collided with any bullet
            if enemy_hit_list or enemyCollideBullet:
                enemy.remove_from_sprite_lists()
            for x in enemyCollideBullet:
                self.window.total_score += 1



            for bullet in enemyCollideBullet: #remove bullets that have collided with the enemy
                bullet.remove_from_sprite_lists()

        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player.center_x
            dest_y = self.player.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle) - 90

            if enemy.center_y <= 0 and enemy.moving_down == True:  # the enemy is outside the bottom edge of the screen
                enemy.moving_down = False
            if enemy.center_y > 600 and enemy.moving_down == False:  # the enemy is above the top edge of the screen
                enemy.moving_down = True
            if enemy.moving_down == True:
                enemy.center_y -= ENEMY_SPEED
            else:
                enemy.center_y += ENEMY_SPEED

            if enemy.center_x <= 0 and enemy.moving_right == True:
                enemy.moving_right = False
            if enemy.center_x > 800 and enemy.moving_right == False:
                enemy.moving_right = True
            if enemy.moving_right == True:
                enemy.center_x -= ENEMY_SPEED
            else:
                enemy.center_x += ENEMY_SPEED

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % FIRE_RATE == 0:
                bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                bullet.description = "enemy"
                bullet.center_x = start_x + BULLET_OFFSET_DISTANCE * math.cos(angle)
                bullet.center_y = start_y + BULLET_OFFSET_DISTANCE * math.sin(angle)

                # Angle the bullet sprite
                bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                bullet.change_x = math.cos(angle) * BULLET_SPEED
                bullet.change_y = math.sin(angle) * BULLET_SPEED

                self.bullet_list.append(bullet)


        hit_list = arcade.check_for_collision_with_list(self.player,
                                                        self.bullet_list)

        for bullet in hit_list:
            if bullet.description == "enemy":
                bullet.remove_from_sprite_lists()
                self.hit += 1

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if not (0 <= bullet.center_y <= SCREEN_HEIGHT and 0 <= bullet.center_x <= SCREEN_WIDTH):
                bullet.remove_from_sprite_lists()
        # prints the bullet list
        # print(self.bullet_list.__len__())

        self.bullet_list.update()
        self.player_list.update()

        if (self.hit >= 10):
            game_over_view = GameOverView()
            game_over_view.time_taken = self.elapsed
            self.window.set_mouse_visible(True)
            self.window.show_view(game_over_view)


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Detects if R key is pressed so you can reload
        if key == arcade.key.R:
            self.ammo = 10

        # Continues shooting with spacebar

        if key == arcade.key.SPACE:
            self.space_pressed = True

        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False
        elif key == arcade.key.SPACE:
            self.space_pressed = False

    def on_mouse_motion(self, x, y, delta_x, delta_y):  # x and y positional arguments
        """Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = y

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.shoot_bullet()

    def shoot_bullet(self):
        if self.ammo > 0:
            bullet = arcade.Sprite(
                ":resources:images/space_shooter/laserRed01.png")  # create a new instance of the bullet
            bullet.description = "player"
            bullet.angle = 0  # Angle the bullet sprite
            bullet.center_x = self.player.center_x
            bullet.center_y = self.player.center_y + BULLET_OFFSET_DISTANCE
            bullet.change_x = 0  # horizontal movement
            bullet.change_y = BULLET_SPEED  # vertical movement
            self.bullet_list.append(bullet)  # adding the bullet to the bullet
            # Ammo Count
            self.ammo -= 1

    def spawn_enemy(self, texture=":resources:images/enemies/frog.png", x=None,
                    y=None):  # texture, x and y are keyword arguments
        enemy = arcade.Sprite(texture, 0.5)
        if x is None or y is None:
            enemy.center_x = random.randint(1, SCREEN_WIDTH)
            enemy.center_y = random.randint(1, SCREEN_HEIGHT)
        else:
            enemy.center_x = x
            enemy.center_y = y
        enemy.angle = 180
        self.enemy_list.append(enemy)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.time_taken = 0



    def on_draw(self):
        arcade.start_render()
        """
        Draw "Game over" across the screen.
        """
        arcade.set_background_color(arcade.color.GRAY)
        texture = arcade.load_texture('doge.jpg copy.jpg')
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, texture)
        arcade.draw_text("Game Over", 240, 400, arcade.color.RED, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)

        time_taken_formatted = f"{round(self.time_taken, 2)} seconds"
        try:
            if (self.highscore < self.time_taken):
                self.highscore = self.time_taken
        except:
            self.highscore = 0
            if (self.highscore < self.time_taken):
                self.highscore = self.time_taken
        arcade.draw_text(f"Score: {time_taken_formatted}",
                         320,
                         220,
                         arcade.color.AMARANTH_PURPLE, 15, font_name="GARA")
        arcade.draw_text(f"High score: {self.highscore} seconds", 320, 190, arcade.color.AMARANTH_PURPLE)
        arcade.draw_text(f"Enemies killed: {self.window.total_score}", 320, 150, arcade.color.AMARANTH_PURPLE)



    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.total_score = 0
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    """ Main method """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.total_score = 0
    instruction_view = InstructionView()
    window.show_view(instruction_view)
    arcade.run()


if __name__ == "__main__":
    main()