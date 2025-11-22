from sly import Parser
from scanner import Scanner


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
        pass

    @_('statements')
    def program_body(self, p):
        pass

    @_('')
    def program_body(self, p):
        pass

    @_('stmt statements')
    def statements(self, p):
        pass

    @_('stmt')
    def statements(self, p):
        pass

    @_('assign_stmt ";"',
       'simple_stmt ";"',
       'block_stmt',
       'if_stmt',
       'while_stmt',
       'for_stmt')
    def stmt(self, p):
        pass

    @_('"{" statements "}"')
    def block_stmt(self, p):
        pass

    @_('IF "(" cond ")" stmt %prec IFX')
    def if_stmt(self, p):
        pass

    @_('IF "(" cond ")" stmt ELSE stmt')
    def if_stmt(self, p):
        pass

    @_('WHILE "(" cond ")" stmt')
    def while_stmt(self, p):
        pass

    @_('FOR id_ref "=" range stmt')
    def for_stmt(self, p):
        pass

    @_('expr ":" expr')
    def range(self, p):
        pass

    @_('BREAK')
    def simple_stmt(self, p):
        pass

    @_('CONTINUE')
    def simple_stmt(self, p):
        pass

    @_('RETURN expr')
    def simple_stmt(self, p):
        pass

    @_('PRINT print_args')
    def simple_stmt(self, p):
        pass

    @_('print_args "," print_arg',
       'print_arg')
    def print_args(self, p):
        pass

    @_('STRING', 'expr')
    def print_arg(self, p):
        pass

    @_('id_ref assign_op expr',
       'ref_matrix assign_op expr',
       'ref_vector assign_op expr')
    def assign_stmt(self, p):
        pass

    @_('MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN', '"="')
    def assign_op(self, p):
        pass

    @_('expr "+" expr',
       'expr "-" expr',
       'expr "*" expr',
       'expr "/" expr')
    def expr(self, p):
        pass

    @_('expr DOTADD expr',
       'expr DOTSUB expr',
       'expr DOTMUL expr',
       'expr DOTDIV expr')
    def expr(self, p):
        pass

    @_('term',
       'matrix_init',
       'mat_func_call',
       'unary_neg',
       'transpose',
       'ref_matrix',
       'ref_vector')
    def expr(self, p):
        pass

    @_('"-" expr %prec UMINUS')
    def unary_neg(self, p):
        pass

    @_('expr "\'"')
    def transpose(self, p):
        pass

    @_('number', 'id_ref')
    def term(self, p):
        pass

    @_('expr EQ expr',
       'expr NE expr',
       'expr LE expr',
       'expr GE expr',
       'expr "<" expr',
       'expr ">" expr')
    def cond(self, p):
        pass

    @_('mat_func "(" INTNUM ")"')
    def mat_func_call(self, p):
        pass

    @_('EYE', 'ONES', 'ZEROS')
    def mat_func(self, p):
        pass

    @_('"[" mat_rows "]"')
    def matrix_init(self, p):
        pass

    @_('mat_rows "," mat_row',
       'mat_row')
    def mat_rows(self, p):
        pass

    @_('"[" row_items "]"')
    def mat_row(self, p):
        pass

    @_('row_items "," row_item',
       'row_item')
    def row_items(self, p):
        pass

    @_('number', 'id_ref', 'matrix_ref')
    def row_item(self, p):
        pass

    @_('ref_vector', 'ref_matrix')
    def matrix_ref(self, p):
        pass

    @_('ID "[" INTNUM "]"')
    def ref_vector(self, p):
        pass

    @_('ID "[" INTNUM "," INTNUM "]"')
    def ref_matrix(self, p):
        pass

    @_('ID')
    def id_ref(self, p):
        pass

    @_('INTNUM', 'FLOATNUM')
    def number(self, p):
        pass

    def error(self, p):
        if p:
            print(f"Syntax error at line {p.lineno}: {p.type}('{p.value}')")
        else:
            print("Unexpected end of input")

