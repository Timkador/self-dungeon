from cmath import inf
import arcade
from random import randint, choice
from math import sqrt
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
        self.game = None
    def manual_edit(self, inst, name, scolor):
        self.colmanual[name] = [[inst[0], inst[1], inst[2]], scolor]
        if len(inst) == 4:
            self.colmanual[name] = [self.colmanual[name][0], self.colmanual[name][1], inst[3]]
    def color_change(self):
        for name, inst in self.colmanual.items():
            if len(inst) == 3:
                for i in inst[2]:
                    if i == 'f':
                        self.flip_color(name, inst)
                    if i == 'g' and self.game != None:
                        for j in self.game.entities:
                            if j.entity['entype'] == name:
                                self.randinrange(j.entity['color'], name, 'background')
            else:
                self.color[name] = [max(min(255, int(self.color[inst[1]][0]*inst[0][0])), 0), max(min(255, int(self.color[inst[1]][1]*inst[0][1])), 0), max(min(255, int(self.color[inst[1]][2]*inst[0][2])), 0)]
    def random_color(self, name):
        self.color[name] = [randint(66, 200), randint(66, 200), randint(66, 200)]
        colorb.color_change()
    def randinrange(self, name, inst, colorname):
        self.color[name] = [
            max(min(randint(int(self.colmanual[inst][0][0][0]*self.color[colorname][0]), int(self.colmanual[inst][0][0][1]*self.color[colorname][0])), 255), 0),
            max(min(randint(int(self.colmanual[inst][0][1][0]*self.color[colorname][1]), int(self.colmanual[inst][0][1][1]*self.color[colorname][1])), 255), 0),
            max(min(randint(int(self.colmanual[inst][0][2][0]*self.color[colorname][2]), int(self.colmanual[inst][0][2][1]*self.color[colorname][2])), 255), 0)
            ]
    def flip_color(self, name, inst):
        self.color[name] = [255-max(min(255, int(self.color[inst[1]][0]*inst[0][0])), 0), 255-max(min(255, int(self.color[inst[1]][1]*inst[0][1])), 0), 255-max(min(255, int(self.color[inst[1]][2]*inst[0][2])), 0)]
    def modify_color(self, color, inst):
        return [max(min(255, color[0]*self.colmanual[inst][0][0]), 0), max(min(255, color[1]*self.colmanual[inst][0][1]), 0), max(min(255, color[2]*self.colmanual[inst][0][2]), 0)]

colorb = Color([125,125,125])
cmult = {
    'wall': (.5, .5, .5),
    'empty': (1.5, 1.5, 1.5),
    'on_blockmod': (.75, .75, .75, 'm'),
    'player': (1, 1, 1, 'f'),
    'enemy': ([0.9, 1.1], [0.9, 1.1], [0.9, 1.1], 'g')
}
for name,c in cmult.items():
    colorb.manual_edit(c, name, 'background')
colorb.color_change()

class Entity():
    def __init__(self, x, y, w, h, colorname, grid, moveable, entype):
        self.entity = {
            'row': x,
            'column': y,
            'width': w,
            'height': h,
            'color': colorname,
            'moveable': moveable,
            'entype': entype
        }
        self.grid = grid
        self.grid.array[self.entity['row']][self.entity['column']].block_stats['on_block'] = self.entity
    def draw_entity(self):
        arcade.draw_rectangle_filled(self.grid.grid_stats['stx']+self.grid.grid_stats['sqwidth']*self.entity['column'], 
                                    self.grid.grid_stats['sty']+self.grid.grid_stats['sqheight']*self.entity['row'], 
                                    self.entity['width'], self.entity['height'], colorb.color[self.entity['color']])
    def pos_around(self, p_check=False):
        blocks = [
            self.grid.array[min(self.entity['row']+1, self.grid.grid_stats['y_am']-1)][self.entity['column']],
            self.grid.array[max(self.entity['row']-1, 0)][self.entity['column']],
            self.grid.array[self.entity['row']][min(self.entity['column']+1, self.grid.grid_stats['x_am']-1)],
            self.grid.array[self.entity['row']][max(self.entity['column']-1, 0)]]
        block_list = []
        for b in blocks:
            if b.block_stats['passable'] == True or not p_check:
                if not (b.block_stats['x'] == self.entity['column'] and b.block_stats['y'] == self.entity['row']):
                    block_list.append(b)
        return block_list
    def move(self):
        moves = self.pos_around(True)
        if len(moves) != 0 and self.entity['moveable']:
            move = choice(moves)
            self.grid.array[self.entity['row']][self.entity['column']].block_stats['on_block'] = 0
            self.grid.array[self.entity['row']][self.entity['column']].block_stats['passable'] = True
            self.grid.array[self.entity['row']][self.entity['column']].color_definer()
            self.entity['row'] = move.block_stats['y']
            self.entity['column'] = move.block_stats['x']
            self.grid.array[self.entity['row']][self.entity['column']].block_stats['on_block'] = self.entity
            self.grid.array[self.entity['row']][self.entity['column']].block_stats['passable'] = False
            self.grid.array[self.entity['row']][self.entity['column']].color_definer()

