#!/usr/bin/env python3
"""
Парсер каталога AI-инструментов.
Источник 1: инструменты.txt (6408 строк)
Источник 2: Сообщение пользователя (9 разделов по функциям)
Выход: /home/z/my-project/scripts/catalog_raw.json
"""
import json
import re
from pathlib import Path

UPLOAD_DIR = Path("/home/z/my-project/upload")
OUT = Path("/home/z/my-project/scripts/catalog_raw.json")

# ─────────────────────────────────────────────
# Источник 1: инструменты.txt
# ─────────────────────────────────────────────
def parse_tools_file():
    """Парсит инструменты.txt — извлекает инструменты из таблиц markdown."""
    text = (UPLOAD_DIR / "инструмменты.txt").read_text(encoding="utf-8", errors="replace")
    tools = {}
    current_category = "Без категории"
    current_subcategory = None
    
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        
        # Заголовок категории (## или #)
        m = re.match(r'^#+\s+(.+)$', s)
        if m:
            current_category = m.group(1).strip()
            current_subcategory = None
            continue
        
        # Подзаголовок (---)
        if s == '---':
            current_subcategory = None
            continue
        
        # Строка таблицы | **name** | description |
        m = re.match(r'^\|\s*\*\*([^*]+)\*\*\s*\|\s*(.+?)\s*\|?\s*$', s)
        if m:
            name = m.group(1).strip()
            desc = m.group(2).strip()
            # Пропускаем заголовки таблиц
            if name.lower() in ('инструмент', 'tool', 'utility') or '---' in name:
                continue
            # Убираем markdown-форматирование из описания
            desc = re.sub(r'`([^`]+)`', r'\1', desc)
            desc = re.sub(r'\*\*([^*]+)\*\*', r'\1', desc)
            
            key = name.lower().replace('-', '').replace('_', '').replace(' ', '')
            if key not in tools:
                tools[key] = {
                    "name": name,
                    "description": desc,
                    "category_from_file": current_category,
                    "source": "инструменты.txt"
                }
            continue
        
        # Строка таблицы без ** (name\tdesc)
        m = re.match(r'^([^\t|]+?)\t+(.+)$', s)
        if m and not s.startswith('|') and not s.startswith('#'):
            name = m.group(1).strip()
            desc = m.group(2).strip()
            if name.lower() in ('инструмент', 'tool', 'utility') or '---' in name or len(name) > 60:
                continue
            if name.lower() in ('表格', '🆕', '✨', '📁', '🌐', '🔤', '📦', '🧪', '🤖', '✅', '🔧', '💻', '⚡', '🎨', '🚀'):
                continue
            desc = re.sub(r'`([^`]+)`', r'\1', desc)
            
            key = name.lower().replace('-', '').replace('_', '').replace(' ', '')
            if key not in tools:
                tools[key] = {
                    "name": name,
                    "description": desc,
                    "category_from_file": current_category,
                    "source": "инструменты.txt"
                }
    
    return list(tools.values())

