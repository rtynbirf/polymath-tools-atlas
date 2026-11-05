#!/usr/bin/env python3
"""
Пересборка HTML с новой схемой:
- Бейджи на карточках: stack (Rust/Python/Zig/Go/C++), autonomy (local/cloud), lifecycle (active/legacy)
- Новые фильтры: по стеку, автономности, жизненному циклу
- Новая секция «Автономный стек ПОЛИМАТа» — то, что работает когда облака упадут
- Машина времени: добавим 6-ю эпоху (Cloud vs Local)
"""
import json
import re
import html
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter

ROOT = Path("/home/z/my-project")
ARTICLES = ROOT / "scripts" / "articles_v2.json"
COURT_LOG = ROOT / "download" / "court-log.json"
OUT = ROOT / "download" / "polymath-catalog.html"

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

articles = json.loads(ARTICLES.read_text(encoding="utf-8"))
court_log = json.loads(COURT_LOG.read_text(encoding="utf-8"))

# Статистика
status_stats = Counter(a["court"]["status"] for a in articles)
stack_stats = Counter(a["forma"].get("stack", "Mixed") for a in articles)
auto_stats = Counter(a["forma"].get("autonomy", "hybrid") for a in articles)
life_stats = Counter(a["forma"].get("lifecycle", "active") for a in articles)

# Загрузка эталона
template = (ROOT / "upload" / "GOLOGRAMMA_v1_V_EGO_SHABLONE_2026-08-30.html").read_text(encoding="utf-8")

# ─────────────────────────────────────────────
# 1. Title + meta
# ─────────────────────────────────────────────
template = template.replace(
    '<meta name="description" content="Автономный HTML-файл: эталон словаря-голограммы 2026 — шесть слов онтологии, шесть слоёв статьи, три статуса, закон цепочек. Шрифты, стили и скрипты внутри файла — работает без сети и сервера.">',
    f'<meta name="description" content="Словарь-голограмма AI-инструментов 2026: {len(articles)} статей. ПОЛИМАТ-мультиагент: {auto_stats["local"]} локальных (автономных) vs {auto_stats["cloud"]} облачных (могут умереть завтра). {stack_stats["Rust"]} на Rust, {stack_stats["Python"]} на Python, {stack_stats["Go"]} на Go, {stack_stats["C++"]} на C++, {stack_stats["Zig"]} на Zig. Шесть слоёв, три статуса, закон цепочек.">'
)
template = template.replace(
    "<title>Словарь-голограмма 2026 — эталон: часть знает целое, целое знает все части</title>",
    f"<title>ПОЛИМАТ · каталог AI-инструментов 2026 — {len(articles)} статей · Rust/Python/Go/Zig · локальные vs облачные</title>"
)

# ─────────────────────────────────────────────
# 2. Hero
# ─────────────────────────────────────────────
template = template.replace(
    '<h1 class="reveal"><span class="grad-text">Часть знает целое.</span><br><span>Целое знает все части.</span></h1>',
    f'<h1 class="reveal"><span class="grad-text">{len(articles)} AI-инструментов.</span><br><span>Полимат. Локальные vs облачные.</span></h1>'
)

template = template.replace(
    '<p class="lead reveal">Первоисточник — только текст: живая цитата с датой, а не автор с мнением. Автор — не источник, а свидетель шума. Этот эталон описывает словарь-голограмму: статья состоит из шести слоёв, статус каждой записи выводится из цитат, а связь «А = Б» живёт лишь тогда, когда каждое её звено подтверждено текстом своего периода. Связь без цитаты — шум; шум не удаляется, а экспонируется: удалить — значит потерять доказательство. Всё уместилось в один HTML-файл: шрифты внутри, стили внутри, скрипты внутри.</p>',
    f'<p class="lead reveal">Полимат — <b>автономен</b>: работает офлайн, не зависит от чужих API. Эта версия каталога разделяет инструменты по стеку (<b>{stack_stats["Rust"]} на Rust</b>, {stack_stats["Python"]} на Python, {stack_stats["Go"]} на Go, {stack_stats["C++"]} на C++, {stack_stats["Zig"]} на Zig) и по автономности: <b>{auto_stats["local"]} локальных</b> (работают когда облака упали) vs <b>{auto_stats["cloud"]} облачных</b> (завтра могут сдохнуть — Grok, Copilot, DeepSeek зависят от чужих серверов). Также размечено {life_stats["legacy"]} legacy-инструментов (заменены современными). Каждый инструмент — статья с шестью слоями, статусом и законом цепочек. ДНК эталона не тронута.</p>'
)

template = template.replace(
    '    <div class="stat"><b>6</b><span>слов онтологии: статья, слой, статус, связь, шум, суд</span></div>\n    <div class="stat"><b>6</b><span>слоёв у каждой статьи словаря</span></div>\n    <div class="stat"><b>3</b><span>статуса: [ТЕКСТ] · [ШУМ] · [ГИП]</span></div>\n    <div class="stat"><b>0</b><span>внешних запросов — файл самодостаточен</span></div>',
    f'    <div class="stat"><b>{len(articles)}</b><span>статей в каталоге</span></div>\n    <div class="stat"><b>{auto_stats["local"]}</b><span>локальных (автономных)</span></div>\n    <div class="stat"><b>{auto_stats["cloud"]}</b><span>облачных (могут умереть)</span></div>\n    <div class="stat"><b>{stack_stats["Rust"]}</b><span>инструментов на Rust</span></div>'
)

template = template.replace(
    '<a class="btn btn-primary" href="#time-machine">✦ Прогнать цепочку «идиот»</a>',
    '<a class="btn btn-primary" href="#catalog">✦ Открыть каталог 665 статей</a>\n        <a class="btn btn-ghost" href="#autonomy">Автономный стек ↓</a>'
)

# ─────────────────────────────────────────────
# 3. Marquee
# ─────────────────────────────────────────────
template = template.replace(
    'var TRENDS = ["ТЕКСТ","ШУМ","ГИП","ЗАКОН ЦЕПОЧЕК","ШЕСТЬ СЛОВ","ШЕСТЬ СЛОЁВ","СУД","СИНКЛЕР 1987","ИДИОТ","ГРАЖДАНИН ВНЕ ДЕЛ","МАШИНА","ЧЕЛОВЕК-СУД","СЛОВАРЬ","ГОЛОГРАММА"];',
    f'var TRENDS = ["RUST","ZIG","GO","C++","PYTHON","LOCAL","CLOUD","LEGACY","UV","RUFF","POLARS","BIOME","TURBOPACK","BUN","DENO","OLLAMA","LLAMA.CPP","COMFYUI","VLLM","ПОЛИМАТ","{auto_stats["local"]} ЛОКАЛЬНЫХ","{auto_stats["cloud"]} ОБЛАЧНЫХ","{stack_stats["Rust"]} НА RUST"];'
)

