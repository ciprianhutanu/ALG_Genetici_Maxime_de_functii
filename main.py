import math
import random
import numpy as np

from decimal import Decimal, getcontext

fisierOUTPUT = open('Evolutie.txt', 'w')

def binarySearch(value, left, right, vect):
    if left == right:
        # print(left, right, vect[left])
        return right
    middle = (left + right) // 2
    if value < vect[middle]:
        return binarySearch(value, left, middle - 1, vect)
    else:
        return binarySearch(value, middle + 1, right, vect)


def codificare(com, num):
    global a, lungime, precizie, d, valuesTO
    getcontext().prec = precizie

    result = False

    if com == "TO":
        number = float(num)
        j = binarySearch(number, 0, 2 ** lungime - 1, valuesTO)
        # print(j)
        result = bin(j)[2:].zfill(lungime)
    elif com == "FROM":
        number = int(num, 2)
        aux = Decimal(number) * Decimal(d) + Decimal(a)
        result = str(aux)
    return result


def selectie(pop, intervaleSelectie):
    global dimensiunePopulatie

    result = []

    if primaAfisare:
        print("\nSelectam:", file=fisierOUTPUT)

    for i in range(dimensiunePopulatie):
        norocos = np.random.uniform(0, 1)
        j = 0
        while norocos > intervaleSelectie[j]:
            j += 1
        result.append(pop[j - 1])

        if primaAfisare:
            print(f"u = {norocos} selectam cromozomul {j}", file=fisierOUTPUT)

    return result



def incrucisare(pop, prob):
    global lungime, primaAfisare
    incr = False

    for i in range(len(pop)):
        norocos = np.random.uniform(0, 1)
        if norocos <= prob:
            if not incr:
                incr = i
            else:
                if primaAfisare:
                    print(f"Recombinare dintre cromozomul {incr} si cromozomul {i}:", file=fisierOUTPUT)

                u = np.random.randint(0, lungime)

                if primaAfisare:
                    print(f"{pop[incr]} {pop[i]} punct {u}", file=fisierOUTPUT)

                aux1 = pop[incr][:u] + pop[i][u:]
                aux2 = pop[i][:u] + pop[incr][u:]
                pop[incr] = aux2
                pop[i] = aux1

                if primaAfisare:
                    print(f"Rezultat\t {aux2} {aux1}", file=fisierOUTPUT)

                incr = False


def mutatie(pop, prob):
    global lungime, primaAfisare

    if primaAfisare:
        print(f"\nProbilitatea de mutatie pentru fiecare gena {prob}", file=fisierOUTPUT)
        print("Au fost modificati cromozomii: ", file=fisierOUTPUT)

    for i in range(len(pop)):
        norocos = np.random.uniform(0, 1)
        if norocos <= prob:

            if primaAfisare:
                print(i + 1, file=fisierOUTPUT)

            poz = np.random.randint(0, lungime)
            pop[i] = pop[i][:poz] + opus(pop[i][poz]) + pop[i][poz+1:]


def opus(bit):
    if bit == "1":
        return "0"
    return "1"


def afisarePopulatie(populatie, f):
    for i, crom in enumerate(populatie):
        x = codificare('FROM', crom)
        print(f"{i + 1}:\t{crom} x = {x} f = {f(float(x))}", file=fisierOUTPUT)


dimensiunePopulatie = 20  # dimensiunea populatiei
a, b = -1, 2  # capetele intervalului
param = [-1, 1, 2]  # paramentrii functiei
precizie = 6  # precizia intervalului
probRecombinare = 0.25  # probabilitate recombinare
probMutatie = 0.1  # probabilitate mutatie
etape = 50  # numarul de etape ale algoritmului

primaAfisare = True

f = lambda x: param[0] * (x ** 2) + param[1] * x + param[2]

lungime = math.ceil(math.log((b - a) * (10 ** precizie), 2))  # lungimea cromozomilor
d = (b - a) / (2 ** lungime)  # dimensiunea

valuesTO = [a + i * d for i in range(2 ** lungime - 1)]

pop = [codificare("TO", np.random.uniform(a, b)) for _ in range(dimensiunePopulatie)]

maxime = []
index = 1

while etape >= index:
    valoareMax = False

    print(f"\nEtapa {index}:", file=fisierOUTPUT)
    afisarePopulatie(pop, f)

    valoriFunctie = [f(float(codificare("FROM", crom))) for crom in pop]

    for val in valoriFunctie:
        if val > valoareMax or valoareMax == False:
            valoareMax = val
    maxime.append(valoareMax)

    sumValFunc = np.sum(valoriFunctie)
    probSelectie = [val / sumValFunc for val in valoriFunctie]
    intervaleSelectie = [np.sum(probSelectie[:i]) for i in range(dimensiunePopulatie + 1)]

    if primaAfisare:
        print("\nProbabilitati selectie", file=fisierOUTPUT)
        for i, prob in enumerate(probSelectie):
            print(f"cromozom\t {i+1}\t probabilitate {prob}", file=fisierOUTPUT)

        print("\nIntervalele de selectie:\n", *intervaleSelectie, file=fisierOUTPUT)

    nouaPop = selectie(pop, intervaleSelectie)

    if primaAfisare:
        print("\nDupa selectie:", file=fisierOUTPUT)
        afisarePopulatie(nouaPop,f)

    if primaAfisare:
        print(f"\nProbabilitatea de incrucisare este: {probRecombinare}", file=fisierOUTPUT)

    incrucisare(nouaPop, probRecombinare)

    if primaAfisare:
        print("\nDupa incrucisare:", file=fisierOUTPUT)
        afisarePopulatie(nouaPop, f)

    mutatie(nouaPop, probMutatie)

    if primaAfisare:
        print("\nDupa mutatie:", file=fisierOUTPUT)
        afisarePopulatie(nouaPop, f)
        primaAfisare = False

    pop = nouaPop
    index += 1

print("\nEvolutie maxime:", file=fisierOUTPUT)
print(*maxime,sep='\n', file=fisierOUTPUT)

fisierOUTPUT.close()
