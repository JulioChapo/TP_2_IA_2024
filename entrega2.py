from simpleai.search import (CspProblem,
                             backtrack,
                             min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             HIGHEST_DEGREE_VARIABLE,
                             LEAST_CONSTRAINING_VALUE)
from itertools import combinations, permutations, product

FRASCOS = ()
DOMINIOS = {}


def cantidad_color(variables, values):
    # Debe haber 4 porciones de color entre todos los frascos
    dictionary = {}

    for contenido in values:
        for color in contenido:
            if color in dictionary:
                dictionary[color] += 1
            else:
                dictionary[color] = 1

    for key, value in dictionary.items():
        if value != 4:
            return False
    return True


def color_al_fondo(variables, values):
    # Ningun color puede comenzar con todos sus segmentos en el fondo
    dictionary = {}
    for frasco in variables:
        if values[frasco][0] in dictionary:
            dictionary[values[frasco][0]] += 1
        else:
            dictionary[values[frasco][0]] = 1

    for key, value in dictionary.items():
        if value == 4:
            return False
    return True


def frascos_ady(variables, values):
    # Si dos frascos son adyacentes, deben compartir al menos un color
    colores1, colores2 = values
    return any(color in colores1 for color in colores2)


def frascos_ady_colores_dif(variables, values):
    # No puede haber mas de 6 colores diferentes entre frascos adyacentes
    colores1, colores2 = values
    return len(set(list(colores1)+list(colores2))) <= 6


def frascos_iguales(variables, values):
    # No puede haber dos frascos exactante iguales
    val1, val2 = values
    return val1 != val2


def generar_restricciones(FRASCOS):
    # Generamos la lista de restricciones para el problema
    # Revisar las restricciones, pq no se bien que valores debe tomar
    restricciones = []

    restricciones.append((FRASCOS, color_al_fondo))
    restricciones.append((FRASCOS, cantidad_color))

    for x in range(len(FRASCOS)-1):
        restricciones.append(((FRASCOS[x], FRASCOS[x+1]), frascos_ady))
        restricciones.append(((FRASCOS[x], FRASCOS[x+1]), frascos_ady_colores_dif))

    for variable1, variable2 in combinations(FRASCOS, 2):
        restricciones.append(((variable1, variable2), frascos_iguales))

    return restricciones


def generar_frascos(colores):
    # Creamos los frascos, de 0 a n, debe haber 1 frasco por color
    frascos = []
    for n in range(len(colores)):
        frascos.append(n)

    return frascos


def generar_dominios(frascos, colores, contenido_parcial):
    # Creo las posibles combinaciones de colores y las agrego al dominio de los frascos
    posibilidades = []
    for posibilidad in product(colores, repeat=4):
        if len(set(posibilidad)) != 1:
            posibilidades.append(posibilidad)
    # Genera las posibles combinaciones de 4 colores
    # Cumple la rest de un frasco de 4 segmentos, y que no este resuelto

    for frasco in frascos:
        DOMINIOS[frasco] = posibilidades

    # El contenido parcial es parte del dominio
    for n, contenido in enumerate(contenido_parcial):
        lista_parcial = []
        for extension in product(colores, repeat=4 - len(contenido)):
            lista_parcial.append(list(contenido) + list(extension))
        DOMINIOS[n] = tuple(map(tuple, lista_parcial))

    return DOMINIOS


def armar_nivel(colores, contenidos_parciales):
    FRASCOS = tuple(generar_frascos(colores))
    DOMINIOS = generar_dominios(FRASCOS, colores, contenidos_parciales)

    restricciones = generar_restricciones(FRASCOS)

    problem = CspProblem(FRASCOS, DOMINIOS, restricciones)
    solution = tuple(min_conflicts(problem).values())

    return solution

if __name__ == "__main__":
    # "RVACLNMO", ["ROOO", "CAA", "NOVA", "MM", "C"]
    colores = ("rojo", "verde", "azul", "celeste", "lila", "naranja", "morado", "verde_oscuro")
    contenidos_parciales = (('rojo', 'verde_oscuro', 'verde_oscuro', 'verde_oscuro'),
                            ('celeste', 'azul', 'azul'),
                            ('naranja', 'verde_oscuro', 'verde', 'azul'),
                            ('amarillo', 'amarillo'), ('celeste',))

    solucion = armar_nivel(colores, contenidos_parciales)
    print("solucion:")
    print(solucion)