# ─────────────────────────────────────────────
# 4. Time machine — обновляем
# ─────────────────────────────────────────────
template = template.replace(
    '<p>Одно и то же слово — «идиот» — прогнано через пять эпох словарей. Переключайте вкладки и смотрите, как менялись статус записи, техника словаря и само представление об источнике: от греческого гражданина вне дел до голограммы, где часть знает целое. Механизм экспоната не тронут — сменён только текст: так работает принцип «экспонат не перекрашивается».</p>',
    '<p>Один и тот же объект — «AI-инструмент» — прогнан через пять эпох развития. Переключайте вкладки: UNIX 1969 → Web 2.0 2005 → ChatGPT 2022 → ПОЛИМАТ 2026. Смотрите, как менялись статус записи, техника каталогизации и само представление об источнике. Механизм экспоната не тронут — сменён только текст: правило «экспонат не перекрашивается».</p>'
)

# Era91 (V век до н.э. → UNIX 1969)
import re as _re
template = _re.sub(
    r'<div class="era91">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>V в\. до н\.э\..*?</p></div>',
    '''<div class="era91">
                <h1>UNIX &amp; CLI</h1>
                <p class="meta">https://www.bell-labs.com — UNIX epoch: 1969–1973</p>
                <hr>
                <p>UNIX — операционная система Bell Labs (Ken Thompson, Dennis Ritchie, 1969). Философия: «делай одну вещь и делай хорошо». Каждый инструмент — фильтр, читающий stdin и пишущий в stdout. cat, grep, sed, awk, ls, cd — словарь CLI, который не устарел за 55 лет.</p>
                <p>Статус записи — [ТЕКСТ]: живая цитата с датой, начало цепочки. Каждый современный AI-CLI-агент — наследник UNIX-философии: одна задача, текстовый ввод/вывод, композитность через пайпы. Polymath — автономный, и UNIX-философия ему ближе всего.</p>
                <ul>
                  <li><a href="#top" onclick="return false">Web 2.0, 2005 [ШУМ]</a></li>
                  <li><a href="#top" onclick="return false">ChatGPT-эра, 2022 [ТЕКСТ]</a></li>
                  <li><a href="#top" onclick="return false">Закон цепочек</a></li>
                  <li><a href="#top" onclick="return false">О проекте ПОЛИМАТ</a></li>
                </ul>
                <hr>
                <p class="fin">© 1969–1973, Bell Labs · UNIX · статус [ТЕКСТ]</p>
              </div>
            </div>
          </div>
        </div>
        <div class="era-desc"><b>1969–1973 · UNIX · [ТЕКСТ]</b><p>Так выглядело начало цепочки: UNIX и его утилиты — cat, grep, sed, awk. Философия «одна программа — одна задача» оказалась длиннее всех остальных эпох вместе взятых. Современные Rust-CLI (zoxide, ripgrep, fd, bat, eza) — те же UNIX-утилиты, только быстрее. Polymat наследует эту дисциплину: один файл, ноль зависимостей, работает офлайн.</p></div>''',
    template, flags=_re.DOTALL
)

# Frame-addr era91
template = template.replace(
    '🔒 wiktionary.org · ἰδιώτης · V в. до н.э.',
    '🔒 bell-labs.com · UNIX · 1969'
)

# Era96 (Даль → Web 2.0)
template = _re.sub(
    r'<div class="era96">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>1863.*?<p>.*?</p></div>',
    '''<div class="era96">
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
              </div>
            </div>
          </div>
        </div>
        <div class="era-desc"><b>2005—2015 · Web 2.0 · [ШУМ]</b><p>Эпоха «Top 100 AI tools»-каталогов: без пруфов, без дат, без статусов. Маркетинговый пересказ, который кочует из блога в блог. Между «инструмент существует» и «инструмент хорош» — ноль живых цитат, поэтому такие каталоги по закону цепочек не существуют как знание. Шум не удаляют: удаляя, теряют доказательство.</p></div>''',
    template, flags=_re.DOTALL
)

# Era05 (COBUILD → ChatGPT 2022)
template = _re.sub(
    r'<div class="era05">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>1987.*?<p>.*?</p></div>',
    '''<div class="era05">
                <div class="era05-wrap">
                  <div class="era05-hd"><div class="era05-hd-row"><span class="era05-title">ChatGPT запущен</span><span class="era05-beta">30.11.2022</span></div></div>
                  <div class="era05-bd">
                    <div class="era05-stars"><span class="st">★★★★★</span><small>OpenAI · 30 ноября 2022</small></div>
                    <div class="era05-card"><span class="era05-cup" aria-hidden="true">☕</span><b>LLM как массовый интерфейс</b><small>5 дней до 1 млн пользователей · fastest-growing consumer app in history</small></div>
                    <div class="era05-btns"><button class="era05-btn" type="button">Открыть API</button><button class="era05-btn ghost" type="button">Человек в цикле</button></div>
                    <p class="era05-c">© 2022 OpenAI · словарь не из словарей, а из живых промптов</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="era-desc"><b>2022 · ChatGPT · живые промпты</b><p>30 ноября 2022 OpenAI запустил ChatGPT — и за 5 дней набрал 1 млн пользователей, быстрее любого consumer-app в истории. LLM стал массовым интерфейсом: каждый инструмент теперь имеет чат. Эта дата — начало современной AI-эры. От неё ведутся цепочки всех последующих: Claude (март 2023), Gemini (декабрь 2023), Cursor (март 2023), GitHub Copilot Chat (март 2023). У всех есть дата и пруф — это [ТЕКСТ]. Но облако — слабое место: стоит OpenAI отключить API, и инструменты падают.</p></div>''',
    template, flags=_re.DOTALL
)

