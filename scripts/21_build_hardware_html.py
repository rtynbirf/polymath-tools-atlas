#!/usr/bin/env python3
"""
HTML-отчёт «ПОЛИМАТ HARDWARE v1» — skinned clone эталона GOLOGRAMMA.
Та же ДНК (CSS/JS/шрифты/секции), другой текст: спецификации железа.
"""
import json
import re
import html
from pathlib import Path

ROOT = Path("/home/z/my-project")
TEMPLATE = ROOT / "upload" / "GOLOGRAMMA_v1_V_EGO_SHABLONE_2026-08-30.html"
OUT = ROOT / "download" / "polymath-hardware.html"

data = json.loads((ROOT / "scripts" / "hardware_calc.json").read_text(encoding="utf-8"))
template = TEMPLATE.read_text(encoding="utf-8")

# ─────────────────────────────────────────────
# 1. Meta + Title
# ─────────────────────────────────────────────
template = template.replace(
    '<meta name="description" content="Автономный HTML-файл: эталон словаря-голограммы 2026 — шесть слов онтологии, шесть слоёв статьи, три статуса, закон цепочек. Шрифты, стили и скрипты внутри файла — работает без сети и сервера.">',
    'ПОЛИМАТ HARDWARE v1 — спецификация железа под локальный мультиагентный LLM-суперстек. 3 конфигурации: Tower Pro 4× RTX 5090 (128GB VRAM), Rack Beast 8× RTX 5090 (256GB VRAM), Mac Studio M3 Ultra (192GB unified). Полный расчёт VRAM/потребления/охлаждения/BOM. Ресурсы не ограничены — локальность прежде всего.'
)
template = template.replace(
    "<title>Словарь-голограмма 2026 — эталон: часть знает целое, целое знает все части</title>",
    "<title>ПОЛИМАТ HARDWARE v1 — локальный мультиагентный LLM-суперстек · спецификация железа</title>"
)

# ─────────────────────────────────────────────
# 2. Hero
# ─────────────────────────────────────────────
template = template.replace(
    '<h1 class="reveal"><span class="grad-text">Часть знает целое.</span><br><span>Целое знает все части.</span></h1>',
    '<h1 class="reveal"><span class="grad-text">Локальный мультиагент.</span><br><span>Полная автономия. Всё на борту.</span></h1>'
)

template = template.replace(
    '<p class="lead reveal">Первоисточник — только текст: живая цитата с датой, а не автор с мнением. Автор — не источник, а свидетель шума. Этот эталон описывает словарь-голограмму: статья состоит из шести слоёв, статус каждой записи выводится из цитат, а связь «А = Б» живёт лишь тогда, когда каждое её звено подтверждено текстом своего периода. Связь без цитаты — шум; шум не удаляется, а экспонируется: удалить — значит потерять доказательство. Всё уместилось в один HTML-файл: шрифты внутри, стили внутри, скрипты внутри.</p>',
    '<p class="lead reveal">Ресурсы не ограничены. Цель — <b>локальность</b>, <b>быстродействие</b>, <b>полная автономия</b>. Никаких облаков, никаких чужих API, ничего что может умереть завтра. На борту крутятся одновременно: <b>LLM 70B</b> (СУД-агент) + <b>3× LLM 8B</b> (МАШИНА/ИИ/СЛОВАРЬ параллельно) + <b>Flux/SDXL</b> (картинки) + <b>Wan 2.5</b> (видео) + <b>Whisper + F5-TTS</b> (голос) + <b>Infinity embeddings</b> (RAG). Три конфигурации железа: <b>Tower Pro</b> ($30K, 128GB VRAM), <b>Rack Beast</b> ($52K, 256GB VRAM), <b>Mac Studio Ultra</b> ($11K, 192GB unified). ДНК эталона не тронута — сменён только текст.</p>'
)

template = template.replace(
    '<a class="btn btn-primary" href="#time-machine">✦ Прогнать цепочку «идиот»</a>',
    '<a class="btn btn-primary" href="#vram">✦ VRAM-бюджет Polymat</a>\n        <a class="btn btn-ghost" href="#configs">3 конфигурации ↓</a>'
)

template = template.replace(
    '    <div class="stat"><b>6</b><span>слов онтологии: статья, слой, статус, связь, шум, суд</span></div>\n    <div class="stat"><b>6</b><span>слоёв у каждой статьи словаря</span></div>\n    <div class="stat"><b>3</b><span>статуса: [ТЕКСТ] · [ШУМ] · [ГИП]</span></div>\n    <div class="stat"><b>0</b><span>внешних запросов — файл самодостаточен</span></div>',
    '    <div class="stat"><b>3</b><span>конфигурации: Tower / Rack / Mac</span></div>\n    <div class="stat"><b>128-256</b><span>GB VRAM на борту</span></div>\n    <div class="stat"><b>9</b><span>задач Polymat в параллель</span></div>\n    <div class="stat"><b>0</b><span>облачных зависимостей</span></div>'
)

# ─────────────────────────────────────────────
# 3. Marquee — ключевые термины железа
# ─────────────────────────────────────────────
template = template.replace(
    'var TRENDS = ["ТЕКСТ","ШУМ","ГИП","ЗАКОН ЦЕПОЧЕК","ШЕСТЬ СЛОВ","ШЕСТЬ СЛОЁВ","СУД","СИНКЛЕР 1987","ИДИОТ","ГРАЖДАНИН ВНЕ ДЕЛ","МАШИНА","ЧЕЛОВЕК-СУД","СЛОВАРЬ","ГОЛОГРАММА"];',
    'var TRENDS = ["RTX 5090","H100 NVL","M3 ULTRA","THREADRIPPER 7995WX","EPYC 9755","256GB VRAM","1TB DDR5 ECC","NVME GEN5","VLLM","OLLAMA","LLAMA.CPP","COMFYUI","WHISPER.CPP","F5-TTS","INFINITY","TENSOR PARALLEL","PAGED ATTENTION","LOCAL FIRST","AUTONOMY","ПОЛИМАТ"];'
)

# ─────────────────────────────────────────────
# 4. Time Machine → Эволюция AI-железа
# ─────────────────────────────────────────────
template = template.replace(
    '<p>Одно и то же слово — «идиот» — прогнано через пять эпох словарей. Переключайте вкладки и смотрите, как менялись статус записи, техника словаря и само представление об источнике: от греческого гражданина вне дел до голограммы, где часть знает целое. Механизм экспоната не тронут — сменён только текст: так работает принцип «экспонат не перекрашивается».</p>',
    '<p>Один и тот же объект — «локальный AI» — прогнан через пять эпох железа. Переключайте вкладки: CPU-инференс 2017 → GPU-революция 2020 → ChatGPT-облако 2022 → Mac Studio 2023 → RTX 5090 era 2025. Смотрите, как менялось представление о том, что значит «локально». Механизм экспоната не тронут — сменён только текст.</p>'
)

