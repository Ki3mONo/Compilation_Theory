from sly import Parser
from scanner import Scanner


class Mparser(Parser):

    tokens = Scanner.tokens

    debugfile = 'parser.out'


    precedence = (
        ('nonassoc', 'IF', 'THEN', 'ELSE'),
        ("left", '+', '-'),
    # to fill ...
    )


    @_('instructions_opt')
    def program(p):
        pass

    @_('instructions')
    def instructions_opt(p):
        pass

    @_('')
    def instructions_opt(p):
        pass

    @_('instructions instruction')
    def instructions(p):
        pass

    @_('instruction')
    def instructions(p):
        pass


    # to finish the grammar
    # ....

