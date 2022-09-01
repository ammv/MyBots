from random import shuffle

class ComputeStep:
    steps = [1,3,4]
    
    @staticmethod
    def easy_step(stones: int) -> int:
        shuffle(ComputeStep.steps)
        for i in ComputeStep.steps:
            if(stones - i == 0):
                return i
        return -1
        
    @staticmethod
    def medium_step(stones: int) -> int:
        shuffle(ComputeStep.steps)
        for i in ComputeStep.steps:
            if(stones - i == 2):
                return i
        return -1
        
    @staticmethod
    def hard_step(stones: int) -> int:
        if(stones == 2): return 1
        shuffle(ComputeStep.steps)
        for i in ComputeStep.steps:
            step = stones - i
            if(ComputeStep.easy_step(step) + ComputeStep.medium_step(step) == -2):
                return i
        return 1
        
    @staticmethod
    def compute(stones: int) -> int:
        step = ComputeStep.easy_step(stones)
        if(step == -1): step = ComputeStep.medium_step(stones)
        if(step == -1): step = ComputeStep.hard_step(stones)
        return step