# Era91 → CPU-инференс 2017
import re as _re
template = _re.sub(
    r'<div class="era91">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>V в\. до н\.э\..*?</p></div>',
    '''<div class="era91">
                <h1>CPU inference</h1>
                <p class="meta">2017 · llama.cpp предок · CPU-only</p>
                <hr>
                <p>До 2017 локальные LLM были фантастикой. GPT-2 (1.5B параметров) появился в 2019 — работал на CPU со скоростью 2 токена в секунду. VGGT, Word2Vec, BERT-base — всё это можно было запустить на ноутбуке, но не как чат-ассистента.</p>
                <p>Статус записи — [ТЕКСТ]: живая цитата с датой, начало цепочки. CPU-инференс — начало локального AI. Geoffrey Hinton в 2017 сказал, что пора остановить обучение радиационных врачей и начать обучать нейросети. Это была эпоха, когда локальный AI значил «у меня на ноуте крутится BERT».</p>
                <ul>
                  <li><a href="#top" onclick="return false">GPU-революция, 2020 [ТЕКСТ]</a></li>
                  <li><a href="#top" onclick="return false">ChatGPT-облако, 2022 [ШУМ]</a></li>
                  <li><a href="#top" onclick="return false">Mac Studio, 2023 [ТЕКСТ]</a></li>
                  <li><a href="#top" onclick="return false">RTX 5090 era, 2025 [ТЕКСТ]</a></li>
                </ul>
                <hr>
                <p class="fin">© 2017-2019 · CPU-only · статус [ТЕКСТ]</p>
              </div>
            </div>
          </div>
        </div>
        <div class="era-desc"><b>2017-2019 · CPU inference · [ТЕКСТ]</b><p>До GPU-эры локальный AI значил: CPU, 2 токена в секунду, маленькие модели. BERT-base (2018) — 110M параметров, работал на ноуте. GPT-2 1.5B (2019) — уже нужен был сервер. Это было время, когда «локально» значило «медленно но бесплатно». Сегодня CPU-инференс живёт только как fallback — для whisper.cpp и small models.</p></div>''',
    template, flags=_re.DOTALL
)

template = template.replace(
    '🔒 wiktionary.org · ἰδιώτης · V в. до н.э.',
    '🔒 github.com/ggerganov/llama.cpp · 2017-2019'
)

# Era96 → GPU-революция 2020 (RTX 3090 24GB)
template = _re.sub(
    r'<div class="era96">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>1863.*?<p>.*?</p></div>',
    '''<div class="era96">
                <div class="era96-box">
                  <div class="era96-head"><h1>☕ RTX 3090 ЭРА ☕</h1><p>GPU 24GB · 2020—2022!!!</p></div>
                  <table class="era96-t"><tbody>
                    <tr>
                      <td class="era96-news"><b>GPU-БОOM!</b><p>— RTX 3090 24GB = $1500</p><p>— LLaMA 7B влезает в VRAM!</p></td>
                      <td class="era96-main"><p class="navy">«LLaMA 7B на одной RTX 3090» — и началась эра локального AI. Скорость: 30-50 ток/сек.</p><p>Автор — не источник. Между «у меня GPU» и «у меня локальный ассистент» был зазор: модели были слабые, контекст короткий, RAG не было.</p><span class="counter blink">СТАТУС: [ШУМ] · «У меня локальный ChatGPT»</span></td>
                    </tr>
                  </tbody></table>
                  <div class="era96-marq">★★★ GPU-РЕВОЛЮЦИЯ ★★★ 24GB VRAM ★★★ LLAMA 7B ★★★ 30 ТОК/СЕК ★★★ ЛОКАЛЬНО!!! ★★★</div>
                  <p class="era96-foot">This entry is [ШУМ] · хранится и экспонируется</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="era-desc"><b>2020-2022 · RTX 3090 · [ШУМ]</b><p>RTX 3090 с 24GB VRAM за $1499 сломал рынок: LLaMA 7B, потом 13B, потом 33B — всё это можно было запустить дома. Но «локальный ChatGPT» было преувеличением: модели путались в простых задачах, контекст 2K, RAG ещё не было. Это был шум — громкий, музейный, но шум. Шум не удаляют: он — доказательство того, что было до настоящего локального AI.</p></div>''',
    template, flags=_re.DOTALL
)

# Era05 → ChatGPT-облако 2022 (но с пометкой что это ШУМ для автономии)
template = _re.sub(
    r'<div class="era05">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>1987.*?<p>.*?</p></div>',
    '''<div class="era05">
                <div class="era05-wrap">
                  <div class="era05-hd"><div class="era05-hd-row"><span class="era05-title">ChatGPT-облако</span><span class="era05-beta">30.11.2022</span></div></div>
                  <div class="era05-bd">
                    <div class="era05-stars"><span class="st">★★★★★</span><small>OpenAI · 30 ноября 2022</small></div>
                    <div class="era05-card"><span class="era05-cup" aria-hidden="true">☕</span><b>Быстро, дёшево, умно — но не локально</b><small>5 дней до 1 млн пользователей · fastest-growing consumer app in history</small></div>
                    <div class="era05-btns"><button class="era05-btn" type="button">Открыть API</button><button class="era05-btn ghost" type="button">Зависим от чужого сервера</button></div>
                    <p class="era05-c">© 2022 OpenAI · облако — не локально, не автономно</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="era-desc"><b>2022 · ChatGPT · облако</b><p>30 ноября 2022 OpenAI запустил ChatGPT — и за 5 дней набрал 1 млн пользователей. Это была победа качества, но не автономии: модель на чужом сервере, цена растёт, ToS меняются, регион могут отключить. Для Polymat эта эпоха — предупреждение: облако удобно, но зависимость. Отсюда начинается обратная волна — к локальному.</p></div>''',
    template, flags=_re.DOTALL
)

# Era13 → Mac Studio M3 Ultra 2023-2024
template = _re.sub(
    r'<div class="era13">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>1992.*?<p>.*?</p></div>',
    '''<div class="era13">
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
        </div>
        <div class="era-desc"><b>2023-2024 · Mac Studio M3 Ultra · [ТЕКСТ]</b><p>Mac Studio M3 Ultra с 192GB unified memory — первый потребительский компьютер, на котором Llama 3 70B Q4 работает целиком в памяти без offload. Плюсы: тишина (18 дБ), 270W потребление, Metal/MLX экосистема. Минусы: нет CUDA, vLLM не работает, скорость в 2-3× ниже RTX 5090. Для тех, кто не терпит шум rack-сервера — оптимальный выбор. 70B бегает, 235B MoE — с offload в CPU, медленно.</p></div>''',
    template, flags=_re.DOTALL
)

# Era26 → RTX 5090 era 2025
template = template.replace(
    '<div class="era26-nav"><b>голограмма</b><span>слои&nbsp;&nbsp;статусы&nbsp;&nbsp;<span class="in">суд</span></span></div>',
    '<div class="era26-nav"><b>RTX 5090</b><span>32GB GDDR7&nbsp;&nbsp;575W&nbsp;&nbsp;<span class="in">4× = 128GB</span></span></div>'
)

