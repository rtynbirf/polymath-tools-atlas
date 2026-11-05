#!/usr/bin/env python3
"""
Точечная доразметка:
1. Cloud-сервисы, которые МОГУТ УМЕРЕТЬ — пометить cloud и lifecycle по репутации
2. Legacy-инструменты, которые я пропустил
3. Стек для явных языков
"""
import json
import re
from pathlib import Path

A = Path("/home/z/my-project/scripts/articles_v2.json")
articles = json.loads(A.read_text(encoding="utf-8"))

# ─────────────────────────────────────────────
# 1. CLOUD-сервисы (могут умереть завтра)
# ─────────────────────────────────────────────
CLOUD_MAP = {
    # LLM API
    "chatgpt": ("cloud", "OpenAI"),
    "claude": ("cloud", "Anthropic"),
    "gemini": ("cloud", "Google"),
    "grok": ("cloud", "xAI"),
    "deepseek": ("cloud", "DeepSeek"),
    "mistral le chat": ("cloud", "Mistral AI"),
    "perplexity": ("cloud", "Perplexity"),
    "ernie bot": ("cloud", "Baidu"),
    "hunyuan": ("cloud", "Tencent"),
    "kimi k2": ("cloud", "Moonshot"),
    "kimi docs": ("cloud", "Moonshot"),
    "qwen chat": ("cloud", "Alibaba"),
    "glm/chatglm": ("cloud", "Zhipu"),
    "you.com": ("cloud", "You.com"),
    "genspark": ("cloud", "Genspark"),
    "phind": ("cloud", "Phind"),
    "character.ai": ("cloud", "Character.AI"),
    "poe": ("cloud", "Quora"),
    "huggingchat": ("cloud", "Hugging Face"),
    "pi (inflection)": ("cloud", "Inflection"),
    
    # IDE cloud
    "github copilot": ("cloud", "GitHub/Microsoft"),
    "cursor": ("cloud", "Anysphere"),
    "windsurf": ("cloud", "Codeium"),
    "devin": ("cloud", "Cognition"),
    "replit ghostwriter": ("cloud", "Replit"),
    "amazon codewhisperer": ("cloud", "AWS"),
    "tabnine": ("cloud", "Tabnine"),
    "sourcegraph cody": ("cloud", "Sourcegraph"),
    "mistral le chat": ("cloud", "Mistral"),
    "google antigravity": ("cloud", "Google"),
    "devin desktop": ("cloud", "Cognition"),
    "copilot cli": ("cloud", "GitHub"),
    "qwen code": ("cloud", "Alibaba"),
    
    # Image cloud
    "midjourney": ("cloud", "Midjourney"),
    "dall·e 3": ("cloud", "OpenAI"),
    "dall-e 3": ("cloud", "OpenAI"),
    "gpt image 2": ("cloud", "OpenAI"),
    "adobe firefly": ("cloud", "Adobe"),
    "leonardo.ai": ("cloud", "Leonardo"),
    "ideogram": ("cloud", "Ideogram"),
    "kandinsky": ("cloud", "Sber"),
    "шедеврум": ("cloud", "Yandex"),
    "grok imagine": ("cloud", "xAI"),
    "seedream 4.0": ("cloud", "ByteDance"),
    "imagen 4": ("cloud", "Google"),
    "recraft": ("cloud", "Recraft"),
    "magnific ai": ("cloud", "Magnific"),
    "krea": ("cloud", "Krea"),
    "playground": ("cloud", "Playground"),
    "freepik ai": ("cloud", "Freepik"),
    "photoroom": ("cloud", "Photoroom"),
    "fotor ai": ("cloud", "Fotor"),
    "canva ai": ("cloud", "Canva"),
    "artbreeder": ("cloud", "Artbreeder"),
    "looka": ("cloud", "Looka"),
    "brandmark": ("cloud", "Brandmark"),
    "hatchful": ("cloud", "Shopify"),
    "iconify ai": ("cloud", "Iconify"),
    "nanobanana": ("cloud", "Google"),
    "hidream": ("cloud", "HiDream"),
    
    # Video cloud
    "sora 2": ("cloud", "OpenAI"),
    "sora": ("cloud", "OpenAI"),
    "veo 3": ("cloud", "Google"),
    "veo 3.1": ("cloud", "Google"),
    "kling 2.0": ("cloud", "Kuaishou"),
    "kling 3.0": ("cloud", "Kuaishou"),
    "runway": ("cloud", "Runway"),
    "synthesia": ("cloud", "Synthesia"),
    "heygen": ("cloud", "HeyGen"),
    "d-id": ("cloud", "D-ID"),
    "colossyan": ("cloud", "Colossyan"),
    "invideo ai": ("cloud", "InVideo"),
    "luma dream machine": ("cloud", "Luma"),
    "pika labs": ("cloud", "Pika"),
    "hailuo": ("cloud", "MiniMax"),
    "pixverse": ("cloud", "PixVerse"),
    "wan 2.5": ("cloud", "Alibaba"),
    "wan 2.6": ("cloud", "Alibaba"),
    "wan 2.7": ("cloud", "Alibaba"),
    "seedance": ("cloud", "ByteDance"),
    "happyhorse": ("cloud", "HappyHorse"),
    "wonder studio": ("cloud", "Wonder Dynamics"),
    "deepbrain ai": ("cloud", "DeepBrain"),
    "topview": ("cloud", "Topview"),
    "creatify ai": ("cloud", "Creatify"),
    "zeely ai": ("cloud", "Zeely"),
    "lumen5": ("cloud", "Lumen5"),
    "kapwing": ("cloud", "Kapwing"),
    "veed.io": ("cloud", "Veed"),
    "pictory": ("cloud", "Pictory"),
    "descript": ("cloud", "Descript"),
    "topaz video ai": ("cloud", "Topaz"),
    "capcut ai": ("cloud", "ByteDance"),
    
    # Audio cloud
    "suno ai": ("cloud", "Suno"),
    "udio": ("cloud", "Udio"),
    "elevenlabs": ("cloud", "ElevenLabs"),
    "elevenlabs music": ("cloud", "ElevenLabs"),
    "murf.ai": ("cloud", "Murf"),
    "play.ht": ("cloud", "Play.ht"),
    "naturalreader": ("cloud", "NaturalSoft"),
    "amazon polly": ("cloud", "AWS"),
    "google lyria": ("cloud", "Google"),
    "lovo ai": ("cloud", "Lovo"),
    "synthesys": ("cloud", "Synthesys"),
    "bark": ("cloud", "Suno"),
    "stable audio 3.0": ("cloud", "Stability AI"),
    "soundraw": ("cloud", "Soundraw"),
    "aiva": ("cloud", "AIVA"),
    "amper music": ("cloud", "Amper"),
    "boomy": ("cloud", "Boomy"),
    "soundful": ("cloud", "Soundful"),
    "mureka": ("cloud", "Mureka"),
    "beatoven.ai": ("cloud", "Beatoven"),
    "soundverse": ("cloud", "Soundverse"),
    "treblo": ("cloud", "Treblo"),
    "ace-step": ("cloud", "ACE"),
    "lalal.ai": ("cloud", "Lalal"),
    "moises": ("cloud", "Moises"),
    "krisp": ("cloud", "Krisp"),
    "adobe podcast": ("cloud", "Adobe"),
    "izotope rx": ("cloud", "iZotope"),
    "rask ai": ("cloud", "Rask"),
    "papercup": ("cloud", "Papercup"),
    "happy scribe": ("cloud", "Happy Scribe"),
    "submagic": ("cloud", "Submagic"),
    "zeemo": ("cloud", "Zeemo"),
    "captions.ai": ("cloud", "Captions"),
    "speechify": ("cloud", "Speechify"),
    "voicemod": ("cloud", "Voicemod"),
    "landr": ("cloud", "LANDR"),
    "uberduck": ("cloud", "Uberduck"),
    "rvc ai": ("cloud", "RVC"),
    
    # Transcription cloud
    "otter.ai": ("cloud", "Otter"),
    "fireflies.ai": ("cloud", "Fireflies"),
    "fathom": ("cloud", "Fathom"),
    "tl;dv": ("cloud", "tl;dv"),
    "meetgeek": ("cloud", "MeetGeek"),
    "avoma": ("cloud", "Avoma"),
    "assemblyai": ("cloud", "AssemblyAI"),
    "deepgram": ("cloud", "Deepgram"),
    "speechmatics": ("cloud", "Speechmatics"),
    "whisper api": ("cloud", "OpenAI"),
    "sonix": ("cloud", "Sonix"),
    "castmagic": ("cloud", "Castmagic"),
    "plaud notepin": ("cloud", "Plaud"),
    "bee": ("cloud", "Bee"),
    
    # Documents cloud
    "grammarly": ("cloud", "Grammarly"),
    "languagetool": ("cloud", "LanguageTool"),
    "prowritingaid": ("cloud", "Prowritingaid"),
    "hemingway editor": ("cloud", "Hemingway"),
    "wordtune": ("cloud", "Wordtune"),
    "resoomer": ("cloud", "Resoomer"),
    "scholarcy": ("cloud", "Scholarcy"),
    "quillbot": ("cloud", "QuillBot"),
    "tldr this": ("cloud", "TLDR This"),
    "consensus": ("cloud", "Consensus"),
    "scite.ai": ("cloud", "Scite"),
    "elicit": ("cloud", "Elicit"),
    "frase": ("cloud", "Frase"),
    "surfer ai": ("cloud", "Surfer"),
    "anyword": ("cloud", "Anyword"),
    "surferseo": ("cloud", "SurferSEO"),
    "clearscope": ("cloud", "Clearscope"),
    
    # Presentations
    "gamma": ("cloud", "Gamma"),
    "aippt": ("cloud", "AIPPT"),
    "plus ai": ("cloud", "Plus AI"),
    "deckary": ("cloud", "Deckary"),
    "beautiful.ai": ("cloud", "Beautiful.ai"),
    "tome ai": ("cloud", "Tome"),
    "pitch ai": ("cloud", "Pitch"),
    "slidesgo ai": ("cloud", "Slidesgo"),
    "alai": ("cloud", "Alai"),
    "prezent": ("cloud", "Prezent"),
    "chronicle": ("cloud", "Chronicle"),
    "ludus": ("cloud", "Ludus"),
    "visme": ("cloud", "Visme"),
    
    # Маркетинг
    "mailchimp ai": ("cloud", "Mailchimp"),
    "brevo": ("cloud", "Brevo"),
    "airops": ("cloud", "AirOps"),
    "opus clip": ("cloud", "Opus Clip"),
    "meet sona": ("cloud", "Meet Sona"),
    
    # OCR cloud
    "mistral ocr": ("cloud", "Mistral"),
    "google document ai": ("cloud", "Google"),
    "abbyy finereader": ("cloud", "ABBYY"),
    "adobe scan": ("cloud", "Adobe"),
    "amazon textract": ("cloud", "AWS"),
    "azure document intelligence": ("cloud", "Microsoft"),
    
    # Тесты и платформы
    "quizgecko ai": ("cloud", "Quizgecko"),
    "classmarker ai": ("cloud", "ClassMarker"),
    
    # HR / Business
    "hubspot ai": ("cloud", "HubSpot"),
    "salesforce einstein": ("cloud", "Salesforce"),
    "semrush ai": ("cloud", "SEMrush"),
    "jasper ai": ("cloud", "Jasper"),
    "eightfold ai": ("cloud", "Eightfold"),
    "pymetrics": ("cloud", "Pymetrics"),
    "kasisto": ("cloud", "Kasisto"),
    "alphasense": ("cloud", "AlphaSense"),
    
    # Юрист
    "spellbook": ("cloud", "Spellbook"),
    "robin ai": ("cloud", "Robin AI"),
    "harvey": ("cloud", "Harvey"),
    "cocounsel": ("cloud", "Cocounsel"),
    "luminance": ("cloud", "Luminance"),
    "donotpay": ("cloud", "DoNotPay"),
    "legalzoom": ("cloud", "LegalZoom"),
    "lawgeex": ("cloud", "LawGeex"),
    
    # Недвижимость
    "matterport ai": ("cloud", "Matterport"),
    "cupix": ("cloud", "Cupix"),
    
    # Образование
    "duolingo max": ("cloud", "Duolingo"),
    "khanmigo": ("cloud", "Khan Academy"),
    "socratic": ("cloud", "Google"),
    "scispace": ("cloud", "SciSpace"),
    "connected papers": ("cloud", "Connected Papers"),
    "litmaps": ("cloud", "Litmaps"),
    "researchrabbit": ("cloud", "ResearchRabbit"),
    
    # Здоровье
    "ada health": ("cloud", "Ada Health"),
    "buoy health": ("cloud", "Buoy"),
    "headspace ai": ("cloud", "Headspace"),
    "calm ai": ("cloud", "Calm"),
    "freeletics ai": ("cloud", "Freeletics"),
    "eatthismuch": ("cloud", "EatThisMuch"),
    "plantjammer": ("cloud", "PlantJammer"),
    "chef watson": ("cloud", "IBM"),
    
    # Презентации от cloud-vendors
    "microsoft 365 copilot": ("cloud", "Microsoft"),
    "google workspace ai": ("cloud", "Google"),
    "notion ai": ("cloud", "Notion"),
    "craft ai": ("cloud", "Craft"),
    "clickup ai": ("cloud", "ClickUp"),
    "wps ai": ("cloud", "Kingsoft"),
    "zoho writer": ("cloud", "Zoho"),
    
    # Автоматизация cloud
    "zapier": ("cloud", "Zapier"),
    "make": ("cloud", "Make"),
    "bardeen": ("cloud", "Bardeen"),
    
    # Сайт-генераторы
    "wix ai": ("cloud", "Wix"),
    "framer ai": ("cloud", "Framer"),
    "durable ai": ("cloud", "Durable"),
    "10web": ("cloud", "10Web"),
    "teleporthq": ("cloud", "TeleportHQ"),
    "v0 by vercel": ("cloud", "Vercel"),
    "shopify ai": ("cloud", "Shopify"),
    "ecwid ai": ("cloud", "Ecwid"),
    "flutterflow ai": ("cloud", "FlutterFlow"),
    "adalo ai": ("cloud", "Adalo"),
    "glide ai": ("cloud", "Glide"),
    "figma ai": ("cloud", "Figma"),
    "uizard": ("cloud", "Uizard"),
    "galileo ai": ("cloud", "Galileo"),
    "locofy ai": ("cloud", "Locofy"),
    
    # БД cloud
    "pinecone": ("cloud", "Pinecone"),
    "turso": ("cloud", "Turso"),
    
    # Observability cloud
    "langsmith": ("cloud", "LangChain"),
    "braintrust": ("cloud", "Braintrust"),
    "helicone": ("cloud", "Helicone"),
    
    # Безопасность cloud
    "lakera guard": ("cloud", "Lakera"),
    "lasso security": ("cloud", "Lasso"),
    
    # Synth data cloud
    "gretel.ai": ("cloud", "Gretel"),
    "tonic.ai": ("cloud", "Tonic"),
    "mostly ai": ("cloud", "Mostly AI"),
    "mockaroo ai": ("cloud", "Mockaroo"),
    
    # Прочее cloud
    "deepware scanner": ("cloud", "Deepware"),
    "hive moderation": ("cloud", "Hive"),
    "originality ai": ("cloud", "Originality"),
    "copyleaks": ("cloud", "Copyleaks"),
    "copyscape": ("cloud", "Copyscape"),
    
    # Voice cloud
    "vapi ai": ("cloud", "Vapi"),
    "retell ai": ("cloud", "Retell"),
    "openai realtime api": ("cloud", "OpenAI"),
    
    # Browser cloud
    "skyvern": ("cloud", "Skyvern"),
    
    # 3D cloud
    "meshy": ("cloud", "Meshy"),
    "tripo ai": ("cloud", "Tripo"),
    "rodin": ("cloud", "Rodin"),
    "luma ai capture": ("cloud", "Luma"),
    "kaedim": ("cloud", "Kaedim"),
    "masterpiece studio": ("cloud", "Masterpiece"),
    "spline ai": ("cloud", "Spline"),
    "scenario": ("cloud", "Scenario"),
    "layer.ai": ("cloud", "Layer"),
    "rosebud ai": ("cloud", "Rosebud"),
    "inworld ai": ("cloud", "Inworld"),
    "cascadeur": ("cloud", "Cascadeur"),
    "move ai": ("cloud", "Move AI"),
    "rokoko": ("cloud", "Rokoko"),
    "deep motion": ("cloud", "Deep Motion"),
    "nvidia omniverse": ("cloud", "NVIDIA"),
}