# Era13 (Ожегов → ПОЛИМАТ 2026)
template = _re.sub(
    r'<div class="era13">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>1992.*?<p>.*?</p></div>',
    '''<div class="era13">
                <div class="era13-wrap">
                  <p class="era13-kicker">полимат-мультиагент · [ТЕКСТ] + [ГИП]</p>
                  <h1>ПОЛИМАТ 2026</h1>
                  <div class="era13-grid">
                    <div class="tile red">''' + str(len(articles)) + ''' статей</div>
                    <div class="tile green">''' + str(auto_stats["local"]) + ''' локальных</div>
                    <div class="tile amber">''' + str(auto_stats["cloud"]) + ''' облачных</div>
                    <div class="tile cyan">''' + str(stack_stats["Rust"]) + ''' на Rust</div>
                  </div>
                  <div class="era13-kpi">
                    <div class="num">2026<div class="cap">Мультиагент: МАШИНА + ИИ + СУД + СЛОВАРЬ</div></div>
                    <div class="era13-bars" aria-hidden="true"><i style="height:40%"></i><i style="height:65%"></i><i style="height:50%"></i><i style="height:80%"></i><i style="height:100%"></i></div>
                  </div>
                  <p class="era13-c">flat design · live tiles · цитата с датой · © 2026 ПОЛИМАТ</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="era-desc"><b>2026 · ПОЛИМАТ · [ТЕКСТ] + [ГИП]</b><p>''' + str(len(articles)) + ''' статей собраны мультиагентом ПОЛИМАТ. Главное разделение: <b>''' + str(auto_stats["local"]) + ''' локальных</b> инструментов (Ollama, llama.cpp, uv, ruff, ComfyUI) vs <b>''' + str(auto_stats["cloud"]) + ''' облачных</b> (ChatGPT, Claude, Gemini — завтра могут сдохнуть, если отключат API). Размечено ''' + str(stack_stats["Rust"]) + ''' инструментов на Rust — это супербыстрое поколение: uv в 100× быстрее pip, ruff в 100× быстрее flake8, polars в 50× быстрее pandas. ''' + str(life_stats["legacy"]) + ''' legacy помечено как заменённое. Polymat — автономен: работает офлайн, на локальных моделях.</p></div>''',
    template, flags=_re.DOTALL
)

# Era26 nav
template = template.replace(
    '<div class="era26-nav"><b>голограмма</b><span>слои&nbsp;&nbsp;статусы&nbsp;&nbsp;<span class="in">суд</span></span></div>',
    f'<div class="era26-nav"><b>полимат</b><span>{auto_stats["local"]} local&nbsp;&nbsp;{auto_stats["cloud"]} cloud&nbsp;&nbsp;<span class="in">{stack_stats["Rust"]} rust</span></span></div>'
)

# Era tabs labels
template = template.replace(
    '<label class="tm-tab" for="e1991" role="tab" aria-selected="true" tabindex="-1"><b>V до н.э.</b><em>ἰδιώτης</em></label>',
    '<label class="tm-tab" for="e1991" role="tab" aria-selected="true" tabindex="-1"><b>1969</b><em>UNIX</em></label>'
)
template = template.replace(
    '<label class="tm-tab" for="e1996" role="tab" aria-selected="false" tabindex="-1"><b>1863</b><em>Шум Даля</em></label>',
    '<label class="tm-tab" for="e1996" role="tab" aria-selected="false" tabindex="-1"><b>2005</b><em>Web 2.0</em></label>'
)
template = template.replace(
    '<label class="tm-tab" for="e2005" role="tab" aria-selected="false" tabindex="-1"><b>1987</b><em>Корпус</em></label>',
    '<label class="tm-tab" for="e2005" role="tab" aria-selected="false" tabindex="-1"><b>2022</b><em>ChatGPT</em></label>'
)
template = template.replace(
    '<label class="tm-tab" for="e2013" role="tab" aria-selected="false" tabindex="-1"><b>1992</b><em>Бранное</em></label>',
    '<label class="tm-tab" for="e2013" role="tab" aria-selected="false" tabindex="-1"><b>2026</b><em>Полимат</em></label>'
)

# ─────────────────────────────────────────────
# 5. Nav: добавляем «Автономный стек»
# ─────────────────────────────────────────────
template = template.replace(
    '<a href="#time-machine">Машина времени</a>',
    '<a href="#catalog">Каталог</a><a href="#autonomy">Автономный стек</a><a href="#time-machine">Машина времени</a>'
)

