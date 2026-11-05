import json
from pathlib import Path
from collections import Counter

articles = json.loads(Path("/home/z/my-project/scripts/articles.json").read_text(encoding="utf-8"))

# Статистика по статусам
status_counts = Counter(a["court"]["status"] for a in articles)
print("Статусы:", dict(status_counts))

# Статистика по категориям
cat_counts = Counter(a["forma"].get("category", "?") for a in articles)
print("\nПо категориям:")
for c, n in cat_counts.most_common():
    print(f"  {n:4d}  {c}")

# Топ-15 статей с наибольшим числом связей
print("\nТоп-15 статей по числу исходящих связей:")
sorted_by_links = sorted(articles, key=lambda a: -len(a["whole"].get("chain_out", [])))
for a in sorted_by_links[:15]:
    print(f"  {len(a['whole'].get('chain_out', [])):3d} ← {a['forma']['name']:35s} [{a['court']['status']}]")

# Все TEXT-статьи
print("\nВсе [ТЕКСТ] статьи:")
for a in articles:
    if a["court"]["status"] == "TEXT":
        print(f"  • {a['forma']['name']:35s} → {len(a['text'])} цитат, {len(a['whole'].get('chain_out', []))} связей")

# Пример структуры одной статьи
print("\nПример статьи (Cursor):")
for a in articles:
    if "cursor" in a["forma"]["name"].lower():
        print(json.dumps(a, ensure_ascii=False, indent=2)[:2000])
        break
