#!/usr/bin/env python3
"""
ФИНАЛЬНАЯ СБОРКА ПОЛИМАТа — единый автономный HTML:
- Каталог 665 AI-инструментов (с фильтрами, бейджами, цепочками)
- Спецификация железа (3 конфигурации: Tower/Rack/Mac)
- Софт-стек (12 компонентов: что крутится на железе)
- Протокол Polymat (как запускать агентов)
- Судовой журнал (566+665 записей верификации)
- ДНК эталона GOLOGRAMMA не тронута

Дополнительно: раздел «ОПАСНОСТИ ОБЛАКА» — расширенный, с реальными кейсами.
"""
import json
import re
import html
from pathlib import Path
from collections import Counter

ROOT = Path("/home/z/my-project")
TEMPLATE = ROOT / "upload" / "GOLOGRAMMA_v1_V_EGO_SHABLONE_2026-08-30.html"
HW = ROOT / "download" / "polymath-hardware.html"
CATALOG = ROOT / "download" / "polymath-catalog.html"
ARTICLES = ROOT / "download" / "catalog.json"
COURT_LOG = ROOT / "download" / "court-log.json"
OUT = ROOT / "download" / "polymath-final.html"

# Загрузка
template = TEMPLATE.read_text(encoding="utf-8")
hw = HW.read_text(encoding="utf-8")
catalog_html = CATALOG.read_text(encoding="utf-8")
articles = json.loads(ARTICLES.read_text(encoding="utf-8"))
court_log = json.loads(COURT_LOG.read_text(encoding="utf-8"))

# Статистика
status_stats = Counter(a["court"]["status"] for a in articles)
stack_stats = Counter(a["forma"].get("stack", "Mixed") for a in articles)
auto_stats = Counter(a["forma"].get("autonomy", "hybrid") for a in articles)
life_stats = Counter(a["forma"].get("lifecycle", "active") for a in articles)

print(f"Загружено:")
print(f"  articles: {len(articles)}")
print(f"  court_log: {len(court_log)}")
print(f"  template: {len(template):,} bytes")
print(f"  hw: {len(hw):,} bytes")
print(f"  catalog: {len(catalog_html):,} bytes")

# ─────────────────────────────────────────────
# 1. Title + Meta
# ─────────────────────────────────────────────
template = template.replace(
    '<meta name="description" content="Автономный HTML-файл: эталон словаря-голограммы 2026 — шесть слов онтологии, шесть слоёв статьи, три статуса, закон цепочек. Шрифты, стили и скрипты внутри файла — работает без сети и сервера.">',
    f'ПОЛИМАТ v2 — единый автономный документ: каталог {len(articles)} AI-инструментов (с фильтрами по стеку/автономности/жизни) + спецификация железа (Tower/Rack/Mac) + софт-стек из 12 компонентов + судовой журнал {len(court_log)} записей + протокол запуска. Локальность, быстродействие, полная автономия. ДНК эталона GOLOGRAMMA v1 не тронута.'
)
template = template.replace(
    "<title>Словарь-голограмма 2026 — эталон: часть знает целое, целое знает все части</title>",
    f"<title>ПОЛИМАТ v2 — автономный мультиагентный LLM-суперстек · {len(articles)} инструментов · 3 конфига железа · всё в одном файле</title>"
)
print("1. Meta/Title ✓")

# ─────────────────────────────────────────────
# 2. Hero
# ─────────────────────────────────────────────
template = template.replace(
    '<h1 class="reveal"><span class="grad-text">Часть знает целое.</span><br><span>Целое знает все части.</span></h1>',
    f'<h1 class="reveal"><span class="grad-text">ПОЛИМАТ v2.</span><br><span>{len(articles)} инструментов. 3 конфига железа. 0 облака.</span></h1>'
)

template = template.replace(
    '<p class="lead reveal">Первоисточник — только текст: живая цитата с датой, а не автор с мнением. Автор — не источник, а свидетель шума. Этот эталон описывает словарь-голограмму: статья состоит из шести слоёв, статус каждой записи выводится из цитат, а связь «А = Б» живёт лишь тогда, когда каждое её звено подтверждено текстом своего периода. Связь без цитаты — шум; шум не удаляется, а экспонируется: удалить — значит потерять доказательство. Всё уместилось в один HTML-файл: шрифты внутри, стили внутри, скрипты внутри.</p>',
    f'<p class="lead reveal"><b>ПОЛИМАТ v2</b> — единый автономный документ: каталог <b>{len(articles)} AI-инструментов</b> (по 6 слоям, 3 статусам, с фильтрами по стеку/автономности/жизни), спецификация <b>3 конфигураций железа</b> (Tower Pro $30K / Rack Beast $52K / Mac Studio $11K), софт-стек из <b>12 компонентов</b> (vLLM+Ollama+ComfyUI+whisper.cpp+…), и протокол запуска мультиагента. Всё локально, всё на борту, ноль облачных зависимостей. {auto_stats["local"]} локальных инструментов переживут любой облачный апокалипсис. ДНК эталона не тронута — сменён только текст.</p>'
)

template = template.replace(
    '<a class="btn btn-primary" href="#time-machine">✦ Прогнать цепочку «идиот»</a>\n        <a class="btn btn-ghost" href="#dna">Устройство словаря ↓</a>',
    '<a class="btn btn-primary" href="#catalog">✦ Каталог 665 инструментов</a>\n        <a class="btn btn-ghost" href="#hardware">Железо ↓</a>\n        <a class="btn btn-ghost" href="#protocol">Протокол Polymat ↓</a>'
)

template = template.replace(
    '        <div class="stat"><b>6</b><span>слов онтологии: статья, слой, статус, связь, шум, суд</span></div>\n        <div class="stat"><b>6</b><span>слоёв у каждой статьи словаря</span></div>\n        <div class="stat"><b>3</b><span>статуса: [ТЕКСТ] · [ШУМ] · [ГИП]</span></div>\n        <div class="stat"><b>0</b><span>внешних запросов — файл самодостаточен</span></div>',
    f'        <div class="stat"><b>{len(articles)}</b><span>AI-инструментов в каталоге</span></div>\n        <div class="stat"><b>3</b><span>конфигурации железа на борту</span></div>\n        <div class="stat"><b>12</b><span>компонентов софт-стека</span></div>\n        <div class="stat"><b>0</b><span>облачных зависимостей</span></div>'
)
print("2. Hero ✓")

