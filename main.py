import pygame

pygame.init()

running = True
screenWidth = 800
screenHeight = 400

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
            "IIIIIIIIIIIIIIIIaIIII"
        ]

    def draw(self):
        for i, row in enumerate(self.level):
            for j, column in enumerate(row):
                if column == "I":
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (j * self.cellSize, i * self.cellSize, self.cellSize, self.cellSize))

    def cellTaken(self, coord):
        return self.level[coord[1]][coord[0]] == "I"


class Pathfinder:
    def __init__(self, cellSize, cellmap):
        self.target = ()
        self.location = ()
        self.cellSize = cellSize
        self.cellmap = cellmap
        self.emptyCells = self.findEmptyCells()
        self.junctions = self.getJunctions()
        self.path = []

    def cellEmpty(self, coord):
        return self.cellmap[coord[1]][coord[0]] != "I"

    def findEmptyCells(self):
        empty = []
        for y in range(len(self.cellmap)):
            for x in range(len(self.cellmap[y])):
                if self.cellEmpty((x, y)):
                    empty.append((x, y))
        return empty

    def adjacentCells(self, cell):
        x, y = cell
        cells = [False, False, False, False]  # right, left, up, down

        if x + 1 < 20 and self.cellEmpty((x + 1, y)):
            cells[0] = True
        if x - 1 >= 0 and self.cellEmpty((x - 1, y)):
            cells[1] = True
        if y - 1 >= 0 and self.cellEmpty((x, y - 1)):
            cells[2] = True
        if y + 1 < 10 and self.cellEmpty((x, y + 1)):
            cells[3] = True

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
        
    def getClosestCellInDir(self, startingCell):
        x, y = startingCell
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # right, left, up, down
        encounterTypes = [0] * 4
        distances = [0] * 4

        for i, (dx, dy) in enumerate(directions):
            dist = 1
            while True:
                nx, ny = x + dx * dist, y + dy * dist
                if (nx, ny) == self.target:
                    encounterTypes[i] = 2
                    distances[i] = dist
                    break
                elif (nx, ny) in self.junctions:
                    encounterTypes[i] = 0
                    distances[i] = dist
                    break
                elif (nx, ny) not in self.emptyCells:
                    encounterTypes[i] = 1
                    distances[i] = dist - 1
                    break
                dist += 1

        return encounterTypes, distances

    def createPaths(self):
        self.path.clear()
        checkList = [self.location]
        listPos = 0
        visited = set()
        targetFound = False

        while not targetFound and listPos < len(checkList):
            current = checkList[listPos]
            listPos += 1
            if current in visited:
                continue
            visited.add(current)

            encounterTypes, distances = self.getClosestCellInDir(current)

            for i in range(4):
                if distances[i] == 0:
                    continue

                if i == 0:
                    end = (current[0] + distances[i], current[1])
                elif i == 1:
                    end = (current[0] - distances[i], current[1])
                elif i == 2:
                    end = (current[0], current[1] - distances[i])
                elif i == 3:
                    end = (current[0], current[1] + distances[i])

                self.path.append((current, end))

                if encounterTypes[i] == 2:
                    targetFound = True
                    break
                elif encounterTypes[i] == 0:
                    checkList.append(end)

    def draw(self):
        cellSize = self.cellSize
        for junction in self.junctions:
            pygame.draw.rect(screen, (255, 100, 0),
                             (junction[0] * cellSize, junction[1] * cellSize, cellSize, cellSize))

        if self.target:
            pygame.draw.rect(screen, (255, 0, 0),
                             (self.target[0] * cellSize, self.target[1] * cellSize, cellSize, cellSize))
        if self.location:
            pygame.draw.rect(screen, (0, 0, 255),
                             (self.location[0] * cellSize, self.location[1] * cellSize, cellSize, cellSize))

        for start, end in self.path:
            startPos = (start[0] * cellSize + cellSize / 2, start[1] * cellSize + cellSize / 2)
            endPos = (end[0] * cellSize + cellSize / 2, end[1] * cellSize + cellSize / 2)
            pygame.draw.line(screen, (0, 255, 0), startPos, endPos, 2)


grid = Grid(40)
pathfinding = Pathfinder(40, grid.level)

pathfinding.location = (8, 5)
pathfinding.target = (6, 1)
pathfinding.createPaths()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouseX, mouseY = pygame.mouse.get_pos()
    gridX = mouseX // pathfinding.cellSize
    gridY = mouseY // pathfinding.cellSize

    if pygame.mouse.get_pressed()[0]:
        if not grid.cellTaken((gridX, gridY)):
            pathfinding.location = (gridX, gridY)
            pathfinding.createPaths()

    if pygame.mouse.get_pressed()[2]:
        if not grid.cellTaken((gridX, gridY)):
            pathfinding.target = (gridX, gridY)
            pathfinding.createPaths()

    screen.fill((0, 0, 0))
    grid.draw()
    pathfinding.draw()
    pygame.display.update()
