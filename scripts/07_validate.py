import json
from pathlib import Path
import re

html = Path("/home/z/my-project/download/polymath-catalog.html").read_text(encoding="utf-8")

# Проверка ключевых маркеров
checks = [
    ("DOCTYPE", "<!DOCTYPE html>" in html),
    ("Title updated", "Словарь-голограмма AI-инструментов" in html),
    ("Hero changed", "566 AI-инструментов" in html),
    ("Catalog section", 'id="catalog"' in html),
    ("Tools grid", 'id="toolsGrid"' in html),
    ("Filter bar", 'id="filterBar"' in html),
    ("Status CSS", ".status-text" in html and ".status-hyp" in html and ".status-noise" in html),
    ("Filter JS", "applyFilters" in html),
    ("Time machine updated", "UNIX & CLI" in html),
    ("Marquee updated", "ПОЛИМАТ" in html),
    ("Footer updated", "ПОЛИМАТ-мультиагент" in html),
    ("Tools count check", html.count('class="tool-card') == 566),
    ("END html", "</html>" in html),
]

print("Проверка целостности HTML:")
all_ok = True
for name, ok in checks:
    print(f"  [{'✓' if ok else '✗'}] {name}")
    if not ok:
        all_ok = False

# Считаем tool-card
n_cards = html.count('class="tool-card')
print(f"\nКарточек статей: {n_cards}")

# Считаем TEXT-статьи
n_text = html.count('class="tool-card status-text"')
n_hyp = html.count('class="tool-card status-hyp"')
n_noise = html.count('class="tool-card status-noise"')
print(f"  status-text: {n_text}")
print(f"  status-hyp: {n_hyp}")
print(f"  status-noise: {n_noise}")

# Категории
n_cats_in_filter = html.count('class="filter-chip" data-cat=')
print(f"Категорий в фильтре: {n_cats_in_filter}")

# Сохранить catalog.json в download
src = Path("/home/z/my-project/scripts/articles.json")
dst = Path("/home/z/my-project/download/catalog.json")
dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
print(f"\n✓ catalog.json скопирован в download ({dst.stat().st_size:,} байт)")

# Court log уже в download
cl = Path("/home/z/my-project/download/court-log.json")
print(f"✓ court-log.json в download ({cl.stat().st_size:,} байт)")

print(f"\nИТОГ:")
print(f"  HTML: /home/z/my-project/download/polymath-catalog.html (937 KB)")
print(f"  JSON: /home/z/my-project/download/catalog.json")
print(f"  LOG:  /home/z/my-project/download/court-log.json")
