from collections import defaultdict, deque
from itertools import permutations


class AFND_e:
    def __init__(self):
        self.estados = set()
        self.inicial = None
        self.finales = set()
        self.transiciones = defaultdict(lambda: defaultdict(set))

    def agregar_estado(self, nombre_estado):
        self.estados.add(nombre_estado)

    def establecer_inicial(self, nombre_estado):
        self.agregar_estado(nombre_estado)
        self.inicial = nombre_estado

    def agregar_final(self, nombre_estado):
        self.agregar_estado(nombre_estado)
        self.finales.add(nombre_estado)

    def agregar_transicion(self, desde, simbolo, hacia):
        self.agregar_estado(desde)
        self.agregar_estado(hacia)
        self.transiciones[desde][simbolo].add(hacia)

    def mostrar(self):
        print(f"Estado inicial: {self.inicial}")
        print(f"Estados finales: {self.finales}")
        print("Transiciones:")
        for desde in self.transiciones:
            for simbolo in self.transiciones[desde]:
                for hacia in self.transiciones[desde][simbolo]:
                    print(f"  {desde} --{simbolo}--> {hacia}")

    @staticmethod
    def son_isomorfos(afnd1, afnd2):
        if len(afnd1.estados) != len(afnd2.estados):
            return False
        if len(afnd1.finales) != len(afnd2.finales):
            return False
        if afnd1.inicial is None or afnd2.inicial is None:
            return False

        mapeo = {}
        visitados = set()
        cola = deque([(afnd1.inicial, afnd2.inicial)])
        mapeo[afnd1.inicial] = afnd2.inicial

        while cola:
            e1, e2 = cola.popleft()
            if (e1 in afnd1.finales) != (e2 in afnd2.finales):
                return False
            visitados.add((e1, e2))

            trans1 = afnd1.transiciones.get(e1, {})
            trans2 = afnd2.transiciones.get(e2, {})

            if set(trans1.keys()) != set(trans2.keys()):
                return AFND_e.son_isomorfos_extended(afnd1, afnd2)

            for simbolo in trans1:
                destinos1 = sorted(trans1[simbolo])
                destinos2 = sorted(trans2[simbolo])

                if len(destinos1) != len(destinos2):
                    return False

                for d1, d2 in zip(destinos1, destinos2):
                    if d1 in mapeo:
                        if mapeo[d1] != d2:
                            return False
                    else:
                        mapeo[d1] = d2
                        if (d1, d2) not in visitados:
                            cola.append((d1, d2))

        return True

    @staticmethod
    def son_isomorfos_extended(afnd1, afnd2):
        if len(afnd1.estados) != len(afnd2.estados):
            return False
        if len(afnd1.finales) != len(afnd2.finales):
            return False

        estados1 = list(afnd1.estados)
        estados2 = list(afnd2.estados)

        for perm in permutations(estados2):
            mapping = dict(zip(estados1, perm))

            if mapping[afnd1.inicial] != afnd2.inicial:
                continue

            finales_mapeados = {mapping[f] for f in afnd1.finales}
            if finales_mapeados != set(afnd2.finales):
                continue

            match = True
            for estado1 in afnd1.transiciones:
                trans1 = afnd1.transiciones[estado1]
                estado2 = mapping[estado1]
                trans2 = afnd2.transiciones.get(estado2, {})

                if set(trans1.keys()) != set(trans2.keys()):
                    match = False
                    break

                for simbolo in trans1:
                    destinos1 = {mapping[d] for d in trans1[simbolo]}
                    destinos2 = set(trans2.get(simbolo, []))
                    if destinos1 != destinos2:
                        match = False
                        break

                if not match:
                    break

            if match:
                return True

        return False
