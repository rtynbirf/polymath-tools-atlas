#!/usr/bin/env python3
"""
ПОЛИМАТ HARDWARE v1 — расчёт железа под локальный мультиагентный LLM-суперстек.
Без ограничений по бюджету. Цель: локальность + быстродействие + полная автономия.

Сценарий: на борту крутятся одновременно
  - LLM 70B Q4 (СУД-агент)              ~48 GB VRAM
  - LLM 8B Q8 ×3 (МАШИНА/ИИ/СЛОВАРЬ)    ~24 GB VRAM
  - SDXL/Flux dev (картинки)             ~16 GB VRAM
  - Wan 2.5 / Sora-локальные (видео)     ~40 GB VRAM
  - Whisper-large-v3 + F5-TTS (голос)    ~6 GB VRAM
  - Infinity embedding (RAG)             ~4 GB VRAM
  - vLLM paged attention + KV cache      ~20 GB VRAM
                                       ─────────────
                                       ИТОГО: ~158 GB VRAM

Это означает: либо 4× RTX 5090 (128GB), либо 8× RTX 5090 (256GB),
либо 2× H100 NVL (188GB), либо Mac Studio M3 Ultra 192GB unified.
"""
import json
from pathlib import Path

# ─────────────────────────────────────────────
# VRAM-бюджет под каждую задачу Polymat
# ─────────────────────────────────────────────
VRAM_BUDGET = [
    {"task": "LLM 70B Q4_K_M (СУД-агент, главный)",         "vram_gb": 48, "model": "Llama 3.3 70B / Qwen3-72B / DeepSeek-V3", "engine": "vLLM / llama.cpp", "tokens_sec": "35-50"},
    {"task": "LLM 8B Q8 ×3 (параллельные агенты)",          "vram_gb": 24, "model": "Llama 3.1 8B ×3 инстанса", "engine": "vLLM ×3", "tokens_sec": "180-250 каждый"},
    {"task": "LLM 235B MoE Q4 (опционально, топ-качество)", "vram_gb": 130, "model": "Qwen3-235B-A22B / DeepSeek-V3.2-671B", "engine": "vLLM + tensor parallel", "tokens_sec": "20-30"},
    {"task": "SDXL / Flux dev (генерация картинок)",        "vram_gb": 16, "model": "FLUX.1-dev / SDXL Turbo / Ideogram", "engine": "ComfyUI / diffusers", "tokens_sec": "1 img / 3 сек"},
    {"task": "Wan 2.5 / Kling-loc (генерация видео 5сек)",  "vram_gb": 40, "model": "Wan 2.5 / CogVideoX 5B / Open-Sora", "engine": "ComfyUI", "tokens_sec": "5 сек видео / 4 мин"},
    {"task": "Whisper-large-v3 (STT)",                      "vram_gb": 4,  "model": "faster-whisper large-v3", "engine": "faster-whisper", "tokens_sec": "Realtime ×12"},
    {"task": "F5-TTS / StyleTTS2 (голос)",                  "vram_gb": 4,  "model": "F5-TTS, StyleTTS2, Piper", "engine": "F5-TTS", "tokens_sec": "Realtime ×4"},
    {"task": "Infinity / TEI (embeddings для RAG)",         "vram_gb": 4,  "model": "bge-m3, gte-large, nomic-embed", "engine": "infinity / TEI", "tokens_sec": "10K docs/sec"},
    {"task": "KV cache + paged attention buffer",           "vram_gb": 20, "model": "—", "engine": "vLLM PagedAttention", "tokens_sec": "—"},
]

# Сценарий A — стандартный Polymat (без видео)
TOTAL_A = sum(t["vram_gb"] for t in VRAM_BUDGET if "видео" not in t["task"])
# Сценарий B — полный Polymat (с видео)
TOTAL_B = sum(t["vram_gb"] for t in VRAM_BUDGET)
# Сценарий C — с 235B MoE
TOTAL_C = TOTAL_B - 48 + 130  # заменяем 70B на 235B

