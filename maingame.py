from cmath import inf
import arcade
from random import randint, choice
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Self-dungeon"
move_frequence = 0.0
draw_refresh_rate = 0.0

class Color():
    def __init__(self, background):
        self.color = {
            'background': background
        }
        self.colmanual = {}
    def manual_edit(self, instructions, name, scolor):
        self.colmanual[name] = [instructions, scolor]
        self.color[name] = [int(self.color[scolor][0]*instructions[0]), int(self.color[scolor][1]*instructions[1]), int(self.color[scolor][2]*instructions[2])]
    def color_change(self):
        for name, inst in self.colmanual.items():
            self.color[name] = [max(min(255, int(self.color[inst[1]][0]*inst[0][0])), 0), max(min(255, int(self.color[inst[1]][1]*inst[0][1])), 0), max(min(255, int(self.color[inst[1]][2]*inst[0][2])), 0)]
    def random_color(self, name):
        self.color[name] = [randint(0, 255), randint(0, 255), randint(0, 255)]
        colorb.color_change()

colorb = Color([125,125,125])
cmult = {
    'wall': (0.5,0.5,0.5),
    'empty': (1.5,1.5,1.5),
    'walp': (0,0,0),
    'empl': (2,2,2)
}
for name,c in cmult.items():
    colorb.manual_edit(c, name, 'background')

class Player():
    def __init__(self, x, y, w, h, color, grid):
        self.player = {
            'row': x,
            'column': y,
            'width': w,
            'height': h,
            'color': color,
        }
        self.grid = grid
        self.grid.array[self.player['row']][self.player['column']].block_stats['has_player'] = 1
    def draw_player(self):
        arcade.draw_rectangle_filled(self.grid.grid_stats['stx']+self.grid.grid_stats['sqwidth']*self.player['column'], 
                                    self.grid.grid_stats['sty']+self.grid.grid_stats['sqheight']*self.player['row'], 
                                    self.player['width'], self.player['height'], self.player['color'])
    def move(self):
        blocks = [
            self.grid.array[min(self.player['row']+1, self.grid.grid_stats['rows']-1)][self.player['column']],
            self.grid.array[max(self.player['row']-1, 0)][self.player['column']],
            self.grid.array[self.player['row']][min(self.player['column']+1, self.grid.grid_stats['columns']-1)],
            self.grid.array[self.player['row']][max(self.player['column']-1, 0)]]
        moves = []
        for b in blocks:
            if b.block_stats['passable'] == True:
                if not (b.block_stats['x'] == self.player['column'] and b.block_stats['y'] == self.player['row']):
                    moves.append(b)
        if len(moves) != 0:
            move = choice(moves)
            self.grid.array[self.player['row']][self.player['column']].block_stats['has_player'] = 0
            self.grid.array[self.player['row']][self.player['column']].color_definer()
            self.player['row'] = move.block_stats['y']
            self.player['column'] = move.block_stats['x']
            self.grid.array[self.player['row']][self.player['column']].block_stats['has_player'] = 1
            self.grid.array[self.player['row']][self.player['column']].color_definer()

class Grid():
    def __init__(self, rows, columns, sqwidth, sqheight):
        self.grid_stats = {
            'rows': rows,
            'columns': columns,
            'sqwidth': sqwidth,
            'sqheight': sqheight,
            'stx': SCREEN_WIDTH/2-sqwidth*columns/2,
            'sty': SCREEN_HEIGHT/2-sqheight*rows/2
        }
        self.array = []
    def build_array(self):
        for i in range(self.grid_stats['rows']):
            row = []
            for j in range(self.grid_stats['columns']):
                row.append(Block(j, i, choice([True, True, False])))
                row[-1].color_definer()
            self.array.append(row)
    def grid_draw(self, linesize=1):
        for i in range(self.grid_stats['rows']):
            for j in range(self.grid_stats['columns']):
                arcade.draw_rectangle_filled(self.grid_stats['stx']+(self.grid_stats['sqheight']*j), self.grid_stats['sty']+(self.grid_stats['sqwidth']*i), self.grid_stats['sqwidth']-linesize, self.grid_stats['sqheight']-linesize, self.array[i][j].block_stats['color'])
    def update_color(self):
        for i in self.array:
            for j in i:
                j.color_definer()
    def closest_block(self, x, y):
        x_list = []
        y_list = []
        for i in range(len(self.array)):
            y_list.append(abs(self.grid_stats['sty']+(self.array[i][0].block_stats['y'])*self.grid_stats['sqheight']-y))
        for i in range(len(self.array[0])):
            x_list.append(abs(self.grid_stats['stx']+(self.array[0][i].block_stats['x'])*self.grid_stats['sqwidth']-x))
        print([x_list.index(min(x_list)), y_list.index(min(y_list))])
        return [x_list.index(min(x_list)), y_list.index(min(y_list))]
        

class Block():
    def __init__(self, x, y, passable):
        self.block_stats = {
            'x': x, 
            'y': y,
            'passable': passable,
            'has_player': 0
        }
    def color_definer(self):
        global colorb
        if not self.block_stats['passable']:
            if not self.block_stats['has_player']:
                self.block_stats['color'] = colorb.color['wall']
            else:
                self.block_stats['color'] = colorb.color['walp']
        else:
            if not self.block_stats['has_player']:
                self.block_stats['color'] = colorb.color['empty']
            else:
                self.block_stats['color'] = colorb.color['empl']   

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(colorb.color['background'])
        self.grid = Grid(10, 5, 40, 40)
        self.grid.build_array()
        self.player = Player(randint(0,self.grid.grid_stats['rows']-1), randint(0,self.grid.grid_stats['columns']-1), 20, 20, (22,222,22), self.grid)
        self.move_frequence = 0.0
    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
    def on_draw(self):
        self.clear()
    def on_update(self, delta_time):
        global move_frequence
        move_frequence += delta_time
        if move_frequence > 1:
            self.player.move()
            move_frequence = 0.0
        arcade.start_render()
        self.grid.grid_draw(2)
        self.player.draw_player()            
        arcade.finish_render()
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.C:
            colorb.random_color('background')
            self.grid.update_color()
            arcade.set_background_color(colorb.color['background'])
    def on_mouse_press(self, x, y, button, modifiers):
        pos = self.grid.closest_block(x,y)
        self.grid.array[pos[1]][pos[0]].block_stats['passable'] = not self.grid.array[pos[1]][pos[0]].block_stats['passable']
        self.grid.array[pos[1]][pos[0]].color_definer()

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()