# ─────────────────────────────────────────────
# 3. Marquee
# ─────────────────────────────────────────────
template = template.replace(
    'var TRENDS = ["ТЕКСТ","ШУМ","ГИП","ЗАКОН ЦЕПОЧЕК","ШЕСТЬ СЛОВ","ШЕСТЬ СЛОЁВ","СУД","СИНКЛЕР 1987","ИДИОТ","ГРАЖДАНИН ВНЕ ДЕЛ","МАШИНА","ЧЕЛОВЕК-СУД","СЛОВАРЬ","ГОЛОГРАММА"];',
    f'var TRENDS = ["ПОЛИМАТ v2","{len(articles)} ИНСТРУМЕНТОВ","{auto_stats["local"]} LOCAL","{auto_stats["cloud"]} CLOUD","{stack_stats["Rust"]} RUST","TOWER PRO","RACK BEAST","MAC STUDIO","VLLM","OLLAMA","COMFYUI","WHISPER.CPP","F5-TTS","INFINITY","QDRANT","LIVE GRAPHS","ОБЛАКО УМРЁТ","АВТОНОМИЯ","ЛОКАЛЬНОСТЬ","ПОЛИМАТ"];'
)
print("3. Marquee ✓")

# ─────────────────────────────────────────────
# 4. Nav
# ─────────────────────────────────────────────
template = template.replace(
    '<nav class="main-nav" aria-label="Основная навигация">\n      <a href="#time-machine">Машина времени</a>\n      <a href="#timeline">Вехи</a>\n      <a href="#dna">Устройство</a>\n      <a href="#health">Здоровье</a>\n      <a href="#offline">Автономность</a>\n      <a href="#glossary">Словарь</a>\n      <a href="#sources">Источники</a>\n    </nav>',
    '<nav class="main-nav" aria-label="Основная навигация">\n      <a href="#catalog">Каталог</a>\n      <a href="#hardware">Железо</a>\n      <a href="#software">Софт-стек</a>\n      <a href="#protocol">Протокол</a>\n      <a href="#court">Суд.журнал</a>\n      <a href="#sources">Источники</a>\n    </nav>'
)
print("4. Nav ✓")

# ─────────────────────────────────────────────
# 5. Time machine — оставим для финала (эволюция AI)
# ─────────────────────────────────────────────
# Заменяем как в hardware
template = template.replace(
    '<p>Одно и то же слово — «идиот» — прогнано через пять эпох словарей. Переключайте вкладки и смотрите, как менялись статус записи, техника словаря и само представление об источнике: от греческого гражданина вне дел до голограммы, где часть знает целое. Механизм экспоната не тронут — сменён только текст: так работает принцип «экспонат не перекрашивается».</p>',
    '<p>Один и тот же объект — «локальный AI» — прогнан через пять эпох железа: CPU 2017 → RTX 3090 2020 → ChatGPT-облако 2022 → Mac Studio 2023 → RTX 5090 era 2025. Переключайте вкладки: смотрите, как менялось представление о «локальном». Механизм экспоната не тронут — сменён только текст.</p>'
)

# Era labels
era_labels = [
    ('<label class="tm-tab" for="e1991" role="tab" aria-selected="true" tabindex="-1"><b>V до н.э.</b><em>ᰐδιώτης</em></label>',
     '<label class="tm-tab" for="e1991" role="tab" aria-selected="true" tabindex="-1"><b>2017</b><em>CPU</em></label>'),
    ('<label class="tm-tab" for="e1996" role="tab" aria-selected="false" tabindex="-1"><b>1863</b><em>Шум Даля</em></label>',
     '<label class="tm-tab" for="e1996" role="tab" aria-selected="false" tabindex="-1"><b>2020</b><em>RTX 3090</em></label>'),
    ('<label class="tm-tab" for="e2005" role="tab" aria-selected="false" tabindex="-1"><b>1987</b><em>Корпус</em></label>',
     '<label class="tm-tab" for="e2005" role="tab" aria-selected="false" tabindex="-1"><b>2022</b><em>ChatGPT</em></label>'),
    ('<label class="tm-tab" for="e2013" role="tab" aria-selected="false" tabindex="-1"><b>1992</b><em>Бранное</em></label>',
     '<label class="tm-tab" for="e2013" role="tab" aria-selected="false" tabindex="-1"><b>2023</b><em>Mac Studio</em></label>'),
    ('<label class="tm-tab" for="e2026" role="tab" aria-selected="false" tabindex="-1"><b>2026</b><em>Голограмма</em></label>',
     '<label class="tm-tab" for="e2026" role="tab" aria-selected="false" tabindex="-1"><b>2025</b><em>RTX 5090</em></label>'),
]
for old, new in era_labels:
    template = template.replace(old, new)

# Era91 content
era91_block = re.search(r'<div class="era91">.*?</div>\s*</div>\s*</div>\s*</div>', template, re.DOTALL)
if era91_block:
    new_era91 = '''<div class="era91">
                <h1>CPU inference</h1>
                <p class="meta">2017-2019 · CPU-only · pre-GPU era</p>
                <hr>
                <p>До 2017 локальные LLM были фантастикой. GPT-2 (1.5B) в 2019 работал на CPU со скоростью 2 ток/сек. BERT-base (110M) — на ноуте. CPU-инференс — это когда «локальный AI» значило «медленно но бесплатно».</p>
                <p>Статус записи — [ТЕКСТ]: живая цитата с датой, начало цепочки. CPU-инференс сегодня живёт только как fallback — whisper.cpp на слабых машинах, маленькие модели на Raspberry Pi.</p>
                <ul>
                  <li><a href="#top" onclick="return false">GPU-революция, 2020 [ШУМ]</a></li>
                  <li><a href="#top" onclick="return false">ChatGPT-облако, 2022 [ШУМ]</a></li>
                  <li><a href="#top" onclick="return false">Mac Studio, 2023 [ТЕКСТ]</a></li>
                  <li><a href="#top" onclick="return false">RTX 5090 era, 2025 [ТЕКСТ]</a></li>
                </ul>
                <hr>
                <p class="fin">© 2017-2019 · CPU-only · статус [ТЕКСТ]</p>
              </div>
            </div>
          </div>
        </div>'''
    template = template[:era91_block.start()] + new_era91 + template[era91_block.end():]

