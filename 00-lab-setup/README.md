# Lab Setup - Configuración del Entorno

Este módulo te guiará en la configuración del entorno de desarrollo para el curso de LangGraph.

## Requisitos Previos

- Windows 10/11, macOS, o Linux
- Conexión a internet
- Permisos de administrador (para instalación de Python)

## Paso 1: Instalación de Python

### Windows
1. Descarga Python 3.12+ desde [python.org](https://www.python.org/downloads/)
2. Durante la instalación, **marca** "Add Python to PATH"
3. Verifica la instalación:
```bash
python --version
```

### macOS
```bash
brew install python@3.12
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

## Paso 2: Verificar Versiones de Python Disponibles

```bash
py --list
```

Deberías ver Python 3.12 o superior. Si no lo tienes, instálalo desde python.org.

## Paso 3: Crear Entorno Virtual

Navega al **root del curso** (no a la carpeta 00-lab-setup):

```bash
cd D:\botpro\llms\courses\langGraph\langGraph-course
```

Crea el entorno virtual con Python 3.12+:

```bash
py -3.12 -m venv venv
```

## Paso 4: Activar Entorno Virtual

### Windows
```bash
venv\Scripts\activate
```

### macOS/Linux
```bash
source venv/bin/activate
```

Deberías ver `(venv)` al inicio de tu línea de comando.

## Paso 5: Instalar Dependencias

```bash
pip install --upgrade pip
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

## Paso 6: Configurar Variables de Entorno

El archivo `.env.00` ya está listo para esta lección (sin API keys necesarias).

Para lecciones futuras, copia `.env.example` y renombra según necesites (.env.01, .env.02, etc.)

## Paso 7: Verificar Instalación

Navega a la carpeta 00-lab-setup:

```bash
cd 00-lab-setup
python verify_setup.py
```

Si todo está correcto, verás: ✅ Todo configurado correctamente

## Paso 8: Prueba LangGraph

```bash
python hello_langgraph.py
```

## Troubleshooting

### Error: "python no reconocido"
- Windows: Reinstala Python y marca "Add to PATH"
- Reinicia la terminal

### Error: py --list no funciona
- Reinstala Python desde python.org
- Asegúrate de usar el instalador oficial de Windows

### Error: pip install falla
- Actualiza pip: `python -m pip install --upgrade pip`
- Usa Python 3.12 o superior

### Error: ModuleNotFoundError
- Asegúrate que el venv esté activado
- Verifica que estés en el root del curso
- Reinstala: `pip install -r requirements.txt`

## Estructura del Proyecto

```
langGraph-course/
├── venv/                    # Entorno virtual compartido
├── requirements.txt         # Dependencias centralizadas
├── .env.example            # Template de variables
├── .env.00                 # Variables para Lab Setup
├── 00-lab-setup/
│   ├── README.md
│   ├── verify_setup.py
│   └── hello_langgraph.py
└── 01-fundamentos/         # Próxima lección
```

## Próximos Pasos

Una vez completado el setup, continúa con la **Lección 1: Fundamentos de LangGraph**