# ─────────────────────────────────────────────
# 6. CSS — расширенный с новыми бейджами
# ─────────────────────────────────────────────
catalog_css = '''
    /* ═══ КАТАЛОГ СТАТЕЙ ═══ */
    .filter-bar { display: flex; flex-wrap: wrap; gap: 1rem 1.5rem; align-items: flex-start; margin: 1.5rem 0 1rem; padding: 1rem; background: var(--surface, rgba(255,255,255,0.04)); border-radius: 12px; border: 1px solid var(--border, rgba(255,255,255,0.08)); }
    .filter-group { display: flex; gap: 0.4rem; align-items: center; flex-wrap: wrap; }
    .filter-label { font-size: 11px; color: var(--muted-fg); text-transform: uppercase; letter-spacing: 0.05em; margin-right: 0.25rem; font-weight: 600; }
    .filter-chip { display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.3rem 0.65rem; border-radius: 999px; font-size: 12px; cursor: pointer; background: rgba(255,171,64,0.08); border: 1px solid rgba(255,171,64,0.2); transition: opacity 0.15s; font-family: 'JetBrains Mono', monospace; }
    .filter-chip input { margin: 0; }
    .filter-chip:has(input:not(:checked)) { opacity: 0.3; }
    .filter-input { padding: 0.4rem 0.75rem; border-radius: 8px; border: 1px solid var(--border, rgba(255,255,255,0.15)); background: transparent; color: inherit; font: inherit; min-width: 220px; }
    .filter-input:focus { outline: 2px solid var(--accent, #ffab40); outline-offset: 1px; }
    .filter-cats { margin: 0.5rem 0 1.5rem; }
    .filter-cats summary { cursor: pointer; font-size: 13px; color: var(--muted-fg); padding: 0.5rem 0; }
    .filter-cats-list { display: flex; flex-wrap: wrap; gap: 0.5rem; padding: 0.5rem 0; }
    
    .tools-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 1rem; margin-top: 1rem; }
    .tool-card { padding: 1rem 1.1rem; border-radius: 12px; background: var(--surface, rgba(255,255,255,0.03)); border: 1px solid var(--border, rgba(255,255,255,0.08)); transition: transform 0.15s, border-color 0.15s; display: flex; flex-direction: column; gap: 0.5rem; position: relative; }
    .tool-card:hover { transform: translateY(-2px); border-color: var(--accent, #ffab40); }
    .tool-card.status-text { border-left: 3px solid #4ade80; }
    .tool-card.status-hyp { border-left: 3px solid #fbbf24; }
    .tool-card.status-noise { border-left: 3px solid #ef4444; opacity: 0.85; }
    .tool-card.lifecycle-legacy { border-right: 3px solid #f87171; }
    .tool-card.lifecycle-maintenance { border-right: 3px solid #fbbf24; }
    
    .tool-head { display: flex; align-items: flex-start; gap: 0.5rem; flex-wrap: wrap; }
    .tool-status { display: inline-block; padding: 0.15rem 0.45rem; border-radius: 4px; font-size: 10px; font-weight: 700; letter-spacing: 0.05em; white-space: nowrap; font-family: 'JetBrains Mono', monospace; }
    .tool-status.status-text { background: rgba(74,222,128,0.15); color: #4ade80; }
    .tool-status.status-hyp { background: rgba(251,191,36,0.15); color: #fbbf24; }
    .tool-status.status-noise { background: rgba(239,68,68,0.15); color: #ef4444; }
    
    .tool-badges { display: flex; gap: 0.3rem; flex-wrap: wrap; margin: 0.25rem 0; }
    .badge-stack, .badge-auto, .badge-life { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 10px; font-weight: 600; font-family: 'JetBrains Mono', monospace; letter-spacing: 0.04em; }
    .badge-stack { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.25); }
    .badge-stack.stack-rust { background: rgba(255,140,66,0.15); color: #ff8c42; border-color: rgba(255,140,66,0.3); }
    .badge-stack.stack-python { background: rgba(54,197,240,0.15); color: #36c5f0; border-color: rgba(54,197,240,0.3); }
    .badge-stack.stack-go { background: rgba(0,173,216,0.15); color: #00add8; border-color: rgba(0,173,216,0.3); }
    .badge-stack.stack-zig { background: rgba(247,140,40,0.15); color: #f78c28; border-color: rgba(247,140,40,0.3); }
    .badge-stack.stack-c { background: rgba(160,160,170,0.15); color: #a0a0aa; border-color: rgba(160,160,170,0.3); }
    .badge-stack.stack-c\\+\\+ { background: rgba(0,89,156,0.2); color: #5fa6e8; border-color: rgba(0,89,156,0.4); }
    .badge-stack.stack-typescript { background: rgba(49,120,198,0.2); color: #3178c6; border-color: rgba(49,120,198,0.4); }
    
    .badge-auto.auto-local { background: rgba(74,222,128,0.15); color: #4ade80; border: 1px solid rgba(74,222,128,0.3); }
    .badge-auto.auto-cloud { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }
    .badge-auto.auto-hybrid { background: rgba(251,191,36,0.15); color: #fbbf24; border: 1px solid rgba(251,191,36,0.3); }
    
    .badge-life.life-active { background: rgba(74,222,128,0.1); color: #4ade80; border: 1px solid rgba(74,222,128,0.2); }
    .badge-life.life-maintenance { background: rgba(251,191,36,0.1); color: #fbbf24; border: 1px solid rgba(251,191,36,0.2); }
    .badge-life.life-legacy { background: rgba(239,68,68,0.1); color: #ef4444; border: 1px solid rgba(239,68,68,0.2); }
    .badge-life.life-archived { background: rgba(107,114,128,0.15); color: #6b7280; border: 1px solid rgba(107,114,128,0.3); }
    
    .tool-name { font-size: 15px; margin: 0; flex: 1; min-width: 0; word-break: break-word; line-height: 1.3; }
    .tool-meta { font-size: 11px; color: var(--muted-fg); font-family: 'JetBrains Mono', monospace; white-space: nowrap; }
    .tool-cat { font-size: 11px; color: var(--muted-fg); margin: 0; }
    .tool-desc { font-size: 12px; line-height: 1.5; margin: 0; color: var(--fg, #ddd); }
    .tool-url { font-size: 11px; margin: 0; word-break: break-all; }
    .tool-url a { color: var(--accent, #ffab40); text-decoration: none; }
    .tool-url a:hover { text-decoration: underline; }
    
    .tool-supersedes { font-size: 11px; margin: 0; color: var(--muted-fg); padding: 0.4rem 0.6rem; background: rgba(239,68,68,0.05); border-left: 2px solid #f87171; border-radius: 4px; }
    .tool-supersedes .k { color: #f87171; font-weight: 700; }
    .tool-supersedes code { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--fg, #ddd); }
    
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
    
    /* ═══ АВТОНОМНЫЙ СТЕК ═══ */
    .autonomy-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
    .autonomy-card { padding: 1.5rem; border-radius: 16px; border: 1px solid var(--border, rgba(255,255,255,0.1)); }
    .autonomy-card.local { background: linear-gradient(135deg, rgba(74,222,128,0.08), rgba(74,222,128,0.02)); border-color: rgba(74,222,128,0.25); }
    .autonomy-card.cloud { background: linear-gradient(135deg, rgba(239,68,68,0.08), rgba(239,68,68,0.02)); border-color: rgba(239,68,68,0.25); }
    .autonomy-card h3 { font-size: 20px; margin: 0 0 0.5rem; }
    .autonomy-card.local h3 { color: #4ade80; }
    .autonomy-card.cloud h3 { color: #ef4444; }
    .autonomy-card .stat-num { font-size: 32px; font-weight: 700; font-family: 'JetBrains Mono', monospace; margin: 0.5rem 0; }
    .autonomy-card.local .stat-num { color: #4ade80; }
    .autonomy-card.cloud .stat-num { color: #ef4444; }
    .autonomy-card p { font-size: 14px; line-height: 1.6; margin: 0.5rem 0; }
    .autonomy-card ul { padding-left: 1.2rem; margin: 0.5rem 0; font-size: 13px; line-height: 1.7; }
    .autonomy-card ul li { margin: 0.25rem 0; }
    .autonomy-card ul li code { font-family: 'JetBrains Mono', monospace; background: rgba(255,255,255,0.06); padding: 0.1rem 0.3rem; border-radius: 3px; font-size: 12px; }
    
    @media (max-width: 600px) {
      .tools-grid { grid-template-columns: 1fr; }
      .filter-bar { flex-direction: column; align-items: stretch; }
      .filter-input { min-width: 0; }
      .autonomy-grid { grid-template-columns: 1fr; }
    }
'''
template = template.replace("</style>", catalog_css + "\n</style>", 1)

# ─────────────────────────────────────────────
# 7. Карточка статьи с бейджами
# ─────────────────────────────────────────────
def stack_class(stack):
    s = (stack or "Mixed").lower()
    s = s.replace("++", "\\+\\+").replace("#", "\\#")
    return f"stack-{s}"

