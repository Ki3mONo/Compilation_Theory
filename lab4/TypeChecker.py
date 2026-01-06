import AST
from SymbolTable import SymbolTable, VariableSymbol


class NodeVisitor(object):

    def visit(self, node):
        if node is None:
            return None
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)


class TypeChecker(NodeVisitor):

    def __init__(self):
        self.table = SymbolTable(None, "global")
        self.loop_nesting = 0

    def error(self, message, lineno):
        print(f"Line {lineno}: {message}")

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        symbol = self.table.get(node.name)
        if symbol:
            return symbol.type
        else:
            self.error(f"Undefined variable '{node.name}'", node.lineno)
            return None

    def visit_BinExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        op = node.op

        if type1 is None or type2 is None:
            return None

        def get_dims(t):
            if isinstance(t, tuple):
                if t[0] == 'vector':
                    return (t[1],)
                elif t[0] == 'matrix':
                    return (t[1], t[2])
            return None

        def get_elem_type(t):
            if isinstance(t, tuple):
                return t[-1]
            return t

        dims1 = get_dims(type1)
        dims2 = get_dims(type2)

        is_matrix1 = isinstance(type1, tuple)
        is_matrix2 = isinstance(type2, tuple)

        if op in ['.+', '.-', '.*', './']:
            if not is_matrix1 or not is_matrix2:
                self.error(f"Element-wise operation '{op}' requires matrix/vector operands", node.lineno)
                return None
            if dims1 != dims2:
                self.error(f"Incompatible dimensions {dims1} and {dims2} for operation '{op}'", node.lineno)
                return None
            elem_type = 'float' if get_elem_type(type1) == 'float' or get_elem_type(type2) == 'float' else 'int'
            if type1[0] == 'matrix':
                return ('matrix', type1[1], type1[2], elem_type)
            else:
                return ('vector', type1[1], elem_type)

        if op in ['+', '-']:
            if is_matrix1 != is_matrix2:
                self.error(f"Cannot perform '{op}' on scalar and matrix/vector", node.lineno)
                return None
            if is_matrix1 and is_matrix2:
                if dims1 != dims2:
                    self.error(f"Incompatible dimensions {dims1} and {dims2} for operation '{op}'", node.lineno)
                    return None
                elem_type = 'float' if get_elem_type(type1) == 'float' or get_elem_type(type2) == 'float' else 'int'
                if type1[0] == 'matrix':
                    return ('matrix', type1[1], type1[2], elem_type)
                else:
                    return ('vector', type1[1], elem_type)
            if type1 == 'float' or type2 == 'float':
                return 'float'
            return 'int'

        if op == '*':
            if is_matrix1 and is_matrix2:
                if len(dims1) == 2 and len(dims2) == 2:
                    if dims1[1] != dims2[0]:
                        self.error(f"Incompatible dimensions {dims1} and {dims2} for matrix multiplication", node.lineno)
                        return None
                    elem_type = 'float' if get_elem_type(type1) == 'float' or get_elem_type(type2) == 'float' else 'int'
                    return ('matrix', dims1[0], dims2[1], elem_type)
                elif len(dims1) == 1 and len(dims2) == 1:
                    if dims1[0] != dims2[0]:
                        self.error(f"Incompatible vector dimensions for operation '*'", node.lineno)
                        return None
                    return 'float'
                else:
                    self.error(f"Incompatible dimensions for multiplication", node.lineno)
                    return None
            elif is_matrix1 != is_matrix2:
                elem_type = 'float' if get_elem_type(type1) == 'float' or get_elem_type(type2) == 'float' else 'int'
                matrix_type = type1 if is_matrix1 else type2
                if matrix_type[0] == 'matrix':
                    return ('matrix', matrix_type[1], matrix_type[2], elem_type)
                else:
                    return ('vector', matrix_type[1], elem_type)
            if type1 == 'float' or type2 == 'float':
                return 'float'
            return 'int'

        if op == '/':
            if is_matrix1 and is_matrix2:
                self.error(f"Cannot divide matrix by matrix", node.lineno)
                return None
            elif is_matrix1:
                if type1[0] == 'matrix':
                    return ('matrix', type1[1], type1[2], 'float')
                else:
                    return ('vector', type1[1], 'float')
            elif is_matrix2:
                self.error(f"Cannot divide scalar by matrix", node.lineno)
                return None
            return 'float'

        return None

    def visit_RelExpr(self, node):
        self.visit(node.left)
        self.visit(node.right)
        return 'int'

    def visit_Assign(self, node):
        type_right = self.visit(node.right)
        
        if isinstance(node.left, AST.Variable):
            if node.op != '=':
                symbol = self.table.get(node.left.name)
                if not symbol:
                    self.error(f"Undefined variable '{node.left.name}'", node.lineno)
                    return None
            self.table.put(node.left.name, VariableSymbol(node.left.name, type_right))
        elif isinstance(node.left, AST.Ref):
            symbol = self.table.get(node.left.name)
            if not symbol:
                self.error(f"Undefined variable '{node.left.name}'", node.lineno)
            else:
                self.visit_Ref(node.left)
        
        return type_right

    def visit_UnaryExpr(self, node):
        return self.visit(node.expr)

    def visit_Transpose(self, node):
        expr_type = self.visit(node.expr)
        if expr_type is None:
            return None
        if not isinstance(expr_type, tuple):
            self.error(f"Transpose requires matrix/vector operand", node.lineno)
            return None
        if expr_type[0] == 'matrix':
            return ('matrix', expr_type[2], expr_type[1], expr_type[3])
        return expr_type

    def visit_Vector(self, node):
        if not node.elements:
            return ('vector', 0, 'unknown')
        
        first_type = self.visit(node.elements[0])
        if first_type is None:
            return None
        
        if isinstance(first_type, tuple) and first_type[0] == 'vector':
            first_size = first_type[1]
            for i, elem in enumerate(node.elements[1:], 2):
                elem_type = self.visit(elem)
                if elem_type is None:
                    continue
                if not isinstance(elem_type, tuple) or elem_type[0] != 'vector':
                    self.error(f"Inconsistent types in matrix initialization", node.lineno)
                    return None
                if elem_type[1] != first_size:
                    self.error(f"Row {i} has {elem_type[1]} elements, expected {first_size}", node.lineno)
                    return None
            return ('matrix', len(node.elements), first_size, first_type[2])
        else:
            for elem in node.elements[1:]:
                elem_type = self.visit(elem)
                if elem_type != first_type and not (first_type in ['int', 'float'] and elem_type in ['int', 'float']):
                    self.error(f"Inconsistent types in vector initialization", node.lineno)
            return ('vector', len(node.elements), first_type)

    def visit_Ref(self, node):
        symbol = self.table.get(node.name)
        if not symbol:
            self.error(f"Undefined variable '{node.name}'", node.lineno)
            return None
        
        type_sym = symbol.type
        if not isinstance(type_sym, tuple):
            self.error(f"Variable '{node.name}' is not indexable", node.lineno)
            return None

        dims = []
        if type_sym[0] == 'vector':
            dims = [type_sym[1]]
        elif type_sym[0] == 'matrix':
            dims = [type_sym[1], type_sym[2]]

        if len(node.indices) != len(dims):
            self.error(f"Wrong number of indices for '{node.name}': got {len(node.indices)}, expected {len(dims)}", node.lineno)
            return None

        for i, index in enumerate(node.indices):
            if isinstance(index, AST.IntNum):
                val = index.value
                if val < 0 or val >= dims[i]:
                    self.error(f"Index {val} out of bounds for '{node.name}' (dimension size is {dims[i]})", node.lineno)
            else:
                t = self.visit(index)
                if t is not None and t != 'int':
                    self.error(f"Index must be an integer", node.lineno)

        return type_sym[-1]

    def visit_Function(self, node):
        if node.name in ['zeros', 'ones', 'eye']:
            args = node.args
            
            if len(args) == 0:
                self.error(f"Function '{node.name}' requires at least 1 argument", node.lineno)
                return None
            
            if len(args) > 2:
                self.error(f"Function '{node.name}' accepts at most 2 arguments", node.lineno)
                return None
            
            val1, val2 = None, None

            for i, arg in enumerate(args):
                t = self.visit(arg)
                if t != 'int':
                    self.error(f"Argument {i+1} of '{node.name}' must be an integer", node.lineno)
                if isinstance(arg, AST.IntNum):
                    if arg.value <= 0:
                        self.error(f"Argument {i+1} of '{node.name}' must be positive", node.lineno)
                    if i == 0:
                        val1 = arg.value
                    else:
                        val2 = arg.value

            if node.name == 'eye' and len(args) == 2 and val1 is not None and val2 is not None and val1 != val2:
                self.error(f"Function 'eye' requires square dimensions, got {val1}x{val2}", node.lineno)
            
            if val1 is not None:
                if len(args) == 1:
                    return ('matrix', val1, val1, 'int')
                elif val2 is not None:
                    return ('matrix', val1, val2, 'int')
            
            return ('matrix', 0, 0, 'int')

        self.error(f"Unknown function '{node.name}'", node.lineno)
        return None

    def visit_If(self, node):
        self.visit(node.cond)
        self.table = self.table.pushScope("if")
        self.visit(node.if_body)
        self.table = self.table.popScope()
        if node.else_body:
            self.table = self.table.pushScope("else")
            self.visit(node.else_body)
            self.table = self.table.popScope()

    def visit_While(self, node):
        self.visit(node.cond)
        self.loop_nesting += 1
        self.table = self.table.pushScope("while")
        self.visit(node.body)
        self.table = self.table.popScope()
        self.loop_nesting -= 1

    def visit_For(self, node):
        self.visit(node.range)
        self.loop_nesting += 1
        self.table = self.table.pushScope("for")
        self.table.put(node.id, VariableSymbol(node.id, 'int'))
        self.visit(node.body)
        self.table = self.table.popScope()
        self.loop_nesting -= 1

    def visit_Range(self, node):
        start_type = self.visit(node.start)
        end_type = self.visit(node.end)
        if start_type is not None and start_type != 'int':
            self.error(f"Range start must be an integer", node.lineno)
        if end_type is not None and end_type != 'int':
            self.error(f"Range end must be an integer", node.lineno)
        return 'range'

    def visit_Break(self, node):
        if self.loop_nesting == 0:
            self.error(f"'break' used outside of loop", node.lineno)

    def visit_Continue(self, node):
        if self.loop_nesting == 0:
            self.error(f"'continue' used outside of loop", node.lineno)
    
    def visit_Return(self, node):
        if node.expr:
            self.visit(node.expr)

    def visit_Print(self, node):
        for arg in node.args:
            self.visit(arg)

    def visit_Compound(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_Error(self, node):
        pass