# Era tabs labels
template = template.replace(
    '<label class="tm-tab" for="e1991" role="tab" aria-selected="true" tabindex="-1"><b>V до н.э.</b><em>ἰδιώτης</em></label>',
    '<label class="tm-tab" for="e1991" role="tab" aria-selected="true" tabindex="-1"><b>2017</b><em>CPU</em></label>'
)
template = template.replace(
    '<label class="tm-tab" for="e1996" role="tab" aria-selected="false" tabindex="-1"><b>1863</b><em>Шум Даля</em></label>',
    '<label class="tm-tab" for="e1996" role="tab" aria-selected="false" tabindex="-1"><b>2020</b><em>RTX 3090</em></label>'
)
template = template.replace(
    '<label class="tm-tab" for="e2005" role="tab" aria-selected="false" tabindex="-1"><b>1987</b><em>Корпус</em></label>',
    '<label class="tm-tab" for="e2005" role="tab" aria-selected="false" tabindex="-1"><b>2022</b><em>ChatGPT</em></label>'
)
template = template.replace(
    '<label class="tm-tab" for="e2013" role="tab" aria-selected="false" tabindex="-1"><b>1992</b><em>Бранное</em></label>',
    '<label class="tm-tab" for="e2013" role="tab" aria-selected="false" tabindex="-1"><b>2023</b><em>Mac Studio</em></label>'
)
template = template.replace(
    '<label class="tm-tab" for="e2026" role="tab" aria-selected="false" tabindex="-1"><b>2026</b><em>Голограмма</em></label>',
    '<label class="tm-tab" for="e2026" role="tab" aria-selected="false" tabindex="-1"><b>2025</b><em>RTX 5090</em></label>'
)

# Era26 описание — добавим RTX 5090
era26_desc_old = '<b>2026 · Голограмма</b><p>Проект 2026 года: статья из шести слоёв, статус из цитат, суд из подписей. Часть знает целое: каждая статья несёт карту словаря; целое знает все части: словарь пересчитывает статусы сам. Экспонат, который вы смотрите, собран тем же приёмом: чужая оболочка 2026-го, свой текст — и ни одной правки механики. Голографический принцип — в действии, а не на словах.</p>'
era26_desc_new = '<b>2025 · RTX 5090 era · [ТЕКСТ]</b><p>RTX 5090 с 32GB GDDR7 за $2200 — сломал барьер: 4× 5090 = 128GB VRAM в tower-корпусе за $30K. Это сопоставимо с 1× H100 80GB по VRAM, но в 4× дешевле. На таком железе Llama 3.3 70B работает на 50-70 ток/сек, SDXL/Flux — мгновенно, Wan 2.5 видео — за минуты. Локальный мультиагент с 4 параллельными LLM — реальность. Это и есть железо Polymat.</p>'
template = template.replace(era26_desc_old, era26_desc_new)

# Era26 main panel
era26_sub_old = '<p class="era26-sub">Часть знает целое, целое знает все части. Шесть слов онтологии — и ни одного нового термина.</p>'
era26_sub_new = '<p class="era26-sub">4× RTX 5090 = 128GB VRAM. Llama 70B + 3× 8B параллельно. Полная автономия — без облака.</p>'
template = template.replace(era26_sub_old, era26_sub_new)

era26_b26_old = '<div class="b26 full"><span class="cap"><span class="ai">✦</span> шесть слоёв статьи</span><p class="big">ФОРМА · ТЕКСТ · ПОЛЕ · ЦЕЛОЕ · ШУМ · СУД</p><small>МАШИНА ищет · ИИ группирует · СУД утверждает</small></div>'
era26_b26_new = '<div class="b26 full"><span class="cap"><span class="ai">✦</span> ПОЛИМАТ HARDWARE v1</span><p class="big">RTX 5090 · THREADRIPPER · DDR5 ECC · NVME GEN5</p><small>4 GPU = 128GB VRAM · 70B + видео + голос в параллель</small></div>'
template = template.replace(era26_b26_old, era26_b26_new)

# ─────────────────────────────────────────────
# 5. Nav: заменить на аппаратные разделы
# ─────────────────────────────────────────────
template = template.replace(
    '<nav class="main-nav" aria-label="Основная навигация">\n      <a href="#time-machine">Машина времени</a>\n      <a href="#timeline">Вехи</a>\n      <a href="#dna">Устройство</a>\n      <a href="#health">Здоровье</a>\n      <a href="#offline">Автономность</a>\n      <a href="#glossary">Словарь</a>\n      <a href="#sources">Источники</a>\n    </nav>',
    '<nav class="main-nav" aria-label="Основная навигация">\n      <a href="#vram">VRAM-бюджет</a>\n      <a href="#configs">Конфигурации</a>\n      <a href="#bom">BOM/Цены</a>\n      <a href="#power">Питание/Охлаждение</a>\n      <a href="#software">Софт-стек</a>\n      <a href="#sources">Источники</a>\n    </nav>'
)

# ─────────────────────────────────────────────
# 6. CSS — дополнения для отчёта
# ─────────────────────────────────────────────
hw_css = '''
    /* ═══ ПОЛИМАТ HARDWARE ═══ */
    .vram-table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; font-size: 14px; }
    .vram-table th { background: rgba(255,171,64,0.1); color: var(--accent, #ffab40); padding: 0.75rem; text-align: left; font-weight: 600; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 2px solid rgba(255,171,64,0.3); }
    .vram-table td { padding: 0.75rem; border-bottom: 1px solid var(--border, rgba(255,255,255,0.08)); vertical-align: top; }
    .vram-table tr:hover td { background: rgba(255,171,64,0.04); }
    .vram-num { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--accent, #ffab40); }
    .vram-total { background: rgba(255,171,64,0.08); font-weight: 700; }
    .vram-total td { border-top: 2px solid var(--accent, #ffab40); border-bottom: 2px solid var(--accent, #ffab40); }
    
    .scenario-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
    .scenario-card { padding: 1.25rem; border-radius: 12px; background: var(--surface, rgba(255,255,255,0.03)); border: 1px solid var(--border, rgba(255,255,255,0.08)); border-left: 3px solid var(--accent, #ffab40); }
    .scenario-card h4 { margin: 0 0 0.5rem; font-size: 15px; }
    .scenario-card .num { font-size: 28px; font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--accent, #ffab40); margin: 0.5rem 0; }
    .scenario-card p { font-size: 13px; line-height: 1.6; margin: 0.25rem 0; }
    
    .config-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(360px, 1fr)); gap: 1.5rem; margin: 1.5rem 0; }
    .config-card { padding: 1.5rem; border-radius: 16px; background: var(--surface, rgba(255,255,255,0.03)); border: 1px solid var(--border, rgba(255,255,255,0.1)); }
    .config-card.tower { border-color: rgba(74,222,128,0.3); background: linear-gradient(135deg, rgba(74,222,128,0.06), rgba(74,222,128,0.01)); }
    .config-card.rack { border-color: rgba(239,68,68,0.3); background: linear-gradient(135deg, rgba(239,68,68,0.06), rgba(239,68,68,0.01)); }
    .config-card.mac { border-color: rgba(168,85,247,0.3); background: linear-gradient(135deg, rgba(168,85,247,0.06), rgba(168,85,247,0.01)); }
    .config-card h3 { margin: 0 0 0.25rem; font-size: 20px; }
    .config-card.tower h3 { color: #4ade80; }
    .config-card.rack h3 { color: #ef4444; }
    .config-card.mac h3 { color: #a855f7; }
    .config-card .tagline { font-size: 13px; color: var(--muted-fg); margin: 0 0 1rem; font-family: 'JetBrains Mono', monospace; }
    .config-card .use-case { font-size: 13px; line-height: 1.6; margin: 0 0 1rem; padding: 0.75rem; background: rgba(255,255,255,0.04); border-radius: 8px; }
    
    .config-stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem; margin: 1rem 0; }
    .config-stat { padding: 0.75rem; background: rgba(255,255,255,0.04); border-radius: 8px; }
    .config-stat .label { font-size: 11px; color: var(--muted-fg); text-transform: uppercase; letter-spacing: 0.05em; }
    .config-stat .value { font-size: 18px; font-family: 'JetBrains Mono', monospace; font-weight: 700; margin-top: 0.25rem; }
    
    .bom-table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 13px; }
    .bom-table th { background: rgba(255,171,64,0.08); color: var(--accent, #ffab40); padding: 0.6rem 0.75rem; text-align: left; font-weight: 600; font-size: 11px; text-transform: uppercase; border-bottom: 1px solid rgba(255,171,64,0.2); }
    .bom-table td { padding: 0.6rem 0.75rem; border-bottom: 1px solid var(--border, rgba(255,255,255,0.06)); vertical-align: top; }
    .bom-table tr:hover td { background: rgba(255,171,64,0.03); }
    .bom-table .price { font-family: 'JetBrains Mono', monospace; text-align: right; color: var(--accent, #ffab40); font-weight: 600; }
    .bom-table .total-row { background: rgba(255,171,64,0.08); font-weight: 700; }
    .bom-table .total-row td { border-top: 2px solid var(--accent, #ffab40); border-bottom: 2px solid var(--accent, #ffab40); }
    
    .software-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1rem; margin: 1.5rem 0; }
    .software-card { padding: 1rem; border-radius: 10px; background: rgba(255,255,255,0.03); border: 1px solid var(--border, rgba(255,255,255,0.08)); border-left: 3px solid #818cf8; }
    .software-card h4 { margin: 0 0 0.25rem; font-size: 14px; color: #818cf8; font-family: 'JetBrains Mono', monospace; }
    .software-card p { margin: 0.25rem 0; font-size: 12px; line-height: 1.5; color: var(--fg, #ddd); }
    .software-card .role { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 10px; font-weight: 700; font-family: 'JetBrains Mono', monospace; background: rgba(129,140,249,0.15); color: #818cf8; margin-bottom: 0.5rem; }
    
    @media (max-width: 600px) {
      .config-grid { grid-template-columns: 1fr; }
      .config-stats { grid-template-columns: 1fr; }
      .vram-table, .bom-table { font-size: 12px; }
      .vram-table th, .vram-table td, .bom-table th, .bom-table td { padding: 0.5rem; }
    }
'''
template = template.replace("</style>", hw_css + "\n</style>", 1)