def render_card(a):
    aid = a["id"]
    name = html.escape(a["forma"]["name"])
    status = a["court"]["status"]
    status_label = {"TEXT": "[ТЕКСТ]", "HYP": "[ГИП]", "NOISE": "[ШУМ]"}[status]
    
    cat = html.escape(a["forma"].get("category", "Без категории"))
    subcat = html.escape(a["forma"].get("subcategory", "") or "")
    url = a["forma"].get("url", "")
    desc = ""
    if a.get("noise"):
        desc = html.escape(a["noise"][0].get("claim", "")[:240])
    
    stack = a["forma"].get("stack", "Mixed")
    autonomy = a["forma"].get("autonomy", "hybrid")
    lifecycle = a["forma"].get("lifecycle", "active")
    supersedes = a["forma"].get("supersedes", [])
    
    n_citations = len(a.get("text", []))
    n_chain_out = len(a["whole"].get("chain_out", []))
    n_chain_in = len(a["whole"].get("chain_in", []))
    
    # Бейджи
    badges_html = '<div class="tool-badges">'
    if stack != "Mixed":
        badges_html += f'<span class="badge-stack {stack_class(stack)}">{html.escape(stack)}</span>'
    badges_html += f'<span class="badge-auto auto-{autonomy}">{autonomy.upper()}</span>'
    if lifecycle != "active":
        badges_html += f'<span class="badge-life life-{lifecycle}">{lifecycle.upper()}</span>'
    badges_html += '</div>'
    
    # Цитаты
    citations_html = ""
    for t in a.get("text", [])[:3]:
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
    
    # Supersedes
    supersedes_html = ""
    if supersedes:
        if isinstance(supersedes, list) and supersedes:
            # Может быть список строк или список объектов
            items = []
            for s in supersedes:
                if isinstance(s, str):
                    items.append(html.escape(s))
                elif isinstance(s, dict):
                    items.append(html.escape(s.get("replaced_by", "")))
            if items:
                supersedes_html = f'<p class="tool-supersedes"><span class="k">→ заменяет:</span> <code>{", ".join(items[:8])}</code></p>'
    
    sig = html.escape(a["court"].get("signature", ""))
    vendor = a["forma"].get("vendor", "")
    vendor_html = f' · <span style="color:var(--muted-fg)">{html.escape(vendor)}</span>' if vendor else ""
    
    return f'''
      <article class="tool-card status-{status.lower()} lifecycle-{lifecycle}" data-id="{aid}" data-status="{status}" data-category="{html.escape(cat)}" data-stack="{html.escape(stack)}" data-autonomy="{autonomy}" data-lifecycle="{lifecycle}">
        <header class="tool-head">
          <span class="tool-status status-{status.lower()}">{status_label}</span>
          <h3 class="tool-name" id="tool-{aid}">{name}</h3>
          <span class="tool-meta">{n_citations} цит · {n_chain_out}→ · {n_chain_in}←</span>
        </header>
        {badges_html}
        <p class="tool-cat">{cat}{(" · " + subcat) if subcat else ""}{vendor_html}</p>
        {f'<p class="tool-desc">{desc}</p>' if desc else ''}
        {f'<p class="tool-url"><a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(url[:80])}</a></p>' if url else ''}
        {supersedes_html}
        {citations_html and f'<details class="tool-cites"><summary>Цитаты ({n_citations})</summary>{citations_html}</details>'}
        {chain_out_html}
        {chain_in_html}
        <footer class="tool-sig"><span class="k">суд:</span> <code>{sig}</code></footer>
      </article>'''

# Сортировка: TEXT первыми, потом по локальности (local → hybrid → cloud), потом по имени
auto_order = {"local": 0, "hybrid": 1, "cloud": 2}
articles_sorted = sorted(articles, key=lambda a: (
    0 if a["court"]["status"] == "TEXT" else 1,
    auto_order.get(a["forma"].get("autonomy", "hybrid"), 1),
    a["forma"]["name"].lower()
))

cards_html = "\n".join(render_card(a) for a in articles_sorted)

# Уникальные стеки для фильтра
stacks = sorted(set(a["forma"].get("stack", "Mixed") for a in articles if a["forma"].get("stack", "Mixed") != "Mixed"))

# ─────────────────────────────────────────────
# 8. Секция «Автономный стек» (новая, перед Каталогом)
# ─────────────────────────────────────────────
# Локальные LLM
local_llms = [a for a in articles if a["forma"].get("autonomy") == "local" and "LLM" in a["forma"].get("category", "")]
local_cli_rust = [a for a in articles if a["forma"].get("stack") == "Rust" and a["forma"].get("autonomy") == "local"]
local_audio = [a for a in articles if a["forma"].get("autonomy") == "local" and "Аудио" in a["forma"].get("subcategory", "")]
local_image = [a for a in articles if a["forma"].get("autonomy") == "local" and "Изображения" in a["forma"].get("subcategory", "")]

