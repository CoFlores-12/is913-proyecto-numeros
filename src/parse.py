import ply.lex as lex
import ply.yacc as yacc
import re

# PARSE SIDE
tokens = (
    'INTEGER',
    'BIN',
    'HEX',
    'OCT',
    'ROM',
    'ALT',
    'RAND',
    'DOLAR'
)

t_INTEGER = r'\d+'
t_BIN = r'binario+'
t_HEX = r'hexadecimal+'
t_OCT = r'octal+'
t_ROM = r'romano+'
t_ALT = r'alternativo+'
t_RAND = r'aleatorio+'
t_DOLAR = r'\$'

t_ignore = ' \t'

lexer_errors = []
parser_errors = []
destino = ""

def t_error(t):
    global lexer_errors
    lexer_errors.append({"linea": t.lineno, "tipo": "Token desconocido", "valor": t.value})
    t.lexer.skip(1)

lexer = lex.lex()

def p_expression_integer_base_BIN(p):
    '''expression   : INTEGER BIN DOLAR'''
    global destino
    destino = "BIN"
    integer = int(p[1])
    p[0] = bin(integer)[2:]

def p_expression_integer_base_HEX(p):
    '''expression   : INTEGER HEX DOLAR'''
    global destino
    destino = "HEX"
    integer = int(p[1])
    p[0] = hex(integer)[2:]

def p_expression_integer_base_OCT(p):
    '''expression   : INTEGER OCT DOLAR'''
    global destino
    destino = "OCT"
    integer = int(p[1])
    p[0] = oct(integer)[2:]

def p_expression_integer_base_ROM(p):
    '''expression   : INTEGER ROM DOLAR'''
    global destino
    destino = "ROM"
    integer = int(p[1])
    p[0] = to_roman(integer) 

def p_expression_integer_base_ALT(p):
    '''expression   : INTEGER ALT DOLAR'''
    global destino
    destino = "ALT"
    try:
        hora = int(p[1][:2])
        minutos = int(p[1][2:])
        if hora == 0:
            hora_12h = "12"
            designacion = "AM"
        elif hora < 12:
            hora_12h = str(hora)
            designacion = "AM"
        elif hora == 12:
            hora_12h = "12"
            designacion = "PM"
        else:
            hora_12h = str(hora - 12)
            designacion = "PM"
            
        if minutos < 10:
            minutos = "0" + str(minutos)
        else:
            minutos = str(minutos)
            
        hora_12h += ":" + minutos + " " + designacion
        p[0] = hora_12h
    except ValueError as e:
        p[0] = "Error: " + str(e)

def p_expression_integer_base_RAND(p):
    '''expression   : INTEGER RAND DOLAR'''
    conversiones = [p_expression_integer_base_BIN, p_expression_integer_base_HEX, p_expression_integer_base_OCT, p_expression_integer_base_ROM, p_expression_integer_base_ALT]
    conversion_aleatoria = random.choice(conversiones[:-1])
    conversion_aleatoria(p)

def p_expression_integer_integer(p):
    '''expression : INTEGER INTEGER DOLAR'''
    global destino
    destino = "INTEGER"
    number = int(p[1])
    base = int(p[2])
    p[0] = convert_to_base_int(number, base)

def p_error(p):
    global parser_errors
    if p:
        parser_errors.append({"tipo": "Error de sintaxis", "valor": p.value})
    else:
        parser_errors.append({"tipo": "Error de sintaxis", "valor": "Final de la entrada"})

def to_roman(number):
    roman_numerals = {
        1: 'I', 4: 'IV', 5: 'V', 9: 'IX', 10: 'X', 40: 'XL',
        50: 'L', 90: 'XC', 100: 'C', 400: 'CD', 500: 'D', 900: 'CM', 1000: 'M'
    }
    result = ''
    for value, numeral in sorted(roman_numerals.items(), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result

def convert_to_base_int(number, base):
    if base < 2 or base > 36:
        return "Error: Base fuera de rango [2, 36]"
    converted_number = ""
    while number > 0:
        remainder = number % base
        converted_number = str(remainder) + converted_number
        number //= base
    return converted_number if converted_number else "0" 

def mostrar_salida_detalle(data):
    print("Detalle del análisis:")
    print("+-----------------+---------------+-----------------+")
    print("| Línea del token | Tipo de token | Valor o elemento|")
    print("+-----------------+---------------+-----------------+")
    lexer.input(data)
    for token in lexer:
        print(f"| {token.lineno:<15} | {token.type:<13} | {token.value:<15} |")
    print("+-----------------+---------------+-----------------+")
    print("|           Resultado del análisis sintáctico       |")
    print("+-----------------+---------------+-----------------+")

parser = yacc.yacc()

with open("data.txt", 'r') as archivo:
    contenido = archivo.read()
patron = r'(\d+\w+\$)' 
tokens = re.findall(patron, contenido)
for token in tokens:
    print('\n######################## ' + token + ' ########################')
    print(parser.parse(token))
    mostrar_salida_detalle(token)
