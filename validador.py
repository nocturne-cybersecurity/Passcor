#Codigo hecho por Nocturne Github: https://github.com/nocturne-cybersecurity

import bcrypt
import getpass
import time
import re
import os
import json
import hashlib
import sys
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass, asdict
from ascii import mostrar_banner, mostrar_cerradura, mostrar_estadisticas, mostrar_exito, mostrar_error

@dataclass
class IntentoLogin:
    timestamp: float
    intentos: int = 0
    bloqueado_hasta: Optional[float] = None

class RateLimiter:
    def __init__(self, max_attempts: int = 5, window_minutes: int = 15, ban_minutes: int = 60):
        self.max_attempts = max_attempts
        self.window_seconds = window_minutes * 60
        self.ban_seconds = ban_minutes * 60
        self.attempts: Dict[str, IntentoLogin] = {}
        self.lock_file = "login_attempts.json"
        self._load_attempts()

    def _load_attempts(self):
        try:
            if os.path.exists(self.lock_file):
                with open(self.lock_file, 'r') as f:
                    data = json.load(f)
                    for ip, att in data.items():
                        self.attempts[ip] = IntentoLogin(**att)
        except Exception as e:
            print(f"Advertencia: No se pudieron cargar los intentos previos: {e}")

    def _save_attempts(self):
        try:
            with open(self.lock_file, 'w') as f:
                json.dump(
                    {ip: asdict(att) for ip, att in self.attempts.items()},
                    f,
                    default=str
                )
        except Exception as e:
            print(f"Advertencia: No se pudieron guardar los intentos: {e}")

    def _clean_old_attempts(self):
        now = time.time()
        to_remove = []
        for ip, attempt in self.attempts.items():
            if attempt.bloqueado_hasta and attempt.bloqueado_hasta < now:
                to_remove.append(ip)
        for ip in to_remove:
            del self.attempts[ip]
        if to_remove:
            self._save_attempts()

    def register_attempt(self, username: str, success: bool) -> bool:
        """Registra un intento de inicio de sesión y devuelve si está permitido continuar"""
        ip = self._get_client_ip()
        now = time.time()
        
        self._clean_old_attempts()
        
        if ip not in self.attempts:
            self.attempts[ip] = IntentoLogin(timestamp=now)
        
        attempt = self.attempts[ip]
        
        if attempt.bloqueado_hasta and now < attempt.bloqueado_hasta:
            return False
        
        if not success:
            if now - attempt.timestamp > self.window_seconds:
                attempt.timestamp = now
                attempt.intentos = 1
            else:
                attempt.intentos += 1
            
            if attempt.intentos >= self.max_attempts:
                attempt.bloqueado_hasta = now + self.ban_seconds
                print(f"Demasiados intentos fallidos. Intenta de nuevo en {self.ban_seconds // 60} minutos.")
                self._save_attempts()
                return False
            
            self._save_attempts()
        else:
            if ip in self.attempts:
                del self.attempts[ip]
                self._save_attempts()
        
        return True
    
    def _get_client_ip(self) -> str:
        """Obtiene la IP del cliente de forma segura"""
        # En un entorno real, obtendrías la IP de la solicitud HTTP
        # Esto es un ejemplo simplificado
        import socket
        return socket.gethostbyname(socket.gethostname())

# Inicializar el rate limiter
try:
    rate_limiter = RateLimiter(
        max_attempts=5,          # Máximo de intentos permitidos
        window_minutes=15,       # Ventana de tiempo en minutos
        ban_minutes=60           # Tiempo de bloqueo en minutos
    )
except Exception as e:
    print(f"Error al inicializar el sistema de seguridad: {e}")
    exit(1)

import sqlite3
from typing import List, Tuple, Optional

def inicializar_bd():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            hash_contraseña TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def cargar_contraseñas(archivo: str) -> List[str]:
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return [linea.strip() for linea in f if linea.strip()]
    except FileNotFoundError:
        print(f"Advertencia: No se encontró el archivo {archivo}")
        return []

def es_contraseña_comun(contraseña: str, lista_contraseñas: List[str]) -> bool:
    return contraseña in lista_contraseñas

def validar_fortaleza(contraseña: str) -> Tuple[bool, str]:
    if len(contraseña) < 12:
        return False, "La contraseña debe tener al menos 12 caracteres"
    if not re.search(r"[A-Z]", contraseña):
        return False, "Debe contener al menos una letra mayúscula"
    if not re.search(r"[a-z]", contraseña):
        return False, "Debe contener al menos una letra minúscula"
    if not re.search(r"\d", contraseña):
        return False, "Debe contener al menos un número"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", contraseña):
        return False, "Debe contener al menos un carácter especial"
    return True, "Contraseña segura"

