def sum_numbers(a: int, b: int) -> int:
    """
    Descripcion: Suma dos numeros enteros

    *************************************

    Ejemplo:
        sum_numbers(4,3) -> 7
    *************************************

    Args:
        a (int): el primer sumando.
        b (int): el segundo sumando.
    *************************************

    Valor(es) de retorno:
        devuelve el resultado de la suma
    *************************************

    Efectos Secundarios:
        la suma de dos numeros, no siempre puede ser positiva,
        si existe la presencia de algun negativo
    *************************************

    Excepcion:
        ninguna
    *************************************

    Restricciones de llamada:
        solo puede ser llamada dentro del contexto domain.


    """
    return a + b


def rest_numbers(a: int, b: int) -> int:
    """
    Descripcion: Resta del primer entero, el segundo

    *************************************

    Ejemplo:
        resta(4,1) -> 3
    *************************************

    Args:
        a (int): primer entero.
        b (int): segundo entero.
    *************************************

    Valor(es) de retorno:
        El valor resultante de haber restado el segundo del primero.
    *************************************

    Efectos Secundarios:
        no todas las restas seran positivas,
        sobre todo cuando el segundo es mas grande que el primero.
    *************************************

    Excepcion:
        ninguna.
    *************************************

    Restricciones de llamada:
        solo aplica para ser llamada en el contexto domain.


    """
    return a - b
