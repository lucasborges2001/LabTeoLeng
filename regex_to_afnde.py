from AFND_e import AFND_e
def regex_to_afnde(expr):
    def parse(expr):
        #Funcion utilizada para pasar la expresion leida a notacion post-fija
        # Definir literales
        literales = {'a', 'b', 'c'}
        # Definir precedencia
        precedencia = {'*': 3, '.': 2, '|': 1}
        # Inicializamos la pila vacia
        pila_operadores = []
        # Inicializo una salida
        postfijo = []


        for caracter in expr:
            if caracter in literales:
                # Si el caracter es un literal, entonces lo agregamos directamente
                postfijo.append(caracter)
            elif caracter in precedencia:
                # Mientras que la pila no es vacia y la precedencia de nuestro caracter es menor a la maxima en nuestra pila
                while (pila_operadores and precedencia[pila_operadores[-1]] >= precedencia[caracter]):
                    # Agregamos a la salida el operador de la pila (mayor precedencia) que nuestro caracter
                    postfijo.append(pila_operadores.pop())
                # Al final agregamos nuestro caracter a la pila
                pila_operadores.append(caracter)
        # Los elementos que quedaron en la pila, se deben colocar al final
        while pila_operadores != []:
            # Agregamos el de más precedencia
            postfijo.append(pila_operadores[-1])
            # Quitamos el elemento agregado
            pila_operadores.pop()
        #print(salida)
        return postfijo

    def construir(postfijo):
        #Funcion que construye el afnde     
        # Definir literales
        literales = {'a', 'b', 'c'}
        # Inicializamos una pila vacia, en ella iremos almacenando nuestro afnde por partes
        pila = []
        # Establezco un índice para cada uno de los estados
        i = 1
        sol = AFND_e()
        # Inicializamos el afnde
        sol.__init__()
        epsilon = 'e'

        for caracter in postfijo:
            if caracter in literales:
                # Debo construir el autómata para un literal
                # Agregamos el estado desde el que parte el autómata
                sol.agregar_estado(i)
                i = i + 1
                sol.agregar_estado(i)
                sol.agregar_transicion(i-1,caracter,i)
                pila.append({  
                        "expre_regular" : caracter,
                        "estado_inicial" : i-1,
                        "estado_final": i  
                    })
                i = i + 1
            else:
                # Caso de un operador
                if caracter == '.':
                    # Datos del último elemento
                    tope = pila[-1]
                    final_ultimo = tope["estado_final"]
                    inicio_ultimo = tope["estado_inicial"]
                    ult_afnd = tope["expre_regular"]
                    pila.pop()
                    # Datos del penúltimo elemento
                    tope = pila[-1]
                    inicio_penultimo = tope["estado_inicial"]
                    final_penultimo = tope["estado_final"]
                    ant_afnd = tope["expre_regular"]
                    pila.pop()
                    # Datos del nuevo elemento
                    nuevo_afnd = ant_afnd + caracter + ult_afnd
                    pila.append({  
                        "expre_regular" : nuevo_afnd,
                        "estado_inicial" : inicio_penultimo,
                        "estado_final": final_ultimo  
                    })
                
                    # Agrego nuevas transiciones

                    sol.agregar_transicion(final_penultimo,epsilon,inicio_ultimo)
                elif caracter == '|':
                    # Datos del último elemento
                    tope = pila[-1]
                    final_ultimo = tope["estado_final"]
                    inicio_ultimo = tope["estado_inicial"]
                    ult_afnd = tope["expre_regular"]
                    pila.pop()
                    # Datos del penúltimo elemento
                    tope = pila[-1]
                    inicio_penultimo = tope["estado_inicial"]
                    final_penultimo = tope["estado_final"]
                    ant_afnd = tope["expre_regular"]
                    pila.pop()

                    # Creo un nuevo estado inicial
                    nuevo_inicio = i
                    sol.agregar_estado(nuevo_inicio)
                    i = i + 1
                    # Creo un nuevo estado final
                    nuevo_final = i
                    sol.agregar_estado(nuevo_final)
                    i = i + 1
                    # Datos del nuevo elemento
                    nuevo_afnd = ant_afnd + caracter + ult_afnd
                    pila.append({  
                        "expre_regular" : nuevo_afnd,
                        "estado_inicial" : nuevo_inicio,
                        "estado_final": nuevo_final  
                    })
                
                    # Agrego las nuevas transiciones
                    # Agrego la transicion desde el inicio hacia el ultimo afnd y hacia el penultimo afnd
                    sol.agregar_transicion(nuevo_inicio,epsilon,inicio_ultimo)
                    sol.agregar_transicion(nuevo_inicio,epsilon,inicio_penultimo)
                
                    # Agrego la transicion desde el ultimo afnd y el penultimo afnd hacia el nuevo final
                    sol.agregar_transicion(final_ultimo,epsilon,nuevo_final)
                    sol.agregar_transicion(final_penultimo,epsilon,nuevo_final)
                else:
                    # Operador es *                
                    # Datos del último elemento
                    tope = pila[-1]
                    final_ultimo = tope["estado_final"]
                    inicio_ultimo = tope["estado_inicial"]
                    ult_afnd = tope["expre_regular"]
                    pila.pop() 

                    # Creo un nuevo estado inicial
                    nuevo_inicio = i
                    sol.agregar_estado(nuevo_inicio)
                    i = i + 1
                    # Creo un nuevo estado final
                    nuevo_final = i
                    sol.agregar_estado(nuevo_final)
                    i = i + 1

                    # Datos del nuevo elemento
                    nuevo_afnd = ult_afnd + caracter
                    pila.append({  
                        "expre_regular" : nuevo_afnd,
                        "estado_inicial" : nuevo_inicio,
                        "estado_final": nuevo_final  
                    })
                
                    # Agrego las transiciones desde el nuevo inicio hacia el inicio_ultimo y hacia el nuevo_final
                    sol.agregar_transicion(nuevo_inicio,epsilon,inicio_ultimo)
                    sol.agregar_transicion(nuevo_inicio,epsilon,nuevo_final)

                    # Agrego las transiciones desde final_ultimo hacia el nuevo final y inicio_ultimo
                    sol.agregar_transicion(final_ultimo,epsilon,nuevo_final)
                    sol.agregar_transicion(final_ultimo,epsilon,inicio_ultimo)
        final = pila[-1]["estado_final"]
        inicio = pila[-1]["estado_inicial"]
        sol.establecer_inicial(inicio)
        sol.agregar_final(final)
        #sol.mostrar()
        
        return sol

    postfijo = parse(expr)
    return construir(postfijo)