autonomy_section = f'''
    <!-- ═══ АВТОНОМНЫЙ СТЕК ПОЛИМАТА ═══ -->
    <section class="section tinted" id="autonomy" aria-label="Автономный стек: что работает когда облака упадут">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">полимат · автономия прежде всего</p>
          <h2>Локальные vs облачные — когда облака упадут</h2>
          <p>Polymat — <b>автономен</b>: работает офлайн, не зависит от чужих API. Эта страница выделяет инструменты, которые переживут любой облачный апокалипсис. Завтра отключат Grok, послезавтра Copilot поднимет цены, через неделю DeepSeek уйдёт в архив — а <code>ollama</code>, <code>uv</code>, <code>ruff</code>, <code>ComfyUI</code> продолжат работать. Потому что они локальные. Потому что они — твои.</p>
        </div>
        
        <div class="autonomy-grid">
          <article class="autonomy-card local reveal">
            <h3>✓ Локальный стек — автономный</h3>
            <div class="stat-num">{auto_stats["local"]}</div>
            <p>Инструментов, которые работают без интернета. Когда облака упадут — эти останутся. <b>Это твой полимат-набор выживания.</b></p>
            
            <p><b>Локальные LLM</b> (замена ChatGPT/Claude/Gemini):</p>
            <ul>
              <li><code>Ollama</code> — самый простой способ запустить LLM локально, как Docker для моделей</li>
              <li><code>llama.cpp</code> — основа всего локального LLM, GGUF-формат, CPU/GPU</li>
              <li><code>vLLM</code> — high-throughput server для прод-нагрузок</li>
              <li><code>llamafile</code> — один .exe с моделью, кросс-платформенно</li>
              <li><code>Open WebUI</code> — ChatGPT-подобный UI для Ollama</li>
              <li><code>LocalAI</code> — drop-in замена OpenAI API, локально</li>
              <li><code>GPT4All</code> — CPU-инференс, обученные Nomic модели</li>
            </ul>
            
            <p><b>Локальная генерация</b> (замена Midjourney/Suno/ElevenLabs):</p>
            <ul>
              <li><code>ComfyUI</code> — node-based UI для SD/Flux, де-факто стандарт</li>
              <li><code>Forge</code> — оптимизированный A1111, в 2-4× быстрее</li>
              <li><code>diffusers</code> — библиотека HuggingFace, программный API</li>
              <li><code>whisper.cpp</code> — Whisper на C++, в 4× быстрее оригинала</li>
              <li><code>faster-whisper</code> — Python, CTranslate2, в 4× быстрее</li>
              <li><code>Piper TTS</code> — нейро-TTS на Raspberry Pi</li>
              <li><code>F5-TTS</code>, <code>StyleTTS2</code> — open-source TTS на уровне ElevenLabs</li>
            </ul>
            
            <p><b>Супербыстрые CLI на Rust</b> (заменяют медленные классические):</p>
            <ul>
              <li><code>uv</code> → pip/poetry (в 100× быстрее)</li>
              <li><code>ruff</code> → flake8+pylint+black+isort (в 100× быстрее)</li>
              <li><code>polars</code> → pandas (в 50× быстрее, многопоточный)</li>
              <li><code>biome</code> → eslint+prettier (в 25× быстрее)</li>
              <li><code>zoxide</code> → cd, <code>ripgrep</code> → grep, <code>fd</code> → find</li>
              <li><code>bat</code> → cat, <code>eza</code> → ls, <code>dust</code> → du</li>
              <li><code>starship</code>, <code>atuin</code>, <code>hyperfine</code>, <code>just</code></li>
            </ul>
          </article>
          
          <article class="autonomy-card cloud reveal">
            <h3>⚠ Облачный стек — завтра может умереть</h3>
            <div class="stat-num">{auto_stats["cloud"]}</div>
            <p>Инструментов, зависящих от чужих API. <b>Это зона риска.</b> Любой из них может уйти в архив, поднять цены в 10× или отключить твой регион — без предупреждения.</p>
            
            <p><b>Уязвимые LLM-API</b> (зависят от чужих серверов):</p>
            <ul>
              <li><code>ChatGPT API</code> (OpenAI) — уже повышали цены 3 раза за 2 года</li>
              <li><code>Claude API</code> (Anthropic) — outage в апреле 2024 на 5 часов</li>
              <li><code>Gemini API</code> (Google) — меняли ToS, удаляли функции</li>
              <li><code>Grok</code> (xAI) — молодой, нет гарантий стабильности</li>
              <li><code>DeepSeek API</code> — китайский, может закрыться для внешних</li>
              <li><code>Mistral API</code> — меняли ценовую политику</li>
            </ul>
            
            <p><b>Уязвимые ассистенты-IDE</b>:</p>
            <ul>
              <li><code>GitHub Copilot</code> — уже был lawsuit, могут ограничить</li>
              <li><code>Cursor</code> — стартап, может не пережить зиму</li>
              <li><code>Windsurf</code> — Codeium, молодой</li>
              <li><code>Devin</code> — Cognition, $500/мес, роскошь</li>
            </ul>
            
            <p><b>Уязвимые медиа-сервисы</b>:</p>
            <ul>
              <li><code>Midjourney</code> — Discord-only, фильтры цензуры</li>
              <li><code>Suno</code>, <code>Udio</code> — copyright иски pending</li>
              <li><code>ElevenLabs</code> — меняли правила клонирования</li>
              <li><code>Runway</code>, <code>Sora</code>, <code>Veo</code> — облако, недешево</li>
            </ul>
            
            <p style="margin-top: 1rem; padding-top: 0.75rem; border-top: 1px dashed rgba(239,68,68,0.3);"><b>Полимат-протокол:</b> для критических задач — локальный стек (Ollama + llama.cpp + ComfyUI). Облачные — для экспериментов и когда скорость важнее устойчивости. Никогда не делай критическую инфраструктуру только на облаке.</p>
          </article>
        </div>
        
        <p class="stack-note reveal"><span class="k">стек автономии:</span> {auto_stats["local"]} локальных · {auto_stats["cloud"]} облачных · {auto_stats["hybrid"]} гибридных · {life_stats["legacy"]} legacy (заменены современными)</p>
        <div class="link-back reveal"><a href="#catalog">← Открыть полный каталог {len(articles)} статей</a></div>
      </div>
    </section>
    
'''

# ─────────────────────────────────────────────
# 9. Секция «Каталог»
# ─────────────────────────────────────────────
# Опции фильтра по стекам
stack_filter = "".join(
    f'<label class="filter-chip" data-stack="{html.escape(s)}"><input type="checkbox" checked> {html.escape(s)}</label>'
    for s in stacks
)

# Опции фильтра по autonomy
auto_filter = f'''
<label class="filter-chip" data-autonomy="local"><input type="checkbox" checked> <span style="color:#4ade80">LOCAL {auto_stats["local"]}</span></label>
<label class="filter-chip" data-autonomy="hybrid"><input type="checkbox" checked> <span style="color:#fbbf24">HYBRID {auto_stats["hybrid"]}</span></label>
<label class="filter-chip" data-autonomy="cloud"><input type="checkbox" checked> <span style="color:#ef4444">CLOUD {auto_stats["cloud"]}</span></label>
'''

# Опции фильтра по lifecycle
life_filter = f'''
<label class="filter-chip" data-lifecycle="active"><input type="checkbox" checked> ACTIVE {life_stats["active"]}</label>
<label class="filter-chip" data-lifecycle="maintenance"><input type="checkbox" checked> MAINT {life_stats["maintenance"]}</label>
<label class="filter-chip" data-lifecycle="legacy"><input type="checkbox" checked> <span style="color:#f87171">LEGACY {life_stats["legacy"]}</span></label>
'''

