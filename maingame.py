import arcade
from random import randint, choice
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Self-dungeon"
delta_stockpile = 0.0

class Color():
    def __init__(self, background):
        self.color = {
            'background': background
        }
        self.colmanual = {}
    def manual_edit(self, instructions, name, scolor):
        self.colmanual[name] = [instructions, scolor]
        self.color[name] = [int(scolor[0]*instructions[0]), int(scolor[1]*instructions[1]), int(scolor[2]*instructions[2])]
    def color_change(self):
        for name, inst in self.colmanual.items:
            self.color[name] = [max(min(255, int(inst[1][0]*inst[0][0])), 0), max(min(255, int(inst[1][1]*inst[0][1])), 0), max(min(255, int(inst[1][2]*inst[0][2])), 0)]
        
colorb = Color([125,125,125])
cmult = {
    'wall': (0.5,0.5,0.5),
    'empty': (1.5,1.5,1.5),
    'walp': (0,0,0),
    'empl': (2,2,2)
}
for name,c in cmult.items():
    colorb.manual_edit(c, name, colorb.color['background'])

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
        if len(blocks) != 0:
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
            'stx': SCREEN_WIDTH//2-sqwidth*rows//2,
            'sty': SCREEN_HEIGHT//2-sqheight*columns//2
        }
        self.array = []
    def build_array(self):
        for i in range(self.grid_stats['rows']):
            row = []
            for j in range(self.grid_stats['columns']):
                row.append(Block(j, i, choice([True, False])))
                row[-1].color_definer()
            self.array.append(row)
    def grid_draw(self, linesize=1):
        for i in range(self.grid_stats['rows']):
            for j in range(self.grid_stats['columns']):
                arcade.draw_rectangle_filled(self.grid_stats['stx']+(self.grid_stats['sqheight']*j), self.grid_stats['sty']+(self.grid_stats['sqwidth']*i), self.grid_stats['sqwidth']-linesize, self.grid_stats['sqheight']-linesize, self.array[i][j].block_stats['color'])

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
        self.delta_stockpile = 0.0
    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
    def on_draw(self):
        self.clear()
    def on_update(self, delta_time):
        global delta_stockpile
        delta_stockpile += delta_time
        if delta_stockpile > 1:
            self.player.move()
            arcade.start_render()
            self.grid.grid_draw(2)
            self.player.draw_player()            
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