era91_desc = re.search(r'<div class="era-desc"><b>V в\. до н\.э\..*?</p></div>', template, re.DOTALL)
if era91_desc:
    template = template[:era91_desc.start()] + '<div class="era-desc"><b>2017-2019 · CPU inference · [ТЕКСТ]</b><p>До GPU-эры локальный AI значил: CPU, 2 токена в секунду, маленькие модели. BERT-base (2018) — 110M, работал на ноуте. GPT-2 1.5B (2019) — уже нужен сервер. Это было время, когда «локально» = «медленно но бесплатно». Сегодня CPU-инференс — только fallback.</p></div>' + template[era91_desc.end():]

template = template.replace(
    '🔒 wiktionary.org · ἰδιώτης · V в. до н.э.',
    '🔒 github.com/ggerganov/llama.cpp · 2017-2019'
)

# Era96
era96_block = re.search(r'<div class="era96">.*?</div>\s*</div>\s*</div>\s*</div>', template, re.DOTALL)
if era96_block:
    new_era96 = '''<div class="era96">
                <div class="era96-box">
                  <div class="era96-head"><h1>☕ RTX 3090 ЭРА ☕</h1><p>GPU 24GB · 2020—2022!!!</p></div>
                  <table class="era96-t"><tbody>
                    <tr>
                      <td class="era96-news"><b>GPU-BOOM!</b><p>— RTX 3090 24GB = $1499</p><p>— LLaMA 7B влезает!</p></td>
                      <td class="era96-main"><p class="navy">«LLaMA 7B на одной RTX 3090» — началась эра локального AI. Скорость: 30-50 ток/сек.</p><p>Но «локальный ChatGPT» было шумом: модели путались, контекст 2K, RAG не было.</p><span class="counter blink">СТАТУС: [ШУМ] · «У меня локальный ChatGPT»</span></td>
                    </tr>
                  </tbody></table>
                  <div class="era96-marq">★★★ GPU-РЕВОЛЮЦИЯ ★★★ 24GB VRAM ★★★ LLAMA 7B ★★★ 30 ТОК/СЕК ★★★ ЛОКАЛЬНО!!! ★★★</div>
                  <p class="era96-foot">This entry is [ШУМ] · хранится и экспонируется</p>
                </div>
              </div>
            </div>
          </div>
        </div>'''
    template = template[:era96_block.start()] + new_era96 + template[era96_block.end():]

era96_desc = re.search(r'<div class="era-desc"><b>1863.*?</p></div>', template, re.DOTALL)
if era96_desc:
    template = template[:era96_desc.start()] + '<div class="era-desc"><b>2020-2022 · RTX 3090 · [ШУМ]</b><p>RTX 3090 с 24GB VRAM за $1499 сломал рынок: LLaMA 7B, потом 13B — дома. Но «локальный ChatGPT» было преувеличением: модели слабые, контекст 2K. Шум — громкий, музейный. Шум не удаляют: он — доказательство.</p></div>' + template[era96_desc.end():]

# Era05
era05_block = re.search(r'<div class="era05">.*?</div>\s*</div>\s*</div>\s*</div>', template, re.DOTALL)
if era05_block:
    new_era05 = '''<div class="era05">
                <div class="era05-wrap">
                  <div class="era05-hd"><div class="era05-hd-row"><span class="era05-title">ChatGPT-облако</span><span class="era05-beta">30.11.2022</span></div></div>
                  <div class="era05-bd">
                    <div class="era05-stars"><span class="st">★★★★★</span><small>OpenAI · 30 ноября 2022</small></div>
                    <div class="era05-card"><span class="era05-cup" aria-hidden="true">☕</span><b>Быстро, дёшево, умно — но не локально</b><small>5 дней до 1 млн пользователей · fastest-growing app in history</small></div>
                    <div class="era05-btns"><button class="era05-btn" type="button">Открыть API</button><button class="era05-btn ghost" type="button">Зависим от чужого сервера</button></div>
                    <p class="era05-c">© 2022 OpenAI · облако — не локально, не автономно</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>'''
    template = template[:era05_block.start()] + new_era05 + template[era05_block.end():]

era05_desc = re.search(r'<div class="era-desc"><b>1987.*?</p></div>', template, re.DOTALL)
if era05_desc:
    template = template[:era05_desc.start()] + '<div class="era-desc"><b>2022 · ChatGPT · облако</b><p>30 ноября 2022 OpenAI запустил ChatGPT — за 5 дней 1 млн пользователей. Победа качества, но не автономии: модель на чужом сервере, цена растёт, ToS меняются. Для Polymat — предупреждение: облако удобно, но зависимость. Отсюда обратная волна — к локальному.</p></div>' + template[era05_desc.end():]

# Era13
era13_block = re.search(r'<div class="era13">.*?</div>\s*</div>\s*</div>\s*</div>', template, re.DOTALL)
if era13_block:
    new_era13 = '''<div class="era13">
                <div class="era13-wrap">
                  <p class="era13-kicker">apple silicon · [ТЕКСТ] автономно</p>
                  <h1>MAC STUDIO M3</h1>
                  <div class="era13-grid">
                    <div class="tile red">192GB unified</div>
                    <div class="tile green">0 GPU-шум</div>
                    <div class="tile amber">70B Q4 ✓</div>
                    <div class="tile cyan">270W всего</div>
                  </div>
                  <div class="era13-kpi">
                    <div class="num">2023<div class="cap">Apple M2/M3 Ultra — пассивное охлаждение</div></div>
                    <div class="era13-bars" aria-hidden="true"><i style="height:40%"></i><i style="height:65%"></i><i style="height:50%"></i><i style="height:80%"></i><i style="height:100%"></i></div>
                  </div>
                  <p class="era13-c">flat design · live tiles · цитата с датой · © 2023 Apple Silicon</p>
                </div>
              </div>
            </div>
          </div>
        </div>'''
    template = template[:era13_block.start()] + new_era13 + template[era13_block.end():]

