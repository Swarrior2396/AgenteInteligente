#!/usr/bin/env python3
"""
Script para ejecutar el bot de PetHealth sin dependencias de OpenAI
"""

import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def check_environment():
    """Verifica que las variables de entorno estén configuradas"""
    required_vars = ['TELEGRAM_BOT_TOKEN']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Error: Las siguientes variables de entorno no están configuradas:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPor favor, configúralas en el archivo .env")
        return False
    
    return True

def main():
    """Función principal"""
    print("🏥 Iniciando PetHealth Telegram Bot (Versión Offline)...")
    print("✅ Esta versión funciona sin OpenAI API")
    print("📋 Usando recomendaciones predefinidas")
    
    if not check_environment():
        sys.exit(1)
    
    try:
        from main_offline import main as run_bot
        run_bot()
    except KeyboardInterrupt:
        print("\n👋 Bot detenido por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando el bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