# ─────────────────────────────────────────────
# 7. Заменяем секции ДНК на аппаратные
# ─────────────────────────────────────────────
# Найдём timeline-секцию и заменим на VRAM-бюджет
# Сначала найдём границы секции timeline
timeline_start = template.find('<!-- ═══')
# Найдём секцию timeline
timeline_section_start = template.find('<section class="section container tm"')
# Лучше: заменим содержимое секции timeline

# Удалим секцию timeline (станет частью new sections)
# Найдём конец секции timeline (</section> после </div> секции tm)
tm_match = _re.search(r'<section class="section container tm"[^>]*>.*?</section>', template, _re.DOTALL)
if tm_match:
    template = template[:tm_match.start()] + "{{TIMELINE_PLACEHOLDER}}" + template[tm_match.end():]

# Также удалим секцию ДНК (заменится на конфигурации)
dna_match = _re.search(r'<section class="section tinted"[^>]*id="dna"[^>]*>.*?</section>', template, _re.DOTALL)
if dna_match:
    template = template[:dna_match.start()] + "{{DNA_PLACEHOLDER}}" + template[dna_match.end():]

# И секцию здоровья заменим на питание/охлаждение
health_match = _re.search(r'<section class="section tinted"[^>]*id="health"[^>]*>.*?</section>', template, _re.DOTALL)
if health_match:
    template = template[:health_match.start()] + "{{HEALTH_PLACEHOLDER}}" + template[health_match.end():]

# И секцию автономности заменим на software-stack
offline_match = _re.search(r'<section class="section"[^>]*id="offline"[^>]*>.*?</section>', template, _re.DOTALL)
if offline_match:
    template = template[:offline_match.start()] + "{{OFFLINE_PLACEHOLDER}}" + template[offline_match.end():]

# И глоссарий заменим на источники
glossary_match = _re.search(r'<section class="section tinted"[^>]*id="glossary"[^>]*>.*?</section>', template, _re.DOTALL)
if glossary_match:
    template = template[:glossary_match.start()] + "{{GLOSSARY_PLACEHOLDER}}" + template[glossary_match.end():]

# ─────────────────────────────────────────────
# 8. Секции VRAM-бюджет
# ─────────────────────────────────────────────
vram_rows = ""
for v in data["vram_budget"]:
    vram_rows += f'''
        <tr>
          <td><strong>{html.escape(v['task'])}</strong><br><small style="color:var(--muted-fg)">{html.escape(v['model'])}</small></td>
          <td class="vram-num">{v['vram_gb']} GB</td>
          <td><code style="font-family:'JetBrains Mono',monospace;font-size:11px;">{html.escape(v['engine'])}</code></td>
          <td style="font-size:12px;">{html.escape(v['tokens_sec'])}</td>
        </tr>'''

vram_section = f'''
    <!-- ═══ VRAM-БЮДЖЕТ ПОЛИМАТа ═══ -->
    <section class="section container" id="vram" aria-label="VRAM-бюджет: сколько памяти нужно Polymat">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · vram budget</p>
          <h2>Сколько VRAM нужно Polymat</h2>
          <p>Polymat — мультиагент: одновременно крутятся <b>1× LLM 70B</b> (СУД-агент, главное рассуждение), <b>3× LLM 8B</b> (МАШИНА/ИИ/СЛОВАРЬ параллельно), <b>Flux/SDXL</b> для картинок, <b>Wan 2.5</b> для видео, <b>Whisper + F5-TTS</b> для голоса, <b>Infinity embeddings</b> для RAG. Это не «запустить одну модель» — это полноценный локальный дата-центр в одной коробке.</p>
        </div>
        
        <table class="vram-table reveal">
          <thead>
            <tr>
              <th>Задача Polymat</th>
              <th>VRAM</th>
              <th>Engine</th>
              <th>Скорость</th>
            </tr>
          </thead>
          <tbody>
            {vram_rows}
            <tr class="vram-total">
              <td><strong>ИТОГО параллельно (без видео, 70B)</strong></td>
              <td class="vram-num">{data['totals']['A']} GB</td>
              <td colspan="2">Tower Pro (128GB) — с натяжкой, нужно выгружать видео</td>
            </tr>
            <tr class="vram-total">
              <td><strong>ИТОГО параллельно (полный, 70B + видео)</strong></td>
              <td class="vram-num">{data['totals']['B']} GB</td>
              <td colspan="2">Rack Beast (256GB) — комфортно</td>
            </tr>
            <tr class="vram-total">
              <td><strong>ИТОГО с 235B MoE (топ-качество)</strong></td>
              <td class="vram-num">{data['totals']['C']} GB</td>
              <td colspan="2">Rack Beast 8× 5090 (256GB) — только влезает</td>
            </tr>
          </tbody>
        </table>
        
        <div class="scenario-grid reveal">
          <div class="scenario-card">
            <h4>Сценарий A: 70B без видео</h4>
            <div class="num">{data['totals']['A']} GB</div>
            <p><b>Tower Pro</b> (4× RTX 5090, 128GB) — не влезает полностью, нужно выгружать 2 из 3 LLM 8B или SDXL по требованию. <b>Rack Beast</b> (256GB) — с запасом 100GB.</p>
          </div>
          <div class="scenario-card">
            <h4>Сценарий B: 70B + видео</h4>
            <div class="num">{data['totals']['B']} GB</div>
            <p>Только <b>Rack Beast</b> (256GB) или <b>Mac Studio Ultra</b> (192GB unified) — последний с offload в CPU, медленно. Видео можно гонять по очереди с выгрузкой остальных моделей.</p>
          </div>
          <div class="scenario-card">
            <h4>Сценарий C: 235B MoE</h4>
            <div class="num">{data['totals']['C']} GB</div>
            <p>Только <b>Rack Beast</b> (256GB) с offload 100GB в DDR5 (12-channel EPYC). Скорость 10-20 ток/сек, но это SOTA-качество локально.</p>
          </div>
        </div>
        <p class="stack-note reveal"><span class="k">правило:</span> VRAM ≠ RAM. VRAM — это память GPU, быстрая (868 ГБ/с на RTX 5090), но маленькая. RAM — медленная (85 ГБ/с на DDR5-5600), но её можно поставить 1TB. Offload в RAM работает, но в 10× медленнее.</p>
      </div>
    </section>
'''

