import arcade
from random import randint, choice
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Self-dungeon"
delta_stockpile = 0.0

#Color of the game is basaed of a single background color, because I think that's a cool idea. If that won't work, I'll just use it for convinient color assignment.
class Color():
    def __init__(self, background):
        self.color = {
            'background': background
        }
        self.colmanual = {}
    #Colormanual is formatted into a list of 3 multipliers that are multiplied by to get a correct color value
    def manual_edit(self, instructions, name, scolor):
        self.colmanual[name] = [instructions, scolor]
        self.color[name] = [int(scolor[0]*instructions[0]), int(scolor[1]*instructions[1]), int(scolor[2]*instructions[2])]
    def color_change(self):
        for name, inst in self.colmanual.items:
            self.color[name] = [max(min(255, int(inst[1][0]*inst[0][0])), 0), max(min(255, int(inst[1][1]*inst[0][1])), 0), max(min(255, int(inst[1][2]*inst[0][2])), 0)]
        
colorb = Color([11,201,56])
cmult = {
    'wall': (0.5,0.5,0.5),
    'empty': (1.5,1.5,1.5)
}
for name,c in cmult.items():
    colorb.manual_edit(c, name, colorb.color['background'])

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

class Grid():
    def __init__(self, hsq, vsq):
        self.grid_stats = {
            'hsq': hsq,
            'vsq': vsq
        }
        self.array = []
    def build_array(self):
        for i in range(self.grid_stats['hsq']):
            row = []
            for j in range(self.grid_stats['vsq']):
                row.append(Block(int(randint(0,9))))
                row[-1].color_definer()
            self.array.append(row)
    def grid_draw(self, x, y, sqwidth, sqheight, linesize=1):
        for i in range(self.grid_stats['vsq']):
            for j in range(self.grid_stats['hsq']):
                arcade.draw_rectangle_filled(x+(sqwidth*j), y+(sqheight*i), sqwidth-linesize, sqwidth-linesize, self.array[j][i].block_stats['color'])

class Block():
    def __init__(self, passable):
        self.block_stats = {
            'passable': passable
        }
    def color_definer(self):
        global colorb
        if not self.block_stats['passable']:
            self.block_stats['color'] = colorb.color['wall']
        else:
            self.block_stats['color'] = colorb.color['empty']



class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(colorb.color['background'])
        self.player = Player(80, 80, 20, 20, (22,222,22), 40)
        self.grid = Grid(40,20)
        self.delta_stockpile = 0.0
    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.grid.build_array()
    def on_draw(self):
        self.clear()
    def on_update(self, delta_time):
        global delta_stockpile
        delta_stockpile += delta_time
        if delta_stockpile > 0.5:
            self.player.move()
            arcade.start_render()
            self.grid.grid_draw(0, 0, 40, 40, 2)
            arcade.draw_rectangle_filled(self.player.player['x'], self.player.player['y'], self.player.player['width'], self.player.player['height'], self.player.player['color'])
            arcade.finish_render()
            delta_stockpile = 0.0
    def on_key_release(self, key, modifiers):
        pass

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()