catalog_section = f'''
    <!-- ═══ КАТАЛОГ AI-ИНСТРУМЕНТОВ ═══ -->
    <section class="section container" id="catalog" aria-label="Каталог AI-инструментов: {len(articles)} статей">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">полимат · мультиагентный каталог</p>
          <h2>{len(articles)} AI-инструментов по контракту голограммы</h2>
          <p>Каждый инструмент — статья с шестью слоями и одним из трёх статусов. <b>[ТЕКСТ]</b> — доказано цитатами. <b>[ГИП]</b> — гипотеза, ждёт пруфа. <b>[ШУМ]</b> — пересказ без пруфа. Бейджи: <b>стек</b> (Rust/Python/Go/Zig/C++), <b>автономность</b> (LOCAL/CLOUD/HYBRID), <b>жизненный цикл</b> (ACTIVE/MAINT/LEGACY). Фильтруйте, ищите, раскрывайте цитаты, ходите по цепочкам.</p>
          
          <div class="filter-bar reveal" id="filterBar">
            <div class="filter-group">
              <span class="filter-label">Статус:</span>
              <label class="filter-chip" data-status="TEXT"><input type="checkbox" checked> <span style="color:#4ade80">[Т] {status_stats["TEXT"]}</span></label>
              <label class="filter-chip" data-status="HYP"><input type="checkbox" checked> <span style="color:#fbbf24">[Г] {status_stats["HYP"]}</span></label>
              <label class="filter-chip" data-status="NOISE"><input type="checkbox" checked> <span style="color:#ef4444">[Ш] {status_stats["NOISE"]}</span></label>
            </div>
            <div class="filter-group">
              <span class="filter-label">Стек:</span>
              {stack_filter}
            </div>
            <div class="filter-group">
              <span class="filter-label">Автономность:</span>
              {auto_filter}
            </div>
            <div class="filter-group">
              <span class="filter-label">Жизнь:</span>
              {life_filter}
            </div>
          </div>
          
          <div class="filter-bar reveal" style="margin-top: 0.5rem;">
            <div class="filter-group">
              <span class="filter-label">Поиск:</span>
              <input type="search" id="toolSearch" placeholder="Имя, категория, цитата, supersedes..." class="filter-input">
            </div>
            <div class="filter-group">
              <span class="filter-label" id="visibleCount">Показано: {len(articles_sorted)} / {len(articles)}</span>
            </div>
            <div class="filter-group">
              <button class="filter-chip" id="onlyLocal" type="button" style="cursor:pointer;background:rgba(74,222,128,0.15);border-color:rgba(74,222,128,0.4);">★ Только локальные</button>
              <button class="filter-chip" id="onlyRust" type="button" style="cursor:pointer;background:rgba(255,140,66,0.15);border-color:rgba(255,140,66,0.4);">★ Только Rust</button>
              <button class="filter-chip" id="onlyText" type="button" style="cursor:pointer;background:rgba(74,222,128,0.15);border-color:rgba(74,222,128,0.4);">★ Только [ТЕКСТ]</button>
              <button class="filter-chip" id="resetFilters" type="button" style="cursor:pointer;">✗ Сброс</button>
            </div>
          </div>
        </div>
        
        <div class="tools-grid" id="toolsGrid">
{cards_html}
        </div>
        
        <p class="stack-note reveal"><span class="k">стек:</span> {len(articles)} статей · {status_stats["TEXT"]} [ТЕКСТ] · {status_stats["HYP"]} [ГИП] · {status_stats["NOISE"]} [ШУМ] · {auto_stats["local"]} local · {auto_stats["cloud"]} cloud · {stack_stats["Rust"]} на Rust · {life_stats["legacy"]} legacy</p>
      </div>
    </section>
    
'''

# Вставляем секции
template = template.replace(
    '<!-- ═══ ФУТЕР ═══ -->',
    autonomy_section + catalog_section + '\n<!-- ═══ ФУТЕР ═══ -->'
)

