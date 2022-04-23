import arcade
from random import randint, choice
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Self-dungeon"
act = 0
tick = 100
delta_stockpile = 0.0

class Player():
    def __init__(self, x, y, w, h, color, mov_dis):
        self.player = {
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'color': color,
            'mov_dis': mov_dis
        }

    def move(self):
            ch = choice(['x-1', 'x1', 'y-1', 'y+1'])
            self.player[ch[0]] = self.player[ch[0]] + int(ch[1:])*self.player['mov_dis']
            if self.player[ch[0]] < 0:
                self.player[ch[0]] += self.player['mov_dis']
            elif ch[0] == 'x' and self.player[ch[0]] > SCREEN_WIDTH:
                self.player[ch[0]] -= self.player['mov_dis']
            elif ch[0] == 'y' and self.player[ch[0]] > SCREEN_HEIGHT:
                self.player[ch[0]] -= self.player['mov_dis']

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color((78,5,27))
        self.player = Player(80, 80, 20, 20, (22,222,22), 40)

    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here


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
            self.player.move()
            arcade.start_render()
            self.grid_draw(0,0,40,40,21,16,(156,10,54), 2)
            arcade.draw_rectangle_filled(self.player.player['x'], self.player.player['y'], self.player.player['width'], self.player.player['height'], self.player.player['color'])
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