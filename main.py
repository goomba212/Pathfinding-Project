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
        self.path : list = []

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
        adjecentCells : list =  []
        for i in range(len(self.emptyCells)):
            #0 : right, 1 : left, 2 : up, 3 : down 
            cells = self.adjacentCells(self.emptyCells[i])
            if cells[0] and cells[1]:
                if cells[2] or cells[3]:
                    junctions.append(self.emptyCells[i])
                    adjecentCells.append(cells)

            if cells[2] and cells[3]:
                if cells[0] or cells[1]:
                    junctions.append(self.emptyCells[i])
                    adjecentCells.append(cells)

            if cells[0]^cells[1] and cells[2]^cells[3]: 
                junctions.append(self.emptyCells[i])
                adjecentCells.append(cells)

        cellsToRemove : list = []
        cellsToAdd : list = []

        for i in range(len(junctions)):
            junctionCell : tuple = junctions[i] 
            cells : list = [False, False, False, False]

            if (junctionCell[0]-1, junctionCell[1]) in junctions or adjecentCells[i][0]: cells[0] = True
            if (junctionCell[0]+1, junctionCell[1]) in junctions or adjecentCells[i][1]: cells[1] = True
            if (junctionCell[0], junctionCell[1]-1) in junctions or adjecentCells[i][2]: cells[2] = True
            if (junctionCell[0], junctionCell[1]+1) in junctions or adjecentCells[i][3]: cells[3] = True

            if cells[0] and cells[1] and cells[2] and cells[3]: cellsToRemove.append(junctionCell)

        for i in range(len(cellsToRemove)): junctions.remove(cellsToRemove[i])

        return junctions

    def getClosestCellInDir(self, startingCell : tuple):
        currentCell = False
        currentPos = 1

        distances = [0, 0, 0, 0]
        encounterTypes = [0, 0, 0, 0]
        
        while not currentCell: #right
            #0 = junction, 1 = wall, 2 = target
            if (startingCell[0]+currentPos, startingCell[1]) in self.junctions: 
                distances[0] = currentPos 
                encounterTypes[0] = 0
                currentCell = True
            elif (startingCell[0]+currentPos, startingCell[1]) not in self.emptyCells:
                distances[0] = currentPos-1
                encounterTypes[0] = 1
                currentCell = True
            elif (startingCell[0]+currentPos, startingCell[1]) == self.target:
                distances[0] = currentPos-1
                encounterTypes[0] = 2
                currentCell = True
                
            currentPos += 1

        currentCell = False
        
        while not currentCell: #left
            #0 = junction, 1 = wall, 2 = target
            if (startingCell[0]-currentPos, startingCell[1]) in self.junctions: 
                distances[1] = currentPos
                encounterTypes[1] = 0
                currentCell = True
            elif (startingCell[0]-currentPos, startingCell[1]) not in self.emptyCells:
                distances[1] = currentPos-1
                encounterTypes[1] = 1
                currentCell = True
            elif (startingCell[0]-currentPos, startingCell[1]) == self.target:
                distances[1] = currentPos-1
                encounterTypes[1] = 2
                currentCell = True
                
            currentPos += 1

        currentCell = False
        
        while not currentCell: #up
            #0 = junction, 1 = wall, 2 = target
            if (startingCell[0], startingCell[1]+currentPos) in self.junctions: 
                distances[2] = currentPos
                encounterTypes[2] = 0
                currentCell = True
            elif (startingCell[0], startingCell[1]+currentPos) not in self.emptyCells:
                distances[2] = currentPos-1
                encounterTypes[2] = 1
                currentCell = True
            elif (startingCell[0], startingCell[1]+currentPos) == self.target:
                distances[2] = currentPos-1
                encounterTypes[2] = 2
                currentCell = True
                
            currentPos += 1

        currentCell = False
        
        while not currentCell: #down
            #0 = junction, 1 = wall, 2 = target
            if (startingCell[0], startingCell[1]-currentPos) in self.junctions:
                distances[3] = currentPos
                encounterTypes[3] = 0
                currentCell = True
            elif (startingCell[0], startingCell[1]-currentPos) not in self.emptyCells:
                distances[3] = currentPos-1
                encounterTypes[3] = 1
                currentCell = True
            elif (startingCell[0], startingCell[1]-currentPos) == self.target:
                distances[3] = currentPos-1
                encounterTypes[3] = 2
                currentCell = True
            
            currentPos += 1

        return encounterTypes, distances
        
    def createSutibleSpots(self):
        pass

    def createPaths(self):
        #0 : right, 1 : left, 2 : up, 3 : down 
        self.path.clear()
        checkList : list = [(self.location)]
        listPos = 0
        targetFound = False
        
        while not targetFound:
          if listPos == 0: encounterTypes, distances = self.getClosestCellInDir(self.location)
          else: encounterTypes, distances = self.getClosestCellInDir(checkList[listPos])
          onwards = True
          
          for i in range(4):
              if encounterTypes == 0: 
                if i == 0: checkList.append((self.location[0]+distances[0], self.location[1]))
                if i == 1: checkList.append((self.location[0]-distances[1], self.location[1]))
                if i == 2: checkList.append((self.location[0], self.location[1]+distances[2]))
                if i == 3: checkList.append((self.location[0], self.location[1]-distances[3]))
              if encounterTypes == 1: onwards = False
              if encounterTypes == 2: targetFound = True 
                
              if onwards:  
                self.path.append((self.location, (self.location[0]+distances[0], self.location[1])))
                #self.path.append((self.location, (self.location[0]-distances, self.location[1])))
          #if i == 2: self.path.append((self.location, (self.location[0], self.location[1]+distances)))
          #if i == 3: self.path.append((self.location, (self.location[0], self.location[1]-distances)))
        
    def findPath(self):
        pass

    def draw(self):
        cellSize = self.cellSize
        for i in range(len(self.junctions)): pygame.draw.rect(screen, (255, 100, 0), (self.junctions[i][0]*cellSize, self.junctions[i][1]*cellSize, cellSize, cellSize))
        if self.target != (): pygame.draw.rect(screen, (255, 0, 0), (self.target[0]*cellSize, self.target[1]*cellSize, cellSize, cellSize))
        if self.location != (): pygame.draw.rect(screen, (0, 0, 255), (self.location[0]*cellSize, self.location[1]*cellSize, cellSize, cellSize))
        for i in range(len(self.path)):
            startPos = ((self.path[i][0][0]*cellSize)+cellSize*0.5, (self.path[i][0][1]*cellSize)+cellSize*0.5)
            endPos = ((self.path[i][1][0]*cellSize)+cellSize*0.5, (self.path[i][1][1]*cellSize)+cellSize*0.5)
            pygame.draw.line(screen, (0, 255, 0), startPos, endPos)

