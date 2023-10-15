def sudoku_solver(solved_sudoku):
    satisfiedConstraints = list() #list of satisfied constraints
    domains = [["123456789" for x in range(9)] for y in range(9)] #list of domains for each cell
    initialDomains = domains #to check whether a number was initially contained in the initial pre prune domain otherwise it would be an invalid satisfied constraint
    invalidSudoku = [[-1, -1, -1, -1, -1, -1, -1, -1, -1], #preset invalid sudoku
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                     [-1, -1, -1, -1, -1, -1, -1, -1, -1]]

    def MRV(sudoku):
        initialValue = True #to be able to compare values
        lowestValue = None 

        for y in range(9):
            for x in range(9):
                if sudoku[y][x] == 0: #if the value of the cell is 0
                    if len(domains[y][x]) == 1: #check length of domains and compare
                        return y, x
                    elif initialValue:
                        lowestValue = y, x
                        initialValue = False
                    else:
                        if len(domains[lowestValue[0]][lowestValue[1]]) > len(domains[y][x]):
                            lowestValue = y, x

        if not initialValue:
            return lowestValue[0], lowestValue[1]
        else:
            return None
   
    def LCV(row, col): #choose domain order depending on number of appearances of a value in neighbouring domains
        initialAppearance = True
        appearanceDomainList = list()
        domainListOrder = list()

        for number in domains[row][col]:
            appearances = 0
            for r in range(9):
                if number in domains[r][col] and r != row:
                    appearances = appearances + 1
            for c in range(9):
                if number in domains[row][c] and c != col:
                    appearances = appearances + 1
            initialRow = (row // 3) * 3 #integer division
            initialColumn = (col // 3) * 3 #integer division
            for y in range((initialRow), ((initialRow) + 3), 1): #check square
                for x in range((initialColumn), ((initialColumn) + 3), 1):
                    if number in domains[y][x] and y != row and x != col:
                        appearances = appearances + 1
            if initialAppearance == True:
                appearanceDomainList.append(number + str(appearances))
                initialAppearance = False
            else:
                for x in range(0, len(appearanceDomainList) - 1, 1):
                    if appearances > int(appearanceDomainList[x][1]) and appearances < int(appearanceDomainList[x + 1][1]):
                        appearanceDomainList.insert(x + 1, number + str(appearances))
                if appearances < int(appearanceDomainList[0][1]):
                    appearanceDomainList.insert(0, number + str(appearances))
                else:
                    appearanceDomainList.insert(len(appearanceDomainList), number + str(appearances))
       
        for i in range(0, len(appearanceDomainList), 1):
            domainListOrder.append(appearanceDomainList[i][0])

        return domainListOrder

   
    def update_constraints(num):
        if len(satisfiedConstraints) > 0:
            value = satisfiedConstraints[-1][1] #gets the number involved in domain value pruning
            while num == value: #while the number involved in a domain value pruning is the same as requested
                domainRow = int((satisfiedConstraints[-1][0])[0]) #gets row involved
                domainCol = int((satisfiedConstraints[-1][0])[1]) #gets column involved
                satisfiedConstraints.pop() #removes satsified constraint as no longer satisfied

                if len(domains[domainRow][domainCol]) > 1: #puts value in correct order for backtracking purposes
                    for x in range(0, len(domains[domainRow][domainCol]) - 1, 1):
                        if int((domains[domainRow][domainCol])[x]) < int(value) and int(value) < int((domains[domainRow][domainCol])[x + 1]):
                            domains[domainRow][domainCol] = (domains[domainRow][domainCol])[:x + 1] + value + (domains[domainRow][domainCol])[x + 1:]
                    if int(value) < int((domains[domainRow][domainCol])[0]):
                        domains[domainRow][domainCol] = value + domains[domainRow][domainCol]
                    elif int(value) > int((domains[domainRow][domainCol])[-1]):
                        domains[domainRow][domainCol] = domains[domainRow][domainCol] + value
                elif len(domains[domainRow][domainCol]) == 1:
                    if int(value) < int((domains[domainRow][domainCol])[0]):
                        domains[domainRow][domainCol] = value + domains[domainRow][domainCol]
                    else:
                        domains[domainRow][domainCol] = domains[domainRow][domainCol] + value
                else:
                    domains[domainRow][domainCol] = value

                if len(satisfiedConstraints) > 0: #so an error is not thrown if it is an empty list
                    value = satisfiedConstraints[-1][1]
                else:
                    value = "0"
       
    def initial_is_valid(sudoku): #pre pruning and checking initial sudoku is valid
        initiallyValid = True
       
        for row in range(9):
            for col in range(9):
                if sudoku[row][col] != 0:
                    for r in range(9): #check col by checking value in each row (r)
                        if sudoku[r][col] == 0 and r != row:
                            domains[r][col] = domains[r][col].replace(str(sudoku[row][col]), '') #update values in domains
                        if sudoku[r][col] == sudoku[row][col] and r != row: #makes sure no conflicting values
                            initiallyValid = False
                    for c in range(9): #check row by checking value in each column (c)
                        if sudoku[row][c] == 0 and c != col:
                            domains[row][c] = domains[row][c].replace(str(sudoku[row][col]), '')
                        if sudoku[row][c] == sudoku[row][col] and c != col:
                            initiallyValid = False
               
                    initialRow = (row // 3) * 3 #integer division to obtain either 0, 3 or 6
                    initialColumn = (col // 3) * 3 #integer division
                    for y in range((initialRow), ((initialRow) + 3), 1): #check square
                        for x in range((initialColumn), ((initialColumn) + 3), 1):
                            if row != y and col != x:
                                if sudoku[y][x] == 0:
                                    domains[y][x] = domains[y][x].replace(str(sudoku[row][col]), '')
                                if sudoku[y][x] == sudoku[row][col]:
                                    initiallyValid = False
                    domains[row][col] = ""
                if initiallyValid == False: #to avoid unnecessary looping
                    break
            if initiallyValid == False:
                break
        if initiallyValid == False:
            return False
        else:
            return True

    def forward_checking(sudoku, valueRow, valueColumn, num): #inference
        for row in range(9): #check columns
            if sudoku[row][valueColumn] == 0 and row != valueRow: #cross off values which violate constraints
                if num in initialDomains[row][valueColumn]:
                    domains[row][valueColumn] = domains[row][valueColumn].replace(num, '')
                    satisfiedConstraints.append((str(row) + str(valueColumn), num))
                if domains[row][valueColumn] == "": #if domain is empty, branch is invalid
                    return False
   
        for col in range(9): #check rows
            if sudoku[valueRow][col] == 0 and col != valueColumn:
                if num in initialDomains[valueRow][col]:
                    domains[valueRow][col] = domains[valueRow][col].replace(num, '')
                    satisfiedConstraints.append((str(valueRow) + str(col), num))
                if domains[valueRow][col] == "":
                    return False

        initialRow = (valueRow // 3) * 3 
        initialColumn = (valueColumn // 3) * 3 
        for y in range((initialRow), ((initialRow) + 3), 1): #check square
            for x in range((initialColumn), ((initialColumn) + 3), 1):
                if sudoku[y][x] == 0 and y != valueRow and x != valueColumn:
                    if num in initialDomains[y][x]:
                        domains[y][x] = domains[y][x].replace(num, '')
                        satisfiedConstraints.append((str(y) + str(x), num))
                    if domains[y][x] == "":
                        return False
   
        return True

    def solver(sudoku): #backtracking involving forward checking with heuristic (MRV)
        if not MRV(sudoku):
            return True
        else:
            row, col = MRV(sudoku)

        domainOrder = LCV(row, col)
           
        for number in domainOrder:
            if forward_checking(sudoku, row, col, number):
                sudoku[row][col] = int(number)
                if solver(sudoku):
                    return True
                else:
                    sudoku[row][col] = 0
            update_constraints(number)

        return False

    if initial_is_valid(solved_sudoku):
        initialDomains = domains
        if solver(solved_sudoku):
            return solved_sudoku
        else:
            solved_sudoku = invalidSudoku
            return solved_sudoku
    else:
        solved_sudoku = invalidSudoku
        return solved_sudoku

sudoku = [[4, 0, 0, 0, 0, 0, 8, 3, 0], #preset invalid sudoku
        [0, 0, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 0, 8, 2, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 0, 0, 7, 0, 0, 0, 0],
        [0, 0, 0, 2, 9, 0, 5, 0, 1],
        [5, 0, 1, 0, 0, 0, 9, 0, 4],
        [0, 0, 9, 3, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 5, 9, 0, 0, 3]]

def print_grid():
    solved_sudoku = sudoku_solver(sudoku)
    #initial_is_valid(arr)

    for i in range(9):
        for j in range(9):
            print (solved_sudoku[i][j])
        print ('NEXT LINE')

print_grid()