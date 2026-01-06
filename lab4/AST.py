class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value

class FloatNum(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class RelExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Assign(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class UnaryExpr(Node):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class If(Node):
    def __init__(self, cond, if_body, else_body=None):
        self.cond = cond
        self.if_body = if_body
        self.else_body = else_body

class While(Node):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

class For(Node):
    def __init__(self, id, range, body):
        self.id = id
        self.range = range
        self.body = body

class Break(Node):
    pass

class Continue(Node):
    pass

class Return(Node):
    def __init__(self, expr=None):
        self.expr = expr

class Print(Node):
    def __init__(self, args):
        self.args = args

class Compound(Node):
    def __init__(self, statements):
        self.statements = statements

class Vector(Node):
    def __init__(self, elements):
        self.elements = elements

class Ref(Node):
    def __init__(self, name, indices):
        self.name = name
        self.indices = indices

class Function(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Transpose(Node):
    def __init__(self, expr):
        self.expr = expr

class Error(Node):
    def __init__(self):
        pass
      