grid = Grid(40)
pathfinding = Pathfinder(40, grid.level)

pathfinding.location = (8, 5)
pathfinding.target = (6, 1)

pathfinding.createPaths()
#print(pathfinding.getRow(0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        mouseX, mouseY = pygame.mouse.get_pos()
        if not grid.cellTaken((int((mouseX-(mouseX%pathfinding.cellSize))/pathfinding.cellSize), int((mouseY-(mouseY%pathfinding.cellSize))/pathfinding.cellSize))):
            pathfinding.location = (int((mouseX-(mouseX%grid.cellSize))/grid.cellSize), int((mouseY-(mouseY%grid.cellSize))/grid.cellSize))
            pathfinding.createPaths()

    if pygame.mouse.get_pressed()[2]:
        mouseX, mouseY = pygame.mouse.get_pos()
        if not grid.cellTaken((int((mouseX-(mouseX%pathfinding.cellSize))/pathfinding.cellSize), int((mouseY-(mouseY%pathfinding.cellSize))/pathfinding.cellSize))):
            pathfinding.target = (int((mouseX-(mouseX%pathfinding.cellSize))/pathfinding.cellSize), int((mouseY-(mouseY%pathfinding.cellSize))/pathfinding.cellSize))

    pygame.Surface.fill(screen, (0, 0, 0))
    mouseX, mouseY = pygame.mouse.get_pos()
    grid.draw()
    pathfinding.draw()
    print((int((mouseX-(mouseX%pathfinding.cellSize))/pathfinding.cellSize), int((mouseY-(mouseY%pathfinding.cellSize))/pathfinding.cellSize)))

    pygame.display.update()
