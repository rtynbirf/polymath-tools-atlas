from pathlib import Path
p = Path("/home/z/my-project/download/polymath-hardware.html")
html = p.read_text(encoding="utf-8")

checks = [
    ("Title", "ПОЛИМАТ HARDWARE v1" in html),
    ("Hero заголовок", "Локальный мультиагент" in html),
    ("Nav: VRAM-бюджет", 'href="#vram"' in html),
    ("Nav: Конфигурации", 'href="#configs"' in html),
    ("Nav: BOM/Цены", 'href="#bom"' in html),
    ("Nav: Питание/Охлаждение", 'href="#power"' in html),
    ("Nav: Софт-стек", 'href="#software"' in html),
    ("VRAM section", 'id="vram"' in html),
    ("VRAM table", 'class="vram-table' in html),
    ("Configs section", 'id="configs"' in html),
    ("Tower Pro card", 'class="config-card tower' in html),
    ("Rack Beast card", 'class="config-card rack' in html),
    ("Mac Studio card", 'class="config-card mac' in html),
    ("BOM section", 'id="bom"' in html),
    ("BOM Tower table", 'Tower Pro — $30,249' in html),
    ("BOM Rack table", 'Rack Beast — $51,700' in html),
    ("BOM Mac table", 'Mac Studio Ultra — $10,649' in html),
    ("Power section", 'id="power"' in html),
    ("Software section", 'id="software"' in html),
    ("Software cards (12+)", html.count('class="software-card') >= 12),
    ("Time machine: CPU era", 'CPU inference' in html),
    ("Time machine: RTX 3090", 'RTX 3090' in html),
    ("Time machine: ChatGPT", 'ChatGPT-облако' in html),
    ("Time machine: Mac Studio", 'MAC STUDIO M3' in html),
    ("Time machine: RTX 5090", 'RTX 5090 era' in html),
    ("Sources обновлены", 'RTX 5090 official' in html),
    ("END html", "</html>" in html),
]

print("ФИНАЛЬНАЯ ПРОВЕРКА HTML:")
print("─" * 60)
all_ok = True
for name, ok in checks:
    print(f"  [{'✓' if ok else '✗'}] {name}")
    if not ok: all_ok = False

print(f"\nРазмер: {p.stat().st_size:,} байт ({p.stat().st_size/1024:.1f} KB)")
print(f"\n{'✓ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ' if all_ok else '✗ ЕСТЬ ОШИБКИ'}")

# Список файлов
print("\nФайлы в /home/z/my-project/download/:")
for f in sorted(Path("/home/z/my-project/download").iterdir()):
    if f.is_file():
        print(f"  {f.stat().st_size:>10,}  {f.name}")
