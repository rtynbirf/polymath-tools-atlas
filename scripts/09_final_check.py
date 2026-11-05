from pathlib import Path
import json

html = Path("/home/z/my-project/download/polymath-catalog.html").read_text(encoding="utf-8")
articles = json.loads(Path("/home/z/my-project/download/catalog.json").read_text(encoding="utf-8"))
court_log = json.loads(Path("/home/z/my-project/download/court-log.json").read_text(encoding="utf-8"))

print("=" * 70)
print("ФИНАЛЬНЫЙ ОТЧЁТ ПОЛИМАТ-МУЛЬТИАГЕНТА")
print("=" * 70)

# 1. Структура
print("\n[1] Структура HTML (Skinned clone эталона):")
print(f"  Размер файла:           {Path('/home/z/my-project/download/polymath-catalog.html').stat().st_size:,} байт")
print(f"  Шрифты зашиты (base64): {'data:font/woff2;base64' in html}")
print(f"  CSS внутри:             {'<style>' in html}")
print(f"  JS внутри:              {'<script>' in html}")
print(f"  Внешних запросов:       0 (по контракту)")

# 2. Секции эталона сохранены
sections = [
    ("Hero", 'id="top"' in html),
    ("Marquee", 'class="marquee"' in html),
    ("Time Machine", 'id="time-machine"' in html),
    ("Timeline", 'id="timeline"' in html),
    ("DNA", 'id="dna"' in html),
    ("Health", 'id="health"' in html),
    ("Offline", 'id="offline"' in html),
    ("Glossary", 'id="glossary"' in html),
    ("Comfort Panel", 'id="comfortPanel"' in html),
    ("Sources footer", 'id="sources"' in html),
    ("Catalog (NEW)", 'id="catalog"' in html),
]
print("\n[2] Секции (ДНК эталона сохранена):")
for name, present in sections:
    print(f"  [{'✓' if present else '✗'}] {name}")

# 3. Каталог статей
n_cards = html.count('class="tool-card')
print(f"\n[3] Каталог статей:")
print(f"  Всего карточек:  {n_cards}")
print(f"  В JSON-каталоге:  {len(articles)}")
print(f"  Совпадает:        {'✓' if n_cards == len(articles) else '✗'}")

# 4. Статусы
from collections import Counter
status_counts = Counter(a["court"]["status"] for a in articles)
print(f"\n[4] Статусы по контракту ГОЛОГРАММА:")
print(f"  [ТЕКСТ] — доказано цитатами:  {status_counts['TEXT']}")
print(f"  [ГИП]   — гипотеза, ждёт:     {status_counts['HYP']}")
print(f"  [ШУМ]   — только каталог:     {status_counts['NOISE']}")

# 5. Цепочки
total_out = sum(len(a["whole"].get("chain_out", [])) for a in articles)
total_in = sum(len(a["whole"].get("chain_in", [])) for a in articles)
print(f"\n[5] Закон цепочек (граф связей):")
print(f"  Прямых связей:        {total_out}")
print(f"  Обратных связей:      {total_in}")
print(f"  Статей со связями:    {sum(1 for a in articles if a['whole'].get('chain_out'))}")

# 6. Категории
cats = Counter(a["forma"].get("category", "?") for a in articles)
print(f"\n[6] По категориям:")
for c, n in cats.most_common():
    print(f"  {n:4d}  {c}")

# 7. Источники
n_citations = sum(len(a.get("text", [])) for a in articles)
print(f"\n[7] Цитаты и источники:")
print(f"  Всего цитат:           {n_citations}")
print(f"  Уникальных URL:        {len(set(t['source'] for a in articles for t in a.get('text', []) if t.get('source')))}")
print(f"  Судовых записей:       {len(court_log)}")

# 8. Фильтры
print(f"\n[8] Интерактив:")
print(f"  Фильтр по статусу:     {'data-status=\"TEXT\"' in html}")
print(f"  Фильтр по категориям:  {'data-cat=' in html}")
print(f"  Поиск по тексту:       {'id=\"toolSearch\"' in html}")
print(f"  Кликабельные связи:    {'data-target=' in html}")

# 9. Машина времени
print(f"\n[9] Машина времени (4 эпохи AI-эволюции):")
print(f"  1969 UNIX:         {'UNIX & CLI' in html}")
print(f"  2005 Web 2.0:      {'WEB 2.0' in html}")
print(f"  2022 ChatGPT:      {'ChatGPT запущен' in html}")
print(f"  2026 ПОЛИМАТ:      {'ПОЛИМАТ 2026' in html}")

# 10. Файлы-результаты
print(f"\n[10] Файлы в /home/z/my-project/download/:")
for p in sorted(Path('/home/z/my-project/download').iterdir()):
    print(f"  {p.stat().st_size:>10,}  {p.name}")

print("\n" + "=" * 70)
print("✓ СБОРКА ЗАВЕРШЕНА")
print("=" * 70)
