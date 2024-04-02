class TTEntry():
    def __init__(self, depth, value, type, age):
        self.depth = depth
        self.value = value
        self.type = type
        self.age = age

class ExpTTEntry(TTEntry):
    def __init__(self, depth, value, type, age, exp_weights):
        super().__init__(depth, value, type, age)
        self.exp_weights = exp_weights