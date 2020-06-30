#Importamos las librerias necesarias
import math
import multiprocessing
import random
import sys
import time

#Creamos variables globales de usuario y contraeña
usuario = '21838473@live.uem.es'
contrasena = '123'

#############################################################################################################  MERGE

#Función para la realización del merge
def merge(*args):
    left, right = args[0] if len(args) == 1 else args
    left_length, right_length = len(left), len(right)
    left_index, right_index = 0, 0
    merged = []

    while left_index < left_length and right_index < right_length:
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1
    if left_index == left_length:
        merged.extend(right[right_index:])
    else:
        merged.extend(left[left_index:])
    return merged

#Funcion para la ordenación mergesort
def mergesort(data):
    length = len(data)

    if length <= 1:
        return data

    middle = length // 2
    left = mergesort(data[:middle])
    right = mergesort(data[middle:])
    return merge(left, right)

#Funcion para la paralelización del mergesort entre los diferentes nucleos de la cpu
def mergesortparl(data):

    #Haciendo uso del metodo pool, almacenamos los procesos en ejecucion. ividimos el array en partes iguales en funcion del numero de procesos.
    processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=processes)
    tam = int(math.ceil(float(len(data)) / processes))
    data = [data[i * tam:(i + 1) * tam] for i in range(processes)]
    data = pool.map(mergesort, data)

    #Ordenamos todas las particiones en una sola, obteniendo asi el arrayfinalado ordenado
    while len(data) > 1:
        #Cuando las aprticiones son impares realizamos "pop" de la ultima y la incluimos despues de un recorrido del bucle
        extra = data.pop() if len(data) % 2 == 1 else None
        data = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]
        data = pool.map(merge, data) + ([extra] if extra else [])
    return data[0]

#############################################################################################################  FIBO

#Función para el calculo de fibonacci de manera secuencial
def fibo(n):
    #Inicializamos los dos primeros valores a 0 y 1 para iniciar la secuencia
    a = 0
    b = 1

    if n < 0:
        print("No has introducido un valor válido...")
    elif n == 0:
        return a
    elif n == 1:
        return b
    else:
        for i in range(1, n):
            c = a + b
            a = b
            b = c
        return b

#Funcion paralela para dividir las distribuciont entre los nucleos de la cpu
def fiboparl(n):

    #Miramos los cores de nuestra maquina
    n_cores = multiprocessing.cpu_count()  
    print('Numero de cores del pc: ', n_cores)

    #Ya que fibonacci es secuencial divido la carga de trabajo haciendo semi-sumas de las partes que asigno a cada core (en mi caso 8 cores)
    #Decomponemos las secuencias en los distintos cores del ordenador
    distribuciont = [n - 3, n - 4, n - 4, n - 5, n - 4, n - 5, n - 5, n - 6] 
    arrayfinal = multiprocessing.RawArray('d', n_cores)
    cores = []

    for core in range(n_cores):
        cores.append(
            multiprocessing.Process(target=coredistrib, args=(core, distribuciont[core], arrayfinal)))
    for core in cores:
        #Haciendo uso del metodo star inicio la carga de los trabajos para cada uno de los cores de mi cpu
        core.start()
    for core in cores:
        #Mediante el uso del metodo join se bloquean los hilos hasta que terminan su tarea todos los cores
        core.join()
    #Inicializo la secuencia a 0 para poder iniciar el algoritmo
    fibo = 0
    for sum in arrayfinal:
        fibo += sum
    return fibo

#Funcion paralela para distribuir las distribuciont mediante la llamada a la funcion fibo secuencial 
def coredistrib(indice, tarea, arrayfinal):
    Fib = fibo(tarea)
    arrayfinal[indice] = Fib

#Función para la eleccion del usuario de la opcion deseada
def menu():
    choice = '0'
    bool = False

    while bool != True:
        print("|------------------------------------------------------------|")
        print("|    ****** UNIVERSIDAD EUROPEA DE MADRID ******             |")
        print("|    Escuela de Arquitectura, Ingenieria y Disenio           |")
        print("|            Arturo Alba Sanchez-Mayoral                     |")
        print("|                                                            |")
        print("|    A: MergeSort                                            |")
        print("|    B: Fibonacci                                            |")
        print("|    S: SALIR                                                |")
        print("|------------------------------------------------------------|")
        choice = input("\nIntroduzca su opcion: ")

        if choice == "S" or choice == "s":
            print("\nGracias por usar nuestra aplicacion")
            bool = True

        elif choice == "A" or choice == "a":
            
            #El tamaño del array sera el numero de expediente
            tam = 21838473
            data_unsorted = [random.randint(0, tam) for _ in range(tam)]

            for sort in mergesort, mergesortparl:
                start = time.time()
                data_sorted = sort(data_unsorted)
                end = time.time() - start
                print("El array ha sido ordenado gracias a", sort.__name__, "en", end, "segundos",
                      "y su correccion del orden es: ", sorted(data_unsorted) == data_sorted)

            print("El array que resulta, desordenado es:", data_unsorted)
            print("El array que resulta, ordenado es", data_sorted)

        elif choice == "B" or choice == "b":
            n = int(input("Introduzca el numero que desee: "))
            inicioS = time.time()
            print('Fibonacci de manera secuencial: ')
            print(fibo(n))  
            finS = time.time()
            inicioP = time.time()
            print('Fibonacci de manera paralela: ')
            print(fiboparl(n))  
            finP = time.time()
            print('El tiempo de ejecución de manera secuencial ha sido: ', finS - inicioS)
            print('El tiempo de ejecución de manera paralela ha sido: ', finP - inicioP)

        else:
            print("\nTiene que seleccionar A o B...")

#Main
if __name__ == "__main__":
    fin = False
    while (fin == False):
        u = input("\nIntroduzca su correo de la universidad: ")
        p = input("\nIntroduzca su contrasena: ")
        if usuario == u and contrasena == p:
            print("\nLogin realizado correctamente")
            fin = True
            menu()
        else:
            print("\nError al realizar el login")