# ─────────────────────────────────────────────
# 9. Секция конфигураций
# ─────────────────────────────────────────────
configs_section = '''
    <!-- ═══ 3 КОНФИГУРАЦИИ ═══ -->
    <section class="section tinted" id="configs" aria-label="3 конфигурации железа">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · hardware configs</p>
          <h2>Три конфигурации — от Tower до Rack Beast</h2>
          <p>Ресурсы не ограничены. Цель — локальность, быстродействие, полная автономия. Выбрал три варианта под разные сценарии: <b>Tower Pro</b> для домашней/офисной сборки с водянкой (4× 5090, $30K), <b>Rack Beast</b> для 235B MoE без компромиссов (8× 5090, $52K), <b>Mac Studio Ultra</b> для тех кто не терпит шум (192GB unified, $11K, 270W).</p>
        </div>
        
        <div class="config-grid reveal">
          
          <!-- TOWER PRO -->
          <article class="config-card tower reveal">
            <h3>Tower Pro — рабочая станция</h3>
            <p class="tagline">4× RTX 5090 / 128GB VRAM / Threadripper 7995WX / 512GB DDR5 ECC</p>
            <p class="use-case"><b>Сценарий A+B</b> (70B + видео + все агенты). Домашняя/офисная сборка. Водянка на 4 GPU, тишина 38 дБ. Помещается под столом. Меняет игру: 128GB VRAM в одной коробке за $30K — это уровень 1.5× H100, но в 4× дешевле.</p>
            
            <div class="config-stats">
              <div class="config-stat"><div class="label">Цена</div><div class="value">$30,249</div></div>
              <div class="config-stat"><div class="label">VRAM</div><div class="value">128 GB</div></div>
              <div class="config-stat"><div class="label">RAM</div><div class="value">512 GB</div></div>
              <div class="config-stat"><div class="label">CPU</div><div class="value">96C</div></div>
              <div class="config-stat"><div class="label">Потребление</div><div class="value">2.4 kW</div></div>
              <div class="config-stat"><div class="label">Шум</div><div class="value">38 дБ</div></div>
            </div>
            
            <p style="font-size:13px;line-height:1.6;margin-top:1rem;"><b>Что потянет параллельно:</b></p>
            <ul style="font-size:12px;line-height:1.7;padding-left:1.2rem;">
              <li>LLM 70B Q4 (СУД) — 48GB ✓</li>
              <li>LLM 8B Q8 ×3 (агенты) — 24GB ✓</li>
              <li>SDXL/Flux dev — 16GB ✓</li>
              <li>Whisper + F5-TTS + embeddings — 12GB ✓</li>
              <li>KV cache — 20GB ✓</li>
              <li><b>Запас: 8GB</b> — Wan 2.5 видео по очереди (выгрузка остальных)</li>
            </ul>
            <p style="font-size:13px;margin-top:1rem;padding:0.5rem;background:rgba(74,222,128,0.08);border-radius:6px;"><b>Вердикт:</b> оптимально для 95% задач Polymat. Видео — по очереди.</p>
          </article>
          
          <!-- RACK BEAST -->
          <article class="config-card rack reveal">
            <h3>Rack Beast — серверный монстр</h3>
            <p class="tagline">8× RTX 5090 / 256GB VRAM / EPYC 9755 128C / 1.15TB DDR5 ECC</p>
            <p class="use-case"><b>Сценарий C</b> (235B MoE + 70B + видео + всё параллельно). 4U rackmount, нужен 19" шкаф или гараж. Шум 65 дБ — отдельная комната. 256GB VRAM позволяет запустить Qwen3-235B-A22B Q4 + одновременно 70B для судьи + видео + голос. Без компромиссов.</p>
            
            <div class="config-stats">
              <div class="config-stat"><div class="label">Цена</div><div class="value">$51,700</div></div>
              <div class="config-stat"><div class="label">VRAM</div><div class="value">256 GB</div></div>
              <div class="config-stat"><div class="label">RAM</div><div class="value">1.15 TB</div></div>
              <div class="config-stat"><div class="label">CPU</div><div class="value">128C</div></div>
              <div class="config-stat"><div class="label">Потребление</div><div class="value">3.8 kW</div></div>
              <div class="config-stat"><div class="label">Шум</div><div class="value">65 дБ</div></div>
            </div>
            
            <p style="font-size:13px;line-height:1.6;margin-top:1rem;"><b>Что потянет параллельно:</b></p>
            <ul style="font-size:12px;line-height:1.7;padding-left:1.2rem;">
              <li>LLM 235B MoE Q4 (топ-качество) — 130GB ✓</li>
              <li>LLM 70B Q4 (СУД) — 48GB ✓</li>
              <li>SDXL/Flux — 16GB ✓</li>
              <li>Wan 2.5 видео — 40GB ✓</li>
              <li>Whisper + F5-TTS + embeddings — 12GB ✓</li>
              <li><b>Запас: 10GB</b> — всё в параллель, без выгрузки</li>
            </ul>
            <p style="font-size:13px;margin-top:1rem;padding:0.5rem;background:rgba(239,68,68,0.08);border-radius:6px;"><b>Вердикт:</b> единственный вариант для 235B MoE параллельно со всем стеком. Нужна отдельная комната (тепло 3.8kW).</p>
          </article>
          
          <!-- MAC STUDIO ULTRA -->
          <article class="config-card mac reveal">
            <h3>Mac Studio M3 Ultra</h3>
            <p class="tagline">Apple M3 Ultra 32C / 192GB unified / 80-core GPU / 270W</p>
            <p class="use-case"><b>Сценарий A</b> (70B + картинки + голос, без видео). Тихая альтернатива: 18 дБ (бесшумен), 270W (в 9× меньше Tower), помещается на столе. Минус: нет CUDA, vLLM не работает, только Metal/MLX. Скорость в 2-3× ниже RTX 5090.</p>
            
            <div class="config-stats">
              <div class="config-stat"><div class="label">Цена</div><div class="value">$10,649</div></div>
              <div class="config-stat"><div class="label">Unified</div><div class="value">192 GB</div></div>
              <div class="config-stat"><div class="label">GPU</div><div class="value">80 core</div></div>
              <div class="config-stat"><div class="label">CPU</div><div class="value">32C</div></div>
              <div class="config-stat"><div class="label">Потребление</div><div class="value">270 W</div></div>
              <div class="config-stat"><div class="label">Шум</div><div class="value">18 дБ</div></div>
            </div>
            
            <p style="font-size:13px;line-height:1.6;margin-top:1rem;"><b>Что потянет параллельно:</b></p>
            <ul style="font-size:12px;line-height:1.7;padding-left:1.2rem;">
              <li>LLM 70B Q4 (через MLX) — 48GB ✓</li>
              <li>LLM 8B Q8 ×3 — 24GB ✓ (медленнее CUDA)</li>
              <li>SDXL/Flux (через DiffusersBee) — 16GB ✓</li>
              <li>Whisper.cpp + F5-TTS — 12GB ✓</li>
              <li><b>Запас: 92GB</b> — много места, но скорость ниже</li>
              <li>235B MoE — только с offload, очень медленно</li>
            </ul>
            <p style="font-size:13px;margin-top:1rem;padding:0.5rem;background:rgba(168,85,247,0.08);border-radius:6px;"><b>Вердикт:</b> для тех кто ценит тишину. Не для 235B, не для видео. Лучшая начальная точка.</p>
          </article>
          
        </div>
        
        <p class="stack-note reveal"><span class="k">правило:</span> 1× RTX 5090 (32GB, $2200) по VRAM эквивалентен 1.3× Mac Studio (192GB unified, но shared). По скорости CUDA в 2-3× быстрее Metal. Tower Pro — оптимум цена/производительность для Polymat.</p>
      </div>
    </section>
'''

