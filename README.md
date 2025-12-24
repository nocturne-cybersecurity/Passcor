# Passcor Gestor de Contraseñas Seguras

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Passcor es una herramienta de línea de comandos para generar y validar contraseñas seguras, con protección contra ataques de fuerza bruta.

## Características

-  Generador de contraseñas seguras
-  Validador de fortaleza de contraseñas
-  Protección contra fuerza bruta con rate limiting
-  Almacenamiento seguro de contraseñas con bcrypt
-  Base de datos SQLite para usuarios
-  Lista de contraseñas comunes para validación

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/nocturne-cybersecurity/Passcor.git
   cd Passcor
   ```

2. Crea un entorno virtual (recomendado):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Generador de Contraseñas

```bash
python3 generador.py
```

Opciones disponibles:
```
En la terminal escribe python3 generador.py --help para ver las opciones disponibles

-l, --longitud LONGITUD    Longitud de la contraseña (mínimo 12)
--sin-mayusculas          Excluir mayúsculas
--sin-minusculas          Excluir minúsculas
--sin-numeros             Excluir números
--sin-especiales          Excluir caracteres especiales
--incluir-ambiguos        Incluir caracteres ambiguos (l,1,I,0,O)
-n, --cantidad CANTIDAD   Número de contraseñas a generar
--no-copiar               No copiar al portapapeles
```

### Validador de Contraseñas

```bash
python3 validador.py
```

El validador ofrece un menú interactivo para:
1. Crear nuevo usuario
2. Iniciar sesión
3. Salir

## Estructura del Proyecto

```
.
├── generador.py          # Script para generar contraseñas seguras
├── validador.py          # Script para validar y gestionar usuarios
├── contras.txt           # Lista de contraseñas comunes
├── data.JSON             # Contraseñas de ejemplo por categorías
├── usuarios.db           # Base de datos SQLite (se crea automáticamente)
├── login_attempts.json   # Registro de intentos de inicio de sesión
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Este archivo que estas leyendo jaja
```

## Medidas de Seguridad

- Uso de bcrypt para el hashing de contraseñas
- Rate limiting para prevenir ataques de fuerza bruta
- Validación de fortaleza de contraseñas
- Exclusión de contraseñas comunes
- Almacenamiento seguro de credenciales

## Contribución

Las contribuciones son bienvenidas. Por favor, lee las [guías de contribución](CONTRIBUTING.md) para más detalles.

## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## Autor

- **Nocturne** - [GitHub](https://github.com/nocturne-cybersecurity)
