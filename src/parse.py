import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'INTEGER',
    'BIN',
    'HEX',
    'OCT',
    'ROM'
)

t_INTEGER = r'\d+'
t_BIN = r'binario+'
t_HEX = r'hexadecimal+'
t_OCT = r'octal+'
t_ROM = r'romanos+'

t_ignore = ' \t'

def t_error(t):
    print(f"Token desconocido: '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def p_expression_integer_base(p):
    '''expression   : INTEGER BIN
                    | INTEGER HEX
    				| INTEGER OCT
    			    | INTEGER ROM'''
    integer = int(p[1])
    base_str = p[2]
    p[0] = convert_to_base(integer, base_str)

def p_expression_integer_integer(p):
    '''expression : INTEGER INTEGER'''
    number = int(p[1])
    base = int(p[2])
    p[0] = convert_to_base_int(number, base)

def p_error(p):
    if p:
        return (f"Error de sintaxis en la entrada en '{p.value}'")
    else:
        return ("Error de sintaxis al final de la entrada")


def convert_to_base(number, base_str):
    if base_str == "binario":
        return bin(number)[2:]  
    elif base_str == "hexadecimal":
        return hex(number)[2:]  
    elif base_str == "octal":
        return oct(number)[2:] 
    elif base_str == "romanos":
        return to_roman(number) 
    else:
        return "Base no soportada"
        
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


class Parse():
    def __init__(self):
        self.parser = yacc.yacc()

    def parse(self, input_string):
        return self.parser.parse(input_string.lower())

parse = Parse()
parse.parse("2binario")