# ─────────────────────────────────────────────
# 10. BOM-таблицы (детальные)
# ─────────────────────────────────────────────
def render_bom(cfg_name, cfg):
    parts = ["chassis", "cpu", "motherboard", "ram", "gpus", "storage", "psu", "cooling", "network", "ups"]
    rows = ""
    for p in parts:
        part = cfg.get(p, {})
        if not isinstance(part, dict):
            continue
        model = html.escape(part.get("model", "—"))
        notes = html.escape(part.get("notes", ""))
        price = part.get("price_usd", 0)
        if price == 0 and cfg_name == "Mac Studio Ultra":
            if p == "chassis":
                price = 6999  # базовая цена Mac включена в chassis
                model = "Apple Mac Studio M3 Ultra 192GB (включая SoC/CPU/GPU/RAM/motherboard/SSD)"
        rows += f'''
            <tr>
              <td><strong>{p.upper()}</strong></td>
              <td>{model}<br><small style="color:var(--muted-fg)">{notes}</small></td>
              <td class="price">${price:,}</td>
            </tr>'''
    rows += f'''
            <tr class="total-row">
              <td colspan="2"><strong>ИТОГО {cfg_name}</strong></td>
              <td class="price">${cfg['total_price_usd']:,}</td>
            </tr>'''
    return rows

bom_section = f'''
    <!-- ═══ BOM/ЦЕНЫ ═══ -->
    <section class="section container" id="bom" aria-label="BOM: детали и цены">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · bill of materials</p>
          <h2>BOM — детали и цены</h2>
          <p>Полные спецификации по каждой конфигурации. Цены — розничные США на сентябрь 2025, в долларах. В РФ/СНГ умножить на 1.5-2× (санкции, доставка, таможня). Все компоненты доступны на Newegg/Amazon/B&H, кроме Threadripper PRO — через OEM-каналы.</p>
        </div>
        
        <h3 class="reveal" style="color:#4ade80;">Tower Pro — $30,249</h3>
        <table class="bom-table reveal">
          <thead><tr><th>Компонент</th><th>Модель</th><th>Цена</th></tr></thead>
          <tbody>{render_bom("Tower Pro", data["configs"]["Tower Pro"])}</tbody>
        </table>
        
        <h3 class="reveal" style="color:#ef4444;margin-top:2.5rem;">Rack Beast — $51,700</h3>
        <table class="bom-table reveal">
          <thead><tr><th>Компонент</th><th>Модель</th><th>Цена</th></tr></thead>
          <tbody>{render_bom("Rack Beast", data["configs"]["Rack Beast"])}</tbody>
        </table>
        
        <h3 class="reveal" style="color:#a855f7;margin-top:2.5rem;">Mac Studio Ultra — $10,649</h3>
        <table class="bom-table reveal">
          <thead><tr><th>Компонент</th><th>Модель</th><th>Цена</th></tr></thead>
          <tbody>{render_bom("Mac Studio Ultra", data["configs"]["Mac Studio Ultra"])}</tbody>
        </table>
        
        <p class="stack-note reveal"><span class="k">варианты:</span> Tower Pro можно собрать на 2× RTX 5090 (64GB VRAM, $20K) — хватит для 70B + 1 агент. Rack Beast можно заменить на 4× H100 NVL (376GB VRAM, $120K) — для enterprise. Mac Studio M4 Ultra (ожидается Q1 2026) поднимет unified memory до 256GB.</p>
      </div>
    </section>
'''

