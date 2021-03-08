class Memory:
    def __init__(self): 
        self.clear()

    def clear(self): 
        self.actions = []
        
    def add_to_memory(self, new_action): 
        self.actions.append(new_action)