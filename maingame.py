from cmath import inf
import arcade
from random import randint, choice, shuffle
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

colorb = Color([100,100,100])
cmult = {
    'wall': (.5, .5, .5),
    'empty': (1.5, 1.5, 1.5),
    'on_blockmod': (.75, .75, .75, 'm'),
    'player': (1, 1, 1, 'f'),
    'enemy': ([0.5, 2], [0.5, 2], [0.5, 2], 'g')
}
for name,c in cmult.items():
    colorb.manual_edit(c, name, 'background')
colorb.color_change()

class Entity():
    def __init__(self, x, y, w, h, colorname, grid, moveable, entype):
        self.entity = {
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'color': colorname,
            'moveable': moveable,
            'entype': entype
        }
        self.grid = grid
        self.grid.array[self.entity['x']][self.entity['y']].block_stats['on_block'] = self.entity
    def draw_entity(self):
        arcade.draw_rectangle_filled(self.grid.grid_stats['stx']+self.grid.grid_stats['sqwidth']*self.entity['x'], 
                                    self.grid.grid_stats['sty']+self.grid.grid_stats['sqheight']*self.entity['y'], 
                                    self.entity['width'], self.entity['height'], colorb.color[self.entity['color']])
    def pos_around(self, p_check=False):
        blocks = [
            self.grid.array[min(self.entity['x']+1, self.grid.grid_stats['x_am']-1)][self.entity['y']],
            self.grid.array[max(self.entity['x']-1, 0)][self.entity['y']],
            self.grid.array[self.entity['x']][min(self.entity['y']+1, self.grid.grid_stats['y_am']-1)],
            self.grid.array[self.entity['x']][max(self.entity['y']-1, 0)]
            ]
        block_list = []
        for b in blocks:
            if b.block_stats['passable'] == True or not p_check:
                if not (b.block_stats['x'] == self.entity['x'] and b.block_stats['y'] == self.entity['y']):
                    block_list.append(b)
        return block_list
    def move(self):
        moves = self.pos_around(True)
        if len(moves) != 0 and self.entity['moveable']:
            move = choice(moves)
            self.grid.array[self.entity['x']][self.entity['y']].block_stats['on_block'] = 0
            self.grid.array[self.entity['x']][self.entity['y']].block_stats['passable'] = True
            self.grid.array[self.entity['x']][self.entity['y']].color_definer()
            self.entity['x'] = move.block_stats['x']
            self.entity['y'] = move.block_stats['y']
            self.grid.array[self.entity['x']][self.entity['y']].block_stats['on_block'] = self.entity
            self.grid.array[self.entity['x']][self.entity['y']].block_stats['passable'] = False
            self.grid.array[self.entity['x']][self.entity['y']].color_definer()

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
                enm_pos.append([i, [i.entity['x'], i.entity['y']]])
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
    def __init__(self, name, rtype=0):
        self.room_stats = {
            'tiles': [],
            'wall_tiles': [],
            'name': name,
            'type': rtype,
            'color': name
            }
    def activate_walls(self):
        for i in self.room_stats['wall_tiles']:
            i.block_stats['passable'] = False
            if i in self.room_stats['tiles']:
                self.room_stats['tiles'].remove(i)
    def mark_walls(self):
        for i in self.room_stats['wall_tiles']:
            i.block_stats['on_block'] = self.room_stats                                                                        
