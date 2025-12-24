#codidgo hecho por Nocturne Github: https://github.com/nocturne-cybersecurity

import secrets
import string
import argparse
import pyperclip
import sys
import time
from typing import List
from ascii import mostrar_banner, mostrar_llave, mostrar_estadisticas, mostrar_exito, mostrar_error

def generar_contraseña(
    longitud: int = 16,
    usar_mayusculas: bool = True,
    usar_minusculas: bool = True,
    usar_numeros: bool = True,
    usar_especiales: bool = True,
    excluir_ambiguos: bool = True
) -> str:
    if longitud < 12:
        raise ValueError("La longitud mínima debe ser 12 caracteres")
    
    if not any([usar_mayusculas, usar_minusculas, usar_numeros, usar_especiales]):
        raise ValueError("Debe habilitar al menos un tipo de caracteres")
    
    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    numeros = string.digits
    especiales_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?'
    
    ambiguos = 'l1I0O'
    
    caracteres = ''
    if usar_minusculas:
        caracteres += minusculas
    if usar_mayusculas:
        caracteres += mayusculas
    if usar_numeros:
        caracteres += numeros
    if usar_especiales:
        caracteres += especiales_chars
    
    if excluir_ambiguos:
        caracteres = ''.join(c for c in caracteres if c not in ambiguos)
    
    password = []
    
    if usar_minusculas:
        password.append(secrets.choice([c for c in minusculas if c not in ambiguos or not excluir_ambiguos]))
    if usar_mayusculas:
        password.append(secrets.choice([c for c in mayusculas if c not in ambiguos or not excluir_ambiguos]))
    if usar_numeros:
        password.append(secrets.choice([c for c in numeros if c not in ambiguos or not excluir_ambiguos]))
    if usar_especiales:
        password.append(secrets.choice(especiales_chars))
    
    while len(password) < longitud:
        password.append(secrets.choice(caracteres))
    
    secrets.SystemRandom().shuffle(password)
    
    return ''.join(password)

def calcular_entropia(contraseña: str) -> float:
    import math
    from collections import Counter
    
    frecuencias = Counter(contraseña)
    longitud = len(contraseña)
    
    entropia = 0
    for count in frecuencias.values():
        p = count / longitud
        entropia -= p * math.log2(p)
    
    return entropia * longitud

def mostrar_ayuda():
    print("\nGenerador de Contraseñas Seguras - Ayuda")
    print("=" * 80)
    print("\nUso: python generador.py [opciones]\n")
    print("Opciones disponibles:")
    print("""
  -h, --help            Muestra este mensaje de ayuda y termina

  -l, --longitud LONGITUD
                        Longitud de la contraseña (por defecto: 16, mínimo: 12)

  -n, --cantidad CANTIDAD
                        Número de contraseñas a generar (por defecto: 1)

Opciones de caracteres:
  --sin-mayusculas      Excluir letras mayúsculas (A-Z)
  --sin-minusculas      Excluir letras minúsculas (a-z)
  --sin-numeros         Excluir números (0-9)
  --sin-especiales      Excluir caracteres especiales (!@#$%^&*()_+-=[]{}|;:,.<>?)
  --incluir-ambiguos    Incluir caracteres ambiguos (l,1,I,0,O)

Opciones de salida:
  --no-copiar           No copiar automáticamente la contraseña al portapapeles

Ejemplos:
  python generador.py -l 20 --sin-especiales
  python generador.py --longitud 12 --cantidad 3 --no-copiar
  python generador.py --sin-numeros --incluir-ambiguos
""")
    exit(0)

def main():
    # Mostrar banner al inicio
    if len(sys.argv) == 1 or '--help' in sys.argv or '-h' in sys.argv:
        mostrar_banner()
    
    # Configurar el parser de argumentos
    parser = argparse.ArgumentParser(
        description='Generador de contraseñas seguras',
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='Ejemplos de uso:\n'
    )
    
    # Añadir argumentos
    parser.add_argument(
        '-h', '--help', 
        action='store_true',
        help='Muestra este mensaje de ayuda y termina'
    )
    parser.add_argument(
        '-l', '--longitud', 
        type=int, 
        default=16, 
        help=argparse.SUPPRESS  # Ocultamos la ayuda por defecto
    )
    parser.add_argument(
        '--sin-mayusculas', 
        action='store_false', 
        dest='mayusculas', 
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '--sin-minusculas', 
        action='store_false', 
        dest='minusculas', 
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '--sin-numeros', 
        action='store_false', 
        dest='numeros', 
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '--sin-especiales', 
        action='store_false', 
        dest='especiales', 
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '--incluir-ambiguos', 
        action='store_false', 
        dest='excluir_ambiguos', 
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '-n', '--cantidad', 
        type=int, 
        default=1, 
        help=argparse.SUPPRESS
    )
    parser.add_argument(
        '--no-copiar', 
        action='store_false', 
        dest='copiar', 
        help=argparse.SUPPRESS
    )
    
    # Parsear argumentos
    args = parser.parse_args()
    
    # Mostrar ayuda si se solicita
    if args.help:
        mostrar_ayuda()
        
    # Validar longitud mínima
    if args.longitud < 12:
        print("Error: La longitud mínima de la contraseña debe ser 12 caracteres.")
        print("Use --help para más información.")
        exit(1)
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*60)
        print("\033[1mGENERANDO CONTRASEÑA SEGURA...\033[0m")
        print("="*60)
        
        # Mostrar animación de carga
        def mostrar_carga():
            for _ in range(3):
                for c in ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']:
                    sys.stdout.write(f'\r{c} Generando... ')
                    sys.stdout.flush()
                    time.sleep(0.1)
        
        # Iniciar la generación
        mostrar_llave()
        mostrar_carga()
        
        for _ in range(args.cantidad):
            password = generar_contraseña(
                longitud=max(args.longitud, 12),
                usar_mayusculas=args.mayusculas,
                usar_minusculas=args.minusculas,
                usar_numeros=args.numeros,
                usar_especiales=args.especiales,
                excluir_ambiguos=args.excluir_ambiguos
            )
            
            # Mostrar la contraseña generada
            print("\n\n\033[1;32m✓ CONTRASEÑA GENERADA CON ÉXITO\033[0m")
            print("\n" + "-"*60)
            print(f"\033[1;36m{password}\033[0m")
            print("-"*60)
            
            # Mostrar estadísticas
            entropia = calcular_entropia(password)
            mostrar_estadisticas(entropia, len(password))
            
            # Copiar al portapapeles si es una sola contraseña
            if args.copiar and args.cantidad == 1:
                try:
                    pyperclip.copy(password)
                    print("\n\033[1;32m✓ Contraseña copiada al portapapeles\033[0m")
                except Exception as e:
                    print(f"\n\033[1;31m✗ No se pudo copiar al portapapeles: {e}\033[0m")
            
            # Pequeña pausa entre contraseñas si hay más de una
            if _ < args.cantidad - 1:
                print("\n" + "-"*60)
                print("Generando siguiente contraseña...\n")
                time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n\033[1;33m[!] Operación cancelada por el usuario\033[0m")
        return 1
    except Exception as e:
        mostrar_error()
        print(f"\nDetalles del error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        import pyperclip
    except ImportError:
        print("¡Atención! El módulo 'pyperclip' no está instalado.")
        print("La funcionalidad de copiar al portapapeles no estará disponible.")
        print("Puedes instalarlo con: pip install pyperclip")
        
        import types
        sys.modules['pyperclip'] = types.SimpleNamespace(copy=lambda x: None)
        pyperclip = sys.modules['pyperclip']
    
    import sys
    sys.exit(main())