# Применяем cloud-разметку
marked_cloud = 0
for a in articles:
    name_lower = a["forma"]["name"].lower().strip()
    # Проверяем по подстроке
    for key, (auto, vendor) in CLOUD_MAP.items():
        if key in name_lower:
            if a["forma"].get("autonomy") in ("hybrid", "Mixed", ""):
                a["forma"]["autonomy"] = auto
                if not a["forma"].get("vendor"):
                    a["forma"]["vendor"] = vendor
                marked_cloud += 1
                break

print(f"Помечено cloud: {marked_cloud}")

# ─────────────────────────────────────────────
# 2. Дополнительная разметка стека
# ─────────────────────────────────────────────
STACK_RULES = [
    (r"\b(rust|cargo|crates\.io|на rust|rust-)", "Rust"),
    (r"\b(python|pip|django|flask|pydantic|pandas|numpy)", "Python"),
    (r"\b(golang|go-|lazygit|lazydocker|fzf|caddy)", "Go"),
    (r"\b(zig|bun|ghostty)", "Zig"),
    (r"\b(c\+\+|cpp|qt)", "C++"),
    (r"\b(typescript|node\.js|deno|nuxt|next\.js|svelte|react|vue)", "TypeScript"),
    (r"\b(c#|dotnet|\.net|wpf)", "C#"),
    (r"\b(ocaml|reasonml)", "OCaml"),
    (r"\b(php|laravel|symfony)", "PHP"),
    (r"\b(ruby|rails)", "Ruby"),
    (r"\b(perl)", "Perl"),
    (r"\b(c\b|ansi c|glibc|posix)", "C"),
]

