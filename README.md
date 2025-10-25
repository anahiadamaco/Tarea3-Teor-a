# Analizador FORTRAN77 (subconjunto) - Tarea 3

Requisitos:
- Python 3.8+

Estructura:
- lexer.py
- parser.py
- ast.py
- util.py
- main.py
- tests/

Cómo ejecutar:
$ python main.py tests/prog_valido.for

Salidas:
- Lista de tokens por consola
- Árbol sintáctico impreso en consola
- Archivo DOT generado: ast.dot (puedes convertirlo a PNG con Graphviz: dot -Tpng ast.dot -o ast.png)

Notas:
- El lexer reconoce comentarios que comienzan con 'C' al inicio de línea.
- El parser espera la palabra reservada END al final del programa.
- Extensiones sugeridas: interfaz gráfica ligera, manejo de más palabras reservadas, soporte para número reales con notación científica, y pasar a un parser LR(1).