import arcade
from random import randint, choice
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Self-dungeon"
act = 0
tick = 100
delta_stockpile = 0.0

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color((78,5,27))
        self.player = None

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.player = {
            'x': 80,
            'y': 80,
            'width': 20,
            'height': 20,
            'color': (22,222,22),
            'mov_dis': 40
        }

    def on_draw(self):
        self.clear()


    def grid_draw(self, x, y, sqwidth, sqheight, horsquares, versquares, rgbcolor, linesize=1):
        for i in range(versquares):
            for j in range(horsquares):
                arcade.draw_rectangle_filled(x+(sqwidth*j), y+(sqheight*i), sqwidth-linesize, sqwidth-linesize, rgbcolor)

    def on_update(self, delta_time):
        global delta_stockpile
        delta_stockpile += delta_time
        if delta_stockpile > 0.5:
            ch = choice(['x-1', 'x1', 'y-1', 'y+1'])
            self.player[ch[0]] = self.player[ch[0]] + int(ch[1:])*self.player['mov_dis']
            if self.player[ch[0]] < 0:
                self.player[ch[0]] += self.player['mov_dis']
            elif ch[0] == 'x' and self.player[ch[0]] > SCREEN_WIDTH:
                self.player[ch[0]] -= self.player['mov_dis']
            elif ch[0] == 'y' and self.player[ch[0]] > SCREEN_HEIGHT:
                self.player[ch[0]] -= self.player['mov_dis']
            arcade.start_render()
            self.grid_draw(0,0,40,40,21,16,(156,10,54), 2)
            arcade.draw_rectangle_filled(self.player['x'], self.player['y'], self.player['width'], self.player['height'], self.player['color'])
            arcade.finish_render()
            delta_stockpile = 0.0
        
    
    def on_key_release(self, key, modifiers):
        pass



def main():
    """ Main function """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()