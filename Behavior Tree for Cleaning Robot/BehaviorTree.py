import time
import random

DEBUG = False

INITIAL = 1
SUCCEEDED = 0
RUNNING = 2
FAILED = -1

class BaseNode:
    def __init__(self, name):
        self.name = name
        self.status = INITIAL
        self.blackboard = None

    def run(self):
        raise NotImplementedError()

class CompositeNode(BaseNode):
    def __init__(self, name):
        super().__init__(name)

    def run(self):
        raise NotImplementedError()

class SequenceNode(CompositeNode):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def append_child(self, child):
        self.children.append(child)
        child.blackboard = self.blackboard

    def run(self):
        if DEBUG: print("\033[93mDEBUG: SequenceNode.run:", self.name, "\033[0m")
        self.status = RUNNING
        for child in self.children:
            if DEBUG: print("\033[93mDEBUG: SequenceNode.run attempt child:", self.name, child.name, "\033[0m")
            result = child.run()
            if result == FAILED:
                self.status = result
                if DEBUG: print("\033[93mDEBUG: SequenceNode.run child failed:", self.name, child.name, "\033[0m")
                return self.status
        self.status = SUCCEEDED
        if DEBUG: print("\033[93mDEBUG: SequenceNode.run finish:", self.name, self.status, "\033[0m")
        return self.status

class SelectionNode(CompositeNode):
    def __init__(self, name):
        super().__init__(name)
        self.children = []

    def append_child(self, child):
        self.children.append(child)
        child.blackboard = self.blackboard

    def run(self):
        if DEBUG: print("\033[93mDEBUG: SelectionNode.run:", self.name, "\033[0m")
        self.status = RUNNING
        for child in self.children:
            if DEBUG: print("\033[93mDEBUG: SelectionNode.run attempt child:", self.name, child.name, "\033[0m")
            result = child.run()
            if result == SUCCEEDED:
                self.status = result
                if DEBUG: print("\033[93mDEBUG: SelectionNode.run child succeeded:", self.name, child.name, "\033[0m")
                return self.status
        self.status = FAILED
        if DEBUG: print("\033[93mDEBUG: SelectionNode.run finish:", self.name, self.status, "\033[0m")
        return self.status

class PriorityNode(CompositeNode):
    def __init__(self, name):
        super().__init__(name)
        self.children = {}

    def append_child(self, child, priority):
        self.children[child] = priority
        child.blackboard = self.blackboard

    def run(self):
        if DEBUG: print("\033[93mDEBUG: PriorityNode.run:", self.name, "\033[0m")
        self.status = RUNNING
        for child, _ in sorted(self.children.items(), key=lambda item: item[1]):
            if DEBUG: print("\033[93mDEBUG: PriorityNode.run attemp child:", self.name, child.name, "\033[0m")
            result = child.run()
            if result == SUCCEEDED:
                self.status = result
                return self.status
        self.status = FAILED
        return self.status

class DecoratorNode(BaseNode):
    def __init__(self, name):
        super().__init__(name)

class LogicalNegationNode(DecoratorNode):
    def __init__(self, name):
        super().__init__(name)
        self.child = None

    def set_child(self, child):
        self.child = child
        child.blackboard = self.blackboard

    def run(self):
        if DEBUG: print("\033[93mDEBUG: LogicalNegationNode.run:", self.name, "\033[0m")
        self.status = RUNNING
        result = self.child.run()
        if (result == FAILED):
            result = SUCCEEDED
        else:
            result = FAILED
        self.status = result
        if DEBUG: print("\033[93mDEBUG: LogicalNegationNode.run finish:", self.name, self.status, "\033[0m")
        return result

class UntilSuccessNode(DecoratorNode):
    def __init__(self, name, limit = 300):
        super().__init__(name)
        self.limit = limit
        self.child = None

    def set_child(self, child):
        self.child = child
        child.blackboard = self.blackboard

    def run(self):
        if DEBUG: print("\033[93mDEBUG: UntilSuccessNode.run:", self.name, "\033[0m")
        cycle = 0
        self.status = RUNNING
        
        while (True):
            result = self.child.run()
            if result == SUCCEEDED:
                self.status = SUCCEEDED
                return self.status
            cycle = cycle + 1
            if cycle >= self.limit:
                self.status = FAILED
                return self.status
            time.sleep(0.01)