print("VRAM-БЮДЖЕТ ПОЛИМАТа:")
print("─" * 80)
for t in VRAM_BUDGET:
    print(f"  {t['vram_gb']:3d} GB   {t['task']}")
print("─" * 80)
print(f"  Сценарий A (без видео, 70B):            {TOTAL_A} GB VRAM")
print(f"  Сценарий B (полный Polymat, 70B+видео): {TOTAL_B} GB VRAM")
print(f"  Сценарий C (полный + 235B MoE):         {TOTAL_C} GB VRAM")
print()

# ─────────────────────────────────────────────
# Три конфигурации
# ─────────────────────────────────────────────
CONFIGS = {
    "Tower Pro": {
        "name": "Tower Pro — рабочая станция Polymat",
        "tagline": "4× RTX 5090 / 128GB VRAM / Threadripper / 512GB RAM",
        "use_case": "Сценарий A+B: 70B + видео + все агенты. Домашняя/офисная сборка.",
        "chassis": {
            "model": "Fractal Design Define 7 XL (или Phanteks Enthoo Pro 2)",
            "form_factor": "Full Tower E-ATX",
            "price_usd": 200,
            "notes": "Вмещает до 4 двухслотовых GPU, 8× 3.5\" отсеков, шумоизоляция"
        },
        "cpu": {
            "model": "AMD Ryzen Threadripper PRO 7995WX",
            "cores": 96,
            "price_usd": 9999,
            "notes": "8-channel DDR5 ECC, 128 PCIe 5.0 lanes, идеально для 4 GPU + NVMe"
        },
        "motherboard": {
            "model": "ASUS Pro WS WRX90E-SAGE SE",
            "price_usd": 1300,
            "notes": "WRX90E, 7× PCIe 5.0 x16, 8-channel DDR5, 10GbE"
        },
        "ram": {
            "model": "8× 64GB Kingston FURY Renegade DDR5-5600 ECC RDIMM",
            "total_gb": 512,
            "price_usd": 3500,
            "notes": "8-channel ECC, обязательно для 235B MoE offload"
        },
        "gpus": {
            "model": "4× NVIDIA GeForce RTX 5090 32GB",
            "total_vram_gb": 128,
            "price_usd": 4 * 2200,
            "notes": "32GB GDDR7 каждая, 4× PCIe 5.0 x16, потребление 575W каждая"
        },
        "storage": {
            "model": "2× Samsung 990 Pro 4TB NVMe (RAID0) + 2× Seagate IronWolf Pro 20TB (RAID1)",
            "price_usd": 700 + 1100,
            "notes": "RAID0 NVMe: 14 ГБ/с для моделей; RAID1 HDD: 40TB для HuggingFace cache"
        },
        "psu": {
            "model": "2× Corsair AX1600i 1600W + Add2PSU синхронизатор",
            "total_w": 3200,
            "price_usd": 2 * 700 + 50,
            "notes": "Два независимых блока, цифровой мониторинг"
        },
        "cooling": {
            "model": "Custom water loop EKWB: 4× GPU + CPU, 2× MO-R3 420 радиатора",
            "price_usd": 1500,
            "notes": "Тихо при 2kW нагрузки, иначе шум как у турбины"
        },
        "network": {
            "model": "ASUS XG-C100C 10GbE PCIe + Mellanox ConnectX-5 25GbE (опция)",
            "price_usd": 200,
            "notes": "Для связи с кластером mini-PC (опционально)"
        },
        "ups": {
            "model": "APC Smart-UPS SRT 3000VA + внешний батарейный модуль",
            "price_usd": 1500,
            "notes": "30 мин автономии под полной нагрузкой 2.4kW"
        },
        "total_price_usd": 0,  # посчитаем ниже
        "total_vram_gb": 128,
        "max_model_size_gb": 110,  # оставляем запас
        "estimated_power_w": 2400,  # при полной нагрузке
        "estimated_noise_db": 38,  # при водянке
        "estimated_heat_kw": 2.4  # выделяет в помещение
    },
    
    "Rack Beast": {
        "name": "Rack Beast — серверный монстр для 235B MoE",
        "tagline": "8× RTX 5090 / 256GB VRAM / EPYC / 1TB RAM / 19\" rack",
        "use_case": "Сценарий C: 235B MoE параллельно с 70B + видео. Полный полимат без компромиссов.",
        "chassis": {
            "model": "Supermicro CSE-745BTQ-R1K28B 4U rackmount",
            "form_factor": "4U Rackmount (нужен 19\" шкаф или гараж)",
            "price_usd": 1800,
            "notes": "8× PCIe 3.0 x16, redundancy 2× 1000W, шум 65 дБ"
        },
        "cpu": {
            "model": "AMD EPYC 9755 (Turin, 128 ядер)",
            "cores": 128,
            "price_usd": 12000,
            "notes": "12-channel DDR5-6400, 160 PCIe 5.0 lanes — хватит на 8 GPU + NVMe массив"
        },
        "motherboard": {
            "model": "Supermicro H13DSG-OAN-CPU (включена в chassis)",
            "price_usd": 0,
            "notes": "Dual SP5, 12-channel DDR5, IPMI"
        },
        "ram": {
            "model": "12× 96GB Samsung DDR5-5600 RDIMM ECC",
            "total_gb": 1152,
            "price_usd": 9000,
            "notes": "12-channel ECC, 1.1TB — для offload 235B в CPU при необходимости"
        },
        "gpus": {
            "model": "8× NVIDIA GeForce RTX 5090 32GB (или 4× H100 NVL 94GB)",
            "total_vram_gb": 256,
            "price_usd": 8 * 2200,
            "notes": "256GB VRAM для 235B Q4 + 70B Q4 параллельно + видео + KV cache"
        },
        "storage": {
            "model": "4× Samsung 990 Pro 4TB NVMe RAID10 (через Broadcom 9500-16i) + 4× Seagate Exos X22 22TB RAID6",
            "price_usd": 4 * 350 + 4 * 450 + 800,
            "notes": "RAID10 NVMe: 8TB net + 28 ГБ/с; RAID6 HDD: 44TB net для моделей"
        },
        "psu": {
            "model": "2× Supermicro PWS-2K04A-1R 2000W redundant",
            "total_w": 4000,
            "price_usd": 800,
            "notes": "Redundant, hot-swap, IPMI мониторинг"
        },
        "cooling": {
            "model": "Штатные blower-кулеры GPU + 6× Noctua A14 industrial",
            "price_usd": 300,
            "notes": "Шум 65 дБ, нужен шкаф в отдельной комнате"
        },
        "network": {
            "model": "Mellanox ConnectX-7 100GbE + 2× 25GbE bonding",
            "price_usd": 1200,
            "notes": "Для распределённого inference между нодами"
        },
        "ups": {
            "model": "APC Symmetra LX 8kVA + внешний батарейный модуль",
            "price_usd": 5000,
            "notes": "Полная защита 4kW нагрузки, 20 мин автономии"
        },
        "total_price_usd": 0,
        "total_vram_gb": 256,
        "max_model_size_gb": 220,
        "estimated_power_w": 3800,
        "estimated_noise_db": 65,
        "estimated_heat_kw": 3.8
    },
    
    "Mac Studio Ultra": {
        "name": "Mac Studio M3 Ultra — тихая альтернатива",
        "tagline": "M3 Ultra 32C / 192GB unified / 60TB Thunderbolt 5",
        "use_case": "Сценарий A: 70B + картинки + голос. Тихо, холодно, для тех кто не терпит шум rack-сервера.",
        "chassis": {
            "model": "Apple Mac Studio (M3 Ultra, 2025)",
            "form_factor": "Compact 197×197×95 mm, 1.8 кг",
            "price_usd": 0,  # включено в систему
            "notes": "Полностью пассивное охлаждение, бесшумный"
        },
        "cpu": {
            "model": "Apple M3 Ultra (32-core CPU: 24P + 8E)",
            "cores": 32,
            "price_usd": 0,  # SoC
            "notes": "Unified memory: GPU и CPU делят одну DDR5"
        },
        "motherboard": {
            "model": "Apple logic board M3 Ultra",
            "price_usd": 0,
            "notes": "Thunderbolt 5 (120 Гбит/с) — для внешних NVMe"
        },
        "ram": {
            "model": "192GB unified memory (LPDDR5-8400)",
            "total_gb": 192,
            "price_usd": 0,  # включено
            "notes": "800 ГБ/с пропускная способность, можно грузить 70B Q4 целиком + ещё 100GB под остальные задачи"
        },
        "gpus": {
            "model": "M3 Ultra 80-core GPU (встроенный)",
            "total_vram_gb": 192,  # shared
            "price_usd": 0,
            "notes": "Нет CUDA: только Metal/MLX. llama.cpp поддерживает. vLLM — нет."
        },
        "storage": {
            "model": "Встроенный 8TB SSD + внешний OWC ThunderBay 8 (4× 20TB HDD RAID5) через TB5",
            "price_usd": 1200 + 2200,
            "notes": "Встроенный SSD: 5 ГБ/с; внешний массив: 80TB net для моделей"
        },
        "psu": {
            "model": "Apple 270W встроенный",
            "total_w": 270,
            "price_usd": 0,
            "notes": "Всего 270W потребление всей системы"
        },
        "cooling": {
            "model": "Apple пассивное охлаждение с двумя радиаторами",
            "price_usd": 0,
            "notes": "Бесшумный даже при 100% нагрузке"
        },
        "network": {
            "model": "10GbE встроенный",
            "price_usd": 0,
            "notes": "Также 2× TB5 для внешних GPU-боксов (не рекомендуется)"
        },
        "ups": {
            "model": "APC Back-UPS Pro 1500VA",
            "price_usd": 250,
            "notes": "270W нагрузки — 30+ мин автономии"
        },
        "total_price_usd": 0,  # посчитаем — базовый Mac + апгрейды
        "total_vram_gb": 192,
        "max_model_size_gb": 160,  # оставляем 32GB под систему/другое
        "estimated_power_w": 270,
        "estimated_noise_db": 18,
        "estimated_heat_kw": 0.27
    }
}

