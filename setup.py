"""
Скрипт налаштування Telegram Fitness Bot
"""

import os
import subprocess
import sys

def create_logs_directory():
    """Створення папки для логів"""
    if not os.path.exists('logs'):
        os.makedirs('logs')
        print("✅ Створено папку logs/")

def install_requirements():
    """Встановлення залежностей"""
    print("📦 Встановлення залежностей...")
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Залежності встановлені успішно")
    except subprocess.CalledProcessError:
        print("❌ Помилка встановлення залежностей")
        return False
    """
    return True

def setup_env_file():
    """Налаштування .env файлу"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ Створено .env файл з шаблону")
            print("⚠️ Відредагуйте .env файл з вашими налаштуваннями")
        else:
            print("❌ Файл .env.example не знайдено")
            return False
    else:
        print("✅ Файл .env вже існує")
    return True

def main():
    """Головна функція налаштування"""
    print("🏃‍♂️ Налаштування Telegram Fitness Bot")
    print("=" * 40)

    # Створення необхідних папок
    create_logs_directory()

    # Встановлення залежностей
    if not install_requirements():
        sys.exit(1)

    # Налаштування .env
    if not setup_env_file():
        sys.exit(1)

    print("\n🎉 Налаштування завершено!")
    print("📝 Не забудьте відредагувати .env файл з вашими токенами")
    print("🚀 Запустіть бота: python main.py")

if __name__ == "__main__":
    main()