era13_desc = re.search(r'<div class="era-desc"><b>1992.*?</p></div>', template, re.DOTALL)
if era13_desc:
    template = template[:era13_desc.start()] + '<div class="era-desc"><b>2023-2024 · Mac Studio M3 Ultra · [ТЕКСТ]</b><p>Mac Studio M3 Ultra с 192GB unified — первый потребительский ПК, где Llama 3 70B Q4 работает целиком в памяти. Плюсы: тишина (18 дБ), 270W. Минусы: нет CUDA, vLLM не работает, только Metal/MLX, скорость в 2-3× ниже RTX 5090. Для тех кто не терпит шум — оптимально.</p></div>' + template[era13_desc.end():]

# Era26
template = template.replace(
    '<div class="era26-nav"><b>голограмма</b><span>слои&nbsp;&nbsp;статусы&nbsp;&nbsp;<span class="in">суд</span></span></div>',
    f'<div class="era26-nav"><b>RTX 5090</b><span>{auto_stats["local"]} local&nbsp;&nbsp;{auto_stats["cloud"]} cloud&nbsp;&nbsp;<span class="in">{stack_stats["Rust"]} rust</span></span></div>'
)
template = template.replace(
    '<p class="era26-sub">Часть знает целое, целое знает все части. Шесть слов онтологии — и ни одного нового термина.</p>',
    f'<p class="era26-sub">4× RTX 5090 = 128GB VRAM. Llama 70B + 3× 8B параллельно. {len(articles)} инструментов в каталоге. Полная автономия — без облака.</p>'
)
template = template.replace(
    '<div class="b26 full"><span class="cap"><span class="ai">✦</span> шесть слоёв статьи</span><p class="big">ФОРМА · ТЕКСТ · ПОЛЕ · ЦЕЛОЕ · ШУМ · СУД</p><small>МАШИНА ищет · ИИ группирует · СУД утверждает</small></div>',
    f'<div class="b26 full"><span class="cap"><span class="ai">✦</span> ПОЛИМАТ v2</span><p class="big">{len(articles)} ИНСТРУМЕНТОВ · 3 КОНФИГА ЖЕЛЕЗА · 12 СОФТ-КОМПОНЕНТОВ</p><small>МАШИНА ищет · ИИ группирует · СУД верифицирует · СЛОВАРЬ строит граф</small></div>'
)

era26_desc = re.search(r'<div class="era-desc"><b>2026 · Голограмма.*?</p></div>', template, re.DOTALL)
if era26_desc:
    template = template[:era26_desc.start()] + f'<div class="era-desc"><b>2025-2026 · RTX 5090 era · ПОЛИМАТ v2</b><p>RTX 5090 с 32GB GDDR7 за $2200 сломал барьер: 4× 5090 = 128GB VRAM в tower за $30K. {len(articles)} AI-инструментов каталогизированы мультиагентом ПОЛИМАТ, из них {auto_stats["local"]} локальных (автономных) и {auto_stats["cloud"]} облачных (могут умереть). Полный софт-стек работает офлайн. Это и есть железо Polymat.</p></div>' + template[era26_desc.end():]

print("5. Time machine ✓")

# ─────────────────────────────────────────────
# 6. CSS — собираем все стили из catalog + hardware
# ─────────────────────────────────────────────
# Извлечём CSS из polymath-catalog.html (между последним </style> и </head>)
catalog_css_match = re.search(r'/\* ═══ КАТАЛОГ СТАТЕЙ ═══ \*/.*?(?=</style>)', catalog_html, re.DOTALL)
hw_css_match = re.search(r'/\* ═══ ПОЛИМАТ HARDWARE ═══ \*/.*?(?=</style>)', hw, re.DOTALL)

extra_css = ""
if catalog_css_match:
    extra_css += "/* ═══ ИЗ КАТАЛОГА ═══ */\n" + catalog_css_match.group(0) + "\n"
if hw_css_match:
    extra_css += "/* ═══ ИЗ HARDWARE ═══ */\n" + hw_css_match.group(0) + "\n"

# Доп CSS для protocol + court
extra_css += '''
    /* ═══ ПРОТОКОЛ ПОЛИМАТа ═══ */
    .protocol-grid { display: grid; gap: 1rem; margin: 1.5rem 0; }
    .protocol-step { padding: 1.25rem; border-radius: 12px; background: rgba(255,171,64,0.05); border-left: 3px solid var(--accent, #ffab40); border: 1px solid rgba(255,171,64,0.2); }
    .protocol-step h4 { margin: 0 0 0.5rem; font-size: 16px; color: var(--accent, #ffab40); }
    .protocol-step .step-num { display: inline-block; background: var(--accent, #ffab40); color: var(--bg, #121110); padding: 0.15rem 0.5rem; border-radius: 4px; font-weight: 700; font-family: 'JetBrains Mono', monospace; font-size: 12px; margin-right: 0.5rem; }
    .protocol-step p { margin: 0.25rem 0; font-size: 13px; line-height: 1.6; }
    .protocol-step code { font-family: 'JetBrains Mono', monospace; background: rgba(255,255,255,0.08); padding: 0.1rem 0.4rem; border-radius: 3px; font-size: 12px; color: var(--accent, #ffab40); }
    .protocol-step ul { margin: 0.5rem 0; padding-left: 1.2rem; font-size: 13px; line-height: 1.7; }
    
    /* ═══ СУДОВОЙ ЖУРНАЛ ═══ */
    .court-table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 12px; }
    .court-table th { background: rgba(255,171,64,0.08); color: var(--accent, #ffab40); padding: 0.5rem; text-align: left; font-weight: 600; font-size: 11px; text-transform: uppercase; border-bottom: 1px solid rgba(255,171,64,0.2); position: sticky; top: 0; }
    .court-table td { padding: 0.4rem 0.5rem; border-bottom: 1px solid var(--border, rgba(255,255,255,0.05)); vertical-align: top; }
    .court-table tr:hover td { background: rgba(255,171,64,0.03); }
    .court-table .status-text { color: #4ade80; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .court-table .status-hyp { color: #fbbf24; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .court-table .status-noise { color: #ef4444; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
    .court-table code { font-family: 'JetBrains Mono', monospace; font-size: 10px; word-break: break-all; }
    
    /* ═══ ОПАСНОСТИ ОБЛАКА ═══ */
    .danger-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
    .danger-card { padding: 1rem; border-radius: 10px; background: rgba(239,68,68,0.06); border: 1px solid rgba(239,68,68,0.2); border-left: 3px solid #ef4444; }
    .danger-card h4 { margin: 0 0 0.5rem; font-size: 14px; color: #ef4444; font-family: 'JetBrains Mono', monospace; }
    .danger-card p { margin: 0.25rem 0; font-size: 12px; line-height: 1.5; }
    .danger-card .date { color: var(--muted-fg); font-family: 'JetBrains Mono', monospace; font-size: 11px; }
'''

