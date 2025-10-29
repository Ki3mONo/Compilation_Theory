import sys
from sly import Lexer


class Scanner(Lexer):
    tokens = {
        IF, ELSE, FOR, WHILE,
        BREAK, CONTINUE, RETURN,
        EYE, ZEROS, ONES,
        PRINT,
        
        ID, INTNUM, FLOATNUM, STRING,
        
        DOTADD, DOTSUB, DOTMUL, DOTDIV,
        
        ADDASSIGN, SUBASSIGN, MULASSIGN, DIVASSIGN,
        
        LE, GE, NE, EQ,
    }
    
    literals = {
        '=', '+', '-', '*', '/', 
        '(', ')', '[', ']', '{', '}',
        ':', "'", ',', ';',
        '<', '>'
    }
    
    ignore = ' \t'
    
    ignore_comment = r'\#.*'
        
    LE = r'<='
    GE = r'>='
    NE = r'!='
    EQ = r'=='
    
    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'
    
    ADDASSIGN = r'\+='
    SUBASSIGN = r'-='
    MULASSIGN = r'\*='
    DIVASSIGN = r'/='
    
    @_(r'\d+\.\d*([eE][+-]?\d+)?',
       r'\.\d+([eE][+-]?\d+)?',
       r'\d+[eE][+-]?\d+')
    def FLOATNUM(self, t):
        t.value = float(t.value)
        return t
    
    @_(r'\d+')
    def INTNUM(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'"[^"]*"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    ID['if'] = IF
    ID['else'] = ELSE
    ID['for'] = FOR
    ID['while'] = WHILE
    ID['break'] = BREAK
    ID['continue'] = CONTINUE
    ID['return'] = RETURN
    ID['eye'] = EYE
    ID['zeros'] = ZEROS
    ID['ones'] = ONES
    ID['print'] = PRINT
    
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)
    
    def error(self, t):
        print(f"Line {self.lineno}: Illegal character '{t.value[0]}'")
        self.index += 1


if __name__ == '__main__':

    lexer = Scanner()

    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    with open(filename, "r") as file:
        text = file.read()

    for tok in lexer.tokenize(text):
        print(f"({tok.lineno}): {tok.type}({tok.value})")


  