class TimerNode(DecoratorNode):
    def __init__(self, name, tick):
        super().__init__(name)
        self.tick = tick
        self.child = None

    def set_child(self, child):
        self.child = child
        child.blackboard = self.blackboard

    def run(self):
        if DEBUG: print("\033[93mDEBUG: TimerNode.run:", self.name, "\033[0m")
        self.status = RUNNING
        self.child.run()
        print("Pretend", self.tick, "seconds passed...")
        self.status = SUCCEEDED
        return self.status

class TaskNode(BaseNode):
    def __init__(self, name, impl):
        super().__init__(name)
        self.impl = impl

    def run(self):
        if DEBUG: print("\033[93mDEBUG: TaskNode.run start:", self.name, "\033[0m")
        self.status = RUNNING
        result = self.impl()
        self.status = result
        if DEBUG: print("\033[93mDEBUG: TaskNode.run finish:", self.name, self.status, "\033[0m")
        return self.status

class ConditionNode(BaseNode):
    def __init__(self, name, condition):
        super().__init__(name)
        self.condition = condition

    def run(self):
        self.status = RUNNING
        if DEBUG: print("\033[93mDEBUG: ConditionNode.run start:", self.name, "\033[0m", "\033[0m")
        self.status = self.condition(self)
        if DEBUG: print("\033[93mDEBUG: ConditionNode.run finish:", self.name, self.status, "\033[0m")
        return self.status

class Roomba:
    def __init__(self, blackboard):
        self.blackboard = blackboard

    def find_home(self):
        home = "earth"
        self.blackboard["blackboard"] = home
        print("Low battery!")
        print("Home found at:", home)
        return SUCCEEDED

    def go_home(self):
        print("Going home at:", self.blackboard["blackboard"])
        return SUCCEEDED

    def dock(self):
        print("Docked! Now charging!")
        self.blackboard["BATTERY_LEVEL"] = 100
        return SUCCEEDED

    def clean_spot(self):
        print("Now clean spot!")
        self.blackboard["BATTERY_LEVEL"] = self.blackboard["BATTERY_LEVEL"] - 5
        time.sleep(1)
        return SUCCEEDED

    def general_clean(self):
        print("Do general cleaning!")
        self.blackboard["BATTERY_LEVEL"] = self.blackboard["BATTERY_LEVEL"] - 5
        return SUCCEEDED

    def done_spot(self):
        print("Spot Cleaning done!")
        self.blackboard["SPOT_CLEANING"] = False
        return SUCCEEDED

    def done_general(self):
        print("General Cleaning done!")
        self.blackboard["GENERAL_CLEANING"] = False
        return SUCCEEDED

    def clean_floor(self):
        print("Now clean floor!")
        self.blackboard["BATTERY_LEVEL"] = self.blackboard["BATTERY_LEVEL"] - 5
        time.sleep(1)
        rnd = random.randint(1, 10)
        if DEBUG: print("\033[93mDEBUG: clean_floor random value:", rnd, "\033[0m")
        if rnd >= 1 and rnd <= 3:
            print("Clean floor failed!")
            return FAILED
        else:
            print("Clean floor succeeded!")
            return SUCCEEDED

    def do_nothing(self):
        print("Nothing we can do!")
        return SUCCEEDED

    def run(self):
        root = PriorityNode("root")
        root.blackboard = self.blackboard

        sequence_1 = SequenceNode("sequence_1")
        selection_2 = SelectionNode("selection_2")
        task_3 = TaskNode("task_3", self.do_nothing)
        root.append_child(sequence_1, 1)
        root.append_child(selection_2, 2)
        root.append_child(task_3, 3)

        #P1: battery check
        condition_1_1 = ConditionNode("condition_1_1", lambda x: SUCCEEDED if x.blackboard['BATTERY_LEVEL'] < 30 else FAILED)
        task_1_2 = TaskNode("task_1_2", self.find_home)
        task_1_3 = TaskNode("task_1_3", self.go_home)
        task_1_4 = TaskNode("task_1_4", self.dock)
        for item in [condition_1_1, task_1_2, task_1_3, task_1_4]: sequence_1.append_child(item)
        
        sequence_2_1 = SequenceNode("sequence_2_1")
        sequence_2_2 = SequenceNode("sequence_2_2")
        for item in [sequence_2_1, sequence_2_2]: selection_2.append_child(item)

        #P2-1 spot
        condition_2_1_1 = ConditionNode("condition_2_1_1", lambda x: SUCCEEDED if x.blackboard['SPOT_CLEANING'] == True else FAILED)
        timer_2_1_2 = TimerNode("timer_2_1_2", 20)
        task_2_1_3 = TaskNode("task_2_1_3", self.done_spot)
        for item in [condition_2_1_1, timer_2_1_2, task_2_1_3]: sequence_2_1.append_child(item)
        task_2_1_2_1 = TaskNode("task_2_1_2_1", self.clean_spot)
        timer_2_1_2.set_child(task_2_1_2_1)

        #p2-2 general cleaning
        condition_2_2_1 = ConditionNode("condition_2_2_1",lambda x: SUCCEEDED if x.blackboard['GENERAL_CLEANING'] == True else FAILED)
        sequence_2_2_2 = SequenceNode("sequence_2_2_2")
        for item in [condition_2_2_1, sequence_2_2_2]: sequence_2_2.append_child(item)

        priority_2_2_2_1 = PriorityNode("priority_2_2_2_1")
        task_2_2_2_2 = TaskNode("task_2_2_2_2", self.done_general)
        for item in [priority_2_2_2_1, task_2_2_2_2]: sequence_2_2_2.append_child(item)

        sequence_2_2_2_1_1 = SequenceNode("sequence_2_2_2_1_1")
        untilSuccess_2_2_2_1_2 = UntilSuccessNode("untilSuccess_2_2_2_1_2")
        priority_2_2_2_1.append_child(sequence_2_2_2_1_1, 1)
        priority_2_2_2_1.append_child(untilSuccess_2_2_2_1_2, 2)


        condition_2_2_2_1_1_1 = ConditionNode("condition_2_2_2_1_1_1", lambda x: SUCCEEDED if (x.blackboard['BATTERY_LEVEL'] > 30 and x.blackboard['DUSTY_SPOT'] == True) else FAILED)
        timer_2_2_2_1_1_2 = TimerNode("timer_2_2_2_1_1_1", 35)
        for item in [condition_2_2_2_1_1_1, timer_2_2_2_1_1_2]: sequence_2_2_2_1_1.append_child(item)
        task_2_2_2_1_1_2_1 = TaskNode("task_2_2_2_1_1_2", self.clean_spot)
        timer_2_2_2_1_1_2.set_child(task_2_2_2_1_1_2_1)

        task_2_2_2_1_2_1 = TaskNode("task_2_2_2_1_2_1", self.clean_floor)
        untilSuccess_2_2_2_1_2.set_child(task_2_2_2_1_2_1)

        root.run()
        print("root.run", root.run())