def hash_contraseña(contraseña: str) -> bytes:
    return bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt(rounds=14))

def guardar_usuario(usuario: str, contraseña: str) -> bool:
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        hashed = hash_contraseña(contraseña)
        cursor.execute(
            "INSERT INTO usuarios (usuario, hash_contraseña) VALUES (?, ?)",
            (usuario, hashed.decode('utf-8'))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verificar_contraseña(usuario: str, contraseña: str) -> bool:
    try:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT hash_contraseña FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        resultado = cursor.fetchone()
        if resultado:
            hashed = resultado[0].encode('utf-8')
            return bcrypt.checkpw(contraseña.encode('utf-8'), hashed)
        return False
    finally:
        conn.close()

def mostrar_menu():
    """Muestra el menú principal con arte ASCII"""
    mostrar_cerradura()
    print("\n\033[1;36m=== GESTOR DE CONTRASEÑAS SEGURAS ===\033[0m")
    print("\033[1m1. Crear nuevo usuario")
    print("2. Iniciar sesión")
    print("3. Salir\033[0m\n")

def main():
    # Mostrar banner al inicio
    mostrar_banner()
    
    # Inicializar base de datos y cargar contraseñas comunes
    try:
        inicializar_bd()
        contraseñas_comunes = cargar_contraseñas('TXT/contras.txt')
    except Exception as e:
        mostrar_error()
        print(f"\nError al inicializar el sistema: {e}")
        return 1

    while True:
        print("\n--- Sistema de Gestión de Contraseñas ---")
        print("1. Crear nuevo usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '3':
            print("¡Hasta luego!")
            break

        elif opcion == '1':
            usuario = input("Ingrese nombre de usuario: ").strip()
            while True:
                contraseña = getpass.getpass("Ingrese su contraseña (mínimo 12 caracteres, mayúsculas, minúsculas, números y caracteres especiales): ")

                es_valida, mensaje = validar_fortaleza(contraseña)
                if not es_valida:
                    print(f"Error: {mensaje}")
                    continue

                if es_contraseña_comun(contraseña, contraseñas_comunes):
                    print("¡Alerta! Esta contraseña es muy común y fácil de adivinar.")
                    continue

                confirmacion = getpass.getpass("Confirme su contraseña: ")
                if contraseña != confirmacion:
                    print("Las contraseñas no coinciden. Intente de nuevo.")
                    continue

                if guardar_usuario(usuario, contraseña):
                    print("¡Usuario creado exitosamente!")
                else:
                    print("Error: El nombre de usuario ya existe.")
                time.sleep(1)
                break

        elif opcion == '2':
            usuario = input("Usuario: ").strip()
            contraseña = getpass.getpass("Contraseña: ")

            # Verificar rate limiting
            if not rate_limiter.register_attempt(usuario, False):
                print("Demasiados intentos fallidos. Por favor, intente más tarde.")
                time.sleep(2)  # Pequeño retraso para evitar fuerza bruta
                continue

            # Verificar credenciales
            credenciales_validas = verificar_contraseña(usuario, contraseña)
            
            # Registrar intento exitoso/fallido
            rate_limiter.register_attempt(usuario, credenciales_validas)

            if credenciales_validas:
                print("\n" + "="*50)
                print(f"¡Bienvenido, {usuario}!")
                print("="*50 + "\n")
                # Limpiar intentos fallidos después de un inicio de sesión exitoso
                rate_limiter.register_attempt(usuario, True)
                break
            else:
                print("Usuario o contraseña incorrectos. Intente de nuevo.")
                # Mostrar advertencia de seguridad después de varios intentos fallidos
                ip = rate_limiter._get_client_ip()
                if ip in rate_limiter.attempts:
                    remaining_attempts = rate_limiter.max_attempts - rate_limiter.attempts[ip].intentos
                    if remaining_attempts > 0:
                        print(f"Advertencia: Le quedan {remaining_attempts} intentos antes del bloqueo.")
                time.sleep(1)  # Añadir retraso para evitar fuerza bruta

        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    try:
        import bcrypt
    except ImportError:
        print("Error: El módulo 'bcrypt' no está instalado.")
        print("Por favor, instálalo con: pip install bcrypt")
        exit(1)
    main()