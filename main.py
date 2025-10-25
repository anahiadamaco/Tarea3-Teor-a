import sys
from lexer import Lexer, LexerError
from parser import Parser, ParserError
from util import pprint_tree, to_dot

def run_code(text):
    try:
        lex = Lexer(text)
        tokens = list(lex.tokenize())
        print('--- TOKENS ---')
        for t in tokens:
            print(t)
        print('--------------')

        parser = Parser(tokens)
        ast = parser.parse()
        print('\n--- ARBOL SINTACTICO ---')
        pprint_tree(ast)
        dotfile = to_dot(ast, filename='ast.dot')
        print(f'\nDOT generado: {dotfile} (puedes visualizar con: dot -Tpng ast.dot -o ast.png)')
    except LexerError as le:
        print('Error Léxico:', le)
    except ParserError as pe:
        print('Error Sintáctico:', pe)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: python main.py archivo.for')
        print('Ejemplo: python main.py tests/prog1.for')
        sys.exit(1)
    path = sys.argv[1]
    with open(path,'r', encoding='utf-8') as f:
        code = f.read()
    run_code(code)