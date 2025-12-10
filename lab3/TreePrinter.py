import AST

def addToClass(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

class TreePrinter:
    indent_str = "|  "

    @staticmethod
    def printIndented(string, indent):
        print(TreePrinter.indent_str * indent + string)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        TreePrinter.printIndented(str(self.value), indent)

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        TreePrinter.printIndented(str(self.value), indent)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        TreePrinter.printIndented(self.value, indent)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        TreePrinter.printIndented(self.name, indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        TreePrinter.printIndented(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.RelExpr)
    def printTree(self, indent=0):
        TreePrinter.printIndented(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Assign)
    def printTree(self, indent=0):
        TreePrinter.printIndented(self.op, indent)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.UnaryExpr)
    def printTree(self, indent=0):
        TreePrinter.printIndented(self.op, indent)
        self.expr.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        TreePrinter.printIndented("IF", indent)
        self.cond.printTree(indent + 1)
        TreePrinter.printIndented("THEN", indent)
        self.if_body.printTree(indent + 1)
        if self.else_body:
            TreePrinter.printIndented("ELSE", indent)
            self.else_body.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        TreePrinter.printIndented("WHILE", indent)
        self.cond.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        TreePrinter.printIndented("FOR", indent)
        self.id.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.body.printTree(indent + 1)

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        TreePrinter.printIndented("BREAK", indent)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        TreePrinter.printIndented("CONTINUE", indent)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        TreePrinter.printIndented("RETURN", indent)
        if self.expr:
            self.expr.printTree(indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        TreePrinter.printIndented("PRINT", indent)
        for arg in self.args:
            arg.printTree(indent + 1)

    @addToClass(AST.Compound)
    def printTree(self, indent=0):
        for stmt in self.statements:
            stmt.printTree(indent)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        TreePrinter.printIndented("VECTOR", indent)
        for elem in self.elements:
            elem.printTree(indent + 1)

    @addToClass(AST.Ref)
    def printTree(self, indent=0):
        TreePrinter.printIndented("REF", indent)
        TreePrinter.printIndented(self.name, indent + 1)
        for idx in self.indices:
            idx.printTree(indent + 1)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        TreePrinter.printIndented(self.name, indent)
        self.args.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        TreePrinter.printIndented("RANGE", indent)
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        TreePrinter.printIndented("TRANSPOSE", indent)
        self.expr.printTree(indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass

