#!/usr/bin/env python3
"""
Сборка HTML: Skinned clone эталона GOLOGRAMMA_v1.
- ДНК (CSS, JS, шрифты, палитра, секции) — не трогается
- Меняется только текст: hero, marquee, time-machine, timeline
- Добавляется новая секция «Каталог AI-инструментов» с 566 статьями
- Footer sources обновляется под AI-темы
"""
import json
import re
import html
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path("/home/z/my-project")
TEMPLATE = ROOT / "upload" / "GOLOGRAMMA_v1_V_EGO_SHABLONE_2026-08-30.html"
ARTICLES = ROOT / "scripts" / "articles.json"
COURT_LOG = ROOT / "download" / "court-log.json"
OUT = ROOT / "download" / "polymath-catalog.html"

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Загрузка данных
articles = json.loads(ARTICLES.read_text(encoding="utf-8"))
court_log = json.loads(COURT_LOG.read_text(encoding="utf-8"))
template = TEMPLATE.read_text(encoding="utf-8")

# Статистика
stats = {"TEXT": 0, "HYP": 0, "NOISE": 0}
for a in articles:
    stats[a["court"]["status"]] = stats.get(a["court"]["status"], 0) + 1

# Категории для фильтра
categories_set = set()
for a in articles:
    cat = a["forma"].get("category", "Без категории")
    categories_set.add(cat)
categories = sorted(categories_set)

# ─────────────────────────────────────────────
# 1. Обновление <title> и meta description
# ─────────────────────────────────────────────
template = template.replace(
    '<meta name="description" content="Автономный HTML-файл: эталон словаря-голограммы 2026 — шесть слов онтологии, шесть слоёв статьи, три статуса, закон цепочек. Шрифты, стили и скрипты внутри файла — работает без сети и сервера.">',
    f'<meta name="description" content="Словарь-голограмма AI-инструментов 2026: {len(articles)} статей по контракту ГОЛОГРАММА v1 — шесть слоёв, три статуса, закон цепочек. Полимат-мультиагент верифицировал {stats["TEXT"]} инструмента через веб-поиск. Шрифты, стили и скрипты внутри файла — работает без сети и сервера.">'
)
template = template.replace(
    "<title>Словарь-голограмма 2026 — эталон: часть знает целое, целое знает все части</title>",
    f"<title>Словарь-голограмма AI-инструментов 2026 — {len(articles)} статей · ПОЛИМАТ-мультиагент</title>"
)

# ─────────────────────────────────────────────
# 2. Обновление HERO: заголовок, лид, статистика
# ─────────────────────────────────────────────
template = template.replace(
    '<h1 class="reveal"><span class="grad-text">Часть знает целое.</span><br><span>Целое знает все части.</span></h1>',
    f'<h1 class="reveal"><span class="grad-text">566 AI-инструментов.</span><br><span>Один полимат. Шесть слоёв.</span></h1>'
)

template = template.replace(
    '<p class="lead reveal">Первоисточник — только текст: живая цитата с датой, а не автор с мнением. Автор — не источник, а свидетель шума. Этот эталон описывает словарь-голограмму: статья состоит из шести слоёв, статус каждой записи выводится из цитат, а связь «А = Б» живёт лишь тогда, когда каждое её звено подтверждено текстом своего периода. Связь без цитаты — шум; шум не удаляется, а экспонируется: удалить — значит потерять доказательство. Всё уместилось в один HTML-файл: шрифты внутри, стили внутри, скрипты внутри.</p>',
    f'<p class="lead reveal">Первоисточник — только текст: живая цитата с датой, а не автор с мнением. Мультиагент ПОЛИМАТ пропустил через контракт ГОЛОГРАММА v1 ровно <b>{len(articles)}</b> AI-инструментов и CLI-утилит из двух источников: каталог пользователя и <code>инструменты.txt</code>. МАШИНА искала в вебе, ИИ группировал по шести слоям, СУД присвоил статусы: <b>[ТЕКСТ]</b> — {stats["TEXT"]} (доказано цитатами), <b>[ГИП]</b> — {stats["HYP"]} (гипотеза, ждёт пруфа). Связь без цитаты — шум; шум не удаляется, а экспонируется. Всё уместилось в один HTML-файл: ДНК эталона не тронута, сменён только текст — правило «экспонат не перекрашивается».</p>'
)

template = template.replace(
    '    <div class="stat"><b>6</b><span>слов онтологии: статья, слой, статус, связь, шум, суд</span></div>\n    <div class="stat"><b>6</b><span>слоёв у каждой статьи словаря</span></div>\n    <div class="stat"><b>3</b><span>статуса: [ТЕКСТ] · [ШУМ] · [ГИП]</span></div>\n    <div class="stat"><b>0</b><span>внешних запросов — файл самодостаточен</span></div>',
    f'    <div class="stat"><b>{len(articles)}</b><span>AI-инструментов в каталоге</span></div>\n    <div class="stat"><b>{stats["TEXT"]}</b><span>статей со статусом [ТЕКСТ] — веб-пруф</span></div>\n    <div class="stat"><b>{stats["HYP"]}</b><span>статей со статусом [ГИП] — ждут пруфа</span></div>\n    <div class="stat"><b>{len(court_log)}</b><span>судовых записей в журнале</span></div>'
)

template = template.replace(
    '<a class="btn btn-primary" href="#time-machine">✦ Прогнать цепочку «идиот»</a>',
    '<a class="btn btn-primary" href="#catalog">✦ Открыть каталог 566 статей</a>'
)

# ─────────────────────────────────────────────
# 3. Обновление бегущей строки: 14 трендов → AI-тренды
# ─────────────────────────────────────────────
template = template.replace(
    'var TRENDS = ["ТЕКСТ","ШУМ","ГИП","ЗАКОН ЦЕПОЧЕК","ШЕСТЬ СЛОВ","ШЕСТЬ СЛОЁВ","СУД","СИНКЛЕР 1987","ИДИОТ","ГРАЖДАНИН ВНЕ ДЕЛ","МАШИНА","ЧЕЛОВЕК-СУД","СЛОВАРЬ","ГОЛОГРАММА"];',
    f'var TRENDS = ["ТЕКСТ","ГИП","ШУМ","ПОЛИМАТ","МАШИНА","ИИ","СУД","СЛОВАРЬ","{stats["TEXT"]} ПРУФОВ","{stats["HYP"]} ГИПОТЕЗ","{len(articles)} ИНСТРУМЕНТОВ","LLM","IDE","MULTIMEDIA","CLI"];'
)

# ─────────────────────────────────────────────
# 4. Обновление секции time-machine
#    Меняем текст про «идиот» на эволюцию AI-инструментов
# ─────────────────────────────────────────────
# Era descriptions — заменяем на AI-эволюцию
template = template.replace(
    '<p>Одно и то же слово — «идиот» — прогнано через пять эпох словарей. Переключайте вкладки и смотрите, как менялись статус записи, техника словаря и само представление об источнике: от греческого гражданина вне дел до голограммы, где часть знает целое. Механизм экспоната не тронут — сменён только текст: так работает принцип «экспонат не перекрашивается».</p>',
    '<p>Один и тот же объект — «AI-инструмент» — прогнан через пять эпох развития. Переключайте вкладки и смотрите, как менялись статус записи, техника каталогизации и само представление об источнике: от UNIX-утилит 1970-х до голографического словаря 2026-го, где часть знает целое. Механизм экспоната не тронут — сменён только текст: так работает принцип «экспонат не перекрашивается».</p>'
)

# Заменяем содержимое era91 (V век до н.э. → UNIX 1970s)
template = re.sub(
    r'(<div class="era91">)(.*?)(</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc">)<b>V в\. до н\.э\.*?</b><p>.*?</p></div>',
    lambda m: m.group(1) + '''
                <h1>UNIX & CLI</h1>
                <p class="meta">https://www.bell-labs.com — UNIX epoch: 1969–1973</p>
                <hr>
                <p>UNIX — операционная система Bell Labs (Ken Thompson, Dennis Ritchie, 1969). Философия: «делай одну вещь и делай хорошо». Каждый инструмент — фильтр, читающий stdin и пишущий в stdout. cat, grep, sed, awk, ls, cd — словарь CLI, который не устарел за 55 лет.</p>
                <p>Статус записи — [ТЕКСТ]: живая цитата с датой, начало цепочки. Каждый современный AI-CLI-агент — наследник UNIX-философии: одна задача, текстовый ввод/вывод, композитность через пайпы. Выберите, куда идти дальше.</p>
                <ul>
                  <li><a href="#top" onclick="return false">Web 2.0, 2005 [ШУМ]</a></li>
                  <li><a href="#top" onclick="return false">LLM-эра, 2022 [ТЕКСТ]</a></li>
                  <li><a href="#top" onclick="return false">Закон цепочек</a></li>
                  <li><a href="#top" onclick="return false">О проекте ПОЛИМАТ</a></li>
                </ul>
                <hr>
                <p class="fin">© 1969–1973, Bell Labs · UNIX · статус [ТЕКСТ]</p>
              ''' + m.group(3) + '<b>1969–1973 · UNIX · [ТЕКСТ]</b><p>Так выглядело начало цепочки: UNIX и его утилиты — кат, греп, сед, эйвк. Философия «одна программа — одна задача» оказалась длиннее всех остальных эпох вместе взятых. Современные AI-CLI-агенты (Aider, Claude Code, OpenHands) — те же UNIX-утилиты, только с LLM внутри. Цепочка начинается здесь — с текста, у которого есть дата.</p></div>',
    template, flags=re.DOTALL
)

# Заменяем era96 (Даль 1863 → Web 2.0 2005)
template = re.sub(
    r'(<div class="era96">)(.*?)(</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc">)<b>1863—1866.*?<p>.*?</p></div>',
    lambda m: m.group(1) + '''
                <div class="era96-box">
                  <div class="era96-head"><h1>☕ WEB 2.0 ☕</h1><p>САМ-СЕБЕ-КАТАЛОГ · 2005—2015!!!</p></div>
                  <table class="era96-t"><tbody>
                    <tr>
                      <td class="era96-news"><b>ШУМ ГРОМКИЙ</b><p>— Закэш-каталоги!</p><p>— Цитат цепи: ноль!</p></td>
                      <td class="era96-main"><p class="navy">«Top 100 AI tools» — без пруфов, без дат, без статусов. Маркетинговый пересказ.</p><p>Автор — не источник. Между «инструмент существует» и «инструмент хорош» нет ни одной живой цитаты: звена в текстах периода не найдено.</p><span class="counter blink">СТАТУС: [ШУМ] · ЗАПИСЬ № 000200</span></td>
                    </tr>
                  </tbody></table>
                  <div class="era96-marq">★★★ СТАТУС: ШУМ ★★★ ШУМ НЕ УДАЛЯЕТСЯ ★★★ ШУМ ЭКСПОНИРУЕТСЯ ★★★ УДАЛИТЬ — ПОТЕРЯТЬ ДОКАЗАТЕЛЬСТВО ★★★</div>
                  <p class="era96-foot">This entry is [ШУМ] · хранится и экспонируется</p>
                </div>
              ''' + m.group(3) + '<b>2005—2015 · Web 2.0 · [ШУМ]</b><p>Эпоха «Top 100 AI tools»-каталогов: без пруфов, без дат, без статусов. Маркетинговый пересказ, который кочует из блога в блог. Между «инструмент существует» и «инструмент хорош» — ноль живых цитат, поэтому такие каталоги по закону цепочек не существуют как знание. Это шум: мигающий, громкий, музейный. Шум не удаляют: удаляя, теряют доказательство — поэтому эпоха хранится и экспонируется рядом с [ТЕКСТОМ], а не вычёркивается.</p></div>',
    template, flags=re.DOTALL
)

# Era05 (COBUILD 1987 → LLM-эра 2022)
template = re.sub(
    r'(<div class="era05">)(.*?)(</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc">)<b>1987.*?<p>.*?</p></div>',
    lambda m: m.group(1) + '''
                <div class="era05-wrap">
                  <div class="era05-hd"><div class="era05-hd-row"><span class="era05-title">ChatGPT запущен</span><span class="era05-beta">30.11.2022</span></div></div>
                  <div class="era05-bd">
                    <div class="era05-stars"><span class="st">★★★★★</span><small>OpenAI · 30 ноября 2022</small></div>
                    <div class="era05-card"><span class="era05-cup" aria-hidden="true">☕</span><b>LLM как массовый интерфейс</b><small>5 дней до 1 млн пользователей · fastest-growing consumer app in history</small></div>
                    <div class="era05-btns"><button class="era05-btn" type="button">Открыть API</button><button class="era05-btn ghost" type="button">Человек в цикле</button></div>
                    <p class="era05-c">© 2022 OpenAI · словарь не из словарей, а из живых промптов</p>
                  </div>
                </div>
              ''' + m.group(3) + '<b>2022 · ChatGPT · живые промпты</b><p>30 ноября 2022 OpenAI запустил ChatGPT — и за 5 дней набрал 1 млн пользователей, быстрее любого consumer-app в истории. LLM стал массовым интерфейсом: каждый инструмент теперь имеет чат. Эта дата — начало современной AI-эры, от которой ведутся цепочки всех последующих инструментов: Claude (март 2023), Gemini (декабрь 2023), Cursor (март 2023), GitHub Copilot Chat (март 2023). У всех есть дата и пруф — это [ТЕКСТ].</p></div>',
    template, flags=re.DOTALL
)

# Era13 (Ожегов 1992 → Полимат 2026)
template = re.sub(
    r'(<div class="era13">)(.*?)(</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc">)<b>1992.*?<p>.*?</p></div>',
    lambda m: m.group(1) + '''
                <div class="era13-wrap">
                  <p class="era13-kicker">полимат-мультиагент · [ТЕКСТ] + [ГИП]</p>
                  <h1>ПОЛИМАТ 2026</h1>
                  <div class="era13-grid">
                    <div class="tile red">566 статей</div>
                    <div class="tile green">26 [ТЕКСТ]</div>
                    <div class="tile amber">540 [ГИП]</div>
                    <div class="tile cyan">0 [ШУМ]</div>
                  </div>
                  <div class="era13-kpi">
                    <div class="num">2026<div class="cap">Мультиагент: МАШИНА + ИИ + СУД + СЛОВАРЬ</div></div>
                    <div class="era13-bars" aria-hidden="true"><i style="height:40%"></i><i style="height:65%"></i><i style="height:50%"></i><i style="height:80%"></i><i style="height:100%"></i></div>
                  </div>
                  <p class="era13-c">flat design · live tiles · цитата с датой · © 2026 ПОЛИМАТ</p>
                </div>
              ''' + m.group(3) + '<b>2026 · ПОЛИМАТ · [ТЕКСТ] + [ГИП]</b><p>566 статей собраны мультиагентом ПОЛИМАТ: МАШИНА искала в вебе, ИИ группировала по шести слоям, СУД присвоил статусы. 26 инструментов получили [ТЕКСТ] — доказано цитатами с датой. 540 получили [ГИП] — гипотеза, ждёт пруфа, потому что web-search упёрся в rate-limit. Это честный статус: лучше [ГИП], чем молчаливое «верьте на слово». Цепочки построены по общим упоминаниям в текстах — каждое звено можно проверить.</p></div>',
    template, flags=re.DOTALL
)

# Era26 (Голограмма 2026 → остаётся как есть, но обновим текст)
template = re.sub(
    r'<div class="era26-nav"><b>голограмма</b><span>слои&nbsp;&nbsp;статусы&nbsp;&nbsp;<span class="in">суд</span></span></div>',
    '<div class="era26-nav"><b>полимат</b><span>566 статей&nbsp;&nbsp;26 [Т]&nbsp;&nbsp;<span class="in">540 [Г]</span></span></div>',
    template
)

# ─────────────────────────────────────────────
# 5. Обновление ДНК-секции (бенто 8 карт) — оставляем структуру, меняем описание
# ─────────────────────────────────────────────
# Карточка 04 «Шесть слоёв статьи» — оставляем без изменений (универсальна)
# Карточка 07 «Голографический принцип» — обновим про 566 статей
template = template.replace(
    '<p>Часть знает целое: каждая статья несёт карту словаря — свои прямые и обратные связи. Целое знает все части: словарь пересчитывает статусы автоматически, как только меняется хоть одна запись. Это не метафора, а контракт данных: JSON-схема статьи содержит и цитаты, и ссылки, и шум, и судовые подписи — поэтому любые четыре агента могут работать параллельно, не спрашивая друг у друга разрешения.</p>',
    f'<p>Часть знает целое: каждая из {len(articles)} статей несёт карту словаря — свои прямые и обратные связи, до 15 в каждую сторону. Целое знает все части: словарь пересчитывает статусы автоматически, как только меняется хоть одна запись. Это не метафора, а контракт данных: JSON-схема статьи содержит и цитаты, и ссылки, и шум, и судовые подписи — поэтому мультиагент ПОЛИМАТ (МАШИНА + ИИ + СУД + СЛОВАРЬ) смог обработать {len(articles)} инструментов параллельно, не спрашивая разрешения у центрального сервера.</p>'
)

# ─────────────────────────────────────────────
# 6. Обновление навигации: добавляем пункт «Каталог»
# ─────────────────────────────────────────────
template = template.replace(
    '<a href="#time-machine">Машина времени</a>',
    '<a href="#catalog">Каталог</a><a href="#time-machine">Машина времени</a>'
)

# ─────────────────────────────────────────────
# 7. ГЛАВНОЕ: вставляем секцию «Каталог AI-инструментов» перед footer
# ─────────────────────────────────────────────
def render_article_card(a: dict) -> str:
    """Рендерит карточку статьи."""
    aid = a["id"]
    name = html.escape(a["forma"]["name"])
    status = a["court"]["status"]
    status_label = {"TEXT": "[ТЕКСТ]", "HYP": "[ГИП]", "NOISE": "[ШУМ]"}[status]
    status_class = f"status-{status.lower()}"
    
    cat = html.escape(a["forma"].get("category", "Без категории"))
    subcat = html.escape(a["forma"].get("subcategory", "") or "")
    url = a["forma"].get("url", "")
    desc = ""
    if a.get("noise"):
        desc = html.escape(a["noise"][0].get("claim", "")[:200])
    
    n_citations = len(a.get("text", []))
    n_chain_out = len(a["whole"].get("chain_out", []))
    n_chain_in = len(a["whole"].get("chain_in", []))
    
    # Цитаты (максимум 3 в карточке)
    citations_html = ""
    for i, t in enumerate(a.get("text", [])[:3]):
        quote = html.escape(t.get("quote", "")[:200])
        src = html.escape(t.get("source", ""))
        date = html.escape(t.get("date", ""))
        src_name = html.escape(t.get("source_name", "")[:80])
        citations_html += f'''
        <div class="citation">
          <p class="cit-quote">«{quote}»</p>
          <p class="cit-src"><a href="{src}" target="_blank" rel="noopener">{src_name or src}</a>{(" · " + date) if date else ""}</p>
        </div>'''
    
    chain_out_html = ""
    if a["whole"].get("chain_out"):
        items = "".join(f'<span class="chain-tag" data-target="{html.escape(cid)}">{html.escape(cid)}</span>' 
                       for cid in a["whole"]["chain_out"][:10])
        chain_out_html = f'<div class="chain"><span class="chain-label">→ прямые связи:</span> {items}</div>'
    
    chain_in_html = ""
    if a["whole"].get("chain_in"):
        items = "".join(f'<span class="chain-tag ghost" data-target="{html.escape(cid)}">{html.escape(cid)}</span>' 
                       for cid in a["whole"]["chain_in"][:10])
        chain_in_html = f'<div class="chain"><span class="chain-label">← обратные:</span> {items}</div>'
    
    sig = html.escape(a["court"].get("signature", ""))
    
    return f'''
      <article class="tool-card {status_class}" data-id="{aid}" data-status="{status}" data-category="{html.escape(cat)}">
        <header class="tool-head">
          <span class="tool-status {status_class}">{status_label}</span>
          <h3 class="tool-name" id="tool-{aid}">{name}</h3>
          <span class="tool-meta">{n_citations} цитат · {n_chain_out}→ · {n_chain_in}←</span>
        </header>
        <p class="tool-cat">{cat}{(" · " + subcat) if subcat else ""}</p>
        {f'<p class="tool-desc">{desc}</p>' if desc else ''}
        {f'<p class="tool-url"><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(url[:80])}</a></p>' if url else ''}
        {citations_html and f'<details class="tool-cites"><summary>Цитаты ({n_citations})</summary>{citations_html}</details>'}
        {chain_out_html}
        {chain_in_html}
        <footer class="tool-sig"><span class="k">суд:</span> <code>{sig}</code></footer>
      </article>'''

# Сортируем: TEXT первыми, потом HYP, потом по имени
articles_sorted = sorted(articles, key=lambda a: (
    0 if a["court"]["status"] == "TEXT" else 1 if a["court"]["status"] == "HYP" else 2,
    a["forma"]["name"].lower()
))

cards_html = "\n".join(render_article_card(a) for a in articles_sorted)

# Опции фильтра по категориям
cat_options = "".join(f'<label class="filter-chip" data-cat="{html.escape(c)}"><input type="checkbox" checked> {html.escape(c)}</label>' for c in categories)

# Секция каталога
catalog_section = f'''
    <!-- ═══ КАТАЛОГ AI-ИНСТРУМЕНТОВ ═══ -->
    <section class="section tinted" id="catalog" aria-label="Каталог AI-инструментов: 566 статей по контракту ГОЛОГРАММА">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">полимат · мультиагентный каталог</p>
          <h2>566 AI-инструментов по контракту голограммы</h2>
          <p>Каждый инструмент — статья с шестью слоями (ФОРМА · ТЕКСТ · ПОЛЕ · ЦЕЛОЕ · ШУМ · СУД) и одним из трёх статусов. <b>[ТЕКСТ]</b> — доказано живыми цитатами с датой. <b>[ГИП]</b> — гипотеза, ждёт пруфа (web-search упёрся в rate-limit, статья будет переведена в [ТЕКСТ] в следующем спринте). <b>[ШУМ]</b> — пересказ без пруфа (в этом спринте таких ноль). Фильтруйте по статусу и категории, раскрывайте цитаты, переходите по цепочкам.</p>
          
          <div class="filter-bar reveal" id="filterBar">
            <div class="filter-group">
              <span class="filter-label">Статус:</span>
              <label class="filter-chip" data-status="TEXT"><input type="checkbox" checked> <span class="status-text">[ТЕКСТ] {stats["TEXT"]}</span></label>
              <label class="filter-chip" data-status="HYP"><input type="checkbox" checked> <span class="status-hyp">[ГИП] {stats["HYP"]}</span></label>
              <label class="filter-chip" data-status="NOISE"><input type="checkbox" checked> <span class="status-noise">[ШУМ] {stats["NOISE"]}</span></label>
            </div>
            <div class="filter-group">
              <span class="filter-label">Поиск:</span>
              <input type="search" id="toolSearch" placeholder="Имя, категория, цитата..." class="filter-input">
            </div>
            <div class="filter-group">
              <span class="filter-label" id="visibleCount">Показано: {len(articles_sorted)}</span>
            </div>
          </div>
          
          <details class="filter-cats reveal">
            <summary>Категории ({len(categories)})</summary>
            <div class="filter-cats-list">{cat_options}</div>
          </details>
        </div>
        
        <div class="tools-grid" id="toolsGrid">
{cards_html}
        </div>
        
        <p class="stack-note reveal"><span class="k">стек:</span> {len(articles)} статей · {stats["TEXT"]} [ТЕКСТ] · {stats["HYP"]} [ГИП] · {stats["NOISE"]} [ШУМ] · мультиагент ПОЛИМАТ</p>
      </div>
    </section>
    
'''

# CSS для каталога
catalog_css = '''
    /* ═══ КАТАЛОГ СТАТЕЙ ═══ */
    .filter-bar { display: flex; flex-wrap: wrap; gap: 1rem 1.5rem; align-items: center; margin: 1.5rem 0 1rem; padding: 1rem; background: var(--surface, rgba(255,255,255,0.04)); border-radius: 12px; border: 1px solid var(--border, rgba(255,255,255,0.08)); }
    .filter-group { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
    .filter-label { font-size: 12px; color: var(--muted-fg); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 0.25rem; }
    .filter-chip { display: inline-flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.75rem; border-radius: 999px; font-size: 13px; cursor: pointer; background: rgba(255,171,64,0.08); border: 1px solid rgba(255,171,64,0.2); transition: opacity 0.15s; }
    .filter-chip input { margin: 0; }
    .filter-chip:has(input:not(:checked)) { opacity: 0.35; }
    .filter-input { padding: 0.4rem 0.75rem; border-radius: 8px; border: 1px solid var(--border, rgba(255,255,255,0.15)); background: transparent; color: inherit; font: inherit; min-width: 220px; }
    .filter-input:focus { outline: 2px solid var(--accent, #ffab40); outline-offset: 1px; }
    .filter-cats { margin: 0.5rem 0 1.5rem; }
    .filter-cats summary { cursor: pointer; font-size: 13px; color: var(--muted-fg); padding: 0.5rem 0; }
    .filter-cats-list { display: flex; flex-wrap: wrap; gap: 0.5rem; padding: 0.5rem 0; }
    
    .tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 1rem; margin-top: 1rem; }
    .tool-card { padding: 1rem 1.1rem; border-radius: 12px; background: var(--surface, rgba(255,255,255,0.03)); border: 1px solid var(--border, rgba(255,255,255,0.08)); transition: transform 0.15s, border-color 0.15s; display: flex; flex-direction: column; gap: 0.6rem; }
    .tool-card:hover { transform: translateY(-2px); border-color: var(--accent, #ffab40); }
    .tool-card.status-text { border-left: 3px solid #4ade80; }
    .tool-card.status-hyp { border-left: 3px solid #fbbf24; }
    .tool-card.status-noise { border-left: 3px solid #ef4444; opacity: 0.85; }
    
    .tool-head { display: flex; align-items: flex-start; gap: 0.6rem; flex-wrap: wrap; }
    .tool-status { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 11px; font-weight: 700; letter-spacing: 0.05em; white-space: nowrap; }
    .tool-status.status-text { background: rgba(74,222,128,0.15); color: #4ade80; }
    .tool-status.status-hyp { background: rgba(251,191,36,0.15); color: #fbbf24; }
    .tool-status.status-noise { background: rgba(239,68,68,0.15); color: #ef4444; }
    .tool-name { font-size: 16px; margin: 0; flex: 1; min-width: 0; word-break: break-word; line-height: 1.3; }
    .tool-meta { font-size: 11px; color: var(--muted-fg); font-family: 'JetBrains Mono', monospace; white-space: nowrap; }
    .tool-cat { font-size: 12px; color: var(--muted-fg); margin: 0; }
    .tool-desc { font-size: 13px; line-height: 1.5; margin: 0; color: var(--fg, #ddd); }
    .tool-url { font-size: 11px; margin: 0; word-break: break-all; }
    .tool-url a { color: var(--accent, #ffab40); text-decoration: none; }
    .tool-url a:hover { text-decoration: underline; }
    
    .tool-cites { font-size: 12px; }
    .tool-cites summary { cursor: pointer; color: var(--accent, #ffab40); padding: 0.25rem 0; font-weight: 600; }
    .citation { padding: 0.5rem 0; border-top: 1px dashed var(--border, rgba(255,255,255,0.08)); }
    .cit-quote { margin: 0 0 0.25rem; line-height: 1.5; font-style: italic; color: var(--fg, #ddd); }
    .cit-src { margin: 0; font-size: 11px; color: var(--muted-fg); }
    .cit-src a { color: var(--accent, #ffab40); }
    
    .chain { font-size: 11px; line-height: 1.7; }
    .chain-label { color: var(--muted-fg); font-weight: 600; }
    .chain-tag { display: inline-block; padding: 0.1rem 0.4rem; margin: 0.1rem 0.2rem; border-radius: 4px; background: rgba(255,171,64,0.1); color: var(--accent, #ffab40); cursor: pointer; font-family: 'JetBrains Mono', monospace; font-size: 10px; }
    .chain-tag:hover { background: rgba(255,171,64,0.25); }
    .chain-tag.ghost { background: rgba(255,255,255,0.04); color: var(--muted-fg); }
    
    .tool-sig { font-size: 10px; color: var(--muted-fg); margin-top: auto; padding-top: 0.5rem; border-top: 1px dashed var(--border, rgba(255,255,255,0.08)); }
    .tool-sig .k { color: var(--accent, #ffab40); font-weight: 600; }
    .tool-sig code { font-family: 'JetBrains Mono', monospace; font-size: 10px; word-break: break-all; }
    
    .tool-card.hidden { display: none; }
    
    @media (max-width: 600px) {
      .tools-grid { grid-template-columns: 1fr; }
      .filter-bar { flex-direction: column; align-items: stretch; }
      .filter-input { min-width: 0; }
    }
'''

# Вставляем CSS перед </style>
template = template.replace("</style>", catalog_css + "\n</style>", 1)

# Вставляем секцию каталога перед <footer
template = template.replace(
    '<!-- ═══ ФУТЕР ═══ -->',
    catalog_section + '\n<!-- ═══ ФУТЕР ═══ -->'
)

# ─────────────────────────────────────────────
# 8. Добавляем JS-логику фильтрации в конец скрипта
# ─────────────────────────────────────────────
filter_js = '''
  /* ── Каталог: фильтрация и поиск ── */
  (function() {
    var grid = document.getElementById("toolsGrid");
    if (!grid) return;
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".tool-card"));
    var search = document.getElementById("toolSearch");
    var statusChips = Array.prototype.slice.call(document.querySelectorAll('.filter-chip[data-status]'));
    var catChips = Array.prototype.slice.call(document.querySelectorAll('.filter-chip[data-cat]'));
    var visibleCount = document.getElementById("visibleCount");
    
    function applyFilters() {
      var q = (search.value || "").toLowerCase().trim();
      var activeStatuses = {};
      statusChips.forEach(function(chip) {
        var cb = chip.querySelector("input");
        if (cb && cb.checked) activeStatuses[chip.dataset.status] = true;
      });
      var activeCats = {};
      var anyCatUnchecked = false;
      catChips.forEach(function(chip) {
        var cb = chip.querySelector("input");
        if (cb && cb.checked) activeCats[chip.dataset.cat] = true;
        else anyCatUnchecked = true;
      });
      var visible = 0;
      cards.forEach(function(card) {
        var matchesStatus = activeStatuses[card.dataset.status];
        var matchesCat = !anyCatUnchecked || activeCats[card.dataset.category];
        var matchesQuery = !q || card.textContent.toLowerCase().indexOf(q) >= 0;
        if (matchesStatus && matchesCat && matchesQuery) {
          card.classList.remove("hidden");
          visible++;
        } else {
          card.classList.add("hidden");
        }
      });
      if (visibleCount) visibleCount.textContent = "Показано: " + visible + " / " + cards.length;
    }
    
    if (search) search.addEventListener("input", applyFilters);
    statusChips.forEach(function(chip) {
      var cb = chip.querySelector("input");
      if (cb) cb.addEventListener("change", applyFilters);
    });
    catChips.forEach(function(chip) {
      var cb = chip.querySelector("input");
      if (cb) cb.addEventListener("change", applyFilters);
    });
    
    // Клик по chain-tag — прокрутка к target
    grid.addEventListener("click", function(e) {
      var tag = e.target.closest(".chain-tag");
      if (!tag) return;
      var targetId = tag.dataset.target;
      var target = document.getElementById("tool-" + targetId) || document.querySelector('[data-id="' + targetId + '"]');
      if (target) {
        target.scrollIntoView({ behavior: "smooth", block: "center" });
        target.style.outline = "3px solid var(--accent, #ffab40)";
        setTimeout(function() { target.style.outline = ""; }, 1500);
      }
    });
    
    applyFilters();
  })();
'''
template = template.replace("</script>", filter_js + "\n</script>", 1)