def demo(blackboard):
    blackboard_before = blackboard.copy()
    roomba = Roomba(blackboard)
    roomba.run()
    print(blackboard_before)
    print(blackboard)

print("--------case 1, battery low, go home--------")
blackboard = {
     "HOME_PATH": "",
     "BATTERY_LEVEL": 20,
     "SPOT_CLEANING": False,
     "GENERAL_CLEANING": False,
     "DUSTY_SPOT": False
}
demo(blackboard)

print("--------case 2, battery ok, spot detected, no general cleaning work--------")
blackboard = {
    "HOME_PATH": "",
    "BATTERY_LEVEL": 10,
    "SPOT_CLEANING": True,
    "GENERAL_CLEANING": False,
    "DUSTY_SPOT": False
 }
demo(blackboard)

print("--------case 3, battery ok, spot not found, go general cleaning and dusty spot found--------")
blackboard = {
     "HOME_PATH": "",
     "BATTERY_LEVEL": 60,
     "SPOT_CLEANING": False,
     "GENERAL_CLEANING": True,
     "DUSTY_SPOT": True
}
demo(blackboard)

print("--------case 4, battery ok, spot not found, go general, but no dusty--------")
blackboard = {
    "HOME_PATH": "",
    "BATTERY_LEVEL": 100,
    "SPOT_CLEANING": False,
    "GENERAL_CLEANING": True,
    "DUSTY_SPOT": False,
}
demo(blackboard)

print("--------case 5, battery ok, spot not found, general not needed, then do nothing--------")
blackboard = {
     "HOME_PATH": "",
     "BATTERY_LEVEL": 50,
     "SPOT_CLEANING": False,
     "GENERAL_CLEANING": False,
     "DUSTY_SPOT": False
}
demo(blackboard)

print("--------case 6, low battery, but spot found--------")
blackboard = {
     "HOME_PATH": "",
     "BATTERY_LEVEL": 20,
     "SPOT_CLEANING": True,
     "GENERAL_CLEANING": False,
     "DUSTY_SPOT": False
}
demo(blackboard)