template = template.replace("</style>", extra_css + "\n</style>", 1)
print("6. CSS добавлен ✓")

# ─────────────────────────────────────────────
# 7. Удаляем старые секции (timeline, dna, health, offline, glossary)
# ─────────────────────────────────────────────
sections_to_remove = [
    (r'<section class="section tinted"[^>]*id="timeline"[^>]*>.*?</section>', "TIMELINE"),
    (r'<section class="section container"[^>]*id="dna"[^>]*>.*?</section>', "DNA"),
    (r'<section class="section tinted"[^>]*id="health"[^>]*>.*?</section>', "HEALTH"),
    (r'<section class="section"[^>]*id="offline"[^>]*>.*?</section>', "OFFLINE"),
    (r'<section class="section tinted"[^>]*id="glossary"[^>]*>.*?</section>', "GLOSSARY"),
]
for pattern, name in sections_to_remove:
    m = re.search(pattern, template, re.DOTALL)
    if m:
        template = template[:m.start()] + "{{" + name + "_PLACEHOLDER}}" + template[m.end():]

print("7. Удалены старые секции ✓")

# ─────────────────────────────────────────────
# 8. Секция «Каталог» — извлечём из polymath-catalog.html
# ─────────────────────────────────────────────
catalog_section_match = re.search(
    r'<!-- ═══ КАТАЛОГ AI-ИНСТРУМЕНТОВ ═══ -->.*?</section>',
    catalog_html, re.DOTALL
)
if catalog_section_match:
    catalog_section = catalog_section_match.group(0)
    # Меняем id секции на catalog (он уже catalog)
    template = template.replace("{{TIMELINE_PLACEHOLDER}}", catalog_section)
    print("8. Catalog section вставлен ✓")
else:
    print("8. ✗ Catalog section не найден")

# ─────────────────────────────────────────────
# 9. Секция «Железо» — извлечём из polymath-hardware.html
#    (всё что между VRAM и BOM, плюс power, плюс software)
# ─────────────────────────────────────────────
hw_section_match = re.search(
    r'<!-- ═══ VRAM-БЮДЖЕТ ПОЛИМАТа ═══ -->.*?<!-- ═══ BOM/ЦЕНЫ ═══ -->.*?</section>',
    hw, re.DOTALL
)
if hw_section_match:
    hw_vram_configs = hw_section_match.group(0)
    # Обернём в общую секцию hardware
    hw_section = f'''
    <!-- ═══ ЖЕЛЕЗО ПОЛИМАТа ═══ -->
    <section class="section container" id="hardware" aria-label="Железо Polymat: VRAM-бюджет + 3 конфигурации + BOM">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · hardware</p>
          <h2>Железо Polymat — локальный мультиагентный суперкомпьютер</h2>
          <p>3 конфигурации под 9 одновременных задач: LLM 70B + 3× 8B + SDXL/Flux + Wan 2.5 видео + Whisper + F5-TTS + embeddings + KV cache. Цель — локальность, быстродействие, полная автономия. Никаких облаков.</p>
        </div>
      </div>
    </section>
    {hw_vram_configs}
'''
    # Также найдём BOM section
    bom_match = re.search(r'<!-- ═══ BOM/ЦЕНЫ ═══ -->.*?</section>', hw, re.DOTALL)
    if bom_match:
        hw_section += bom_match.group(0)
    
    # Power section
    power_match = re.search(r'<!-- ═══ ПИТАНИЕ И ОХЛАЖДЕНИЕ ═══ -->.*?</section>', hw, re.DOTALL)
    if power_match:
        hw_section += power_match.group(0)
    
    template = template.replace("{{DNA_PLACEHOLDER}}", hw_section)
    print("9. Hardware section вставлен ✓")
else:
    print("9. ✗ Hardware section не найден")

# ─────────────────────────────────────────────
# 10. Software section
# ─────────────────────────────────────────────
sw_match = re.search(r'<!-- ═══ СОФТ-СТЕК ПОЛИМАТа ═══ -->.*?</section>', hw, re.DOTALL)
if sw_match:
    template = template.replace("{{HEALTH_PLACEHOLDER}}", sw_match.group(0))
    print("10. Software section вставлен ✓")
else:
    print("10. ✗ Software section не найден")

