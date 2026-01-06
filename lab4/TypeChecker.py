from AST import *

from SymbolTable import SymbolTable, VariableSymbol

class TypeChecker(object):

    def __init__(self):
        self.table = SymbolTable(None, "global")
        self.loop_nesting = 0

    def visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
            return
        
        if node is None:
            return None

        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        pass

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
            print(f"Error: Variable '{node.name}' not defined at line {getattr(node, 'lineno', '?')}")
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

        dims1 = get_dims(type1)
        dims2 = get_dims(type2)

        is_matrix1 = isinstance(type1, tuple)
        is_matrix2 = isinstance(type2, tuple)

        if is_matrix1 != is_matrix2:
             print(f"Error: Incompatible types {type1} and {type2} for operation '{op}' at line {getattr(node, 'lineno', '?')}")
             return None

        if is_matrix1 and is_matrix2:
            if op in ['+', '-', '.+', '.-']: 
                if dims1 != dims2:
                    print(f"Error: Incompatible dimensions {dims1} and {dims2} for operation '{op}' at line {getattr(node, 'lineno', '?')}")
                    return None
                return type1 
            elif op in ['*', '/']: 
                if op == '*':
                    if len(dims1) == 2 and len(dims2) == 2: 
                        if dims1[1] != dims2[0]:
                            print(f"Error: Incompatible dimensions {dims1} and {dims2} for operation '{op}' at line {getattr(node, 'lineno', '?')}")
                            return None
                        return ('matrix', dims1[0], dims2[1], type1[3]) 
                elif op == '/':
                    pass
                
                if op in ['.*', './']:
                     if dims1 != dims2:
                        print(f"Error: Incompatible dimensions {dims1} and {dims2} for operation '{op}' at line {getattr(node, 'lineno', '?')}")
                        return None
                     return type1

        if not is_matrix1 and not is_matrix2:
            if type1 != type2:
                if type1 in ['int', 'float'] and type2 in ['int', 'float']:
                    return 'float'
                return 'float' 
            return type1

        return None

    def visit_RelExpr(self, node):
        type1 = self.visit(node.left)
        type2 = self.visit(node.right)
        return 'int'

    def visit_Assign(self, node):
        type_right = self.visit(node.right)
        
        if isinstance(node.left, AST.Variable):
            self.table.put(node.left.name, VariableSymbol(node.left.name, type_right))
        elif isinstance(node.left, AST.Ref):
            symbol = self.table.get(node.left.name)
            if not symbol:
                print(f"Error: Variable '{node.left.name}' not defined at line {getattr(node, 'lineno', '?')}")
            else:
                pass
        
        return type_right

    def visit_Vector(self, node):
        if not node.elements:
            return ('vector', 0, 'unknown')
        
        first_type = self.visit(node.elements[0])
        
        for elem in node.elements[1:]:
            t = self.visit(elem)
            if t != first_type:
                if isinstance(first_type, tuple) and isinstance(t, tuple):
                    if first_type[0] == 'vector' and t[0] == 'vector':
                        if first_type[1] != t[1]:
                            print(f"Error: Vector sizes mismatch in matrix initialization at line {getattr(node, 'lineno', '?')}")
                            return None
                        if first_type[2] != t[2]:
                             pass
                    else:
                        print(f"Error: Incompatible types in vector initialization at line {getattr(node, 'lineno', '?')}")
                        return None
                else:
                     print(f"Error: Incompatible types in vector initialization at line {getattr(node, 'lineno', '?')}")
                     return None

        if isinstance(first_type, tuple) and first_type[0] == 'vector':
            return ('matrix', len(node.elements), first_type[1], first_type[2])
        else:
            return ('vector', len(node.elements), first_type)

    def visit_Ref(self, node):
        symbol = self.table.get(node.name)
        if not symbol:
            print(f"Error: Variable '{node.name}' not defined at line {getattr(node, 'lineno', '?')}")
            return None
        
        type_sym = symbol.type
        if not isinstance(type_sym, tuple):
            print(f"Error: Variable '{node.name}' is not a matrix/vector at line {getattr(node, 'lineno', '?')}")
            return None

        indices = node.indices
        dims = []
        if type_sym[0] == 'vector':
            dims = [type_sym[1]]
        elif type_sym[0] == 'matrix':
            dims = [type_sym[1], type_sym[2]]

        if len(indices) != len(dims):
             print(f"Error: Invalid number of indices for '{node.name}' at line {getattr(node, 'lineno', '?')}")
             return None

        for i, index in enumerate(indices):
            if isinstance(index, AST.IntNum):
                val = index.value
                if val < 0 or val >= dims[i]: 
                    print(f"Error: Index {val} out of bounds for '{node.name}' (dim {dims[i]}) at line {getattr(node, 'lineno', '?')}")
            else:
                t = self.visit(index)
                if t != 'int':
                     print(f"Error: Index must be integer at line {getattr(node, 'lineno', '?')}")

        return type_sym[-1]

    def visit_Function(self, node):
        if node.name in ['zeros', 'ones', 'eye']:
            args = node.args
            if len(args) > 2:
                 print(f"Error: Too many arguments for '{node.name}' at line {getattr(node, 'lineno', '?')}")
                 return None
            
            val1 = None
            val2 = None

            if len(args) >= 1:
                t = self.visit(args[0])
                if t != 'int':
                    print(f"Error: Argument 1 for '{node.name}' must be int at line {getattr(node, 'lineno', '?')}")
                if isinstance(args[0], AST.IntNum):
                    val1 = args[0].value

            if len(args) == 2:
                t = self.visit(args[1])
                if t != 'int':
                    print(f"Error: Argument 2 for '{node.name}' must be int at line {getattr(node, 'lineno', '?')}")
                if isinstance(args[1], AST.IntNum):
                    val2 = args[1].value
            
            if val1 is not None:
                if len(args) == 1:
                    return ('matrix', val1, val1, 'int') 
                elif len(args) == 2 and val2 is not None:
                    return ('matrix', val1, val2, 'int')
            
            return ('matrix', 0, 0, 'int') 

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
        self.visit(node.start)
        self.visit(node.end)
        return 'range'

    def visit_Break(self, node):
        if self.loop_nesting == 0:
            print(f"Error: 'break' outside of loop at line {getattr(node, 'lineno', '?')}")

    def visit_Continue(self, node):
        if self.loop_nesting == 0:
            print(f"Error: 'continue' outside of loop at line {getattr(node, 'lineno', '?')}")
    
    def visit_Return(self, node):
        if node.expr:
            self.visit(node.expr)

    def visit_Print(self, node):
        self.visit(node.args)

    def visit_Compound(self, node):
        for statement in node.statements:
            self.visit(statement)