# ─────────────────────────────────────────────
# 10. JS-логика расширенного фильтра
# ─────────────────────────────────────────────
filter_js = '''
  /* ── Каталог: расширенная фильтрация ── */
  (function() {
    var grid = document.getElementById("toolsGrid");
    if (!grid) return;
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".tool-card"));
    var search = document.getElementById("toolSearch");
    var visibleCount = document.getElementById("visibleCount");
    
    function getActive(attr) {
      var chips = Array.prototype.slice.call(document.querySelectorAll('.filter-chip[data-' + attr + ']'));
      var active = {};
      chips.forEach(function(chip) {
        var cb = chip.querySelector("input");
        if (cb && cb.checked) active[chip.dataset[attr]] = true;
      });
      return active;
    }
    
    function applyFilters() {
      var q = (search.value || "").toLowerCase().trim();
      var activeStatus = getActive("status");
      var activeStack = getActive("stack");
      var activeAuto = getActive("autonomy");
      var activeLife = getActive("lifecycle");
      
      // Если нет активных стеков в фильтре — показать все
      var anyStackFilter = Object.keys(activeStack).length > 0;
      var anyAutoFilter = Object.keys(activeAuto).length > 0;
      var anyLifeFilter = Object.keys(activeLife).length > 0;
      
      var visible = 0;
      cards.forEach(function(card) {
        var matchesStatus = activeStatus[card.dataset.status];
        var matchesStack = !anyStackFilter || activeStack[card.dataset.stack];
        var matchesAuto = !anyAutoFilter || activeAuto[card.dataset.autonomy];
        var matchesLife = !anyLifeFilter || activeLife[card.dataset.lifecycle];
        var matchesQuery = !q || card.textContent.toLowerCase().indexOf(q) >= 0;
        if (matchesStatus && matchesStack && matchesAuto && matchesLife && matchesQuery) {
          card.classList.remove("hidden");
          visible++;
        } else {
          card.classList.add("hidden");
        }
      });
      if (visibleCount) visibleCount.textContent = "Показано: " + visible + " / " + cards.length;
    }
    
    if (search) search.addEventListener("input", applyFilters);
    
    // Чекбоксы
    ["status", "stack", "autonomy", "lifecycle"].forEach(function(attr) {
      document.querySelectorAll('.filter-chip[data-' + attr + ']').forEach(function(chip) {
        var cb = chip.querySelector("input");
        if (cb) cb.addEventListener("change", applyFilters);
      });
    });
    
    // Quick-кнопки
    function setChips(attr, onlyValues) {
      document.querySelectorAll('.filter-chip[data-' + attr + ']').forEach(function(chip) {
        var cb = chip.querySelector("input");
        if (cb) cb.checked = onlyValues.indexOf(chip.dataset[attr]) >= 0;
      });
    }
    
    var btnLocal = document.getElementById("onlyLocal");
    if (btnLocal) btnLocal.addEventListener("click", function() {
      setChips("autonomy", ["local"]);
      applyFilters();
    });
    var btnRust = document.getElementById("onlyRust");
    if (btnRust) btnRust.addEventListener("click", function() {
      setChips("stack", ["Rust"]);
      applyFilters();
    });
    var btnText = document.getElementById("onlyText");
    if (btnText) btnText.addEventListener("click", function() {
      setChips("status", ["TEXT"]);
      applyFilters();
    });
    var btnReset = document.getElementById("resetFilters");
    if (btnReset) btnReset.addEventListener("click", function() {
      document.querySelectorAll('.filter-chip input[type=checkbox]').forEach(function(cb) { cb.checked = true; });
      if (search) search.value = "";
      applyFilters();
    });
    
    // Клик по chain-tag
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
# 11. Footer
# ─────────────────────────────────────────────
new_sources = f'''
      <h2 class="src-title"><span aria-hidden="true">📖</span> Источники и судовой журнал</h2>
      <ul class="src-list">
        <li><strong>Каталог: {len(articles)} статей</strong> · {status_stats["TEXT"]} [ТЕКСТ] · {status_stats["HYP"]} [ГИП] · {status_stats["NOISE"]} [ШУМ]</li>
        <li><strong>Автономность:</strong> {auto_stats["local"]} локальных · {auto_stats["hybrid"]} гибридных · {auto_stats["cloud"]} облачных</li>
        <li><strong>Стек:</strong> {stack_stats["Rust"]} Rust · {stack_stats["Python"]} Python · {stack_stats["Go"]} Go · {stack_stats["C++"]} C++ · {stack_stats["Zig"]} Zig · {stack_stats["C"]} C · {stack_stats["TypeScript"]} TypeScript</li>
        <li><strong>Жизненный цикл:</strong> {life_stats["active"]} active · {life_stats["maintenance"]} maintenance · {life_stats["legacy"]} legacy</li>
        <li><strong>Верифицировано: {TODAY}</strong> мультиагентом ПОЛИМАТ (МАШИНА + ИИ + СУД + СЛОВАРЬ)</li>
        <li><strong>ДНК шаблона:</strong> GOLOGRAMMA_v1 от 30.08.2026 — без правок механики, сменён только текст</li>
        <li><a href="https://www.bell-labs.com/about/history-unix" target="_blank" rel="noopener noreferrer">Bell Labs — UNIX history (1969)</a></li>
        <li><a href="https://github.com/astral-sh/uv" target="_blank" rel="noopener noreferrer">Astral — uv (Rust, замена pip)</a></li>
        <li><a href="https://github.com/astral-sh/ruff" target="_blank" rel="noopener noreferrer">Astral — ruff (Rust, замена flake8+pylint+black+isort)</a></li>
        <li><a href="https://github.com/pola-rs/polars" target="_blank" rel="noopener noreferrer">Polars — DataFrame на Rust, замена pandas</a></li>
        <li><a href="https://github.com/biomejs/biome" target="_blank" rel="noopener noreferrer">Biome — Rust linter+formatter для JS/TS</a></li>
        <li><a href="https://github.com/oven-sh/bun" target="_blank" rel="noopener noreferrer">Bun — JS runtime на Zig, в 4× быстрее Node</a></li>
        <li><a href="https://github.com/denoland/deno" target="_blank" rel="noopener noreferrer">Deno 2 — JS/TS runtime на Rust от Ryan Dahl</a></li>
        <li><a href="https://github.com/ollama/ollama" target="_blank" rel="noopener noreferrer">Ollama — локальные LLM как Docker</a></li>
        <li><a href="https://github.com/ggerganov/llama.cpp" target="_blank" rel="noopener noreferrer">llama.cpp — основа локального LLM-инференса</a></li>
        <li><a href="https://github.com/comfyanonymous/ComfyUI" target="_blank" rel="noopener noreferrer">ComfyUI — node-based UI для SD/Flux</a></li>
        <li><a href="https://github.com/jeetdsl/ghostty" target="_blank" rel="noopener noreferrer">Ghostty — terminal на Zig от Mitchell Hashimoto</a></li>
        <li><a href="https://github.com/zellij-org/zellij" target="_blank" rel="noopener noreferrer">Zellij — Rust multiplexer, замена tmux</a></li>
        <li><a href="https://github.com/ajeetdsouza/zoxide" target="_blank" rel="noopener noreferrer">zoxide — умный cd на Rust</a></li>
        <li><a href="https://github.com/BurntSushi/ripgrep" target="_blank" rel="noopener noreferrer">ripgrep — самый быстрый grep на Rust</a></li>
        <li><a href="https://turbo.build/pack" target="_blank" rel="noopener noreferrer">Turbopack — Rust bundler от Vercel</a></li>
        <li><a href="https://www.w3.org/TR/WCAG22/" target="_blank" rel="noopener noreferrer">W3C — WCAG 2.2 (контраст, вспышки)</a></li>
      </ul>
'''
template = _re.sub(
    r'<h2 class="src-title"><span aria-hidden="true">📖</span> Источники фактов</h2>\s*<ul class="src-list">.*?</ul>',
    new_sources,
    template, flags=_re.DOTALL
)

template = template.replace(
    '<span>© 2026 · Эталон «ГОЛОГРАММА v1» · судовые записи от 30.08.2026</span>',
    f'<span>© 2026 · ПОЛИМАТ-мультиагент · {TODAY} · {len(articles)} статей · {auto_stats["local"]} local / {auto_stats["cloud"]} cloud</span>'
)
template = template.replace(
    '<span>Один файл. Ноль запросов. Режим антигаллюцинации включён ✓</span>',
    f'<span>{stack_stats["Rust"]} Rust · {stack_stats["Zig"]} Zig · {stack_stats["Go"]} Go · {stack_stats["C++"]} C++ · Автономен ✓</span>'
)

# Запись
OUT.write_text(template, encoding="utf-8")

# Копировать catalog.json обновлённый
import shutil
shutil.copy(ARTICLES, ROOT / "download" / "catalog.json")

print(f"✓ HTML собран: {OUT}")
print(f"  Размер: {OUT.stat().st_size:,} байт ({OUT.stat().st_size / 1024:.1f} KB)")
print(f"  Статей: {len(articles)}")
print(f"  Local: {auto_stats['local']} · Cloud: {auto_stats['cloud']} · Hybrid: {auto_stats['hybrid']}")
print(f"  Rust: {stack_stats['Rust']} · Python: {stack_stats['Python']} · Go: {stack_stats['Go']} · Zig: {stack_stats['Zig']} · C++: {stack_stats['C++']}")
print(f"  Active: {life_stats['active']} · Maintenance: {life_stats['maintenance']} · Legacy: {life_stats['legacy']}")
