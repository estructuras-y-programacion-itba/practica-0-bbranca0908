import random
import csv
import os

# -----------------------------
# Datos del juego
# -----------------------------
CATEGORIAS = ["E", "F", "P", "G", "1", "2", "3", "4", "5", "6"]

# Devuelve una lista de longitud 'cantidad' con números al azar del 1 al 6
def tirar_dados(cantidad):
    return [random.randint(1, 6) for i in range(cantidad)]

def mostrar_dados(dados):
    print("\nDados actuales:")
    for i, valor in enumerate(dados, start=1):
        print(f"  {i}: [{valor}]")

#   ENUMERATE:
#   i = 0
#    for valor in cantidad:
#    print(i, valor)
#    i += 1

# Pide dados a retirar
def dados_a_retirar():
    texto = input("\nEscribí los dados que deseas volver a tirar (ej: 1 3 5) o presioná ENTER para quedarte con todos: ").strip() # Elimina espacios en blanco al inicio y al final
    if texto == "":
        return []

    partes = texto.split() # Convierte a lista 
    posiciones = []
    for p in partes:
        if p.isdigit():
            num = int(p)
            if 1 <= num <= 5:
                posiciones.append(num - 1)  # Quiero el índice y este comienza en 0

    posiciones = list(set(posiciones)) # Elimino duplicados
    posiciones.sort() # Ordeno de menor a mayor
    return posiciones # Devuelve los índices de los dados que quiero volver a tirar, si quiero tirar el primer dado devuelve ['0']

# -----------------------------
# Reglas para detectar jugadas
# -----------------------------
def es_generala(dados):
    primero = dados[0]
    for d in dados:
        if d != primero:
            return False
    return True

def es_poker(dados):
    for numero in range(1, 7):
        if dados.count(numero) == 4:
            return True
    return False

# def es_poker(dados):
#     for dado in dados:
#         contador = 0
#         for i in dados:
#             if dado == i:
#                 contador += 1
#         if contador == 4:
#             return True
#     return False
        
def es_full(dados):
    for numero in range(1, 7):
        if dados.count(numero) == 3:
            # encontre el trío, ahora buscao el par
            for otro in range(1, 7):
                if otro != numero and dados.count(otro) == 2:
                    return True
    return False

def es_escalera(dados):
    ordenados = sorted(dados)
    return ordenados == [1, 2, 3, 4, 5] or ordenados == [2, 3, 4, 5, 6]

# -----------------------------
# Puntajes
# -----------------------------
def puntajes_posibles(dados, primera_tirada):
    posibles = {}

    # Jugadas especiales
    if es_escalera(dados):
        puntos = 20 + (5 if primera_tirada else 0)
        posibles["E"] = puntos

    if es_full(dados):
        puntos = 30 + (5 if primera_tirada else 0)
        posibles["F"] = puntos

    if es_poker(dados):
        puntos = 40 + (5 if primera_tirada else 0)
        posibles["P"] = puntos

    if es_generala(dados):
        posibles["G"] = 50

    # Categorías numéricas
    for n in range(1, 7):
        if dados.count(n) > 0:
            posibles[str(n)] = n * dados.count(n)

    return posibles

# -----------------------------
# Planilla y CSV
# -----------------------------
def crear_planilla():
    planilla = {}
    for c in CATEGORIAS:
        planilla[c] = [None, None] # Un None por jugador
    return planilla


def guardar_csv(planilla, nombre_archivo="jugadas.csv"):

    existe = os.path.exists(nombre_archivo) # Chequeo si el archivo existe

    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["jugada", "j1", "j2"])

        for cat in CATEGORIAS:
            if planilla[cat][0] is None:
                j1 = ""
            else:
                j1 = planilla[cat][0]

            if planilla[cat][1] is None:
                j2 = ""
            else:
                j2 = planilla[cat][1]

            writer.writerow([cat, j1, j2])

    if not existe:
        print(f"\nSe creó el archivo {nombre_archivo}.")
    else:
        print(f"\nSe actualizó el archivo {nombre_archivo}.")


def mostrar_planilla(planilla):
    print("\nPLANILLA")
    print("Categoria | J1 | J2")
    print("--------------------")
    for cat in CATEGORIAS:
        if planilla[cat][0] is None:
            j1 = ""
        else:
            j1 = planilla[cat][0]

        if planilla[cat][1] is None:
            j2 = ""
        else:
            j2 = planilla[cat][1]

        print(f"{cat:>8} | {str(j1):>2} | {str(j2):>2}") # Alineación

