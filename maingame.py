import arcade
import _thread
from random import randint, choice 
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Self-dungeon"
act = 0
tick = 100


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.AMAZON)
        self.player = None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.rectangles = []
        self.player = {
            'x': 0,
            'y': 0,
            'width': 20,
            'height': 20,
            'color': (22,222,22),
            'mov_dis': 40
        }

    def on_draw(self):
        self.clear()


    def grid_draw(self, x, y, sqwidth, sqheight, versquares, horsquares, rgbcolor, linesize=1):
        for i in range(versquares):
            for j in range(horsquares):
                arcade.draw_rectangle_filled(x+(sqwidth*j), y+(sqheight*i), sqwidth-linesize, sqwidth-linesize, rgbcolor)

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        pass

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.player['y'] += 40
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player['y'] -= 40
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player['x'] -= 40
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player['x'] += 40
        print(self.player['x'],self.player['y'])
        arcade.start_render()
        self.grid_draw(0,0,40,40,20,15,(156,10,54), 2)
        arcade.draw_rectangle_filled(self.player['x'], self.player['y'], self.player['width'], self.player['height'], self.player['color'])
        arcade.finish_render()



def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()