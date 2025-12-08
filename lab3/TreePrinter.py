import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print("|  " * indent + str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("|  " * indent + self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        print("|  " * indent + self.op)
        self.expr.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print("|  " * indent + "IF")
        self.cond.printTree(indent + 1)
        print("|  " * indent + "THEN")
        self.if_body.printTree(indent + 1)
        if self.else_body:
            print("|  " * indent + "ELSE")
            self.else_body.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("|  " * indent + "WHILE")
        self.cond.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("|  " * indent + "FOR")
        self.id.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("|  " * indent + "BREAK")

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("|  " * indent + "CONTINUE")

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("|  " * indent + "RETURN")
        if self.expr:
            self.expr.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print("|  " * indent + "PRINT")
        for arg in self.args:
            arg.printTree(indent + 1)

    @addToClass(AST.Compound)
    def printTree(self, indent=0):
        for stmt in self.statements:
            stmt.printTree(indent)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("|  " * indent + "VECTOR")
        for elem in self.elements:
            elem.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        print("|  " * indent + "REF")
        print("|  " * (indent + 1) + self.name)
        for idx in self.indices:
            idx.printTree(indent + 1)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print("|  " * indent + self.name)
        self.args.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("|  " * indent + "RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print("|  " * indent + "TRANSPOSE")
        self.expr.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass

