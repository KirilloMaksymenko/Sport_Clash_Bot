#!/usr/bin/env python3
"""
Скрипт для запуску Telegram Fitness Bot
"""

import subprocess
import sys
import os

def check_requirements():
    """Перевірка залежностей"""
    try:
        import aiogram
        import aiosqlite
        import python_dotenv
        print("✅ Всі залежності встановлені")
        return True
    except ImportError as e:
        print(f"❌ Відсутня залежність: {e}")
        print("Встановіть залежності: pip install -r requirements.txt")
        return False

def check_env_file():
    """Перевірка .env файлу"""
    if os.path.exists('.env'):
        print("✅ Файл .env знайдено")
        return True
    else:
        print("❌ Файл .env не знайдено")
        print("Створіть файл .env на основі .env.example")
        return False

def main():
    """Головна функція запуску"""
    print("🏃‍♂️ Telegram Fitness Competition Bot")
    print("=" * 40)

    # Перевірки
    if not check_requirements():
        sys.exit(1)

    if not check_env_file():
        sys.exit(1)

    # Запуск бота
    print("🚀 Запуск бота...")
    try:
        subprocess.run([sys.executable, "main.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️ Бот зупинено користувачем")
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка запуску бота: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
