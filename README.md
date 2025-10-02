# Telegram Wikipedia Bot

Простой Telegram-бот для парсинга статей с Википедии.

## Функции
- Ищет статьи в Википедии по запросу
- Поддерживает русскую и английскую версии
- Управляется через простые команды

## Как запустить
1. **Склонируйте репозиторий:**
   ```bash
   git clone https://github.com/jaydeadlondon/web_scraper.git
   ```
2. **Создайте и активируйте виртуальное окружение:**
    ```bash
   python -m venv venv
   source venv/bin/activate  # Для Linux/macOS
   venv\Scripts\activate    # Для Windows
   ```
3. **Установите зависимости:**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Настройте бота:**
   - Создайте нового бота в Telegram через [@BotFather](https://t.me/BotFather) и получите токен.
   - Откройте файл `scraper.py` и вставьте ваш токен вместо `'YOUR_TELEGRAM_BOT_TOKEN'`.
5. **Запустите бота:**  
   ```bash
   python scraper.py
   ```
## Как использовать
- `/start` - приветственное сообщение.
- `/set_lang ru` - переключить язык на русский.
- `/set_lang en` - переключить язык на английский.
- Отправьте название статьи, чтобы получить ее краткое содержание.

## Примечание
Исключительно для личного использования.