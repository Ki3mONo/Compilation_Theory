from sly import Parser
from scanner import Scanner
import AST


class Mparser(Parser):

    tokens = Scanner.tokens

    start = 'program'
    debugfile = 'parser.out'

    precedence = (
        ('nonassoc', 'IFX'),
        ('nonassoc', 'ELSE'),
        ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
        ('nonassoc', '<', '>', 'LE', 'GE', 'NE', 'EQ'),
        ('left', '+', '-'),
        ('left', 'DOTADD', 'DOTSUB'),
        ('left', '*', '/'),
        ('left', 'DOTMUL', 'DOTDIV'),
        ('right', 'UMINUS'),
        ('left', "'"),
    )

    @_('program_body')
    def program(self, p):
        return p.program_body

    @_('statements')
    def program_body(self, p):
        return AST.Compound(p.statements)

    @_('')
    def program_body(self, p):
        return AST.Compound([])

    @_('stmt statements')
    def statements(self, p):
        return [p.stmt] + p.statements

    @_('stmt')
    def statements(self, p):
        return [p.stmt]

    @_('assign_stmt ";"',
       'simple_stmt ";"',
       'block_stmt',
       'if_stmt',
       'while_stmt',
       'for_stmt')
    def stmt(self, p):
        return p[0]

    @_('"{" statements "}"')
    def block_stmt(self, p):
        return AST.Compound(p.statements)

    @_('IF "(" cond ")" stmt %prec IFX')
    def if_stmt(self, p):
        return AST.If(p.cond, p.stmt)

    @_('IF "(" cond ")" stmt ELSE stmt')
    def if_stmt(self, p):
        return AST.If(p.cond, p.stmt0, p.stmt1)

    @_('WHILE "(" cond ")" stmt')
    def while_stmt(self, p):
        return AST.While(p.cond, p.stmt)

    @_('FOR id_ref "=" range stmt')
    def for_stmt(self, p):
        return AST.For(p.id_ref, p.range, p.stmt)

    @_('expr ":" expr')
    def range(self, p):
        return AST.Range(p.expr0, p.expr1)

    @_('BREAK')
    def simple_stmt(self, p):
        return AST.Break()

    @_('CONTINUE')
    def simple_stmt(self, p):
        return AST.Continue()

    @_('RETURN expr')
    def simple_stmt(self, p):
        return AST.Return(p.expr)

    @_('PRINT print_args')
    def simple_stmt(self, p):
        return AST.Print(p.print_args)

    @_('print_args "," print_arg')
    def print_args(self, p):
        return p.print_args + [p.print_arg]

    @_('print_arg')
    def print_args(self, p):
        return [p.print_arg]

    @_('STRING')
    def print_arg(self, p):
        return AST.String(p.STRING)

    @_('expr')
    def print_arg(self, p):
        return p.expr

    @_('id_ref assign_op expr',
       'ref_matrix assign_op expr',
       'ref_vector assign_op expr')
    def assign_stmt(self, p):
        return AST.Assign(p.assign_op, p[0], p.expr)

    @_('MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN', '"="')
    def assign_op(self, p):
        return p[0]

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr',
       'expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        return AST.BinExpr(p[1], p.expr0, p.expr1)

    @_('term',
       'matrix_init',
       'mat_func_call',
       'unary_neg',
       'transpose',
       'ref_matrix',
       'ref_vector')
    def expr(self, p):
        return p[0]

    @_('"-" expr %prec UMINUS')
    def unary_neg(self, p):
        return AST.UnaryExpr('-', p.expr)

    @_('expr "\'"')
    def transpose(self, p):
        return AST.Transpose(p.expr)

    @_('number', 'id_ref')
    def term(self, p):
        return p[0]

    @_('expr EQ expr',
       'expr NE expr',
       'expr LE expr',
       'expr GE expr',
       'expr "<" expr',
       'expr ">" expr')
    def cond(self, p):
        return AST.RelExpr(p[1], p.expr0, p.expr1)

    @_('mat_func "(" INTNUM ")"')
    def mat_func_call(self, p):
        return AST.Function(p.mat_func, AST.IntNum(int(p.INTNUM)))

    @_('EYE', 'ONES', 'ZEROS')
    def mat_func(self, p):
        return p[0]

    @_('"[" mat_rows "]"')
    def matrix_init(self, p):
        return AST.Vector(p.mat_rows)

    @_('mat_rows "," mat_row')
    def mat_rows(self, p):
        return p.mat_rows + [p.mat_row]

    @_('mat_row')
    def mat_rows(self, p):
        return [p.mat_row]

    @_('"[" row_items "]"')
    def mat_row(self, p):
        return AST.Vector(p.row_items)

    @_('row_items "," row_item')
    def row_items(self, p):
        return p.row_items + [p.row_item]

    @_('row_item')
    def row_items(self, p):
        return [p.row_item]

    @_('number', 'id_ref', 'matrix_ref')
    def row_item(self, p):
        return p[0]

    @_('ref_vector', 'ref_matrix')
    def matrix_ref(self, p):
        return p[0]

    @_('ID "[" INTNUM "]"')
    def ref_vector(self, p):
        return AST.Ref(p.ID, [AST.IntNum(int(p.INTNUM))])

    @_('ID "[" INTNUM "," INTNUM "]"')
    def ref_matrix(self, p):
        return AST.Ref(p.ID, [AST.IntNum(int(p.INTNUM0)), AST.IntNum(int(p.INTNUM1))])

    @_('ID')
    def id_ref(self, p):
        return AST.Variable(p.ID)

    @_('INTNUM')
    def number(self, p):
        return AST.IntNum(int(p.INTNUM))

    @_('FLOATNUM')
    def number(self, p):
        return AST.FloatNum(float(p.FLOATNUM))

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: {p.type}('{p.value}')")
        else:
            print("Unexpected end of input")

