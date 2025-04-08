def regex_to_afnde(expr):
    alfabeto = "abce"
    operadores = "*|."

    # Precedencia * > . > |
    precedencia = {
        '*': 3,
        '.': 2,
        '|': 1
    }
    
    def parse(expr):
        #Funcion utilizada para pasar la expresion leida a notacion post-fija
        # Notación post-fija, es una forma de escribir expresiones en la que los operadores se colocan después de sus operandos.

        # Se utiliza un stack para almacenar los operadores y una lista para la salida
        stack = []
        salida = []

        for char in expr:
            if char in alfabeto:
                salida.append(char)
            elif char in operadores:
                # Si el operador en la pila tiene igual o mayor precedencia, lo sacamos de la pila y lo mandamos a la salida.
                while (stack and precedencia[stack[-1]] >= precedencia[char]):
                    salida.append(stack.pop())
                # Cuando no quedan operadores con mayor o igual precedencia, agrego el actual a la pila
                stack.append(char)
        
        while stack:
            salida.append(stack.pop())

        return salida
        

    def construir(postfijo):
        #Funcion que construye el afnde
        return None

    postfijo = parse(expr)
    return construir(postfijo)