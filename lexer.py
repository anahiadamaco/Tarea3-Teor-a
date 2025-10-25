import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value', 'line', 'col'])

class LexerError(Exception):
    pass

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.col = 1

        # Define token specs (order matters)
        self.token_specification = [
            ('NEWLINE',    r'\n'),
            ('SKIP',       r'[ \t\r]+'),
            ('COMMENT',    r'C[^\n]*'),  # FORTRAN77 comment (starts with C)
            ('COMMA',      r','),
            ('LPAREN',     r'\('),
            ('RPAREN',     r'\)'),
            ('ASSIGN',     r'='),
            ('OP',         r'[\+\-\*/]'),
            ('NUMBER',     r'\d+(\.\d+)?'),
            ('IDENT',      r'[A-Za-z][A-Za-z0-9]*'),
            ('UNKNOWN',    r'.'),
        ]

        self.regex = re.compile('|'.join('(?P<%s>%s)' % pair for pair in self.token_specification))
        self.keywords = {'INTEGER','REAL','END','IF','THEN','ELSE','DO'}

    def tokenize(self):
        for mo in self.regex.finditer(self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NEWLINE':
                self.line += 1
                self.col = 1
                continue
            elif kind == 'SKIP' or kind == 'COMMENT':
                # update column
                self.col += len(value)
                continue
            elif kind == 'IDENT':
                up = value.upper()
                if up in self.keywords:
                    tok = Token('KEYWORD', up, self.line, self.col)
                else:
                    tok = Token('IDENT', value, self.line, self.col)
            elif kind == 'NUMBER':
                tok = Token('NUMBER', value, self.line, self.col)
            elif kind == 'OP':
                tok = Token('OP', value, self.line, self.col)
            elif kind == 'ASSIGN':
                tok = Token('ASSIGN', value, self.line, self.col)
            elif kind in ('LPAREN','RPAREN','COMMA'):
                tok = Token(kind, value, self.line, self.col)
            elif kind == 'UNKNOWN':
                raise LexerError(f'Caracter desconocido {value!r} en linea {self.line} columna {self.col}')
            else:
                continue

            yield tok
            self.col += len(value)