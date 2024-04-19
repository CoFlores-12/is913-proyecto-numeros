from lark import Lark

# Definir la gramática en formato Lark
gramatica = '''
    start: expression
    
    expression: INTEGER palabra_clave? signo_dolar?
              | INTEGER INTEGER signo_dolar?
    
    palabra_clave: BIN
                 | HEX
                 | OCT
                 | ROM
                 | ALT
                 | RAND
    
    INTEGER: /\d+/
    BIN: /binario+/
    HEX: /hexadecimal+/
    OCT: /octal+/
    ROM: /romano+/
    ALT: /alternativo+/
    RAND: /aleatorio+/

    signo_dolar: "$"

    %ignore " \t"
'''

# Crear el analizador sintáctico
analizador = Lark(gramatica, start='start')

# Analizar una cadena de entrada y obtener el árbol de análisis sintáctico
cadena = "123hexadecimal$"
arbol = analizador.parse(cadena)

print(arbol.pretty())