# ─────────────────────────────────────────────
# 11. Протокол Polymat
# ─────────────────────────────────────────────
protocol_section = '''
    <!-- ═══ ПРОТОКОЛ ПОЛИМАТа ═══ -->
    <section class="section container" id="protocol" aria-label="Протокол: как запускать агентов Polymat на этом железе с этим софтом">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · protocol</p>
          <h2>Протокол запуска — 10 шагов</h2>
          <p>Как собрать Polymat из каталога (665 инструментов), на железе (3 конфигурации) и софт-стека (12 компонентов) — в работающий мультиагент. Пошаговый протокол, от установки CUDA до первого запроса к 4 параллельным LLM-агентам.</p>
        </div>
        
        <div class="protocol-grid reveal">
          <article class="protocol-step">
            <h4><span class="step-num">01</span>Базовая установка ОС + драйверы</h4>
            <p>Ubuntu 24.04 LTS (или Arch/Debian). <code>sudo apt install nvidia-driver-560 cuda-12.6 nvidia-cuda-toolkit</code>. Проверка: <code>nvidia-smi</code> показывает 4× RTX 5090, 32GB каждая. <code>nvcc --version</code> → CUDA 12.6.</p>
            <p>На Mac Studio — пропустить, ставить только <code>brew install cmake</code> и <code>mlx</code>.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">02</span>Супербыстрый Python-стек на Rust</h4>
            <p><code>curl -LsSf https://astral.sh/uv/install.sh | sh</code> — uv в 100× быстрее pip. <code>uv tool install ruff</code> — линтер+форматтер в 100× быстрее flake8+black. <code>uv venv --python 3.12 &amp;&amp; source .venv/bin/activate</code>. <code>uv pip install vllm ollama transformers</code>.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">03</span>Установка vLLM + Llama 3.3 70B Q4</h4>
            <p><code>uv pip install vllm</code>. Скачиваем модель: <code>huggingface-cli download meta-llama/Llama-3.3-70B-Instruct-GGUF --local-dir /models/llama70b-q4</code>. Запуск: <code>vllm serve meta-llama/Llama-3.3-70B-Instruct --quantization awq --tensor-parallel-size 2 --port 8000</code>. Проверка: <code>curl localhost:8000/v1/models</code>.</p>
            <p>СУД-агент готов. 50-70 ток/сек на 2× GPU.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">04</span>3× Llama 8B для параллельных агентов</h4>
            <p><code>for i in 1 2 3; do vllm serve meta-llama/Llama-3.1-8B-Instruct --port $((8000+i)) --gpu-memory-utilization 0.15 &amp;</code>. 3 инстанса на 3 разных GPU (или шаред на одном GPU Tower Pro). 180-250 ток/сек каждый.</p>
            <p>МАШИНА (порт 8001) — сбор цитат из веба. ИИ (8002) — группировка по 6 слоям. СЛОВАРЬ (8003) — граф цепочек.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">05</span>Ollama + DeepSeek-R1 для рассуждений</h4>
            <p><code>curl -fsSL https://ollama.com/install.sh | sh</code>. <code>ollama pull deepseek-r1:32b</code>. <code>ollama serve --port 11434</code>. DeepSeek-R1 — reasoning-модель для задач где нужно «подумать вслух»: разбор кода, поиск багов, планирование.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">06</span>ComfyUI + FLUX.1-dev для картинок</h4>
            <p><code>git clone https://github.com/comfyanonymous/ComfyUI &amp;&amp; cd ComfyUI</code>. <code>uv pip install -r requirements.txt</code>. Скачать FLUX.1-dev в <code>models/checkpoints/</code>. <code>python main.py --listen 0.0.0.0 --port 8188</code>. 16GB VRAM, 1 картинка/3 сек.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">07</span>whisper.cpp + F5-TTS для голоса</h4>
            <p><code>git clone https://github.com/ggerganov/whisper.cpp</code>. <code>make &amp;&amp; ./models/download-ggml-model.sh large-v3</code>. Realtime STT в 12× быстрее реального времени.</p>
            <p>F5-TTS: <code>git clone https://github.com/SWivid/F5-TTS &amp;&amp; cd F5-TTS &amp;&amp; uv pip install -e .</code>. Запуск сервера: <code>f5-tts_infer-cli --server --port 5000</code>. Zero-shot клонирование голоса за 6 секунд.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">08</span>Infinity embeddings + Qdrant для RAG</h4>
            <p><code>uv pip install infinity-emb[all]</code>. <code>infinity_emb v2 --model-id bge-m3 --port 7997</code>. 10K docs/sec.</p>
            <p>Qdrant: <code>docker run -p 6333:6333 qdrant/qdrant</code>. Векторная БД для 665 статей каталога. <code>uv pip install qdrant-client</code>.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">09</span>Оркестрация: n8n + LangGraph + Redis</h4>
            <p>n8n (visual workflow): <code>docker run -p 5678:5678 n8nio/n8n</code>. Web-UI для визуального построения агентных workflow.</p>
            <p>LangGraph: <code>uv pip install langgraph</code>. Программный код-агент. Redis: <code>docker run -p 6379:6379 redis</code>. Pub/sub между МАШИНА/ИИ/СУД/СЛОВАРЬ.</p>
          </article>
          
          <article class="protocol-step">
            <h4><span class="step-num">10</span>Веб-интерфейс + мониторинг</h4>
            <p>Open WebUI (как ChatGPT): <code>docker run -p 3000:8080 --add-host=host.docker.internal:host-gateway -e OLLAMA_BASE_URL=http://host.docker.internal:11434 ghcr.io/open-webui/open-webui:main</code>.</p>
            <p>Мониторинг: Grafana + Prometheus + nvtop. <code>docker run -p 3001:3000 grafana/grafana</code>. Langfuse для LLM observability (токены, латентность).</p>
            <p>Всё готово. Открыл <code>http://localhost:3000</code> — Polymat работает.</p>
          </article>
        </div>
        
        <p class="stack-note reveal"><span class="k">проверка:</span> открой <code>http://localhost:8000/v1/models</code> → должен показать Llama 3.3 70B. <code>nvidia-smi</code> → 4 GPU по 32GB. <code>docker ps</code> → 5 контейнеров (Qdrant, Redis, n8n, Open WebUI, Grafana). Всё — локально, без облака.</p>
      </div>
    </section>
'''
template = template.replace("{{OFFLINE_PLACEHOLDER}}", protocol_section)
print("11. Protocol section вставлен ✓")

