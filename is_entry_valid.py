# – is_entry_valid(expr): 
# que verifique si la expresión regular dada cumple con las restricciones definidas. 
# Para eso también deberán corroborar que la expresión regular de entrada
# usa solamente los símbolos válidos ("a","b","c", "e", "*", "|", ".") y 
# no contiene ningún paréntesis u otro símbolo. 
# La salida de esta función será un booleano:
# "True" si la expresión regular dada en la entrada cumple con estas restricciones; 
# "False" en caso contrario.

import re

def is_entry_valid(expr):
    caracteres_validos = "abc*|.e"

    # Verifica que solo tenga caracteres válidos
    if any(char not in caracteres_validos for char in expr):
        return False
    
    # Verifico que las los operadores esten bien usados
    # 1) * -> "abc"* 
    # 2) | -> "abce"|"abce" 
    # 3) . -> "abce"."abce"


    # <------------------------------->
    # <---|CASOS INVÁLIDOS PARA 1)|--->
    # <------------------------------->

    # a) `*` al inicio
    if expr.startswith('*'):
        return False

    # b) `*` después de otro `*`
    if "**" in expr:
        return False

    # c) `*` después de `|` o `.`
    if re.search(r"[|.]\*", expr):
        return False

    # d) `*` después de `e`
    if re.search(r"e\*", expr):
        return False
    

    # <------------------------------->
    # <---|CASOS INVÁLIDOS PARA 2)|--->
    # <------------------------------->

    # a) `|` al inicio o al final
    if expr.startswith('|') or expr.endswith('|'):
        return False

    # b) `|` después de otro `|`
    if "||" in expr:
        return False

    # c) `|` después de `.`
    if re.search(r"\.[|]", expr):
        return False


    # <------------------------------->
    # <---|CASOS INVÁLIDOS PARA 3)|--->
    # <------------------------------->

    # a) `.` al inicio o al final
    if expr.startswith('.') or expr.endswith('.'):
        return False

    # b) `.` después de otro `.`
    if ".." in expr:
        return False

    # c) `.` después de `|`
    if re.search(r"\|[.]", expr):
        return False
    
    return True