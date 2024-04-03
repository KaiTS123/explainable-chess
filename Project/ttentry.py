class TTEntry():
    def __init__(self, depth, value, type, age):
        self.depth = depth
        self.value = value
        self.type = type
        self.age = age

class TTEntryReason(TTEntry):
    def __init__(self, depth, value, type, age, reason):
        super().__init__(depth, value, type, age)
        self.reason = reason