for a in articles:
    if a["forma"].get("stack") in ("Mixed", ""):
        text = (a["forma"]["name"] + " " + (a.get("noise", [{}])[0].get("claim", "") if a.get("noise") else "")).lower()
        for pattern, stack in STACK_RULES:
            if re.search(pattern, text):
                a["forma"]["stack"] = stack
                break

# ─────────────────────────────────────────────
# 3. Lifecycle — точечная разметка
# ─────────────────────────────────────────────
LIFECYCLE_RULES = {
    # maintenance — забытые, но работают
    "ack": "maintenance",
    "tig": "maintenance", 
    "ranger": "maintenance",
    "fff": "maintenance",
    " Automatic1111": "maintenance",
    "fooocus": "maintenance",
    "text-generation-webui": "maintenance",
    "neofetch": "maintenance",  # заброшен автором
    "httpie": "maintenance",
    "exa": "maintenance",  # переименован в eza
    "coqui tts": "maintenance",  # компания закрылась
    "rye": "maintenance",  # автор рекомендует uv
    
    # archived/dead
    "pymetrics": "maintenance",
}

for a in articles:
    name_lower = a["forma"]["name"].lower().strip()
    for key, life in LIFECYCLE_RULES.items():
        if key.lower() in name_lower and a["forma"].get("lifecycle") == "active":
            a["forma"]["lifecycle"] = life

# Сохранить
A.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")

# Статистика финальная
from collections import Counter
stack_stats = Counter(a["forma"].get("stack", "?") for a in articles)
auto_stats = Counter(a["forma"].get("autonomy", "?") for a in articles)
life_stats = Counter(a["forma"].get("lifecycle", "?") for a in articles)

print(f"\nИтого: {len(articles)} статей")
print("\nПо стеку:")
for k, n in stack_stats.most_common():
    print(f"  {n:4d}  {k}")
print("\nПо автономности:")
for k, n in auto_stats.most_common():
    print(f"  {n:4d}  {k}")
print("\nПо жизненному циклу:")
for k, n in life_stats.most_common():
    print(f"  {n:4d}  {k}")

# Сколько supersedes заполнено
n_supersedes = sum(1 for a in articles if a["forma"].get("supersedes"))
print(f"\nС supersedes (что заменяет): {n_supersedes}")