# Посчитаем цены и рассчитаем Mac
for cfg_name, cfg in CONFIGS.items():
    total = 0
    for part_key in ["chassis", "cpu", "motherboard", "ram", "gpus", "storage", "psu", "cooling", "network", "ups"]:
        part = cfg[part_key]
        if isinstance(part, dict) and "price_usd" in part:
            total += part["price_usd"]
    if cfg_name == "Mac Studio Ultra":
        # Базовая цена Mac Studio M3 Ultra 192GB = ~$6999
        total += 6999
    cfg["total_price_usd"] = total

# Сохранить
out = {
    "vram_budget": VRAM_BUDGET,
    "totals": {"A": TOTAL_A, "B": TOTAL_B, "C": TOTAL_C},
    "configs": CONFIGS
}
Path("/home/z/my-project/scripts/hardware_calc.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

print("\nТРИ КОНФИГУРАЦИИ:")
print("─" * 80)
for cfg_name, cfg in CONFIGS.items():
    print(f"\n  {cfg_name}: {cfg['tagline']}")
    print(f"    Цена: ${cfg['total_price_usd']:,}")
    print(f"    VRAM: {cfg['total_vram_gb']} GB")
    print(f"    Max model: {cfg['max_model_size_gb']} GB")
    print(f"    Потребление: {cfg['estimated_power_w']} W")
    print(f"    Шум: {cfg['estimated_noise_db']} дБ")
    print(f"    Тепло: {cfg['estimated_heat_kw']} kW")

print("\n→ /home/z/my-project/scripts/hardware_calc.json")