# ─────────────────────────────────────────────
# 11. Питание/Охлаждение (замена секции здоровья)
# ─────────────────────────────────────────────
power_section = '''
    <!-- ═══ ПИТАНИЕ И ОХЛАЖДЕНИЕ ═══ -->
    <section class="section tinted" id="power" aria-label="Питание и охлаждение">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · power & cooling</p>
          <h2>Питание и охлаждение — критично</h2>
          <p>RTX 5090 потребляет 575W на пике. 4× = 2300W только GPU. Добавим CPU (350W TDP Threadripper), RAM, NVMe, вентиляторы — получаем <b>2.4kW для Tower Pro</b> и <b>3.8kW для Rack Beast</b>. Это сопоставимо с масляным обогревателем на максимуме. Решить вопрос охлаждения — иначе троттлинг убьёт производительность.</p>
        </div>
        
        <div class="bento">
          <article class="card span2 reveal"><span class="icon-chip" aria-hidden="true">01</span><h3>Tower Pro: 2.4 kW тепла</h3>
            <p>Custom water loop EKWB на 4 GPU + CPU. Два радиатора MO-R3 420mm (по 1.2 кг меди каждый) выносят ~2.5kW при дельте 15°C. Насос D5 + резервуар 250ml. Вентиляторы Noctua A14 industrial — 6 шт. на 600 RPM. Шум 38 дБ, как тихий разговор. Без водянки — 4 blower-кулера под нагрузкой дают 65+ дБ, как пылесос.</p></article>
          <article class="card reveal"><span class="icon-chip" aria-hidden="true">02</span><h3>2× PSU 1600W с Add2PSU</h3>
            <p>Один Corsair AX1600i тянет CPU+2 GPU, второй — ещё 2 GPU + периферию. Add2PSU синхронизирует включение. Цифровой мониторинг через iCUE — виден потребление в реальном времени. Альтернатива: 1× Seasonic PRIME TX-2000 (2000W), но нужен special-order.</p></article>
          <article class="card reveal"><span class="icon-chip" aria-hidden="true">03</span><h3>Помещение: 15 m² минимум</h3>
            <p>Tower Pro выделяет 2.4kW тепла в комнату. Летом без кондиционера температура поднимется на 8-10°C за час. Нужен сплит 12000 BTU (3.5kW cold). Rack Beast — 24000 BTU (7kW). Счёт за электричество при 24/7 = 2.4 × 24 × 30 × $0.15 = <b>$260/мес</b> (Tower) или <b>$410/мес</b> (Rack).</p></article>
          <article class="card span2 reveal"><span class="icon-chip" aria-hidden="true">04</span><h3>Rack Beast: 3.8 kW, нужен шкаф</h3>
            <p>4U Supermicro chassis с 8 GPU blower — шум 65 дБ, как сервер в дата-центре. Штатные радиаторы GPU (турбины) выдувают горячий воздух наружу. Помещение должно иметь вытяжку. Альтернатива: иммерсионное охлаждение в баке с Engineered Fluids ElectroCool — добавляет $2000, но тишина и +30% производительности из-за отсутствия троттлинга.</p></article>
          <article class="card reveal"><span class="icon-chip" aria-hidden="true">05</span><h3>UPS обязателен</h3>
            <p>APC Smart-UPS SRT 3000VA для Tower Pro ($1500) — 30 минут автономии при 2.4kW. Для Rack Beast — APC Symmetra LX 8kVA ($5000), 20 минут. Задача UPS не «работать часами» — а корректно завершить vLLM, сохранить модели в cache, избежать повреждения NVMe при сбое.</p></article>
          <article class="card reveal"><span class="icon-chip" aria-hidden="true">06</span><h3>Mac Studio: 270W, без вопросов</h3>
            <p>Mac Studio M3 Ultra потребляет 270W — меньше, чем одна RTX 5090. Пассивное охлаждение, 18 дБ. UPS APC Back-UPS Pro 1500VA ($250) даёт 40+ минут автономии. Идеально для квартиры — никаких спец-требований к помещению.</p></article>
          <article class="card reveal"><span class="icon-chip" aria-hidden="true">07</span><h3>Электрика: 32A 220V линия</h3>
            <p>Для Tower Pro — отдельный автомат 16A на 220V (стандарт в РФ). Для Rack Beast — 32A 220V (нужна спец-розетка CEE 7/7 и линия 4mm²). Стандартная квартирная проводка 2.5mm² на 16A не выдержит 3.8kW持续. Вызов электрика обязателен.</p></article>
          <article class="card reveal"><span class="icon-chip" aria-hidden="true">08</span><h3>Кабели: 4× PCIe 12V-2x6</h3>
            <p>RTX 5090 использует новый разъём 12V-2x6 (600W). 4× GPU = 4× кабеля от PSU. Не использовать переходники 4× 8-pin → 12V-2x6 — они плавятся при пике. Только нативные кабели от Corsair/Seasonic. Проверить затяжку разъёмов — плохо вставленный 12V-2x6 = пожар.</p></article>
        </div>
        <p class="stack-note reveal"><span class="k">нормы:</span> IEC 62368-1 (безопасность) · NFPA 70 (электрика) · ASHRAE TC 9.9 (дата-центр температурные режимы 18-27°C) · OSHA 1910.95 (шум на рабочем месте ≤ 85 дБ)</p>
      </div>
    </section>
'''

# ─────────────────────────────────────────────
# 12. Софт-стек (замена автономности)
# ─────────────────────────────────────────────
software_section = '''
    <!-- ═══ СОФТ-СТЕК ПОЛИМАТа ═══ -->
    <section class="section container" id="software" aria-label="Софт-стек: что крутится на железе">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · software stack</p>
          <h2>Софт-стек — что крутится на железе</h2>
          <p>Железо без софта — кусок кремния. Polymat запускает стек, в котором каждый агент живёт в своём процессе, общается через Redis/NATS, хранит контекст в Qdrant, генерирует медиа через ComfyUI. Всё локальное, всё open-source, всё из <a href="polymath-catalog.html" style="color:var(--accent,#ffab40);">каталога 665 инструментов</a>.</p>
        </div>
        
        <div class="software-grid reveal">
          <article class="software-card">
            <span class="role">СУД-агент (главный)</span>
            <h4>vLLM + Llama 3.3 70B Q4</h4>
            <p>Главный LLM-агент, рассуждает, принимает решения, верифицирует. Запускается через <code>vLLM</code> с PagedAttention, tensor-parallel на 2× GPU. 48GB VRAM, 50-70 ток/сек на Tower Pro.</p>
          </article>
          
          <article class="software-card">
            <span class="role">МАШИНА (поиск/сбор)</span>
            <h4>3× vLLM + Llama 3.1 8B Q8</h4>
            <p>Параллельные агенты для рутинных задач: web-парсинг, классификация, суммаризация. Каждый на своём GPU. 8GB VRAM на инстанс, 180-250 ток/сек каждый. Continual batching обрабатывает 100+ параллельных запросов.</p>
          </article>
          
          <article class="software-card">
            <span class="role">ИИ (рассуждение)</span>
            <h4>Ollama + DeepSeek-R1 32B</h4>
            <p>Reasoning-модель с visible chain-of-thought. Запускается через Ollama (проще API) или vLLM (быстрее). 20GB VRAM. Для задач где нужно «подумать вслух» — разбор кода, поиск багов, планирование.</p>
          </article>
          
          <article class="software-card">
            <span class="role">СЛОВАРЬ (граф)</span>
            <h4>Neo4j + Qdrant + Infinity</h4>
            <p>Граф связей между статьями (Neo4j), векторная база для RAG (Qdrant), embedding server (Infinity на Rust, 10K docs/sec). Хранит весь каталог 665 статей, индексирует новые за секунды.</p>
          </article>
          
          <article class="software-card">
            <span class="role">Генерация картинок</span>
            <h4>ComfyUI + FLUX.1-dev</h4>
            <p>Node-based UI для diffusion-моделей. FLUX.1-dev — лучшее качество. SDXL Turbo — для быстрых набросков. 16GB VRAM, 1 картинка/3 сек. Поддерживает LoRA, ControlNet, IPAdapter.</p>
          </article>
          
          <article class="software-card">
            <span class="role">Генерация видео</span>
            <h4>ComfyUI + Wan 2.5 / CogVideoX</h4>
            <p>Wan 2.5 (Alibaba, open-source) — 5 секунд видео 720p за 4 минуты на 4× 5090. CogVideoX 5B — альтернатива. 40GB VRAM. Полностью локально, без подписки Runway/Sora.</p>
          </article>
          
          <article class="software-card">
            <span class="role">Голос: STT</span>
            <h4>whisper.cpp + faster-whisper</h4>
            <p>Whisper-large-v3 на C++ (whisper.cpp) или Python (faster-whisper). Realtime в 12× быстрее реального времени. 4GB VRAM. Поддержка 99 языков, word-level timestamps через whisperX.</p>
          </article>
          
          <article class="software-card">
            <span class="role">Голос: TTS</span>
            <h4>F5-TTS / StyleTTS2 / Piper</h4>
            <p>F5-TTS — zero-shot клонирование голоса за 6 секунд, качество на уровне ElevenLabs. StyleTTS2 — стиль-перенос. Piper TTS — для Raspberry Pi/edge. 4GB VRAM. Realtime в 4× быстрее.</p>
          </article>
          
          <article class="software-card">
            <span class="role">Code-агенты</span>
            <h4>Aider + OpenHands + Cline</h4>
            <p>Aider — pair programming в терминале. OpenHands — автономный dev-агент. Cline — VS Code extension. Все три через локальный Ollama/vLLM endpoint. Никакого облака, никакой подписки.</p>
          </article>
          
          <article class="software-card">
            <span class="role">Оркестрация</span>
            <h4>n8n + LangGraph + Redis</h4>
            <p>n8n — visual workflow automation. LangGraph — агентный фреймворк. Redis — pub/sub между агентами. Вся логика Polymat: кто что делает, когда зовёт кого, как верифицирует.</p>
          </article>
          
          <article class="software-card">
            <span class="role">Веб-интерфейс</span>
            <h4>Open WebUI + Lobe Chat</h4>
            <p>Open WebUI — самохостящийся UI для Ollama, как ChatGPT. Lobe Chat — альтернатива с плагинами. Оба ходят к локальному vLLM endpoint. Доступ с любого устройства в LAN.</p>
          </article>
          
          <article class="software-card">
            <span class="role">Мониторинг</span>
            <h4>Grafana + Langfuse + nvtop</h4>
            <p>Grafana — дашборд CPU/GPU/RAM. Langfuse — LLM observability (токены, латентность, cost). nvtop — realtime GPU utilization в терминале. Всё локально, без Datadog.</p>
          </article>
        </div>
        
        <p class="stack-note reveal"><span class="k">стек:</span> всё локальное · всё open-source · всё из <a href="polymath-catalog.html" style="color:var(--accent,#ffab40);">каталога Polymat</a> · ноль облачных зависимостей · работает при выключенном интернете</p>
      </div>
    </section>
'''