class Player(Entity):
    def __init__(self, x, y, w, h, colorname, grid, moveable, entype, health, damage):
        super(Player, self).__init__(x, y, w, h, colorname, grid, moveable, entype)
        self.player_stats = {
            'health': health,
            'damage': damage
        }
    def check_enemies(self, entity_list):
        blocks = self.pos_around()
        enm_pos = []
        enm_fnd = []
        for i in entity_list:
            if i.entity['moveable'] == True and i.entity['entype'] == 'enemy':
                enm_pos.append([i, [i.entity['row'], i.entity['column']]])
        if enm_pos:
            for i in enm_pos:
                if self.grid.array[i[1][0]][i[1][1]] in blocks:
                    enm_fnd.append(i[0])
        return [bool(enm_fnd), enm_fnd]
    def attack(self, enemy_list):
        if enemy_list[0] == True:
            choice(enemy_list[1]).enemy_stats['health'] -= self.player_stats['damage']
    def player_action(self):
        self.check_enemies()
        self.attack()
    def check_health(self):
        return [self.player_stats['health'], self.player_stats['health'] > 0]

class Enemy(Entity):
    def __init__(self, x, y, w, h, colorname, grid, moveable, entype, health):
        super(Enemy, self).__init__(x, y, w, h, colorname, grid, moveable, entype)
        self.enemy_stats = {
            'health': health,
        }
    def check_health(self):
        return [self.enemy_stats['health'], self.enemy_stats['health'] > 0]

class Room():
    def __init__(self, name, type=0):
        self.room_stats = {
            'tiles': [],
            'walltiles': [],
            'name': name,
            'type': 0
            }

class RoomManager():
    def __init__(self, array, grid_stats, rooms):
        self.array = array
        self.grid_stats = grid_stats
        self.pos = self.array_pos()
        self.rooms = rooms
        self.room_min = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
    def array_pos(self):
        pos = []
        for i in self.array:
            for j in i:
                if not (j.block_stats['x'] == 0 or j.block_stats['x'] == self.grid_stats['x_am']-1 or j.block_stats['y'] == 0 or j.block_stats['y'] == self.grid_stats['y_am']-1):
                    pos.append([j.block_stats['x'], j.block_stats['y']])
        return pos
    def create(self):
        for i in self.rooms:
            tiles = []
            tiles.append([choice(self.pos)])
            for j in self.room_min:
                tiles[0].append([tiles[0][0][0] + j[0], tiles[0][0][1] + j[1]])
            wall_tiles = []
            for j in self.room_min:
                if j[0] * j[1] == 0:
                    for k in range(3):
                        position = [
                            min(max(tiles[0][0][0]+j[0] * 2 + (k - 1) * abs(j[1]), 0), self.grid_stats['x_am']-1), 
                            min(max(tiles[0][0][1]+j[1] * 2 + (k - 1) * abs(j[0]), 0), self.grid_stats['y_am']-1)
                        ]
                        if position not in tiles[0]:
                            wall_tiles.append(position)
            tiles.append(wall_tiles)
            near_wall_tiles = []
            for j in self.room_min:
                if j[0] * j[1] == 0:
                    for k in range(5):
                        position = [
                            min(max(tiles[0][0][0]+j[0] * 3 + (k - 2) * abs(j[1]), 0), self.grid_stats['x_am']-1), 
                            min(max(tiles[0][0][1]+j[1] * 3 + (k - 2) * abs(j[0]), 0), self.grid_stats['y_am']-1)
                        ]
                        if position not in tiles[0]:
                            near_wall_tiles.append(position)
                elif j[0] * j[1] != 0:
                    position = [
                            min(max(tiles[0][0][0]+j[0] * 2, 0), self.grid_stats['x_am']-1), 
                            min(max(tiles[0][0][1]+j[1] * 2, 0), self.grid_stats['y_am']-1)
                        ]
                    if position not in tiles[0]:
                        near_wall_tiles.append(position)                    
            tiles.append(near_wall_tiles)
            for j in tiles:
                for k in j:
                    if k in self.pos:
                        self.pos.remove(k)
            i.room_stats['tiles'] = tiles[0]
            i.room_stats['wall_tiles'] = tiles[1]
                                                       
