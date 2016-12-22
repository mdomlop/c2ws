#!/usr/bin/python3
# c2ws.py: Convierte un color al más proximo en Web Safe
# v1: mié ene 15 13:06:18 CET 2014
# TODO: Permitir modelos de color hsv, cmyk, hsl, ryb, etc...
# http://es.wikipedia.org/wiki/Modelo_de_color_HSV
# http://www.easyrgb.com/index.php?X=MATH
# BUGS: No siempre se obtiene un tono similar:
#	012345 (azul) > 003333 (verde)

import sys
import argparse

# El modo por defecto de entrada y salida:
defintro = 'hex'
defout = 'hex'

parser = argparse.ArgumentParser()
parser.add_argument('color', nargs='+', type=str,
    help='La lista de colores a convertir')
parser.add_argument('-v', '--verbose', action='store_true',
    help='Incrementa el nivel de verbosidad')
parser.add_argument('-i', '--intro', default=defintro,
    help='Indica que la entrada está en modo: (hex, rgb, nat)')
parser.add_argument('-o', '--out', default=defout,
    help='Produce los resultados según el modo (hex, rgb, nat)')

args = parser.parse_args()


def nextcolor(c, p):
    """ Retorna el color más próximo a "c" dentro de la paleta "p" """
    """ Almacenamos las distancias entre cada tono permitido en la
    paleta y el color especificado. La distancia más corta pertenecerá
    al color más próximo en la paleta """

    # Almacena las diferencias en la lista dif
    i = 0
    dif = list(range(len(p)))
    for shape in p:
        dif[i] = abs(shape - c)  # 244 - 4 == 4 - 244 == 240
        i = i + 1

    # Busca la diferencia más pequeña y la asigna a nextc
    """ La diferencia mínima se establece inicialmente 0xff y se le irá
    asignando cada vez valores más pequeños. No puede existir una diferencia
    mayor debido a que "c" ha sido evaluado previamente """
    mindif = 0xff
    for j in range(len(dif)):
        if mindif > dif[j]:
            mindif = dif[j]
            """ El índice de la diferencia menor corresponde al
            del color en la paleta """
            nextc = p[j]
    return nextc


def colorfilter(px):
    """ Recibe una lista (r, g, b) y le aplica el filtro nextcolor()"""

    # Estos son los únicos colores válidos para rojo, verde o azul:
    palette = (0x00, 0x33, 0x66, 0x99, 0xcc, 0xff)

    # Se asignan colores individualmente:
    r = nextcolor(px[0], palette)
    g = nextcolor(px[1], palette)
    b = nextcolor(px[2], palette)

    rgb = (r, g, b)
    hx = '%02x%02x%02x' % rgb
    natural = int(hx, 16)

    return(hx, rgb, natural)


def valn(n, m):
    """ Valida un número "n" según el modo "m" """

    # Establece variables según el modo
    if m == 'hex':
        base = 16
        mini = 0x0
        maxi = 0xffffff
    elif m == 'rgb':
        base = 10
        mini = 0x0
        maxi = 0xff
    elif m == 'nat':
        base = 10
        mini = 0x0
        maxi = 0xffffff
    else:
        # Nunca debería llegar a ejecutarse:
        print('ALGO HAS HECHO MAL. No conozco el modo', m, file=sys.stderr)
        sys.exit(1)

    # Evalúa si el número n pertenece a la base:
    try:
        n = int(n, base)
    except ValueError:
        print('El número', n, 'no es válido para "' + m + '"',
        file=sys.stderr)
        sys.exit(1)

    # Evalúa si el número n está dentro del rango permitido para su modo
    if (n > maxi) or (n < mini):
        if m == 'hex':  # Para hacer el mensaje de error coherente con hex
            n = hex(n)
            mini = hex(0x0)
            maxi = hex(0xffffff)

        print('El número', n,
        'está fuera del rango permitido para "' + m + '": (',
        mini, '..', maxi, ')',
        file=sys.stderr)
        sys.exit(1)


def hex2rgb(n):
    """ Toma un hex y devuelve rgb: c8 > 0000c8 > (00, 00, 200) """
    valn(n, 'hex')
    n = int(n, 16)  # 200
    n = '%06x' % n  # 0000c8
    return tuple(bytes.fromhex(n))


def nat2rgb(n):
    """ Toma un nat y devuelve rgb: 200 > 0000c8 > (00, 00, 200) """
    valn(n, 'nat')
    n = '%06x' % int(n)  # 0000c8
    return tuple(bytes.fromhex(n))


def rgb2rgb(n):
    """ Toma una cadena rgb y devuelve rgb: '00 00 200' > (00, 00, 200) """
    n = n.split(' ')
    nc = len(n)
    if nc == 3:  # Debe ser 3 (r, g, b)
        for i in range(nc):
            valn(n[i], 'rgb')
            n[i] = '%03i' % int(n[i])  # 0 00 200 > 000 000 200
            n[i] = int(n[i])  # Convertimos la cadena a entero
        return n
    else:
        print('La cantidad de colores del "rgb" no es 3:', n,
        file=sys.stderr)
        sys.exit(1)


def intro2rgb(t):
    """ Devuelve (r, g, b) sin formatear de una entrada hex, nat o rgb """
    if args.intro == 'hex':
        out = hex2rgb(t)
    elif args.intro == 'rgb':
        out = rgb2rgb(t)
    elif args.intro == 'nat':
        out = nat2rgb(t)
    else:
        print('No conozco el formato de entrada:', args.intro,
        file=sys.stderr)
        sys.exit(1)
    return out


def printout():
    """ Imprime la salida según el formato fout.
    fout es el índice de la lista devuelta por colorfilter """
    if args.out == 'hex':
        fout = 0
    elif args.out == 'rgb':
        fout = 1
    elif args.out == 'nat':
        fout = 2
    else:
        print('No conozco el formato de salida:', args.out,
        file=sys.stderr)
        sys.exit(1)

    for c in args.color:  # Se procesan todos los colores indicados
        c = c.lower()
        fc = intro2rgb(c)  # fc es c en formato (r, g, b)
        ws = colorfilter(fc)[fout]  # El color procesado y formateado

        if args.verbose:
            print (c, '=>', ws)
        else:
            print (ws)


printout()
