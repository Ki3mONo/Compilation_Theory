class Node(object):
    def __init__(self):
        self.lineno = None


class IntNum(Node):
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno

class FloatNum(Node):
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno

class String(Node):
    def __init__(self, value, lineno=None):
        self.value = value
        self.lineno = lineno

class Variable(Node):
    def __init__(self, name, lineno=None):
        self.name = name
        self.lineno = lineno

class BinExpr(Node):
    def __init__(self, op, left, right, lineno=None):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

class RelExpr(Node):
    def __init__(self, op, left, right, lineno=None):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

class Assign(Node):
    def __init__(self, op, left, right, lineno=None):
        self.op = op
        self.left = left
        self.right = right
        self.lineno = lineno

class UnaryExpr(Node):
    def __init__(self, op, expr, lineno=None):
        self.op = op
        self.expr = expr
        self.lineno = lineno

class If(Node):
    def __init__(self, cond, if_body, else_body=None, lineno=None):
        self.cond = cond
        self.if_body = if_body
        self.else_body = else_body
        self.lineno = lineno

class While(Node):
    def __init__(self, cond, body, lineno=None):
        self.cond = cond
        self.body = body
        self.lineno = lineno

class For(Node):
    def __init__(self, id, range, body, lineno=None):
        self.id = id
        self.range = range
        self.body = body
        self.lineno = lineno

class Break(Node):
    def __init__(self, lineno=None):
        self.lineno = lineno

class Continue(Node):
    def __init__(self, lineno=None):
        self.lineno = lineno

class Return(Node):
    def __init__(self, expr=None, lineno=None):
        self.expr = expr
        self.lineno = lineno

class Print(Node):
    def __init__(self, args, lineno=None):
        self.args = args
        self.lineno = lineno

class Compound(Node):
    def __init__(self, statements, lineno=None):
        self.statements = statements
        self.lineno = lineno

class Vector(Node):
    def __init__(self, elements, lineno=None):
        self.elements = elements
        self.lineno = lineno

class Ref(Node):
    def __init__(self, name, indices, lineno=None):
        self.name = name
        self.indices = indices
        self.lineno = lineno

class Function(Node):
    def __init__(self, name, args, lineno=None):
        self.name = name
        self.args = args
        self.lineno = lineno

class Range(Node):
    def __init__(self, start, end, lineno=None):
        self.start = start
        self.end = end
        self.lineno = lineno

class Transpose(Node):
    def __init__(self, expr, lineno=None):
        self.expr = expr
        self.lineno = lineno

class Error(Node):
    def __init__(self, lineno=None):
        self.lineno = lineno
      