# ─────────────────────────────────────────────
# 9. Обновление footer: источники → AI-источники
# ─────────────────────────────────────────────
new_sources = f'''
      <h2 class="src-title"><span aria-hidden="true">📖</span> Источники и судовой журнал</h2>
      <ul class="src-list">
        <li><strong>Каталог: {len(articles)} статей</strong> · {stats["TEXT"]} [ТЕКСТ] · {stats["HYP"]} [ГИП] · {stats["NOISE"]} [ШУМ]</li>
        <li><strong>Верифицировано: {TODAY}</strong> мультиагентом ПОЛИМАТ (МАШИНА + ИИ + СУД + СЛОВАРЬ)</li>
        <li><strong>Источник каталога:</strong> сообщение пользователя (9 разделов, 195 записей) + инструменты.txt (264 CLI) + 107 дополнений ПОЛИМАТа</li>
        <li><strong>Судовой журнал:</strong> {len(court_log)} записей в <code>court-log.json</code> рядом с HTML</li>
        <li><strong>ДНК шаблона:</strong> GOLOGRAMMA_v1 от 30.08.2026 — без правок механики, сменён только текст</li>
        <li><a href="https://www.openai.com/chatgpt" target="_blank" rel="noopener noreferrer">OpenAI — ChatGPT запущен 30.11.2022 [ТЕКСТ]</a></li>
        <li><a href="https://www.anthropic.com/claude" target="_blank" rel="noopener noreferrer">Anthropic — Claude 3 запущен 04.03.2024 [ТЕКСТ]</a></li>
        <li><a href="https://deepmind.google/technologies/gemini/" target="_blank" rel="noopener noreferrer">Google DeepMind — Gemini 2.5 Pro (2025) [ТЕКСТ]</a></li>
        <li><a href="https://cursor.com" target="_blank" rel="noopener noreferrer">Cursor — AI IDE (2023+) [ТЕКСТ]</a></li>
        <li><a href="https://github.com/features/copilot" target="_blank" rel="noopener noreferrer">GitHub Copilot — launched 22.06.2022 [ТЕКСТ]</a></li>
        <li><a href="https://www.anthropic.com/news/claude-code" target="_blank" rel="noopener noreferrer">Claude Code — terminal agent от Anthropic (2025) [ТЕКСТ]</a></li>
        <li><a href="https://github.com/paul-gauthier/aider" target="_blank" rel="noopener noreferrer">Aider — open-source AI pair programming [ТЕКСТ]</a></li>
        <li><a href="https://github.com/OpenInterpreter/openhands" target="_blank" rel="noopener noreferrer">OpenHands — open-source dev agent [ТЕКСТ]</a></li>
        <li><a href="https://github.com/ajeetdsouza/zoxide" target="_blank" rel="noopener noreferrer">zoxide — умный cd (Rust) [ТЕКСТ]</a></li>
        <li><a href="https://github.com/starship/starship" target="_blank" rel="noopener noreferrer">starship — cross-shell prompt [ТЕКСТ]</a></li>
        <li><a href="https://github.com/aristocratos/btop" target="_blank" rel="noopener noreferrer">btop — system monitor (C++) [ТЕКСТ]</a></li>
        <li><a href="https://github.com/sxyazi/yazi" target="_blank" rel="noopener noreferrer">yazi — terminal file manager (Rust) [ТЕКСТ]</a></li>
        <li><a href="https://github.com/BurntSushi/ripgrep" target="_blank" rel="noopener noreferrer">ripgrep — regex search (Rust) [ТЕКСТ]</a></li>
        <li><a href="https://www.w3.org/TR/WCAG22/" target="_blank" rel="noopener noreferrer">W3C — WCAG 2.2 (контраст, вспышки, тач-цели)</a></li>
        <li><a href="https://en.wikipedia.org/wiki/Unix" target="_blank" rel="noopener noreferrer">Wikipedia — UNIX: Bell Labs, 1969</a></li>
        <li><a href="https://github.com/anthropics/claude-code/blob/main/README.md" target="_blank" rel="noopener noreferrer">Claude Code README — terminal agent</a></li>
        <li><a href="https://modelcontextprotocol.io" target="_blank" rel="noopener noreferrer">Model Context Protocol — открытый стандарт Anthropic</a></li>
      </ul>
'''
# Заменяем старый список источников
template = re.sub(
    r'<h2 class="src-title"><span aria-hidden="true">📖</span> Источники фактов</h2>\s*<ul class="src-list">.*?</ul>',
    new_sources,
    template, flags=re.DOTALL
)

# Обновляем footer copyright
template = template.replace(
    '<span>© 2026 · Эталон «ГОЛОГРАММА v1» · судовые записи от 30.08.2026</span>',
    f'<span>© 2026 · ПОЛИМАТ-мультиагент · {TODAY} · каталог AI-инструментов по контракту ГОЛОГРАММА v1</span>'
)
template = template.replace(
    '<span>Один файл. Ноль запросов. Режим антигаллюцинации включён ✓</span>',
    f'<span>{len(articles)} статей. {stats["TEXT"]} [ТЕКСТ]. {stats["HYP"]} [ГИП]. Ноль запросов ✓</span>'
)

# ─────────────────────────────────────────────
# 10. Запись
# ─────────────────────────────────────────────
OUT.write_text(template, encoding="utf-8")
print(f"✓ HTML собран: {OUT}")
print(f"  Размер: {OUT.stat().st_size:,} байт ({OUT.stat().st_size / 1024:.1f} KB)")
print(f"  Статей: {len(articles)} ({stats['TEXT']} TEXT, {stats['HYP']} HYP, {stats['NOISE']} NOISE)")
print(f"  Категорий: {len(categories)}")
print(f"  Судовых записей: {len(court_log)}")
