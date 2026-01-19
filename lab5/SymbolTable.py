class Symbol(object):
    def __init__(self, name, type):
        self.name = name
        self.type = type

class VariableSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

class SymbolTable(object):

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.symbols = {}

    def put(self, name, symbol):
        self.symbols[name] = symbol

    def get(self, name):
        s = self.symbols.get(name)
        if s is not None:
            return s
        if self.parent:
            return self.parent.get(name)
        return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent

