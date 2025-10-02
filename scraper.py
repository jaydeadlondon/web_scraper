import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ЗАМЕНИТЕ 'YOUR_TELEGRAM_BOT_TOKEN' НА ВАШ ТОКЕН
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

user_langs = {}

def scrape_wikipedia(title, lang='en'):
    base_url = f"https://{lang}.wikipedia.org/wiki/{title}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    }
    
    response = requests.get(base_url, headers=headers)
    
    if response.status_code != 200:
        if response.status_code == 404:
            return "❌ Статья не найдена. Проверь название и язык."
        return f"Ошибка доступа: {response.status_code}"
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        heading = soup.find("h1", class_="firstHeading").get_text()
    except:
        heading = "Неизвестно"
    
    try:
        paragraphs = soup.select(".mw-parser-output > p")
        
        first_paragraph_text = "Не удалось найти текст."
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                first_paragraph_text = text
                break
    except Exception as e:
        first_paragraph_text = f"Ошибка при извлечении текста: {e}"

    return f"📘 СТАТЬЯ: {heading}\n🔗 Ссылка: {base_url}\n\n📝 Первый абзац:\n{first_paragraph_text}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_langs[user_id] = 'en'
    await update.message.reply_text(
        'Привет! Я бот для парсинга Википедии.\n'
        'Используй /set_lang ru или /set_lang en, чтобы выбрать язык.\n'
        'Затем просто отправь мне название статьи для поиска.'
    )

async def set_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    try:
        lang = context.args[0].lower()
        if lang in ['ru', 'en']:
            user_langs[user_id] = lang
            await update.message.reply_text(f"Язык установлен на {'русский' if lang == 'ru' else 'английский'}.")
        else:
            await update.message.reply_text("Пожалуйста, выбери 'ru' или 'en'.")
    except (IndexError, ValueError):
        await update.message.reply_text("Использование: /set_lang <ru|en>")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    lang = user_langs.get(user_id, 'en')
    
    title = update.message.text.strip().replace(" ", "_")
    
    await update.message.reply_text("⏳ Идет поиск...")
    
    result = scrape_wikipedia(title, lang)
    
    await update.message.reply_text(result)

def main():
    if TOKEN == 'YOUR_TELEGRAM_BOT_TOKEN':
        print("Пожалуйста, замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш настоящий токен в файле scraper.py")
        return

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("set_lang", set_lang))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
