from pathlib import Path
import json
from collections import Counter

html = (Path(__file__).resolve().parents[1] / "polymath-catalog.html").read_text(encoding="utf-8")
articles = json.loads((Path(__file__).resolve().parents[1] / "catalog.json").read_text(encoding="utf-8"))

print("=" * 70)
print("ФИНАЛЬНЫЙ ОТЧЁТ ПОЛИМАТа (версия 2 — с автономией и стеком)")
print("=" * 70)

# Проверка
checks = [
    ("665 карточек", html.count('class="tool-card ') == 665 or html.count('class="tool-card"') + html.count('class="tool-card ') == 665),
    ("Секция autonomy", 'id="autonomy"' in html),
    ("Секция catalog", 'id="catalog"' in html),
    ("Фильтр stack", 'data-stack=' in html),
    ("Фильтр autonomy", 'data-autonomy=' in html),
    ("Фильтр lifecycle", 'data-lifecycle=' in html),
    ("Кнопка onlyLocal", 'id="onlyLocal"' in html),
    ("Кнопка onlyRust", 'id="onlyRust"' in html),
    ("Кнопка onlyText", 'id="onlyText"' in html),
    ("Бейджи stack", 'badge-stack' in html),
    ("Бейджи auto", 'badge-auto' in html),
    ("Бейджи life", 'badge-life' in html),
    ("Supersedes блоки", 'tool-supersedes' in html),
    ("UNIX в time-machine", 'UNIX' in html),
    ("ChatGPT в time-machine", 'ChatGPT' in html),
    ("ПОЛИМАТ в time-machine", 'ПОЛИМАТ' in html),
    ("Ollama в автономной секции", 'Ollama' in html),
    ("uv в автономной секции", '<code>uv</code>' in html),
    ("ruff в автономной секции", '<code>ruff</code>' in html),
    ("ComfyUI в автономной секции", 'ComfyUI' in html),
    ("llama.cpp в автономной секции", 'llama.cpp' in html),
    ("Закрытие </html>", '</html>' in html),
]

print("\nПроверка целостности:")
for name, ok in checks:
    print(f"  [{'✓' if ok else '✗'}] {name}")

# Статистика
status_stats = Counter(a["court"]["status"] for a in articles)
stack_stats = Counter(a["forma"].get("stack", "Mixed") for a in articles)
auto_stats = Counter(a["forma"].get("autonomy", "hybrid") for a in articles)
life_stats = Counter(a["forma"].get("lifecycle", "active") for a in articles)
n_supersedes = sum(1 for a in articles if a["forma"].get("supersedes"))

print(f"\nКаталог: {len(articles)} статей")
print(f"  Статусы:  TEXT={status_stats['TEXT']} HYP={status_stats['HYP']} NOISE={status_stats['NOISE']}")
print(f"  Стек:     Rust={stack_stats['Rust']} Python={stack_stats['Python']} Go={stack_stats['Go']} Zig={stack_stats['Zig']} C++={stack_stats['C++']} C={stack_stats['C']} TS={stack_stats['TypeScript']}")
print(f"  Автономия: Local={auto_stats['local']} Hybrid={auto_stats['hybrid']} Cloud={auto_stats['cloud']}")
print(f"  Жизнь:    Active={life_stats['active']} Maint={life_stats['maintenance']} Legacy={life_stats["legacy"]}")
print(f"  supersedes заполнено: {n_supersedes}")

print(f"\nФайлы:")
for p in sorted(Path('/home/z/my-project/download').iterdir()):
    if p.is_file():
        print(f"  {p.stat().st_size:>10,}  {p.name}")

print("\n" + "=" * 70)
print("✓ СБОРКА v2 ЗАВЕРШЕНА")
print("=" * 70)
