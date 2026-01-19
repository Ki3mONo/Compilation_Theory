
import AST
from Memory import *
from Exceptions import *
from visit import *
import sys
import operator
import numpy as np

sys.setrecursionlimit(10000)


class Interpreter(object):

    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return node.value

    @when(AST.FloatNum)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Variable)
    def visit(self, node):
        return self.memory_stack.get(node.name)

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '.+': np.add,
            '.-': np.subtract,
            '.*': np.multiply,
            './': np.divide,
        }
        
        return ops[node.op](r1, r2)

    @when(AST.RelExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        
        ops = {
            '==': operator.eq,
            '!=': operator.ne,
            '<': operator.lt,
            '>': operator.gt,
            '<=': operator.le,
            '>=': operator.ge,
        }
        
        return ops[node.op](r1, r2)

    @when(AST.UnaryExpr)
    def visit(self, node):
        expr_val = node.expr.accept(self)
        if node.op == '-':
            return -expr_val
        return expr_val

    @when(AST.Assign)
    def visit(self, node):
        value = node.right.accept(self)
        
        if isinstance(node.left, AST.Variable):
            # Simple variable assignment
            if node.op == '=':
                self.memory_stack.set(node.left.name, value)
            elif node.op == '+=':
                old_val = self.memory_stack.get(node.left.name)
                self.memory_stack.set(node.left.name, old_val + value)
            elif node.op == '-=':
                old_val = self.memory_stack.get(node.left.name)
                self.memory_stack.set(node.left.name, old_val - value)
            elif node.op == '*=':
                old_val = self.memory_stack.get(node.left.name)
                self.memory_stack.set(node.left.name, old_val * value)
            elif node.op == '/=':
                old_val = self.memory_stack.get(node.left.name)
                self.memory_stack.set(node.left.name, old_val / value)
        elif isinstance(node.left, AST.Ref):
            # Matrix/vector element assignment
            var = self.memory_stack.get(node.left.name)
            indices = [idx.accept(self) for idx in node.left.indices]
            
            if node.op == '=':
                if len(indices) == 1:
                    var[indices[0]] = value
                elif len(indices) == 2:
                    var[indices[0], indices[1]] = value
            elif node.op == '+=':
                if len(indices) == 1:
                    var[indices[0]] += value
                elif len(indices) == 2:
                    var[indices[0], indices[1]] += value
            elif node.op == '-=':
                if len(indices) == 1:
                    var[indices[0]] -= value
                elif len(indices) == 2:
                    var[indices[0], indices[1]] -= value
            elif node.op == '*=':
                if len(indices) == 1:
                    var[indices[0]] *= value
                elif len(indices) == 2:
                    var[indices[0], indices[1]] *= value
            elif node.op == '/=':
                if len(indices) == 1:
                    var[indices[0]] /= value
                elif len(indices) == 2:
                    var[indices[0], indices[1]] /= value

    @when(AST.If)
    def visit(self, node):
        cond = node.cond.accept(self)
        if cond:
            return node.if_body.accept(self)
        elif node.else_body:
            return node.else_body.accept(self)

    @when(AST.While)
    def visit(self, node):
        r = None
        try:
            while node.cond.accept(self):
                try:
                    r = node.body.accept(self)
                except ContinueException:
                    continue
        except BreakException:
            pass
        return r

    @when(AST.For)
    def visit(self, node):
        r = None
        range_obj = node.range.accept(self)
        start, end = range_obj
        
        try:
            for i in range(start, end + 1):
                self.memory_stack.set(node.id, i)
                try:
                    r = node.body.accept(self)
                except ContinueException:
                    continue
        except BreakException:
            pass
        return r

    @when(AST.Range)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return (start, end)

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Return)
    def visit(self, node):
        if node.expr:
            value = node.expr.accept(self)
            raise ReturnValueException(value)
        else:
            raise ReturnValueException(None)

    @when(AST.Print)
    def visit(self, node):
        values = []
        for arg in node.args:
            val = arg.accept(self)
            values.append(val)
        print(*values)

    @when(AST.Compound)
    def visit(self, node):
        r = None
        for stmt in node.statements:
            r = stmt.accept(self)
        return r

    @when(AST.Vector)
    def visit(self, node):
        elements = []
        for elem in node.elements:
            val = elem.accept(self)
            elements.append(val)
        return np.array(elements)

    @when(AST.Ref)
    def visit(self, node):
        var = self.memory_stack.get(node.name)
        indices = [idx.accept(self) for idx in node.indices]
        
        if len(indices) == 1:
            return var[indices[0]]
        elif len(indices) == 2:
            return var[indices[0], indices[1]]

    @when(AST.Function)
    def visit(self, node):
        if node.name == 'eye':
            size = node.args[0].accept(self)
            return np.eye(size)
        elif node.name == 'zeros':
            if len(node.args) == 1:
                size = node.args[0].accept(self)
                return np.zeros(size)
            elif len(node.args) == 2:
                rows = node.args[0].accept(self)
                cols = node.args[1].accept(self)
                return np.zeros((rows, cols))
        elif node.name == 'ones':
            if len(node.args) == 1:
                size = node.args[0].accept(self)
                return np.ones(size)
            elif len(node.args) == 2:
                rows = node.args[0].accept(self)
                cols = node.args[1].accept(self)
                return np.ones((rows, cols))

    @when(AST.Transpose)
    def visit(self, node):
        expr_val = node.expr.accept(self)
        return expr_val.T

    @when(AST.Error)
    def visit(self, node):
        pass