# ─────────────────────────────────────────────
# 13. Источники (замена footer sources)
# ─────────────────────────────────────────────
sources_section = '''
      <h2 class="src-title"><span aria-hidden="true">📖</span> Источники и спецификации</h2>
      <ul class="src-list">
        <li><strong>NVIDIA RTX 5090:</strong> 32GB GDDR7, 575W TDP, 134 TFLOPS FP16, $1999 MSRP (01.2025)</li>
        <li><strong>AMD Threadripper PRO 7995WX:</strong> 96C/192T, 350W TDP, 8-channel DDR5-5200 ECC, sTR5</li>
        <li><strong>AMD EPYC 9755 (Turin):</strong> 128C/256T, 400W TDP, 12-channel DDR5-6400, SP5</li>
        <li><strong>Apple M3 Ultra:</strong> 32C CPU, 80C GPU, 192GB unified, 800 GB/s bandwidth</li>
        <li><a href="https://github.com/vllm-project/vllm" target="_blank" rel="noopener noreferrer">vLLM — PagedAttention, high-throughput LLM server</a></li>
        <li><a href="https://github.com/ollama/ollama" target="_blank" rel="noopener noreferrer">Ollama — Docker для LLM</a></li>
        <li><a href="https://github.com/ggerganov/llama.cpp" target="_blank" rel="noopener noreferrer">llama.cpp — основа локального LLM-инференса</a></li>
        <li><a href="https://github.com/comfyanonymous/ComfyUI" target="_blank" rel="noopener noreferrer">ComfyUI — node-based UI для SD/Flux</a></li>
        <li><a href="https://github.com/SYSTRAN/faster-whisper" target="_blank" rel="noopener noreferrer">faster-whisper — CTranslate2 Whisper, в 4× быстрее</a></li>
        <li><a href="https://github.com/SWivid/F5-TTS" target="_blank" rel="noopener noreferrer">F5-TTS — open-source zero-shot TTS</a></li>
        <li><a href="https://github.com/michaelfeil/infinity" target="_blank" rel="noopener noreferrer">Infinity — Rust embedding server, в 10× быстрее TEI</a></li>
        <li><a href="https://github.com/qdrant/qdrant" target="_blank" rel="noopener noreferrer">Qdrant — vector DB на Rust</a></li>
        <li><a href="https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/" target="_blank" rel="noopener noreferrer">NVIDIA — RTX 5090 official page</a></li>
        <li><a href="https://www.amd.com/en/products/processors/laptop-threadripper/pro-7000-series.html" target="_blank" rel="noopener noreferrer">AMD — Threadripper PRO 7995WX</a></li>
        <li><a href="https://www.apple.com/mac-studio/" target="_blank" rel="noopener noreferrer">Apple — Mac Studio M3 Ultra</a></li>
        <li><a href="https://www.corsair.com/us/en/p/psu/cp-9020087-na/ax1600i-digital-atx-psu" target="_blank" rel="noopener noreferrer">Corsair AX1600i — цифровой 1600W PSU</a></li>
        <li><a href="https://www.ekwb.com/" target="_blank" rel="noopener noreferrer">EKWB — custom water cooling</a></li>
        <li><a href="https://www.apc.com/" target="_blank" rel="noopener noreferrer">APC — Smart-UPS для серверов</a></li>
      </ul>
'''

# Заменяем старый список источников
template = _re.sub(
    r'<h2 class="src-title"><span aria-hidden="true">📖</span> Источники фактов</h2>\s*<ul class="src-list">.*?</ul>',
    sources_section,
    template, flags=_re.DOTALL
)

# Footer copyright
template = template.replace(
    '<span>© 2026 · Эталон «ГОЛОГРАММА v1» · судовые записи от 30.08.2026</span>',
    '<span>© 2025 · ПОЛИМАТ HARDWARE v1 · спецификация локального мультиагентного LLM-суперстека</span>'
)
template = template.replace(
    '<span>Один файл. Ноль запросов. Режим антигаллюцинации включён ✓</span>',
    '<span>3 конфигурации · 128-256GB VRAM · 0 облачных зависимостей ✓</span>'
)

# ─────────────────────────────────────────────
# 14. Подставляем секции на место плейсхолдеров
# ─────────────────────────────────────────────
# Time-machine section оставляем, заменяем только timeline (там где было про Полимат 2026 — это теперь RTX 5090 era)
template = template.replace("{{TIMELINE_PLACEHOLDER}}", vram_section)
template = template.replace("{{DNA_PLACEHOLDER}}", configs_section)
template = template.replace("{{HEALTH_PLACEHOLDER}}", power_section)
template = template.replace("{{OFFLINE_PLACEHOLDER}}", software_section)
template = template.replace("{{GLOSSARY_PLACEHOLDER}}", bom_section)

# ─────────────────────────────────────────────
# 15. Запись
# ─────────────────────────────────────────────
OUT.write_text(template, encoding="utf-8")

print(f"✓ HTML собран: {OUT}")
print(f"  Размер: {OUT.stat().st_size:,} байт ({OUT.stat().st_size / 1024:.1f} KB)")

# Проверка ключевых маркеров
checks = [
    ("Title", "ПОЛИМАТ HARDWARE v1" in template),
    ("VRAM section", 'id="vram"' in template),
    ("Configs section", 'id="configs"' in template),
    ("BOM section", 'id="bom"' in template),
    ("Power section", 'id="power"' in template),
    ("Software section", 'id="software"' in template),
    ("Tower Pro card", 'class="config-card tower' in template),
    ("Rack Beast card", 'class="config-card rack' in template),
    ("Mac Studio card", 'class="config-card mac' in template),
    ("VRAM table", 'class="vram-table' in template),
    ("BOM tables", template.count('class="bom-table') >= 3),
    ("Software cards", template.count('class="software-card') >= 12),
    ("END html", "</html>" in template),
]
print("\nПроверка:")
for name, ok in checks:
    print(f"  [{'✓' if ok else '✗'}] {name}")