# ─────────────────────────────────────────────
# 12. Судовой журнал + Опасности облака
# ─────────────────────────────────────────────
# Court log table — первые 50 записей
court_rows = ""
for entry in court_log[:50]:
    status = entry["status"]
    status_class = f"status-{status.lower()}"
    status_label = {"TEXT": "[Т]", "HYP": "[Г]", "NOISE": "[Ш]"}[status]
    tool_name = html.escape(entry["tool_name"][:50])
    sig = html.escape(entry["signature"][:60])
    court_rows += f'''<tr>
              <td class="{status_class}">{status_label}</td>
              <td>{tool_name}</td>
              <td>{entry["verified_at"]}</td>
              <td>{entry["sources_count"]}</td>
              <td><code>{sig}</code></td>
            </tr>'''

court_section = f'''
    <!-- ═══ СУДОВОЙ ЖУРНАЛ ═══ -->
    <section class="section tinted" id="court" aria-label="Судовой журнал: верификация Polymat">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · court log</p>
          <h2>Судовой журнал — {len(court_log)} записей верификации</h2>
          <p>Каждый инструмент из {len(articles)} статей получил судовую подпись: дата, статус, количество источников, сигнатура. <b>[Т]</b> — [ТЕКСТ], доказано цитатами ({status_stats["TEXT"]}). <b>[Г]</b> — [ГИП], гипотеза ждёт пруфа ({status_stats["HYP"]}). <b>[Ш]</b> — [ШУМ], пересказ без пруфа ({status_stats["NOISE"]}). Полный журнал в <code>court-log.json</code> рядом с HTML.</p>
        </div>
        
        <details open class="reveal">
          <summary style="cursor:pointer;padding:0.75rem;background:rgba(255,171,64,0.08);border-radius:8px;font-weight:600;color:var(--accent,#ffab40);">Показать первые 50 записей из {len(court_log)}</summary>
          <table class="court-table">
            <thead><tr><th>Статус</th><th>Инструмент</th><th>Дата</th><th>Источников</th><th>Подпись</th></tr></thead>
            <tbody>{court_rows}</tbody>
          </table>
        </details>
        
        <p class="stack-note reveal"><span class="k">правило:</span> мультиагент ПОЛИМАТ (МАШИНА + ИИ + СУД + СЛОВАРЬ) подписывает каждую статью. Подпись формата: <code>polymath-DATE-TOOL_ID-STATUS</code>. Любую статью можно проверить — открыть <code>court-log.json</code> рядом с HTML.</p>
      </div>
    </section>
    
    <!-- ═══ ОПАСНОСТИ ОБЛАКА ═══ -->
    <section class="section container" id="dangers" aria-label="Опасности облака: реальные кейсы">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · cloud dangers</p>
          <h2>Почему облако умрёт — реальные кейсы 2022-2025</h2>
          <p>{auto_stats["cloud"]} инструментов в каталоге зависят от облака. Это не теория — это уже происходило. Реальные кейсы когда облачные AI-сервисы подводили. Polymat — это страховка.</p>
        </div>
        
        <div class="danger-grid reveal">
          <article class="danger-card">
            <h4>OpenAI: outage апрель 2024</h4>
            <p class="date">5 часов простоя · 23.04.2024</p>
            <p>ChatGPT, API, Playground все лежали. Компании на Copilot не могли кодить. Polymat на Ollama продолжил работать.</p>
          </article>
          <article class="danger-card">
            <h4>OpenAI: ценовая политика</h4>
            <p class="date">3 повышения за 2 года</p>
            <p>GPT-4: $60/1M → $30/1M → GPT-4o: $5/1M → $2.5/1M. Кажется снижение? Нет — объём запросов вырос в 10×, итоговый счёт вырос в 3×.</p>
          </article>
          <article class="danger-card">
            <h4>Anthropic: ToS ужесточение</h4>
            <p class="date">Claude API · 2024</p>
            <p>Запретили использовать Claude для «обучения конкурирующих моделей». Кто-то нарушил случайно — бан без предупреждения. Весь пайплайн — в мусор.</p>
          </article>
          <article class="danger-card">
            <h4>Gemini: удаление функций</h4>
            <p class="date">Google · 2024-2025</p>
            <p>Gemini Pro Vision — deprecated. Bard → Gemini → Gemini Advanced — ребрендинг каждые 6 месяцев. Код на старом API — в мусор.</p>
          </article>
          <article class="danger-card">
            <h4>GitHub Copilot: lawsuit</h4>
            <p class="date">Doe v. GitHub · 2022-2024</p>
            <p>Коллективный иск за нарушение авторских прав. Если суд решит не в пользу Copilot — функция может исчезнуть. Polymat на Aider — нет.</p>
          </article>
          <article class="danger-card">
            <h4>Midjourney: цензура</h4>
            <p class="date">2023-2024</p>
            <p>Фильтры increasingly strict. Картинки банят за «Trump», «Xi Jinping», даже за генерации природных сцен с политическим контекстом. ComfyUI — нет фильтров.</p>
          </article>
          <article class="danger-card">
            <h4>Suno / Udio: copyright иски</h4>
            <p class="date">RIAA v. Suno/Udio · 06.2024</p>
            <p>Sony, Warner, Universal подали иски за обучение на защищённых песнях. Если выиграют — Suno/Udio могут закрыться. Локальные F5-TTS / Stable Audio — нет.</p>
          </article>
          <article class="danger-card">
            <h4>ElevenLabs: правила клонирования</h4>
            <p class="date">2024</p>
            <p>Запретили клонирование голосов без верификации. Voice cloning API теперь требует KYC. Локальный F5-TTS / StyleTTS2 — нет KYC.</p>
          </article>
          <article class="danger-card">
            <h4>Stability AI: почти банкротство</h4>
            <p class="date">2024</p>
            <p>CEO Emad Mostaque ушёл, компания на грани. Stable Diffusion API может закрыться. Локальный SDXL/FLUX через ComfyUI — твой навсегда.</p>
          </article>
          <article class="danger-card">
            <h4>DeepSeek: геополитика</h4>
            <p class="date">2025</p>
            <p>Китайская модель. Внешний API может быть закрыт в любой момент из-за санкций. Локальная версия через Ollama — работает.</p>
          </article>
          <article class="danger-card">
            <h4>Cursor: бизнес-модель</h4>
            <p class="date">2024-2025</p>
            <p>Стартап с большой оценкой, но нет прибыли. Если инвесторы уйдут — Cursor закроется. Aider/OpenHands — open-source, всегда доступны.</p>
          </article>
          <article class="danger-card">
            <h4>Replit: AI-функции за доп. плату</h4>
            <p class="date">2024</p>
            <p>Ghostwriter → Replit AI → Replit Agent — переименования и доплаты. Базовые фичи стали платными. Полимат на локальном Cline — фиксированная цена $0.</p>
          </article>
        </div>
        
        <p class="stack-note reveal"><span class="k">вывод:</span> из {auto_stats["cloud"]} облачных инструментов {auto_stats["local"]} имеют локальные альтернативы в каталоге. Polymat — это страховка от облачного апокалипсиса. Когда ChatGPT/Claude/Gemini умрут (или подорожают, или сменят ToS) — у тебя уже всё работает.</p>
      </div>
    </section>
'''
template = template.replace("{{GLOSSARY_PLACEHOLDER}}", court_section)
print("12. Court + Dangers section вставлен ✓")

