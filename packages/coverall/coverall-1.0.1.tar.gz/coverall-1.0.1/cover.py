from bitarray import bitarray
#this is a note

def createMatrix(universe, sets, r_or_c):
    if r_or_c == 'c':
        set_columns = []
        
        for column in range(len(universe)):
            a = bitarray(len(sets))
            a.setall(0)
            set_columns.append(a)
            
        for set in sets:
            for item in set:
                set_columns[universe.index(item)][sets.index(set)] = 1
        
        active_columns = bitarray(len(universe))
        active_rows = bitarray(len(sets))
        active_columns.setall(1)
        active_rows.setall(1)
        
        return [set_columns, active_columns, active_rows]
    else:
        set_rows = []
        
        for row in range(len(sets)):
            a = bitarray(len(universe))
            a.setall(0)
            set_rows.append(a)
            
        for set in sets:
            for item in set:
                set_rows[sets.index(set)][universe.index(item)] = 1
        
        active_columns = bitarray(len(universe))
        active_rows = bitarray(len(sets))
        active_columns.setall(1)
        active_rows.setall(1)
        
        return [set_rows, active_columns, active_rows]
    

def exactCover(universe, sets):
    matrix_set = createMatrix(universe, sets, 'c')
    default_columns = matrix_set[1]
    default_rows = matrix_set[2]
    exactCover.matrix = matrix_set[0]
    
    
    def exactCoverHelper(columns, rows):
        partial_solution = []
        
        if not columns.count(1):
            return 'f'
        
        column_counts = []
        for column in range(len(exactCover.matrix)):
            if columns[column]:
                anded = exactCover.matrix[column]&rows
                column_counts.append(anded.count(1))
            else:
                column_counts.append(float('inf'))
                
        lowest_column = column_counts.index(min(column_counts))
        columns[lowest_column] = 0
        for row in range(len(rows)):
            if rows[row]:
                if exactCover.matrix[lowest_column][row]:
                    temp_rows = rows.copy()
                    temp_columns = columns.copy()
                    temp_rows[row] = 0
                    for item in range(len(columns)):
                        if exactCover.matrix[item][row]:
                            temp_rows = (temp_rows^exactCover.matrix[item])&temp_rows
                            temp_columns[item] = 0
                    rwi = exactCoverHelper(temp_columns, temp_rows)
                    if rwi:
                        partial_solution.append(row)
                        for answer in rwi:
                            partial_solution.append(answer)
                        return partial_solution
        return False
                    
                        
    
    answer = exactCoverHelper(default_columns, default_rows)
    cut_answer = []
    if not answer:
        print("there was no solution found for the given universe and set of sets")
    else:
        for set in range(len(answer)-1):
            cut_answer.append(sets[answer[set]])
    return cut_answer

def setCover(universe, sets, costs=[]):
    matrix_set = createMatrix(universe, sets, 'r')
    default_columns = matrix_set[1]
    default_rows = matrix_set[2]
    matrix = matrix_set[0]
    row_calc_cost = []
    answer = []
    
    I = bitarray(len(universe))
    for item in sets:
        row_calc_cost.append(float('inf'))
    if costs == []:
        for item in sets:
            costs.append(1)
    
    while I.count(1) < len(universe):
        for row in range(len(default_rows)):
            
            if default_rows[row]:
                matrix[row] = matrix[row] & default_columns
                current_row_count = matrix[row].count(1)
                if not current_row_count:
                    default_rows[row] = 0
                    row_calc_cost[row] = float('inf')
                else:
                    row_calc_cost[row] = costs[row]/current_row_count
            else:
                row_calc_cost[row] = float('inf')
        
        next_index = row_calc_cost.index(min(row_calc_cost))
        next_set = matrix[next_index]
        answer.append(sets[next_index])
        default_columns = (default_columns ^ next_set) & default_columns
        I = I | next_set
    
    return answer

def maxCover(universe, sets, max, costs = []):
    matrix_set = createMatrix(universe, sets, 'r')
    default_columns = matrix_set[1]
    default_rows = matrix_set[2]
    matrix = matrix_set[0]
    row_calc_cost = []
    answer = []
    total_cost = 0
    
    I = bitarray(len(universe))
    for item in sets:
        row_calc_cost.append(float('inf'))
    if costs == []:
        for item in sets:
            costs.append(1)
            
    current_cost_min = min(costs)
    
    while not ((I.count(1) == len(universe)) or ((total_cost+current_cost_min) > max)):
        costs_left = []
        for row in range(len(default_rows)):
            
            if default_rows[row]:
                matrix[row] = matrix[row] & default_columns
                current_row_count = matrix[row].count(1)
                if not current_row_count:
                    default_rows[row] = 0
                    row_calc_cost[row] = float('inf')
                else:
                    row_calc_cost[row] = costs[row]/current_row_count
                    costs_left.append(costs[row])
            else:
                row_calc_cost[row] = float('inf')
        
        next_index = row_calc_cost.index(min(row_calc_cost))
        total_cost += costs[next_index]
        next_set = matrix[next_index]
        answer.append(sets[next_index])
        default_columns = (default_columns ^ next_set) & default_columns
        I = I | next_set
    
    return answer