# ─────────────────────────────────────────────
# Источник 2: Каталог из сообщения пользователя
# ─────────────────────────────────────────────
USER_CATALOG = {
  "1. Текст и документы": {
    "1.1 Редактирование, форматирование, конвертация": [
      "AI-форматировщик писем (Gmail, Outlook, Yahoo, ProtonMail, Яндекс.Почта)",
      "Генератор DOCX/DOC",
      "Интеллектуальное редактирование с трекингом изменений (Word/Google Docs)",
      "AI Diff Checker",
      "Генератор PDF (Adobe Acrobat Studio + AI Assistant, Smallpdf AI, PDF24)",
      "Конвертер форматов (DOCX, PDF, ODT, RTF, TXT, Markdown, HTML, EPUB)",
      "AI-OCR (Mistral OCR, PaddleOCR-VL, GLM-OCR, Tesseract, Google Document AI, ABBYY FineReader, Adobe Scan, Amazon Textract, Azure Document Intelligence, OpenOCR)",
      "Корректор грамматики и стиля (Grammarly, LanguageTool, ProWritingAid, Hemingway Editor, Wordtune)",
      "Переписыватель/рефразер",
      "Стилизатор под автора/эпоху/жанр",
      "Редактор под целевую аудиторию",
      "Редактор для цензуры/маскировки данных",
      "Нативные аддоны для редакторов (Plus AI, GPT Workspace, Claude for Word, HyperWrite)",
      "Трансформация промптов в юридические формы (FormsPal, Jotform AI)",
      "Bulk-генерация по шаблонам (Documentero)"
    ],
    "1.2 Структурирование, анализ, научная работа": [
      "Суммаризатор (Resoomer, Scholarcy, QuillBot, TLDR This)",
      "Генератор аннотаций и цитат",
      "Анализ академической литературы (Consensus, Unriddle/Anara AI, Scite.ai, Elicit)",
      "SEO/GEO-оптимизация (Frase, Surfer AI, Anyword)",
      "Генератор планов и структуры",
      "Генератор заключений, выводов, предисловий, введений",
      "Разделитель на смысловые блоки",
      "Генератор оглавлений, индексов, предметных указателей",
      "Аннотатор кода в документах",
      "Генератор гиперссылок и перекрёстных ссылок",
      "Генератор многоязычных версий"
    ],
    "1.3 Шаблоны и спецдокументы": [
      "Шаблоны отчётов (бизнес, финансы, наука)",
      "Юридические документы (NDA, оферты, уставы) — LawGeex, LegalZoom, DoNotPay",
      "Коммерческие предложения (B2B/B2C)",
      "Технические задания (ТЗ, TOR, SOW)",
      "Бизнес-планы",
      "Резюме и CV (Rezi, Zety, Novoresume, Canva AI)",
      "Сопроводительные письма и пресс-релизы",
      "Инструкции, руководства, мануалы, чек-листы",
      "Протоколы собраний и питч-деки",
      "Deckary (стратегические слайды в PowerPoint)",
      "Библиографии (APA, MLA, Chicago, ГОСТ) — Zotero, Mendeley, Citethisforme",
      "Помощник LaTeX (Overleaf AI, TeXstudio)",
      "Транскрипция аудио/видео (Otter.ai, Descript, Sonix, Castmagic)",
      "Транскрибация встреч с CRM (Fireflies.ai, Fathom, tl;dv, MeetGeek, Avoma)",
      "STT-API для разработчиков (AssemblyAI, Deepgram, Speechmatics, Whisper)",
      "Носимые устройства записи (Plaud NotePin, Bee)",
      "Проверка уникальности и детекция ИИ-контента (Copyscape, Originality.ai, Copyleaks)"
    ]
  },
  "2. Генерация контента": {
    "2.1 Креативный и литературный": [
      "Простые объяснения сложных тем",
      "Стихотворные формы (хайку, сонеты, лимерики, басни, оды, эпиграммы, акростихи, свободный стих)",
      "Лингвистические фигуры (метафоры, аналогии, аллитерации, оксюмороны, гиперболы, литоты, каламбуры, персонификации, эвфемизмы, анафоры, эпитеты)",
      "Неологизмы для брендов и проектов",
      "Тосты, речи, поздравления, приглашения",
      "Извинения, рекомендательные письма, характеристики",
      "Эпитафии, девизы, лозунги",
      "Загадки, головоломки, квесты, сюжеты игр",
      "Предсказания, шуточные гороскопы, завязки рассказов",
      "Лор (описания персонажей, локаций, миров)",
      "Диалоги, реплики, нейминг (названия, никнеймы)"
    ],
    "2.2 Маркетинг, продажи, соцсети": [
      "SEO-статьи и мета-описания (SurferSEO, Clearscope, Frase, Anyword)",
      "Контент для лендингов, рассылок, cold-звонков (Mailchimp AI, Brevo, AirOps)",
      "USP, слоганы, миссии",
      "Тексты для баннеров и описаний товаров",
      "Ответы на отзывы и комментарии (ORM)",
      "Посты для соцсетей (Instagram, Facebook, LinkedIn, X, Telegram)",
      "Meet Sona — голос-бренд через интервью",
      "Идеи для контента, подкастов, видео (YouTube, TikTok, Reels, Shorts)",
      "Репурпозинг длинного видео/подкастов в шорты (Opus Clip, Castmagic)",
      "Пресс-киты, FAQ, кейсы, лид-магниты",
      "Push-сообщения, сценарии чат-ботов, CTA",
      "Вакансии и должностные инструкции (LinkedIn, HH.ru)",
      "Объявления для классифайдов (Авито, Авто.ру, Циан)"
    ],
    "2.3 Образование и самоорганизация": [
      "Учебные программы, планы занятий, конспекты",
      "Флешкарты и тесты (Quizgecko AI, ClassMarker AI)",
      "Вопросы для собеседований и экзаменов",
      "Тезисы, обзоры литературы, глоссарии",
      "Планы самообучения, гипотезы, лабораторные работы",
      "AI-переводчики и двуязычные диалоги (DeepL, Google Translate, Reverso, Elsa Speak)"
    ]
  },
  "3. Мультимедиа": {
    "3.1 Изображения, графика, дизайн": [
      "Text-to-Image (Ideogram, Midjourney, DALL·E 3, GPT Image 2, Stable Diffusion XL/3/3.5, Adobe Firefly, Leonardo.AI, Flux, Kandinsky, Grok Imagine, HiDream-O1-Image, Nano Banana Pro/2, Шедеврум)",
      "Векторная графика и брендинг (Recraft V4/V4.1, Looka, Brandmark, Hatchful, Iconify AI)",
      "Аватары, портреты, логотипы (Artbreeder, Fotor AI, Canva AI)",
      "Инфографика, диаграммы, ментальные карты (Piktochart, Venngage, Datawrapper, Flourish, Miro AI)",
      "3D-модели и NFT-арт (NVIDIA Omniverse, Kaedim, Masterpiece Studio)",
      "Стикеры, обои, раскраски, татуировки, паттерны",
      "Апскейл и арт-улучшение (Magnific AI, Krea)",
      "Реставрация фото (Topaz Photo AI, Remini)",
      "E-commerce фото (Photoroom)",
      "Playground, Freepik AI"
    ],
    "3.2 3D-моделирование и анимация": [
      "Text/image-to-3D, сканы (Meshy, Tripo AI, Rodin, Luma AI capture)",
      "Анимация персонажей по видео (Cascadeur, Move AI, Rokoko, Deep Motion)",
      "3D-сцены в браузере (Spline AI)",
      "Игровые ассеты (Scenario, Layer.ai, Rosebud AI)",
      "ИИ-NPC (Inworld AI)"
    ],
    "3.3 Видео и анимация": [
      "T2V / I2V (Seedance 2.0/2.5, Kling 3.0/O3, Wan 2.6/2.7, Hailuo/PixVerse V6, HappyHorse 1.0/1.1, Runway Gen-4.5/Aleph, Sora, Veo 3.1, Luma Dream Machine, Pika Labs, FLUX 3 Video, ModelScope, AnimateDiff, Stable Video Diffusion)",
      "Цифровые аватары и ведущие (Synthesia, HeyGen, D-ID, Colossyan, InVideo AI)",
      "Deepfake и лип-синк (DeepBrain AI, Resemble AI)",
      "LinkedIn-видео из текста (Topview)",
      "Рекламные AI-видео (Creatify AI, Zeely AI)",
      "Маркетинговое видео из текста (Lumen5)",
      "Онлайн-редакторы (Kapwing, Veed.io)",
      "Анимация персонажей по мимике (Act-One от Runway)",
      "Эффекты для роликов (Pikaffect)",
      "Замена актёров CG (Wonder Studio)",
      "Монтаж (CapCut AI, Descript, Topaz Video AI, Pictory)",
      "Видеофоны, тизеры, слайд-шоу (Insta360 AI, Zoom AI Backgrounds)"
    ],
    "3.4 Аудио, музыка, голос": [
      "Музыка по тексту (Suno AI, Udio, ElevenLabs Music, Stable Audio 3.0, Soundraw, AIVA, Amper Music, Boomy, Soundful, Mureka, Beatoven.ai, Soundverse, Treblo, ACE-Step 1.5)",
      "TTS и клонирование голоса (ElevenLabs, Murf.ai, Resemble AI, Play.ht, NaturalReader, Amazon Polly, Google Lyria, Lovo AI/Genny, Synthesys, Bark)",
      "Разделение стемов (Lalal.ai, Moises)",
      "Шумоподавление в реальном времени (Krisp)",
      "Реставрация голоса (Adobe Podcast Enhance Speech, iZotope RX)",
      "Перевод и дубляж видео (Rask AI, Papercup, HeyGen Video Translate, ElevenLabs Dubbing, Caption Hub)",
      "Автосубтитры и капчейнинг (Happy Scribe, Submagic, Zeemo, Captions.ai, Kapwing)",
      "Обработка звука (Krotos Audio)",
      "Подкасты, аудиокниги, джинглы (Descript, Podcast.ai, Speechify)",
      "Рингтоны, ASMR, белый шум, ремиксы, каверы (Voicemod, LANDR, RVC AI, Uberduck)"
    ]
  },
  "4. Программирование и разработка": {
    "4.1 IDE, генерация кода, анализ": [
      "AI-native IDE (Cursor, Claude Code, Google Antigravity, Windsurf, Devin Desktop, Cline, Aider, Continue.dev, JetBrains Air, Kiro, Zed)",
      "Генераторы кода и автодополнение (GitHub Copilot, Tabnine, Amazon CodeWhisperer, Mistral Le Chat, Qwen Code, Sourcegraph Cody, Replit Ghostwriter)",
      "SQL (AI2sql, Text2SQL, SQLizer)",
      "regex (Regex Generator, AI Regex)",
      "API-документация (Postman AI, Swimm)",
      "юнит-тесты (Testim, Diffblue)",
      "UML/ER (Lucidchart AI, Draw.io)",
      "шейдеры (Shadertoy)",
      "код для микроконтроллеров (Arduino, ESP32)",
      "Ревью, дебаггинг, рефакторинг (Snyk AI, GitHub Advanced Security, SonarQube AI, CodeClimate AI, Sourcery)"
    ],
    "4.2 Веб, мобильные приложения, инфраструктура": [
      "Генераторы сайтов и лендингов (Vibecraft, Wix AI, Framer AI, Durable AI, 10Web, TeleportHQ, v0 by Vercel, Meoo)",
      "Интернет-магазины и мобильные приложения (Shopify AI, Ecwid AI, FlutterFlow AI, Adalo AI, Glide AI)",
      "UI/UX-дизайн и прототипы (Figma AI, Uizard, Galileo AI, Locofy AI, Adobe XD + AI)",
      "Анимации, фавиконы, цветовые палитры, шрифты (Animate.css + AI, Lottie AI, Favicon.io AI, Coolors AI, Adobe Color, Fontjoy, AI Font Generator)",
      "Dockerfile, Kubernetes манифесты, CI/CD (GitHub Actions, GitLab CI)",
      "Конфигурации серверов (Nginx, Apache), скрипты автоматизации (Bash, Python, PowerShell)",
      "тесты нагрузки (JMeter, Locust)",
      "фаерволы (iptables, pfSense)",
      "SQL-миграции, документация кода, коммиты"
    ]
  },
  "5. Презентации, аналитика, данные": {
    "5.1 Презентации и инфографика": [
      "Презентации и питч-деки (Gamma, AIPPT, Plus AI, Deckary, Beautiful.ai, Tome AI, Pitch AI, Slidesgo AI, Canva AI, Google Slides AI, Alai, Prezent, Chronicle, Ludus, Visme, PowerPoint Designer)",
      "Блок-схемы, таймлайны, оргструктуры (MindMeister AI, XMind AI, Miro AI, Timeline JS, Office Timeline, OrgChart Now AI)",
      "SWOT, дашборды (Tableau AI, Power BI AI, Looker AI)",
      "Помощник для выступлений"
    ],
    "5.2 Анализ данных и таблицы": [
      "Таблицы и датасеты (Excel Copilot, Google Sheets AI, Rows.com, Airtable AI, Pandas AI)",
      "Диалоговый анализ таблиц (Julius AI)",
      "Коллаборативные ноутбуки (Deepnote, Hex)",
      "BI-отчёты (Tableau AI, Power BI AI, Looker)",
      "Синтетические данные (Mockaroo AI, Synthea)",
      "Визуализации (Flourish AI, Datawrapper AI, heatmaps, корреляционные матрицы)",
      "Прогнозирование (Prophet AI, Google Predictive Analytics, R Studio AI)"
    ]
  },
  "6. Специализированные отрасли": {
    "Образование и наука": [
      "AI-репетиторы (Duolingo Max, Khanmigo, Socratic)",
      "Генераторы тестов, гипотез, планов экспериментов (Quizgecko AI, ClassMarker AI)",
      "Научные статьи (Scite.ai, Elicit)",
      "Анализ литературы (SciSpace, Connected Papers, Litmaps, ResearchRabbit)"
    ],
    "Здоровье, фитнес, питание": [
      "Планы тренировок (Freeletics AI, Vi by LifeBEAM)",
      "Питание и рецепты (EatThisMuch, PlantJammer, Chef Watson)",
      "Медицинские ассистенты (Ada Health, Buoy Health)",
      "Медитации (Headspace AI, Calm AI)",
      "Дневники (Notion AI, Day One AI)"
    ],
    "Личная продуктивность": [
      "SMART-цели, трекеры привычек, списки дел (Todoist AI, TickTick AI)",
      "Генераторы компромиссов, сценариев разговоров, планов на день/неделю/месяц, списков покупок, рекомендаций"
    ],
    "Путешествия и логистика": [
      "Маршруты (Google Trips AI, Roadtrippers AI), гиды, чек-листы, бюджеты, оптимизация доставки"
    ],
    "Финансы и бизнес": [
      "Личный бюджет, налоговые декларации, бизнес-модели (Business Model Canvas AI), стратегии (Strategyzer AI)",
      "Маркетинговые планы (HubSpot AI, SEMrush AI)",
      "Воронки продаж, CRM-отчёты (Salesforce Einstein), аналитика, инвест-советы"
    ],
    "Юриспруденция и недвижимость": [
      "Юридические платформы (Spellbook, Robin AI, Harvey, CoCounsel, Luminance)",
      "Исковые заявления, трудовые договоры, доверенности, консультации (DoNotPay, LegalZoom)",
      "Описания недвижимости, 3D-туры (Matterport AI, Cupix), оценка стоимости"
    ],
    "Автомобили и экология": [
      "Описания автомобилей, маршруты доставки",
      "Эко-советы, отчёты об углеродном следе"
    ]
  },
  "7. Универсальные LLM, ассистенты, платформы": {
    "Языковые модели и чат-боты": [
      "ChatGPT (OpenAI) — GPT-5.6 Sol/Terra/Luna",
      "Claude (Anthropic) — Claude Cowork, Claude Fable 5",
      "Gemini (Google)",
      "Llama (Meta)",
      "Grok (xAI)",
      "Mistral Le Chat",
      "Perplexity, You.com",
      "DeepSeek (V4 Pro)",
      "Qwen Chat (Alibaba), Hunyuan (Tencent), ERNIE Bot (Baidu), GLM/ChatGLM (Zhipu)",
      "Cohere Command",
      "Pi (Inflection), Character.AI, Poe (Quora), HuggingChat"
    ],
    "Локальные и open-source стеки": [
      "Ollama, LM Studio, Open WebUI",
      "OpenHands (агент-разработчик)",
      "LangChain, LlamaIndex (RAG-фреймворки)",
      "Dify, Flowise (no-code LLM-пайплайны)",
      "n8n, Make, Zapier, Bardeen (автоматизация)"
    ],
    "Офисные экосистемы": [
      "Microsoft 365 Copilot (Word, Excel, PowerPoint)",
      "Google Workspace AI (Docs, Sheets, Slides)",
      "Notion AI, Craft AI",
      "ClickUp AI",
      "WPS AI, Kimi Docs/Sheets",
      "Zoho Writer (Zia)"
    ],
    "Корпоративные платформы": [
      "HubSpot AI, Salesforce Einstein",
      "SEMrush AI, Jasper AI",
      "Eightfold AI, Pymetrics (HR)",
      "Kasisto (банки), AlphaSense (финансы)"
    ],
    "Креативные платформы": [
      "Adobe Firefly, Canva Magic Studio, Figma AI"
    ]
  },
  "8. Экспериментальные, агентные, футуристические": [
    "Автономные агенты (AutoGen, CrewAI)",
    "AutoML и fine-tuning (Google Vertex AI, H2O.ai)",
    "Промпт-инженерия (PromptPerfect, AIPRM)",
    "Квантовые алгоритмы (Qiskit AI), биодизайн, цифровые двойники, нейроморфные чипы, этические дилеммы"
  ],
  "9. Безопасность, аудит, этика": [
    "Детекторы deepfake (Deepware Scanner, Hive Moderation)",
    "Детекторы машинного текста (Originality AI, Copyleaks)",
    "Модерация (Google Perspective API, аудит токсичности)",
    "Комплаенс-генераторы (политики конфиденциальности, GDPR, этические гайдлайны)"
  ]
}

