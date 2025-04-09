import pygame

running : bool = True

screenWidth : int = 800
screenHeight : int = 400

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("pathfinding-sim")
class Grid:
    def __init__(self, cellsize):
        self.cellSize = cellsize
        self.level = [
        "IIIIIIIIIIIIIIIIIIII",
        "IOOOOIOOOOOOOOOOOOOI",
        "IOOOIIIIIIIIIIIIOIOI",
        "IOOOIOOOOOOOOOOIOIOI",
        "IOOOIOIIIIOIOOOOOOOI",
        "IOOOOOOOOOOIOOOOIOII",
        "IOOOIOOOOOOOOOOOIOOI",
        "IOIIIOOIIIIIIIOOIOOI",
        "IOOOOOOOOOOOOOOOIOOI",
        "IIIIIIIIIIIIIIIIIIII"
        ]
        #column = 10
        #row == 20

    def draw(self):
        for i, row in enumerate(self.level):
            for j, column in enumerate(row):
                    if column == "I":
                        pygame.draw.rect(screen, (255, 255, 255), (j*self.cellSize, i*self.cellSize, self.cellSize, self.cellSize))

    def cellTaken(self, coord : tuple):
        cell = list(enumerate(self.level[coord[1]]))[coord[0]][1]
        if cell == "I": return True
        else: return False

class Pathfinder:
    def __init__(self, cellSize, cellmap):
        self.target : tuple = ()
        self.location : tuple = ()

        self.cellSize = cellSize
        self.cellmap = cellmap

        self.emptyCells : list  = self.findEmptyCells()
        self.junctions : list = self.getJunctions()

    def getRow(self, rowNum : int):
        row : dict = {}
        for count, value in enumerate(str(self.cellmap[rowNum])):
            row.update({count : value})
        return row

    def cellEmpty(self, coord : tuple):
        cell = list(enumerate(self.cellmap[coord[1]]))[coord[0]][1]
        if cell == "I": return False
        else: return True

    def findEmptyCells(self):
        emptyCells : list = []
        for y in range(len(self.cellmap)):
            for x in range(len(self.cellmap[y])):
                if self.cellEmpty((x, y)): emptyCells.append((x, y))
        return emptyCells

    def adjacentCells(self, cell : tuple):
        #0 : right, 1 : left, 2 : up, 3 : down 
        cells : list = [False, False, False, False]
        rowM : dict = {}
        rowT : dict = {}
        rowB : dict = {}
        for count, value in enumerate(str(self.cellmap[cell[1]])):
            rowM.update({count : value})
        
        if cell[0] != 0: 
            if rowM[cell[0]-1] != "I": cells[0] = True
            if cell[1] != -1: 
                for count, value in enumerate(str(self.cellmap[cell[1]+1])):
                    rowT.update({count : value})
                if rowT[cell[0]] != "I": cells[2] = True

        if cell[0] != 19: 
            if rowM[cell[0]+1] != "I": cells[1] = True
            if cell[1] != 9: 
                for count, value in enumerate(str(self.cellmap[cell[1]-1])):
                    rowB.update({count : value})
                if rowB[cell[0]] != "I": cells[3] = True

        return cells
    
    def getJunctions(self):
        junctions : list = []
        for i in range(len(self.emptyCells)):
            #0 : right, 1 : left, 2 : up, 3 : down 
            cells = self.adjacentCells(self.emptyCells[i])
            if cells[0] and cells[1]:
                if cells[2] or cells[3]:
                    junctions.append(self.emptyCells[i])
            if cells[2] and cells[3]:
                if cells[0] or cells[1]:
                    junctions.append(self.emptyCells[i])

        return junctions
        
    def createSutibleSpots(self):
        pass

    def createPaths(self):
        pass

    def findPath(self):
        pass
    
    def draw(self):
        for i in range(len(self.junctions)): pygame.draw.rect(screen, (255, 100, 0), (self.junctions[i][0]*self.cellSize, self.junctions[i][1]*self.cellSize, self.cellSize, self.cellSize))
        if self.target != (): pygame.draw.rect(screen, (255, 0, 0), (self.target[0]*self.cellSize, self.target[1]*self.cellSize, self.cellSize, self.cellSize))
        if self.location != (): pygame.draw.rect(screen, (0, 0, 255), (self.location[0]*self.cellSize, self.location[1]*self.cellSize, self.cellSize, self.cellSize))

grid = Grid(40)
pathfinding = Pathfinder(40, grid.level)
#print(pathfinding.getRow(0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        mouseX, mouseY = pygame.mouse.get_pos()
        if not grid.cellTaken((int((mouseX-(mouseX%pathfinding.cellSize))/pathfinding.cellSize), int((mouseY-(mouseY%pathfinding.cellSize))/pathfinding.cellSize))):
            pathfinding.location = (int((mouseX-(mouseX%grid.cellSize))/grid.cellSize), int((mouseY-(mouseY%grid.cellSize))/grid.cellSize))

    if pygame.mouse.get_pressed()[2]:
        mouseX, mouseY = pygame.mouse.get_pos()
        if not grid.cellTaken((int((mouseX-(mouseX%pathfinding.cellSize))/pathfinding.cellSize), int((mouseY-(mouseY%pathfinding.cellSize))/pathfinding.cellSize))):
            pathfinding.target = (int((mouseX-(mouseX%pathfinding.cellSize))/pathfinding.cellSize), int((mouseY-(mouseY%pathfinding.cellSize))/pathfinding.cellSize))

    pygame.Surface.fill(screen, (0, 0, 0))
    mouseX, mouseY = pygame.mouse.get_pos()
    #print((int((mouseX-(mouseX%pathfinding.cellSize))/pathfinding.cellSize), int((mouseY-(mouseY%pathfinding.cellSize))/pathfinding.cellSize)))
    pathfinding.draw()
    grid.draw()

    pygame.display.update()
