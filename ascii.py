
def mostrar_banner():
    banner = """    
                                                          
  ███████╗  █████╗ ███████╗███████╗ ██████╗ ██████╗ ██████╗
  ██╔═══██ ██╔══██╗██╔════╝██╔════╝██╔════╝██╔═══██╗██╔══██╗
  ███████║ ███████║███████╗███████╗██║     ██║   ██║██████╔╝
  ██╔════╝ ██╔══██║╚════██║╚════██║██║     ██║   ██║██╔══██╗
  ██║      ██║  ██║███████║███████║╚██████╗╚██████╔╝██║  ██║
  ╚═╝      ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝

    """
    print("\033[1;36m" + banner + "\033[0m")

def mostrar_cerradura():
    cerradura = """
     .--------.
    / .------. \
   / /        \ \
   | |        | |
  _| |________| |_
.' |_|        |_| '.
'._____ ____ _____.'
|     .'____'.     |
'.____'.____.'____.'
'.________________.'
    """
    print("\033[1;34m" + cerradura + "\033[0m")

def mostrar_llave():
    llave = """
           .--.
          /.-. '----------.
          \'-' .--"--""-"-'
           '--'
    """
    print("\033[1;33m" + llave + "\033[0m")

def mostrar_exito():
    print("\n\033[1;32m[✓] Operación exitosa\033[0m")

def mostrar_error():
    print("\n\033[1;31m[!] Ha ocurrido un error\033[0m")

def mostrar_estadisticas(entropia: float, longitud: int):
    print("\n\033[1mEstadísticas de la contraseña:\033[0m")
    print(f"- Longitud: {longitud} caracteres")
    print(f"- Entropía: {entropia:.2f} bits")
    
    if entropia < 40:
        print("- Fortaleza: \033[1;31mDébil\033[0m")
    elif entropia < 80:
        print("- Fortaleza: \033[1;33mModerada\033[0m")
    else:
        print("- Fortaleza: \033[1;32mFuerte\033[0m")