class Grid():
    def __init__(self, x_am, y_am, sqwidth, sqheight):
        self.grid_stats = {
            'x_am': x_am,
            'y_am': y_am,
            'sqwidth': sqwidth,
            'sqheight': sqheight,
            'stx': SCREEN_WIDTH/2-sqwidth*x_am/2,
            'sty': SCREEN_HEIGHT/2-sqheight*y_am/2,
            'room_gen_pos': [],
            'room_walls': [[-1,0], [1,0], [0,-1], [0,1]],
            'room_near_walls': [[1,1], [1,-1], [-1,1], [-1,-1], [-2,0], [2,0], [0,-2], [0,2]]
        }
        self.array = []
        self.rooms = []
        self.gen_blocks = {}
        self.walls = {}
    def empty_array(self):
        for i in range(self.grid_stats['x_am']):
            x = []
            for j in range(self.grid_stats['y_am']):
                x.append(Block(i, j, True))
            self.array.append(x)
    def array_pos(self):
        for i in self.array:
            for j in i:
                if not (j.block_stats['x'] == 0 or j.block_stats['x'] == self.grid_stats['x_am']-1 or j.block_stats['y'] == 0 or j.block_stats['y'] == self.grid_stats['y_am']-1):
                    self.grid_stats['room_gen_pos'].append([j.block_stats['x'], j.block_stats['y']])
    def generate_rooms(self, am):
        self.empty_array()
        self.array_pos()
        for i in range(am):
            self.rooms.append(Room(f'room{i}'))
            colorb.randinrange(f'room{i}', 'enemy', 'background')
        for i in self.rooms:
            tiles = []
            if not self.grid_stats['room_gen_pos']:
                break
            pos = choice(self.grid_stats['room_gen_pos'])
            print(pos)
            tiles.append([self.array[pos[0]][pos[1]]]) 
            wall_tiles = []
            for j in self.grid_stats['room_walls']:
                block = self.array[min(max(tiles[0][0].block_stats['x']+ j[0], 0), self.grid_stats['x_am']-1)][min(max(tiles[0][0].block_stats['y']+ j[1], 0), self.grid_stats['y_am']-1)]
                if block not in tiles[0]:
                    wall_tiles.append(block)
                    i.room_stats['wall_tiles'].append(block)
                    if str(block.block_stats['x'])+' '+str(block.block_stats['y']) in self.gen_blocks.keys():
                        self.gen_blocks[str(block.block_stats['x'])+' '+str(block.block_stats['y'])].append(i)
                    else:
                        self.gen_blocks[str(block.block_stats['x'])+' '+str(block.block_stats['y'])] = [i]
            tiles.append(wall_tiles)
            for j in tiles:
                for k in j:
                    if [k.block_stats['x'], k.block_stats['y']] in self.grid_stats['room_gen_pos']:
                        self.grid_stats['room_gen_pos'].remove([k.block_stats['x'], k.block_stats['y']])
    def expand_rooms(self):
        while self.gen_blocks != {}:
            blockname = choice(list(self.gen_blocks.keys()))
            block = blockname.split()
            block[0], block[1] = int(block[0]), int(block[1])
            ablock = self.array[block[0]][block[1]]
            if len(self.gen_blocks[blockname]) == 1:
                self.gen_blocks[blockname][0].room_stats['tiles'].append(ablock)
                self.gen_blocks[blockname][0].room_stats['wall_tiles'].remove(ablock)
                blocks = [
                self.array[min(block[0]+1, self.grid_stats['x_am']-1)][block[1]],
                self.array[max(block[0]-1, 0)][block[1]],
                self.array[block[0]][min(block[1]+1, self.grid_stats['y_am']-1)],
                self.array[block[0]][max(block[1]-1, 0)]
                ]
                for i in blocks:
                    valid = True
                    for j in self.rooms:
                        if not i in j.room_stats['tiles']:
                            if (i in j.room_stats['wall_tiles'] and j != self.gen_blocks[blockname][0]) or i not in j.room_stats['wall_tiles']:
                                continue
                            else:
                                valid = False
                                break                                
                        else:
                            valid = False
                            break
                    if valid:
                        if str(i.block_stats['x'])+' '+str(i.block_stats['y']) in self.gen_blocks.keys():
                            self.gen_blocks[str(i.block_stats['x'])+' '+str(i.block_stats['y'])].append(self.gen_blocks[blockname][0])
                        else:
                            self.gen_blocks[str(i.block_stats['x'])+' '+str(i.block_stats['y'])] = [self.gen_blocks[blockname][0]]
                        self.gen_blocks[blockname][0].room_stats['wall_tiles'].append(i)
                self.update_color()
            self.gen_blocks.pop(blockname)
    def create_entrances(self):
        pass
    def build_array(self):
        self.generate_rooms(3)
        print(self.gen_blocks)
        self.expand_rooms()
        for i in self.rooms:
            i.activate_walls()
    def grid_draw(self, linesize=1):
        self.update_color()
        for i in range(self.grid_stats['x_am']):
            for j in range(self.grid_stats['y_am']):
                arcade.draw_rectangle_filled(self.grid_stats['stx']+(self.grid_stats['sqwidth']*i), self.grid_stats['sty']+(self.grid_stats['sqheight']*j), self.grid_stats['sqwidth']-linesize, self.grid_stats['sqheight']-linesize, self.array[i][j].block_stats['color'])
    def update_color(self):
        for i in self.array:
            for j in i:
                j.color_definer()
    def closest_block(self, x, y):
        x_list = []
        y_list = []
        for i in range(len(self.array)):
            x_list.append(abs(self.grid_stats['stx']+(self.array[i][0].block_stats['x'])*self.grid_stats['sqwidth']-x))
        for i in range(len(self.array[0])):
            y_list.append(abs(self.grid_stats['sty']+(self.array[0][i].block_stats['y'])*self.grid_stats['sqheight']-y))
        return [x_list.index(min(x_list)), y_list.index(min(y_list))]
    def avablock_list(self):
        pos_pos = []
        for i in self.array:
            for j in i:
                if j.block_stats['passable'] == True:
                    pos_pos.append(j)
        return pos_pos
        
class Block():
    def __init__(self, x, y, passable, room=[]):
        self.block_stats = {
            'x': x, 
            'y': y,
            'passable': passable,
            'on_block': 0,
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
        self.grid = Grid(8, 8, 40, 40)
        self.grid.build_array()
        self.player = Player(randint(0,self.grid.grid_stats['x_am']-1), randint(0,self.grid.grid_stats['y_am']-1), 20, 20, 'player', self.grid, True, 'player', 100, 10)
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
                    self.grid.array[i.entity['x']][i.entity['y']].block_stats['passable'] = True
                    self.grid.array[i.entity['x']][i.entity['y']].block_stats['on_block'] = 0
                    self.entities.remove(i)
                    continue
            for j in self.entities:
                j.move()
                pass
            move_frequence = 0.0
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
        self.grid.array[pos[0]][pos[1]].block_stats['passable'] = not self.grid.array[pos[0]][pos[1]].block_stats['passable']
        self.grid.array[pos[0]][pos[1]].color_definer()

def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    colorb.game = game
    arcade.run()

if __name__ == "__main__":
    main()