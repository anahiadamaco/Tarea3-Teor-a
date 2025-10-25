from lexer import Token, Lexer, LexerError
from ast import ASTNode

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0
        self.current = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current = self.tokens[self.pos]
        else:
            self.current = None

    def expect(self, tok_type, value=None):
        if self.current and self.current.type == tok_type and (value is None or self.current.value == value):
            cur = self.current
            self.advance()
            return cur
        else:
            expected = f'{tok_type}' + (f'({value})' if value else '')
            got = f'{self.current.type}({self.current.value})' if self.current else 'EOF'
            raise ParserError(f'Esperado {expected} pero se obtuvo {got}')

    def parse(self):
        node = ASTNode('program')
        stmts = self.stmt_list()
        node.children = stmts
        # require END keyword at end
        if self.current and self.current.type == 'KEYWORD' and self.current.value == 'END':
            self.advance()
        else:
            raise ParserError('Se esperaba la palabra reservada END al final del programa.')
        return node

    def stmt_list(self):
        stmts = []
        while self.current and not (self.current.type == 'KEYWORD' and self.current.value == 'END'):
            stmts.append(self.stmt())
        return stmts

    def stmt(self):
        if self.current.type == 'KEYWORD' and self.current.value == 'INTEGER':
            return self.declaration()
        elif self.current.type == 'IDENT':
            return self.assignment()
        else:
            raise ParserError(f'Sentencia inválida empezando por {self.current.type}({self.current.value})')

    def declaration(self):
        # INTEGER id, id, ...
        self.expect('KEYWORD', 'INTEGER')
        ids = []
        tok = self.expect('IDENT')
        ids.append(ASTNode('ident', tok.value))
        while self.current and self.current.type == 'COMMA':
            self.advance()  # eat comma
            tok = self.expect('IDENT')
            ids.append(ASTNode('ident', tok.value))
        node = ASTNode('declaration', children=ids)
        return node

    def assignment(self):
        # IDENT = expr
        tok = self.expect('IDENT')
        left = ASTNode('ident', tok.value)
        self.expect('ASSIGN')
        expr = self.expr()
        node = ASTNode('assignment', children=[left, expr])
        return node

    # expr -> term ((+|-) term)*
    def expr(self):
        node = self.term()
        while self.current and (self.current.type == 'OP' and self.current.value in ('+','-')):
            op = self.current.value
            self.advance()
            right = self.term()
            node = ASTNode('binop', value=op, children=[node, right])
        return node

    # term -> factor ((*|/) factor)*
    def term(self):
        node = self.factor()
        while self.current and (self.current.type == 'OP' and self.current.value in ('*','/')):
            op = self.current.value
            self.advance()
            right = self.factor()
            node = ASTNode('binop', value=op, children=[node, right])
        return node

    # factor -> NUMBER | IDENT | (expr)
    def factor(self):
        if self.current.type == 'NUMBER':
            tok = self.current
            self.advance()
            return ASTNode('number', value=tok.value)
        elif self.current.type == 'IDENT':
            tok = self.current
            self.advance()
            return ASTNode('ident', value=tok.value)
        elif self.current.type == 'LPAREN':
            self.advance()
            node = self.expr()
            self.expect('RPAREN')
            return node
        else:
            raise ParserError(f'Factor inválido: {self.current.type}({self.current.value})')