class Grid():
    def __init__(self, x_am, y_am, sqwidth, sqheight):
        self.grid_stats = {
            'x_am': x_am,
            'y_am': y_am,
            'sqwidth': sqwidth,
            'sqheight': sqheight,
            'stx': SCREEN_WIDTH/2-sqwidth*x_am/2,
            'sty': SCREEN_HEIGHT/2-sqheight*y_am/2
        }
        self.array = []
        self.rooms = []
    def empty_array(self):
        for i in range(self.grid_stats['y_am']):
            row = []
            for j in range(self.grid_stats['x_am']):
                row.append(Block(j, i, True))
            self.array.append(row)
    def generate_rooms(self, am):
        self.empty_array()
        room_list = []
        for i in range(am):
            room_list.append(Room(f'room{i}'))
        mng = RoomManager(self.array, self.grid_stats, room_list)
        mng.create()
    def build_array(self):
        self.generate_rooms(5)
    def grid_draw(self, linesize=1):
        for i in range(self.grid_stats['y_am']):
            for j in range(self.grid_stats['x_am']):
                arcade.draw_rectangle_filled(self.grid_stats['stx']+(self.grid_stats['sqwidth']*j), self.grid_stats['sty']+(self.grid_stats['sqheight']*i), self.grid_stats['sqwidth']-linesize, self.grid_stats['sqheight']-linesize, self.array[i][j].block_stats['color'])
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
        return [x_list.index(min(x_list)), y_list.index(min(y_list))]
    def avablock_list(self):
        pos_pos = []
        for i in self.array:
            for j in i:
                if j.block_stats['passable'] == True:
                    pos_pos.append(j)
        return pos_pos
        
class Block():
    def __init__(self, x, y, passable, roomname=[]):
        self.block_stats = {
            'x': x, 
            'y': y,
            'passable': passable,
            'on_block': 0,
            'room': roomname
        }
    def color_definer(self):
        global colorb
        if not self.block_stats['passable']:
            if self.block_stats['on_block'] == 0:
                self.block_stats['color'] = colorb.color['wall']
            else:
                self.block_stats['color'] = colorb.modify_color(colorb.color[self.block_stats['on_block']['color']], 'on_blockmod')
        else:
            if self.block_stats['on_block'] == 0:
                self.block_stats['color'] = colorb.color['empty']
            else:
                self.block_stats['color'] = colorb.modify_color(colorb.color[self.block_stats['on_block']['color']], 'on_blockmod') 

class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(colorb.color['background'])
        self.grid = Grid(12, 12, 40, 40)
        self.grid.build_array()
        self.player = Player(randint(0,self.grid.grid_stats['y_am']-1), randint(0,self.grid.grid_stats['x_am']-1), 20, 20, 'player', self.grid, True, 'player', 100, 10)
        self.entities = [self.player]
        self.move_frequence = 0.0
        self.enemy_count = 0
    def setup(self):
        pass
    def on_draw(self):
        self.clear()
    def on_update(self, delta_time):
        global move_frequence
        move_frequence += delta_time
        if move_frequence > .5:
            if randint(0, 4) == 5:
                if self.grid.grid_stats['y_am']*self.grid.grid_stats['x_am'] > len(self.entities):
                    colorb.randinrange(f'enemy{self.enemy_count}', 'enemy', 'background')
                    if self.grid.avablock_list():
                        block = choice(self.grid.avablock_list())
                        self.entities.append(Enemy(block.block_stats['y'], block.block_stats['x'], 20, 20, f'enemy{self.enemy_count}', self.grid, True, 'enemy', 10))
                        self.enemy_count += 1
                        block.block_stats['on_block'] = self.entities[-1].entity
                        block.block_stats['passable'] = False
            self.player.attack(self.player.check_enemies(self.entities))
            for i in self.entities:
                if not i.check_health()[1]:
                    self.grid.array[i.entity['row']][i.entity['column']].block_stats['passable'] = True
                    self.grid.array[i.entity['row']][i.entity['column']].block_stats['on_block'] = 0
                    self.entities.remove(i)
                    continue
            for j in self.entities:
                j.move()
            move_frequence = 0.0
        self.grid.update_color()
        arcade.start_render()
        self.grid.grid_draw()
        for i in self.entities:
            i.draw_entity()            
        arcade.finish_render()
    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.C:
            colorb.random_color('background')
            self.grid.update_color()
            arcade.set_background_color(colorb.color['background'])
    def on_mouse_press(self, x, y, button, modifiers):
        pos = self.grid.closest_block(x,y)
        print(pos)
        self.grid.array[pos[1]][pos[0]].block_stats['passable'] = not self.grid.array[pos[1]][pos[0]].block_stats['passable']
        self.grid.array[pos[1]][pos[0]].color_definer()

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    colorb.game = game
    arcade.run()

if __name__ == "__main__":
    main()