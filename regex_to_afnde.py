from AFND_e import AFND_e
estado_id = 0

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
        global estado_id

        print(f"Expresión regular en notación postfija: {postfijo}")
        # Crear un autómata vacío
        automata = AFND_e()
        stack = []

        for char in postfijo:
        # Caso base: símbolo del alfabeto (a, b, c, e)
            if char in alfabeto:
                # Creamos un nuevo estado inicial
                inicio = f"s{estado_id}"
                estado_id += 1
                # Creamos un nuevo estado final
                fin = f"s{estado_id}"
                estado_id += 1

                # Agregamos la transición al autómata
                automata.agregar_transicion(inicio, char, fin)
                print(f"Transición: {inicio} --{char}--> {fin}")

                stack.append((inicio, fin))

        # Operadores
            # Concatenación (.)
            elif char == '.':
                frag2 = stack.pop()
                frag1 = stack.pop()

                # Agregamos la transición epsilon entre el final de frag1 y el inicio de frag2
                automata.agregar_transicion(frag1[1], 'e', frag2[0])
                print(f"Transición: {frag1[1]} --e--> {frag2[0]}")

                stack.append((frag1[0], frag2[1]))
            
            # Pipe (|)
            elif char == '|':
                frag2 = stack.pop()
                frag1 = stack.pop()

                # Creamos un nuevo estado inicial
                nuevo_inicio = f"s{estado_id}"
                estado_id += 1
                # Creamos un nuevo estado final
                nuevo_fin = f"s{estado_id}"
                estado_id += 1

                # Conectamos el nuevo inicio a los dos fragmentos con transiciones epsilon
                automata.agregar_transicion(nuevo_inicio, 'e', frag1[0])
                print(f"Transición: {nuevo_inicio} --e--> {frag1[0]}")
                automata.agregar_transicion(nuevo_inicio, 'e', frag2[0])
                print(f"Transición: {nuevo_inicio} --e--> {frag2[0]}")

                # Conectamos los finales de los fragmentos al nuevo fin con transiciones epsilon
                automata.agregar_transicion(frag1[1], 'e', nuevo_fin)
                print(f"Transición: {frag1[1]} --e--> {nuevo_fin}")
                automata.agregar_transicion(frag2[1], 'e', nuevo_fin)
                print(f"Transición: {frag2[1]} --e--> {nuevo_fin}")
                
                stack.append((nuevo_inicio, nuevo_fin))
                
            elif char == '*':
                frag = stack.pop()

                # Creamos un nuevo estado inicial
                nuevo_inicio = f"s{estado_id}"
                estado_id += 1
                # Creamos un nuevo estado final
                nuevo_fin = f"s{estado_id}"
                estado_id += 1

                # Transiciones epsilon al nuevo estado inicial
                automata.agregar_transicion(nuevo_inicio, 'e', frag[0])
                print(f"Transición: {nuevo_inicio} --e--> {frag[0]}")

                # Transición epsilon al nuevo estado final
                automata.agregar_transicion(nuevo_inicio, 'e', nuevo_fin)
                print(f"Transición: {nuevo_inicio} --e--> {nuevo_fin}")

                # Transición epsilon de vuelta al inicio
                automata.agregar_transicion(frag[1], 'e', frag[0])
                print(f"Transición: {frag[1]} --e--> {frag[0]}")

                # Transición epsilon al nuevo estado final
                automata.agregar_transicion(frag[1], 'e', nuevo_fin)
                print(f"Transición: {frag[1]} --e--> {nuevo_fin}")

                stack.append((nuevo_inicio, nuevo_fin))

        inicio = stack.pop()
        # Agregamos el estado inicial del autómata
        automata.establecer_inicial(inicio[0])
        print(f"Estado inicial: {automata.inicial}")
        # Agregamos el estado final al autómata
        automata.agregar_final(inicio[1])
        print(f"Estado final: {automata.finales}")

        automata.mostrar()
        return automata

    postfijo = parse(expr)
    return construir(postfijo)