#1 Tokens
def extraer_token(expresion):
    tokens = []
    numero_actual = ''
    
    for char in expresion:
        if char.isdigit():
            numero_actual += char
        elif char in '+-*/()':
            if numero_actual:
                tokens.append(numero_actual)
                numero_actual = ''
            tokens.append(char)
        elif char.isspace():
            if numero_actual:
                tokens.append(numero_actual)
                numero_actual = ''
    
    if numero_actual:
        tokens.append(numero_actual)
    
    return tokens

# Casos de prueba
assert extraer_token("3 + 5") == ["3", "+", "5"]
assert extraer_token("(1 + 2) * 3") == ["(", "1", "+", "2", ")", "*", "3"]
assert extraer_token("10 / (5 - 3)") == ["10", "/", "(", "5", "-", "3", ")"]
assert extraer_token("4 * (2 + 3) / 5") == ["4", "*", "(", "2", "+", "3", ")", "/", "5"]
assert extraer_token("7 - 2 * (3 + 4)") == ["7", "-", "2", "*", "(", "3", "+", "4", ")"]
assert extraer_token("") == []

print("¡Todos los casos de prueba pasaron!")

#2 Comprobar parentesis

def verificar_parentesis(tokens):
    contador = 0
    for token in tokens:
        if token == "(":
            contador += 1
        elif token == ")":
            contador -= 1
        if contador < 0:
            return False
    return contador == 0

# Casos de prueba
assert verificar_parentesis(["(", "1", "+", "2", "+", "(", "3", "*", "4", ")", "+", "(", "5", "*", "6", ")", ")"]) == True
assert verificar_parentesis(["(", "(", "1", "+", "2", ")", "+", "3"]) == False
assert verificar_parentesis(["(", "1", "+", "3", ")", "*", "4", ")"]) == False
assert verificar_parentesis([]) == True
assert verificar_parentesis(["(", "(", "(", "1", "+", "2"]) == False
assert verificar_parentesis([")", "1", "+", "2", ")"]) == False

print("¡Todos los casos de prueba pasaron!")

#3 Comprobar expresion valida

def es_expresion_valida(lista):
    if not lista:
        return True  # Una lista vacía se considera válida

    es_numero = lambda x: x.isdigit() or (x[0] == '-' and x[1:].isdigit())
    es_operador = lambda x: x in ['+', '-', '*', '/']

    estado = 'espera_numero'  # Estados: 'espera_numero', 'espera_operador'
    parentesis = 0

    for token in lista:
        if token == '(':
            if estado == 'espera_operador':
                return False
            parentesis += 1
        elif token == ')':
            if estado == 'espera_numero' or parentesis == 0:
                return False
            parentesis -= 1
        elif es_numero(token):
            if estado == 'espera_operador':
                return False
            estado = 'espera_operador'
        elif es_operador(token):
            if estado == 'espera_numero':
                return False
            estado = 'espera_numero'
        else:
            return False  # Token no válido

    return parentesis == 0 and estado == 'espera_operador'

# Casos de prueba
assert es_expresion_valida(["(", "1", "+", "2", ")", "*", "3"]) == True
assert es_expresion_valida(["1", "+", "(", ")"]) == False
assert es_expresion_valida(["1", "*", "*", "2"]) == False
assert es_expresion_valida(["(", "1", "+", "2", ")", "/", "(", "3", "-", "4", ")"]) == True
assert es_expresion_valida(["(", "1", "+", "(", "2", "*", "3", ")", "-", "4", ")"]) == True
assert es_expresion_valida(["1", "+", "2", "*", "3", "/", "4"]) == True
assert es_expresion_valida(["1", "+", "+", "2"]) == False
assert es_expresion_valida(["(", "1", "+", "2", "*", "3"]) == False
assert es_expresion_valida(["1", "+", "2", ")", "*", "3"]) == False
assert es_expresion_valida(["(", "1", "+", "2", ")", "*", "(", "3", "/", "4", ")"]) == True

print("¡Todos los casos de prueba pasaron!")

#4

def evaluar(tokens):
    # Paso 1: Resolver los paréntesis primero
    tokens = resolver_parentesis(tokens)
    
    # Paso 2: Resolver las multiplicaciones
    tokens = resolver_multiplicaciones(tokens)
    
    # Paso 3: Resolver las sumas
    return resolver_sumas(tokens)

def resolver_parentesis(tokens):
    stack = []
    i = 0
    while i < len(tokens):
        if tokens[i] == "(":
            stack.append(i)
        elif tokens[i] == ")":
            if stack:
                start = stack.pop()
                subexpresion = tokens[start+1:i]
                resultado = evaluar(subexpresion)
                tokens = tokens[:start] + [str(resultado)] + tokens[i+1:]
                i = start
        i += 1
    return tokens

def resolver_multiplicaciones(tokens):
    i = 1
    while i < len(tokens) - 1:
        if tokens[i] == "*":
            resultado = float(tokens[i-1]) * float(tokens[i+1])
            tokens = tokens[:i-1] + [str(resultado)] + tokens[i+2:]
            i -= 1
        else:
            i += 1
    return tokens

def resolver_sumas(tokens):
    resultado = float(tokens[0])
    i = 1
    while i < len(tokens):
        if tokens[i] == "+":
            resultado += float(tokens[i+1])
        i += 2
    return resultado

# Casos de prueba
assert evaluar(["(", "1", "+", "2", ")", "*", "3"]) == 9
assert evaluar(["1", "+", "2", "*", "3"]) == 7
assert evaluar(["(", "1", "+", "2", ")", "+", "(", "3", "*", "4", ")"]) == 15
assert evaluar(["10", "+", "(", "5", "*", "3", ")", "+", "2"]) == 27
assert evaluar(["(", "2", "+", "3", ")", "*", "(", "4", "+", "1", ")"]) == 25

print("¡Todos los casos de prueba pasaron!")