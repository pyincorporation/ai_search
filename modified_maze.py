import sys, termcolor

class Node():

    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

class StackFronier():
    
    def __init__(self):
        self.frontier = []

    def add_node(self, node):
        self.frontier.append(node)

    def empty_frontier(self):
        return len(self.frontier) == 0
    
    def remove_node(self):
        if self.empty_frontier():
            sys.exit(termcolor.cprint('(^_^): No solution to the maze!'))
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
        
    def contain_state(self, state):
        return any(node.state == state for node in self.frontier)

class QueuFrontier(StackFronier):
    def remove_node(self):
        if self.empty_frontier():
            sys.exit(termcolor.cprint('(^_^): No solution to the maze!'))
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():

    def __init__(self, filename):
        self.filename = filename

        try:
            with open(self.filename) as file:
                file = file.read()
                
                if file.count('A') != 1:
                    sys.exit(termcolor.cprint('(^_^): Maze should have one starting point', 'red'))
                if file.count('B') != 1:
                    sys.exit(termcolor.cprint('(^_^): Maze should have one goal', 'red'))

                self.file_rows = file.splitlines()
                self.file_height = len(self.file_rows)
                self.file_width = max(len(row) for row in self.file_rows)

                self.walls = []                

                for i in range(self.file_height):
                    row = []
                    for j in range(self.file_width):
                        try:
                            if self.file_rows[i][j] == 'A':
                                row.append(False)
                                self.start = (i, j)
                            elif self.file_rows[i][j] == 'B':
                                row.append(False)
                                self.goal = (i, j)
                            elif self.file_rows[i][j] == ' ':
                                row.append(False)
                            else:
                                row.append(True)
                        except IndexError:
                            row.append(True)
                    self.walls.append(row)
                self.solution = None
                
        except FileNotFoundError:
            sys.exit(termcolor.cprint(f'(^_^): File "{self.filename}" is not found in this location!', 'red'))

    def print_maze(self):
        solution = self.solution[1] if self.solution is not None else None
        for i, rows in enumerate(self.walls):
            print()
            for j, cols in enumerate(rows):
                if cols:
                    print('█', end='')
                elif (i, j) == self.start:
                    print('A', end='')
                elif (i, j) == self.goal:
                    print('B', end='')
                elif solution is not None and (i, j) in solution:
                    print('*', end='')
                else:
                    print(' ', end='')
        print()
        print()

    def node_neighbour(self, state):
        row, col = state
        node_candidate = [
            ('up', (row-1, col)),
            ('down', (row+1, col)),
            ('right', (row, col+1)),
            ('left', (row, col-1)),
        ]
        result = []
        # random.shuffle(node_candidate)
        for action, (r, c) in node_candidate:
            if self.file_height > r >= 0 and self.file_width > c >= 0 and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result
    
    def solve_maze(self, frontier_choice):
        self.num_explored_node = 0
        self.explore_node = set()
        start_node = Node(state = self.start, parent = None, action = None)
        print('-'*22)
        if frontier_choice == 1:
            frontier = StackFronier()
            termcolor.cprint('StackFrontier approach', 'blue')
        else:
            frontier = QueuFrontier()
            termcolor.cprint('QueuFrontier approach', 'green')
        print('-'*22)
        frontier.add_node(start_node)
        while True:
            if frontier.empty_frontier():
                sys.exit(termcolor.cprint('(^_^): No solution to the maze!'))
            node_explored = frontier.remove_node()
            if node_explored.state == self.goal:
                print('goal found: ', True)
                actions = []
                cells = []
                while node_explored.parent is not None:
                    actions.append(node_explored.action)
                    cells.append(node_explored.state)
                    node_explored = node_explored.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            self.num_explored_node += 1
            self.explore_node.add(node_explored.state)
            for action, state in self.node_neighbour(node_explored.state):
                if not frontier.contain_state(state) and state not in self.explore_node:
                    child_node = Node(state = state, parent = node_explored, action = action)
                    frontier.add_node(child_node)
            
                
if len(sys.argv) != 2:
    sys.exit(termcolor.cprint('(^_^): Usage: python maze.py <file.txt>', 'red'))
def frontier_choice(prompt, retries = 3, reminder = '(^_^): Please try again!'):
    maze = Maze(sys.argv[1])
    Frontier_options = [1,2]
    
    while True:
        retries -= 1
        try:
            frontier_choice = int(input(prompt))
            if frontier_choice in Frontier_options:
                print('Maze solving:')
                maze.print_maze()
                print('Solving...')
                maze.solve_maze(frontier_choice)
                maze.print_maze()
                print('Nodes explored: ', maze.num_explored_node)
                
                return
            else:
                if retries:
                    termcolor.cprint('(-_-): Enter among the two options [ 1 or 2 ]!', 'red')
        except ValueError:
            if retries:
                termcolor.cprint('(-_-): Opps... Enter a valid value please!', 'red')
        if not retries:
            sys.exit(termcolor.cprint(reminder, 'red'))
        
        
        
        
        
frontier_choice("""Enter an option number>[ StackFrontier(1) |  QueuFrontier(2) ]:""")

