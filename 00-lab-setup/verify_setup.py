"""
Script de verificación del entorno de desarrollo.
Valida que todas las dependencias estén instaladas correctamente.
"""

import sys
from typing import List, Tuple

def check_python_version() -> Tuple[bool, str]:
    """Verifica que Python sea 3.11 o superior."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True, f"✅ Python {version.major}.{version.minor}.{version.micro}"
    return False, f"❌ Python {version.major}.{version.minor} (se requiere 3.11+)"

def check_package(package_name: str) -> Tuple[bool, str]:
    """Verifica que un paquete esté instalado."""
    try:
        module = __import__(package_name.replace("-", "_"))
        version = getattr(module, "__version__", "unknown")
        return True, f"✅ {package_name} ({version})"
    except ImportError:
        return False, f"❌ {package_name} no instalado"

def check_env_file() -> Tuple[bool, str]:
    """Verifica que exista el archivo .env."""
    import os
    if os.path.exists(".env"):
        return True, "✅ Archivo .env encontrado"
    return False, "⚠️  Archivo .env no encontrado (copia .env.example a .env)"

def main():
    print("=" * 60)
    print("VERIFICACIÓN DEL ENTORNO DE DESARROLLO")
    print("=" * 60)
    print()
    
    checks: List[Tuple[bool, str]] = []
    
    # Verificar Python
    checks.append(check_python_version())
    
    # Verificar paquetes críticos
    critical_packages = [
        "langgraph",
        "langchain",
        "langchain_core",
        "langchain_anthropic",
        "langchain_openai",
        "dotenv",
        "httpx",
        "pydantic"
    ]
    
    for package in critical_packages:
        checks.append(check_package(package))
    
    # Verificar archivo .env
    checks.append(check_env_file())
    
    # Mostrar resultados
    for success, message in checks:
        print(message)
    
    print()
    print("=" * 60)
    
    # Resumen
    total = len(checks)
    passed = sum(1 for success, _ in checks if success)
    
    if passed == total:
        print(f"✅ TODO CONFIGURADO CORRECTAMENTE ({passed}/{total})")
        print()
        print("Próximo paso: ejecuta 'python hello_langgraph.py'")
        return 0
    else:
        print(f"⚠️  CONFIGURACIÓN INCOMPLETA ({passed}/{total})")
        print()
        print("Revisa los errores arriba y sigue las instrucciones del README.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
