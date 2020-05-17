import pygame, sys, os, random
import numpy as np

###Creates a sudoku grid with some numbers.###

#constants
screenSize = (450,450)
origin = (0,0)
black = (0,0,0)
white = (255,255,255)
tile_size = (50,50)
number_keys = ["".join(["K_", str(i)]) for i in range(10)]
print(number_keys)

#start
pygame.init()
screen = pygame.display.set_mode(screenSize)
background= pygame.Surface(screenSize)
background.fill(white)

class Bar(object):
    def __init__(self, n, dimensions):
        self.number = n
        self.dimensions = dimensions
        self.position = (0,0)
        self.surface = pygame.Surface(dimensions)
        self.surface.fill(black)

    def draw(self, screen):
        screen.blit(self.surface, self.position)
        
class Vertical_bar(Bar):
    def __init__(self, n, dimensions= [2,450]):
        if n%3==0:
            dimensions = (4,450)
        super().__init__(n, dimensions)
        self.position = (50*n-1, 0)


class Horizontal_bar(Bar):
    def __init__(self, n, dimensions= (450,2)):
        if n%3==0:
            dimensions = (450,4)
        super().__init__(n,dimensions)
        self.position = (0, 50*n-1)

class Bar_list(object):
    def __init__(self, bar_object, amount= 10):
        self.items = [bar_object(i) for i in range(amount)]
    def draw(self, screen):
        for item in self.items:
            item.draw(screen)

class Tile(object):
    def __init__(self, row, column, n= 0,
                font= pygame.font.Font(pygame.font.get_default_font(), 50)):
        self.row = row
        self.font = font
        self.column = column
        self.number = n
        self.revealed= False
        self.position = (row*50+1, column*50+1)
        self.surface_std = pygame.Surface(tile_size)
        self.surface_std.fill(white)
        message = font.render(str(self.number), True, black)
        self.surface_hover = pygame.Surface(tile_size)
        self.surface_hover.fill((255,0,0))
        self.surface_reveal = pygame.Surface(tile_size)
        self.surface_reveal.fill(white)
        self.surface_reveal.blit(message, (10,0))
    def draw(self, screen, mouse_pos):
        if self.revealed:
            screen.blit(self.surface_reveal, self.position)
        elif (mouse_pos[0] in range(self.position[0], self.position[0]+50)and mouse_pos[1] in range(self.position[1], self.position[1]+50)):
            screen.blit(self.surface_hover, self.position)
        else:
            screen.blit(self.surface_std, self.position)
            
    def reveal(self, entry):
        if not self.revealed:
            self.revealed= entry == self.number or entry == 0
            return self.revealed
        else:
            return None
    def hide(self):
        self.revealed = False
        return

    def update(self, n):
        if True:
            self.number = n
            self.surface_std = pygame.Surface(tile_size)
            self.surface_std.fill(white)
            message = self.font.render(str(self.number), True, black)
            self.surface_hover = pygame.Surface(tile_size)
            self.surface_hover.fill((255,0,0))
            self.surface_reveal = pygame.Surface(tile_size)
            self.surface_reveal.fill(white)
            self.surface_reveal.blit(message, (10,0))
            return n

class Tile_list(object):
    def __init__(self, rows= 9, columns= 9):
        self.item_list=[]
        for i in range(rows):
            self.item_list.append([])
            for j in range(columns):
                self.item_list[i].append(Tile(i, j, 0))

    def draw(self, screen, mouse_pos):
        for column in self.item_list:
            for tile in column:
                tile.draw(screen, mouse_pos)

    def reveal(self, entry, pos):
        print(self.item_list[pos[0]][pos[1]].reveal(entry))

    def start_reveal(self, n):
        position_set = set()
        for row in self.item_list:
            for tile in row:
                position_set.add((tile.row,tile.column))
                tile.hide()
        
        for i in range(n):
            position = random.choice(list(position_set))
            position_set.remove(position)
            x = position[0]
            y = position[1]
            self.item_list[x][y].reveal(0)

    def update(self, pos):
        if self.item_list[pos[0]][pos[1]].number == 0:
            n = random.choice(self.possible_values(pos))
            self.item_list[pos[0]][pos[1]].update(n)
    
    def possible_values(self, pos):
        if self.item_list[pos[0]][pos[1]].number != 0:
            return None
        else:
            taken = set()
            for item in self.item_list[pos[0]]:
                taken.add(item.number)
            for i in range(9):
                item = self.item_list[i][pos[1]]
                taken.add(item.number)
            chunk_x = pos[0]//3
            chunk_y = pos[1]//3
            for i in range(chunk_x*3, chunk_x*3+3):
                for j in range(chunk_y*3, chunk_y*3+3):
                    item = self.item_list[i][j]
                    taken.add(item.number)        
            options = list({1,2,3,4,5,6,7,8,9}-taken)
            return options

    def reset(self):
        for row in self.item_list:
            for cell in row:
                cell.update(0)
        


def mouse_to_tile(mouse_pos):
    return (mouse_pos[0]//50, mouse_pos[1]//50)
               

tile_list = Tile_list()

vertical_bars = Bar_list(Vertical_bar)
horizontal_bars = Bar_list(Horizontal_bar)
tile_list.start_reveal(81)


while True:
    curr = 10
    curr_pos = (10,10)
    update_pos = set()
    for i in range(9):
        for j in range(9):
            if (tile_list.possible_values((i,j)) is not None):
                value = len(tile_list.possible_values((i,j)))
                if value < curr:
                    curr = value
                    curr_pos = (i,j)
                    update_pos = set([curr_pos])
                elif value == curr:
                    curr = value
                    curr_pos = (i,j)
                    update_pos.add(curr_pos)
    print (curr, curr_pos)
    if curr == 10:
        break
    elif curr == 0:
        tile_list.reset()
        print("""
Failed to create a sudoku
###Reset Completed###

""")
        continue
    selected = random.choice(list(update_pos))
    print("Revealing ", selected)
    if (tile_list.possible_values(selected) is not None):
        tile_list.update(selected)
    ###Draw
    screen.blit(background, origin)
    tile_list.draw(screen, (0,0))
    vertical_bars.draw(screen)
    horizontal_bars.draw(screen)
    pygame.display.flip()
    #pygame.time.delay(50)

tile_list.start_reveal(40)

while True:
    ###Register events
    mouse_pos = pygame.mouse.get_pos()
    pos = mouse_to_tile(mouse_pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            entry = event.key-48
            if entry in range(0,10):
                tile_list.reveal(entry, pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            tile_list.possible_values(mouse_to_tile(mouse_pos))
            
    ###Draw
    screen.blit(background, origin)
    tile_list.draw(screen, mouse_pos)
    vertical_bars.draw(screen)
    horizontal_bars.draw(screen)
    pygame.display.flip()
    pygame.time.delay(50)

                    