# Devuelvo lista de categorías aún no usadas por ese jugador.
def categorias_disponibles(planilla, jugador_idx):
    disp = []
    for cat in CATEGORIAS:
        if planilla[cat][jugador_idx] is None:
            disp.append(cat)
    return disp


def planilla_completa(planilla):
    for cat in CATEGORIAS:
        if planilla[cat][0] is None or planilla[cat][1] is None:
            return False
    return True # True si ambos jugadores completaron todas las categorías.


def total_jugador(planilla, jugador_idx):
    total = 0
    for cat in CATEGORIAS:
        val = planilla[cat][jugador_idx]
        if val is not None:
            total += val
    return total

# -----------------------------
# Turno
# -----------------------------

def elegir_categoria_para_anotar(planilla, jugador_idx, posibles):
    disponibles = categorias_disponibles(planilla, jugador_idx)
    validas = [c for c in disponibles if c in posibles]

    print("\nCategorías disponibles:", ", ".join(disponibles))

    if len(validas) > 0:
        print("Jugadas válidas que podés anotar ahora:")
        for c in validas:
            print(f"  - {c}: {posibles[c]} puntos")
    else:
        print("No tenés jugadas válidas. Tenés que elegir una categoría y anotar 0.")

    while True:
        cat = input("Elegí una categoría: ").strip().upper()
        if cat in disponibles:
            if cat in posibles:
                return cat, posibles[cat]
            else:
                return cat, 0
        else:
            print("Esa categoría no está disponible. Probá de nuevo.")


def jugar_turno(planilla, jugador_idx, nombre_jugador):
    print(f"\n==============================")
    print(f"Turno de {nombre_jugador}")
    print(f"==============================")

    dados = tirar_dados(5)
    termino_en_primera = True  # Asumo que terminó en la primera tirada

    for numero_tirada in range(1, 4):
        print(f"\nTirada #{numero_tirada}")
        mostrar_dados(dados)

        # Generala Real: generala en la primera tirada
        if numero_tirada == 1 and es_generala(dados):
            print("\n¡GENERALA REAL!")
            if planilla["G"][jugador_idx] is None:
                planilla["G"][jugador_idx] = 80  # 50 + 30 de bonus
            return True  # victoria inmediata

        # En la tercera tirada no se puede volver a tirar
        if numero_tirada == 3:
            break

        posiciones = dados_a_retirar()

        # Si no quiere re-tirar ningún dado, termina el turno
        if len(posiciones) == 0:
            break

        # Re-tira los dados elegidos
        for idx in posiciones:
            dados[idx] = random.randint(1, 6)

        termino_en_primera = False  # re-tiró dados, ya no es primera tirada

    # Calcula los puntajes posibles según si terminó en la primera tirada o no
    posibles = puntajes_posibles(dados, primera_tirada=termino_en_primera)

    cat, puntos = elegir_categoria_para_anotar(planilla, jugador_idx, posibles)
    planilla[cat][jugador_idx] = puntos

    print(f"\nAnotaste {puntos} puntos en {cat}.")
    return False

# -----------------------------
# Juego completo
# -----------------------------
def jugar():
    planilla = crear_planilla()
    nombres = ["Jugador 1", "Jugador 2"]

    # Guardo el CSV inicial
    guardar_csv(planilla)
    mostrar_planilla(planilla)

    jugador_actual = 0

    while True:
        # Juega un turno
        generala_real = jugar_turno(planilla, jugador_actual, nombres[jugador_actual])

        guardar_csv(planilla)
        mostrar_planilla(planilla)

        if generala_real:
            print(f"\n{nombres[jugador_actual]} ganó por Generala Real. Fin del juego.")
            break

        if planilla_completa(planilla):
            print("\nAmbos jugadores completaron todas las categorías. Fin del juego.")
            break

        # Cambio de jugador
        jugador_actual = 1 - jugador_actual

    # Resultado final
    t1 = total_jugador(planilla, 0)
    t2 = total_jugador(planilla, 1)

    print("\n==============================")
    print("RESULTADO FINAL")
    print("==============================")
    print(f"Total Jugador 1: {t1}")
    print(f"Total Jugador 2: {t2}")

    if t1 > t2:
        print("Ganó el Jugador 1.")
    elif t2 > t1:
        print("Ganó el Jugador 2.")
    else:
        print("Empate.")

if __name__ == "__main__":
    jugar()