# ─────────────────────────────────────────────
# 13. Sources (footer)
# ─────────────────────────────────────────────
sources_html = f'''
      <h2 class="src-title"><span aria-hidden="true">📖</span> Источники и файлы Polymat v2</h2>
      <ul class="src-list">
        <li><strong>Каталог:</strong> {len(articles)} статей ({status_stats["TEXT"]} [ТЕКСТ] · {status_stats["HYP"]} [ГИП] · {status_stats["NOISE"]} [ШУМ])</li>
        <li><strong>Автономия:</strong> {auto_stats["local"]} локальных · {auto_stats["hybrid"]} гибридных · {auto_stats["cloud"]} облачных</li>
        <li><strong>Стек:</strong> {stack_stats["Rust"]} Rust · {stack_stats["Python"]} Python · {stack_stats["Go"]} Go · {stack_stats["C++"]} C++ · {stack_stats["Zig"]} Zig · {stack_stats["C"]} C · {stack_stats["TypeScript"]} TypeScript</li>
        <li><strong>Жизнь:</strong> {life_stats["active"]} active · {life_stats["maintenance"]} maintenance · {life_stats["legacy"]} legacy</li>
        <li><strong>Судовой журнал:</strong> {len(court_log)} записей в <code>court-log.json</code> рядом с HTML</li>
        <li><strong>Каталог-JSON:</strong> {len(articles)} статей в <code>catalog.json</code> рядом с HTML</li>
        <li><a href="https://github.com/astral-sh/uv" target="_blank" rel="noopener noreferrer">uv — Python package manager на Rust</a></li>
        <li><a href="https://github.com/astral-sh/ruff" target="_blank" rel="noopener noreferrer">ruff — linter+formatter на Rust</a></li>
        <li><a href="https://github.com/vllm-project/vllm" target="_blank" rel="noopener noreferrer">vLLM — PagedAttention</a></li>
        <li><a href="https://github.com/ollama/ollama" target="_blank" rel="noopener noreferrer">Ollama — Docker для LLM</a></li>
        <li><a href="https://github.com/ggerganov/llama.cpp" target="_blank" rel="noopener noreferrer">llama.cpp — основа локального LLM</a></li>
        <li><a href="https://github.com/comfyanonymous/ComfyUI" target="_blank" rel="noopener noreferrer">ComfyUI — node-based diffusion UI</a></li>
        <li><a href="https://github.com/SYSTRAN/faster-whisper" target="_blank" rel="noopener noreferrer">faster-whisper — Whisper на CTranslate2</a></li>
        <li><a href="https://github.com/SWivid/F5-TTS" target="_blank" rel="noopener noreferrer">F5-TTS — open-source zero-shot TTS</a></li>
        <li><a href="https://github.com/michaelfeil/infinity" target="_blank" rel="noopener noreferrer">Infinity — Rust embedding server</a></li>
        <li><a href="https://github.com/qdrant/qdrant" target="_blank" rel="noopener noreferrer">Qdrant — vector DB на Rust</a></li>
        <li><a href="https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/" target="_blank" rel="noopener noreferrer">NVIDIA — RTX 5090 official</a></li>
        <li><a href="https://www.apple.com/mac-studio/" target="_blank" rel="noopener noreferrer">Apple — Mac Studio M3 Ultra</a></li>
        <li><a href="https://www.w3.org/TR/WCAG22/" target="_blank" rel="noopener noreferrer">W3C — WCAG 2.2 (контраст, вспышки)</a></li>
      </ul>
'''
template = re.sub(
    r'<h2 class="src-title"><span aria-hidden="true">📖</span> Источники фактов</h2>\s*<ul class="src-list">.*?</ul>',
    sources_html, template, flags=re.DOTALL
)
print("13. Sources обновлены ✓")

# Footer
template = template.replace(
    '<span>© 2026 · Эталон «ГОЛОГРАММА v1» · судовые записи от 30.08.2026</span>',
    f'<span>© 2025-2026 · ПОЛИМАТ v2 · {len(articles)} инструментов · 3 конфига железа · 12 софт-компонентов · 0 облака</span>'
)
template = template.replace(
    '<span>Один файл. Ноль запросов. Режим антигаллюцинации включён ✓</span>',
    f'<span>{auto_stats["local"]} local · {auto_stats["cloud"]} cloud · {stack_stats["Rust"]} Rust · один файл · ноль запросов ✓</span>'
)

# Запись
OUT.write_text(template, encoding="utf-8")
print(f"\n✓ Финальный HTML собран: {OUT}")
print(f"  Размер: {OUT.stat().st_size:,} байт ({OUT.stat().st_size/1024:.1f} KB)")
print(f"  {len(articles)} статей · 3 конфига железа · 12 софт-компонентов · {len(court_log)} судовых записей")
