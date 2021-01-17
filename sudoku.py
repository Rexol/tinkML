import os
import random

class Game:
    @staticmethod
    def new_game():
        print("Incert number of filled cells:")
        filled_cells_number = Game.__get_new_game_input()
        return Game.Generator.RUN(filled_cells_number)
        
    @staticmethod
    def load_game():
        try:
            f = open('save.pkl', 'r')
        except IOError as e:
            print(u'Unable to open save file')
            exit()
        else:
            with  f:
                b = []
                if Game.__check_game_save_file(f):

                    i = 0
                    for line in f:
                        l = line.split(',')
                        l.pop()
                        b.append([])
                        for e in l:
                            b[i].append(int(e))
                        i += 1
                else:
                    print('File is corrupted')
                    exit()
                f.close()
                return b

    class Generator:
        @staticmethod
        def RUN(num_of_filled__cells =36):
            board = [[((i*3 + i//3 + j) % (9) + 1) for j in range(9)] for i in range(9)]

            #for i in board:
            #    for e in i:
            #        print(e, end = " ")
            #    print('')
            mix_func = ['Game.Generator.transposing(board)','Game.Generator.swap_rows_small(board)', 'Game.Generator.swap_colums_small(board)', 'Game.Generator.swap_rows_area(board)','Game.Generator.swap_colums_area(board)']

            for i in range(30):
                id_func = random.randrange(0,len(mix_func),1)
                board = eval(mix_func[id_func])

            iterator = 0
            while iterator < 81 - num_of_filled__cells:
                i,j = (random.randrange(0, 9 ,1), random.randrange(0, 9 ,1)) # Выбираем случайную ячейку
                if not board[i][j] == 0:
                    iterator += 1
                    board[i][j] = 0
        
            return board
        
            

        @staticmethod
        def transposing(board):
            board = [list(i) for i in zip(*board)]
            return board

        @staticmethod
        def swap_rows_small(board):
            area = random.randrange(0,3,1)
            line1 = random.randrange(0,3,1)
            N1 = area*3 + line1

            line2 = random.randrange(0,3,1)
            while (line1 == line2):
                line2 = random.randrange(0,3,1)

            N2 = area*3 + line2
            #номер 2 строки для обмена

            board[N1],board[N2] = board[N2], board[N1]
            return board

        @staticmethod
        def swap_colums_small(board):
            board = Game.Generator.transposing(board)
            board = Game.Generator.swap_rows_small(board)
            board = Game.Generator.transposing(board)
            return board

        @staticmethod
        def swap_rows_area(board):
            """ Swap the two area horizon """
            area1 = random.randrange(0,3,1)
            area2 = random.randrange(0,3,1)
            while (area1 == area2):
                area2 = random.randrange(0,3,1)

            for i in range(0, 3):
                N1, N2 = area1*3 + i, area2*3 + i
                board[N1], board[N2] = board[N2], board[N1]
            return board

        @staticmethod
        def swap_colums_area(board):
            board = Game.Generator.transposing(board)
            board = Game.Generator.swap_rows_area(board)
            board = Game.Generator.transposing(board)
            return board
        
    @staticmethod
    def __get_new_game_input():
        filled_cells_string = input()
        while not filled_cells_string.isdigit(): 
            print('Wrong input. Enter an integer from [0;81]')
            filled_cells_string = input()
        return int(filled_cells_string)

    @staticmethod
    def __check_game_save_file(f):
        f = open('save.pkl', 'r')
        it = 0
        for line in f:
            it += 1
            l = line.split(',')
            l.pop()
            if len(l) != 9:
                return False
            for i in l:
                if not i.isdigit():
                    return False
                if int(i) > 9:
                    return False
        if it != 9:
            return False
        return True

    @staticmethod
    def sudoku_solver(grid):
        grid_original = grid
        forwards = True
        i = 0
        it = 0
        while i < 9 * 9:
            it += 1
            if it == 1000:
                for l in grid:
                    print(l)
                print()
                print()
                print()
            #print("Checking original grid cell ")

            if Game.value(grid_original, i) == 0 and forwards:
                #print("Cell is empty in original grid, can place here.")
                for a in range(1, 10):
                    #print("Checking rows, columns, and cells for " + str(a) + "s ...")
                    if a not in Game.cell(grid, i) and a not in Game.row(grid, i) and a not in Game.column(grid, i):
                        #print("Placing a.")
                        grid[Game.grid_ref(i)[0]][Game.grid_ref(i)[1]] = a
                        i += 1
                        #print(grid)
                        break
                    else:
                        #print("Can't place " + str(a) + " here.")
                        if a == 9:
                            #print("We can't place anything here!")
                            forwards = False
                            if i > 0:
                               i -= 1  # goes back a cell
                               break
                            else:
                               forwards = True
                               break
                            #i -= 1
                            #break
            elif Game.value(grid_original, i) != 0 and forwards:
                #print("Cell is filled in original grid, can't place here.")
                i += 1

            elif Game.value(grid_original, i) == 0 and not forwards:
                #print("Cell is empty in original grid, can edit this one.")
                if grid[Game.grid_ref(i)[0]][Game.grid_ref(i)[1]] == 9:
                    #print("Cell can't be any other value; we can't place anything here!")
                    grid[Game.grid_ref(i)[0]][Game.grid_ref(i)[1]] = 0
                    # print("Resetting to zero.")
                    #print(grid)
                    if i >0:
                        i -= 1
                    else:
                        forwards = True
                    #i -= 1
                else:
                    for a in range(grid[Game.grid_ref(i)[0]][Game.grid_ref(i)[1]] + 1, 10):
                        #print("Checking rows, columns, and cells for " + str(a) + "s...")
                        if a not in Game.cell(grid, i) and a not in Game.row(grid, i) and a not in Game.column(grid, i):
                            #print("Placing a.")
                            grid[Game.grid_ref(i)[0]][Game.grid_ref(i)[1]] = a
                            #print(grid)
                            forwards = True
                            i += 1
                            break
                        else:
                            #print("Can't place here.")
                            if a == 9:
                                #print("We can't place anything here!")
                                grid[Game.grid_ref(i)[0]][Game.grid_ref(i)[1]] = 0
                                #print(grid)
                                if i > 0:
                                    i -= 1
                                    break
                                else:
                                    forwards = True
                                    break
                                #i -= 1
                                #break

            elif Game.value(grid_original, i) != 0 and not forwards:
                #print("Cell is filled in orignial grid, can't place here.")
                if i > 0:
                    i -= 1
                else:
                    forwards = True
                #i -= 1

        return grid

    @staticmethod
    def grid_ref(number):
        """function converts linear 0-81 item reference to (y,x) item reference"""
        grid_ref = (number // 9, number % 9)
        # to get the row we divide by nine and ignore the remainder
        # to get the column we divide by nine and only look at the remainder
        return grid_ref

    @staticmethod
    def value(grid, number):
        """function gets value of given linear item"""
        g_r = Game.grid_ref(number)
        value = grid[g_r[0]][g_r[1]]
        # just check a given grid for a given grid reference
        return value

    @staticmethod
    def cell(grid, number):
        """function returns array describing the cell that a linear item is in"""
        g_r = Game.grid_ref(number)
        cell_ref = (g_r[0] // 3, g_r[1] // 3)
        cell = []
        for i in range(3):
            for j in range(3):
                cell.append(grid[cell_ref[0]*3 + i][cell_ref[1]*3+j])
        return cell

    @staticmethod
    def row(grid, number):
        """function returns array describing the row that a linear item is in"""
        g_r = Game.grid_ref(number)
        row_ref = g_r[0]
        row =[]
        for i in range(9):
            row.append(grid[row_ref][i])
        return row

    @staticmethod
    def column(grid, number):
        """function returns array describing the column that a linear item is in"""
        g_r = Game.grid_ref(number)
        column_ref = g_r[1]
        column = []
        for i in range(9):
            column.append(grid[i][column_ref])
        return column


'''--------------------------------------------'''
class GameState:
    def __init__(self, mode = -1):
        self.M = mode
        self.board = []
        if mode == 0:
            self.board = Game.new_game()
        if mode == 1:
            self.board = Game.load_game()
        if mode == -1:
            self.board =[[0 for i in range(9)] for j in range(9)]
        
        self.col = [[] for i in range(9)]
        self.row = [[] for i in range(9)]
        self.square = [[] for i in range(9)]
        self.prefilled = [[0 for i in range(9)] for j in range(9)]
        self.numbers = [0 for i in range(10)]
        self.it = 0
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    self.it += 1
                    self.col[j].append(self.board[i][j])
                    self.row[i].append(self.board[i][j])
                    self.prefilled[i][j] = 1
                    self.square[(i//3)*3 + j//3].append(self.board[i][j])
                    self.numbers[self.board[i][j]] += 1

    def save_game(self):
        f = open('save.pkl', 'w')
        for l in self.board:
            for e in l:
                f.write(str(e))
                f.write(',')
            f.write('\n')
        f.close()

    def make_move(self):
        print('Savw game (insert save) or end input (insert exit)')
        print('Insert coordinates of cell that you want to update, then insert value,\n which you wsnt to insert')
        print('Insert x or save or exit:')
        x = input()
        if x == 'save':
            self.save_game()
            print('GAME SAVED')
        if x == 'exit':
            if self.M != -1:
                exit()
            if self.M == -1:
                return 1
        while not x.isdigit():
            print('Please incert number from 0 to 8:')
            x = input()
        print('Insert y:')
        y = input()
        while not y.isdigit():
            print('Please insert number from 0 to 8:')
            y = input()
        print('Insert value:')
        value = input()
        while not value.isdigit():
            print('Please enter number from 1 to 9:')
            value = input()
        if self.check_move_input(int(x), int(y), int(value)):
            self.change_cell_state(int(x), int(y), int(value))
        else:
            print('Unable update the cell')
            return 0
        return 0

    def check_move_input(self, x, y, value):
        if value == 0:
            return True
        if value in self.row[y]:
            return False
        if value in self.col[x]:
            return False
        if value in self.square[(y//3)*3 + x//3]:
            return False
        #if self.board[y][x] != 0:
        #    return False
        if self.prefilled[y][x] == 1:
            return False
        if self.numbers[value] == 9:
            return False
        return True

    def change_cell_state(self, x, y, value):
        if value != 0:
            self.board[y][x] = value
            self.col[x].append(value)
            self.row[y].append(value)
            self.numbers[value] += 1
            self.it += 1
            self.square[(y//3)*3 + x//3].append(value)
            return
        elif value == 0:
            prev = self.board[y][x]
            self.board[y][x] = 0
            self.col[x].remove(prev)
            self.row[y].remove(prev)
            self.numbers[prev] -= 1
            self.it -= 1
            self.square[(y//3)*3 + x//3].remove(prev)
            return

    def show(self):
        print('| 0 1 2 | 3 4 5 | 6 7 8 |')
        print(' +-------+-------+-------+')
        for i in range(3):
            for j in range(3):
                print(str(i*3 + j), end = "")
                print('|', end = '')
                for k in range(3):
                    for m in range(3):
                        print(' ' + str(self.board[i*3+j][k*3+m]), end = '')
                    print(' |', end='')
                print('')
            print(' +-------+-------+-------+')

if __name__ == '__main__':
    print ('Choose game mode: (0 - I play, 1 - I force to play)')
    mode = input()

    while not mode.isdigit():
        print ('Insert 0 or 1:')
        mode = input()
    mode = int(mode)
    if mode == 1:
        GS = GameState()
        while True:
            os.system('cls||clear')
            GS.show()
            if GS.make_move() == 1:
                break
                # Запустить решение судоку.
        board = Game.sudoku_solver(GS.board)
        print("Problem solved:")
        GS.board = board
        GS.show()
        exit()
    if mode == 0:
        print("0 - new game, 1 - load game")
        start = input()

        while not start.isdigit():
            print ('Insert 0 or 1:')
            start = input()
        GS = GameState(int(start))
        print('Game loaded')
        while True:
            os.system('cls||clear')
            GS.show()
            GS.make_move()
            if GS.it == 81:
                print('WIN')
                exit()