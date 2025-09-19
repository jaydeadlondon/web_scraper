import requests
from bs4 import BeautifulSoup
import sys

def scrape_wikipedia(title, lang='en'):
    base_url = f"https://{lang}.wikipedia.org/wiki/{title}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    }
    
    response = requests.get(base_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Ошибка доступа: {response.status_code}")
        if response.status_code == 404:
            print("❌ Статья не найдена. Проверь название и язык.")
        return
    
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
        first_paragraph_text = "Ошибка при извлечении текста."

    print(f"\n📘 СТАТЬЯ: {heading}")
    print(f"🔗 Ссылка: {base_url}")
    print(f"\n📝 Первый абзац:\n{first_paragraph_text}")

    filename = f"{lang}_{title}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Статья: {heading}\n")
        f.write(f"Ссылка: {base_url}\n\n")
        f.write(f"Текст:\n{first_paragraph_text}\n")
    
    print(f"\n✅ Сохранено в: {filename}")


if __name__ == "__main__":
    print("🌐 Выберите язык:")
    print("1. Русская Википедия (ru)")
    print("2. Английская Википедия (en)")
    
    choice = input("Выберите (1 или 2): ").strip()
    lang = 'ru' if choice == '1' else 'en'
    
    title = input(f"Введите название статьи ({'на русском' if lang == 'ru' else 'на английском'}): ").strip()
    title = title.replace(" ", "_")
    
    scrape_wikipedia(title, lang)