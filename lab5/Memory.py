


class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.memory = {}

    def has_key(self, name):  # variable name
        return name in self.memory

    def get(self, name):         # gets from memory current value of variable <name>
        return self.memory.get(name)

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.memory[name] = value


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.stack = []
        if memory:
            self.stack.append(memory)
        else:
            self.stack.append(Memory("global"))

    def get(self, name):             # gets from memory stack current value of variable <name>
        for mem in reversed(self.stack):
            if mem.has_key(name):
                return mem.get(name)
        return None

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        for mem in reversed(self.stack):
            if mem.has_key(name):
                mem.put(name, value)
                return
        self.stack[-1].put(name, value)

    def push(self, memory): # pushes memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        if self.stack:
            self.stack.pop()