def parse_user_catalog():
    """Разворачивает каталог пользователя в плоский список."""
    out = []
    for cat, sub in USER_CATALOG.items():
        if isinstance(sub, dict):
            for subcat, items in sub.items():
                for item in items:
                    out.append({
                        "name": item,
                        "category": cat,
                        "subcategory": subcat,
                        "source": "user_message"
                    })
        else:
            for item in sub:
                out.append({
                    "name": item,
                    "category": cat,
                    "subcategory": None,
                    "source": "user_message"
                })
    return out

# ─────────────────────────────────────────────
# Главный запуск
# ─────────────────────────────────────────────
if __name__ == "__main__":
    tools_file = parse_tools_file()
    tools_user = parse_user_catalog()
    
    # Объединение без дублей (по нормализованному имени)
    seen = set()
    merged = []
    
    # Сначала из файла (более конкретные названия)
    for t in tools_file:
        key = t["name"].lower().strip()
        # Нормализуем для дедупликации
        norm = re.sub(r'[^a-z0-9а-я]', '', key)
        if norm and norm not in seen:
            seen.add(norm)
            t["category"] = "CLI и утилиты"
            t["subcategory"] = t.get("category_from_file", "Без подкатегории")
            merged.append(t)
    
    # Затем из сообщения пользователя
    for t in tools_user:
        key = t["name"].lower().strip()
        norm = re.sub(r'^[^a-z0-9а-я]', '', key)
        if norm and norm not in seen:
            seen.add(norm)
            merged.append(t)
    
    print(f"Источник 1 (инструменты.txt): {len(tools_file)} инструментов")
    print(f"Источник 2 (сообщение): {len(tools_user)} записей")
    print(f"После дедупликации: {len(merged)} уникальных")
    
    # По категориям
    by_cat = {}
    for t in merged:
        c = t.get("category", "?")
        by_cat[c] = by_cat.get(c, 0) + 1
    print("\nПо категориям:")
    for c, n in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {c}")
    
    OUT.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n→ {OUT}")
