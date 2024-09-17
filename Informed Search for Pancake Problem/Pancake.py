import copy
import heapq
import time

class Node:
    def __init__(self, state, parent, backward_cost, order_added):
        self.state = state
        self.parent = parent
        self.backward_cost = backward_cost
        self.order_added = order_added
        self.depth = 0

    def __lt__(self, other):
        if self.total_cost() != other.total_cost():
            return self.total_cost() < other.total_cost()
        else:
            return self.order_added < other.order_added

    def heuristic(self):
        pancake_gap = 0
        for i in range(len(self.state) - 1):
            if abs(self.state[i] - self.state[i + 1]) != 1:
                pancake_gap += 1

        return pancake_gap

    def flip(self, depth):
        self.depth = depth

        for i in range(int(depth / 2)):
            temp = self.state[i]
            self.state[i] = self.state[depth-i-1]
            self.state[depth - i-1] = temp

        self.backward_cost += depth

        return self


    def total_cost(self):
        total_cost = self.heuristic() + self.backward_cost
        return total_cost


# A star method
class AStarMethod:

    def __init__(self, initial_state):
        self.heap = []
        heapq.heappush(self.heap, Node(initial_state, None, 0, 0))
        self.order_added = 1
        self.visited = []
        self.initial_state = initial_state
        self.length = len(initial_state)
        self.goal = None

    def priority(self):
        for i in range(len(self.heap)-1):
            if self.heap[i].total_cost() < self.heap[i+1].total_cost():
                temp = self.heap[i]
                self.heap[i] = self.heap[i+1]
                self.heap[i+1] = temp
        return True

    def expand(self):

        expand_node = self.heap.pop()
        for i in range(2, self.length +1):
            new_node = copy.deepcopy(expand_node)
            new_node.flip(i)
            new_node.parent = expand_node
            new_node.order_added = self.order_added
            if new_node.state not in self.visited:
                heapq.heappush(self.heap, new_node)
                self.visited.append(new_node.state)
            self.order_added += 1

        self.priority()
        return True


    def verify(self):
        if len(self.heap) == 0:
            self.goal = False
            return True
        for i in self.heap:
            if i.state == list(range(1, self.length + 1)):
                self.goal = i
                return i

        return False


    def run(self):
        solution = self.verify()
        while not solution:
            self.expand()
            solution = self.verify()
        return solution


    def solution(self, node):
        solution_steps = []
        curr_node = node
        while curr_node != None:
            solution_steps.append(curr_node)
            curr_node = curr_node.parent
            
        if len(solution_steps) == 1:
            print("Your stack of pancakes is already sorted!")
            exit()
            
        solution_steps.reverse()
            
        print("To sort the stack", solution_steps[0].state, "do the following:")
        for step in range(1, len(solution_steps)):
            print("Step", step, ": Flip the top", 
                solution_steps[step].depth,
                "pancakes to get", solution_steps[step].state)


#Uniform-Cost-Search method
class UCSMethod:

    def __init__(self, initial_state):
        self.heap = []
        heapq.heappush(self.heap, Node(initial_state, None, 0, 0))
        self.order_added = 1
        self.visited = []
        self.initial_state = initial_state
        self.length = len(initial_state)
        self.goal = None

    def priority(self):
        for i in range(len(self.heap) - 1):
            if self.heap[i].backward_cost < self.heap[i + 1].backward_cost:
                temp = self.heap[i]
                self.heap[i] = self.heap[i + 1]
                self.heap[i + 1] = temp
        return True

    def expand(self):

        expand_node = self.heap.pop()
        for i in range(2, self.length + 1):
            new_node = copy.deepcopy(expand_node)
            new_node.flip(i)
            new_node.parent = expand_node
            new_node.order_added = self.order_added
            if new_node.state not in self.visited:
                heapq.heappush(self.heap, new_node)
                self.visited.append(new_node.state)
            self.order_added += 1

        self.priority()
        return True

    def verify(self):
        if len(self.heap) == 0:
            self.goal = False
            return True
        for i in self.heap:
            if i.state == list(range(1, self.length + 1)):
                self.goal = i
                return i

        return False

    def run(self):
        solution = self.verify()
        while not solution:
            self.expand()
            solution = self.verify()
        return solution

    def solution(self, node):
        solution_steps = []
        curr_node = node
        while curr_node != None:
            solution_steps.append(curr_node)
            curr_node = curr_node.parent

        if len(solution_steps) == 1:
            print("Your stack of pancakes is already sorted!")
            exit()

        solution_steps.reverse()

        print("To sort the stack", solution_steps[0].state, "do the following:")
        for step in range(1, len(solution_steps)):
            print("Step", step, ": Flip the top",
                  solution_steps[step].depth,
                  "pancakes to get", solution_steps[step].state)


if __name__ == "__main__":
    method = "AStar"
    strState = "7,6,1,8,2,4,3,5,9,10"
    state = list(map(int, strState.split(',')))
    if method == "AStar":
        p1 = AStarMethod(state)
        print("-------------------------------------------------------")
        print("use AStar to solve problem state {}".format(str(state)))

    timer_start_A = time.time()
    p1.solution(p1.run())
    timer_end_A = time.time()

    print("A* search cost: ", timer_end_A - timer_start_A, "s")

    method = "Uniform-Cost-Search"
    strState = "7,6,1,8,2,4,3,5,9,10"
    state = list(map(int, strState.split(',')))
    if method == "Uniform-Cost-Search":
        p2 = UCSMethod(state)
        print("-------------------------------------------------------")
        print("use Uniform-Cost-Search to solve problem state {}".format(str(state)))

    timer_start_U = time.time()
    p2.solution(p2.run())
    timer_end_U = time.time()

    print("Uniform Cost search cost: ", timer_end_U - timer_start_U, "s")


    print("finish")
