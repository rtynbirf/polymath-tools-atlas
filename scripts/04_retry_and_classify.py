#!/usr/bin/env python3
"""
Доработка:
1. Реклассификация: статьи, которые были в Волне 1, но web_search упал → [ГИП]
   (не [ШУМ] — это спецификация эталона: гипотеза ждёт пруфа, шум — это пересказ без цитат)
2. Retry для топ-30 не-верифицированных с задержкой 4 сек между запросами
3. Запуск второй попытки для оставшихся приоритетных
"""
import asyncio
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path("/home/z/my-project")
SCRIPTS = ROOT / "scripts"
DOWNLOAD = ROOT / "download"
ARTICLES_PATH = SCRIPTS / "articles.json"
COURT_LOG_PATH = DOWNLOAD / "court-log.json"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

def log(msg, agent="POLYMATH"):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{agent}] {msg}", file=sys.stderr, flush=True)

def web_search(query, num=4):
    cmd = ["z-ai", "function", "-n", "web_search",
           "-a", json.dumps({"query": query, "num": num}),
           "-o", "/tmp/_sr.json"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        if r.returncode != 0:
            return []
        data = json.loads(Path("/tmp/_sr.json").read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception as e:
        return []

def slug(name):
    import re
    s = name.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s).strip('-')
    return s[:64]

def signature(tool_id, status):
    return f"polymath-{TODAY}-{tool_id}-{status}"

# Приоритетный список (30 топ-инструментов, которые должны быть [ТЕКСТ])
PRIORITY_30 = [
    "ChatGPT", "Claude", "Gemini", "Grok", "DeepSeek", "Llama 4 Maverick",
    "Cursor", "Claude Code", "Windsurf", "GitHub Copilot", "Cline",
    "Zed", "Aider", "Continue.dev", "OpenHands", "Codex CLI",
    "Midjourney", "DALL·E 3", "Stable Diffusion XL/3/3.5", "FLUX.2",
    "Suno AI", "ElevenLabs", "Runway Gen-4.5/Aleph", "Sora 2",
    "Veo 3", "Kling 2.0", "Synthesia", "HeyGen",
    "Perplexity, You.com", "Notion AI"
]

async def retry_priority(articles):
    """Retry для топ-30 с большой задержкой."""
    by_id = {a["id"]: a for a in articles}
    
    for i, name in enumerate(PRIORITY_30):
        aid = slug(name)
        if aid not in by_id:
            log(f"  [{i+1}/30] {name} не найден в статьях")
            continue
        
        a = by_id[aid]
        # Пропускаем уже TEXT
        if a["court"]["status"] == "TEXT" and len(a.get("text", [])) >= 2:
            log(f"  [{i+1}/30] {name:30s} уже TEXT, skip")
            continue
        
        log(f"  [{i+1}/30] retry {name}...")
        # 2 запроса с задержкой
        all_results = []
        for q in [f"{name} AI tool official 2025", f"{name} documentation release"]:
            results = await asyncio.to_thread(web_search, q, 4)
            for r in results:
                r["query"] = q
                all_results.append(r)
            await asyncio.sleep(4)  # большая задержка
        
        # Дедупликация
        seen = set()
        unique = []
        for r in all_results:
            u = r.get("url", "")
            if u and u not in seen:
                seen.add(u)
                unique.append(r)
        
        if not unique:
            log(f"    → нет результатов, остаётся HYP")
            a["court"]["status"] = "HYP"
            a["court"]["signature"] = signature(aid, "HYP")
            continue
        
        # Обновляем text layer
        text_layer = []
        for r in unique[:6]:
            quote = (r.get("snippet") or "").strip()
            if quote:
                text_layer.append({
                    "quote": quote[:400],
                    "source": r.get("url", ""),
                    "source_name": r.get("name", "")[:200],
                    "date": r.get("date", ""),
                    "agent": "MACHINE",
                    "query": r.get("query", "")
                })
        a["text"] = text_layer
        
        # Обновляем URL в ФОРМА
        if not a["forma"].get("url") and unique:
            a["forma"]["url"] = unique[0].get("url", "")
        
        # Пересуд
        if len(text_layer) >= 2:
            status = "TEXT"
        elif len(text_layer) == 1:
            status = "HYP"
        else:
            status = "NOISE"
        
        a["court"] = {
            "status": status,
            "verified_at": TODAY,
            "verified_by": "POLYMATH",
            "search_query": "; ".join(set(r.get("query", "") for r in unique if r.get("query"))),
            "sources_count": len(text_layer),
            "signature": signature(aid, status)
        }
        log(f"    → {status} ({len(text_layer)} цитат)")
        await asyncio.sleep(2)
    
    return articles

def reclassify_wave1_failures(articles, court_log):
    """Все NOISE с пустым text → HYP (гипотеза, ждёт пруфа).
    Только те, у кого вообще нет поискового запроса — остаются NOISE (только каталог)."""
    for a in articles:
        if a["court"]["status"] == "NOISE":
            query = a["court"].get("search_query", "")
            if query:  # был поиск, но упал → HYP
                a["court"]["status"] = "HYP"
                a["court"]["signature"] = signature(a["id"], "HYP")
                # Обновить court_log
                for entry in court_log:
                    if entry["tool_id"] == a["id"]:
                        entry["status"] = "HYP"
                        entry["signature"] = a["court"]["signature"]
            # иначе остаётся NOISE (Wave 2 без поиска)
    
    # Wave 2 должна быть HYP (не NOISE), т.к. это гипотезы, ждущие пруфа
    for a in articles:
        if not a["court"].get("search_query"):  # Wave 2
            if a["court"]["status"] == "NOISE":
                a["court"]["status"] = "HYP"
                a["court"]["signature"] = signature(a["id"], "HYP")
                for entry in court_log:
                    if entry["tool_id"] == a["id"]:
                        entry["status"] = "HYP"
                        entry["signature"] = a["court"]["signature"]
                        entry["wave"] = "2"
    
    return articles, court_log

async def main():
    articles = json.loads(ARTICLES_PATH.read_text(encoding="utf-8"))
    court_log = json.loads(COURT_LOG_PATH.read_text(encoding="utf-8"))
    log(f"Загружено: {len(articles)} статей, {len(court_log)} записей журнала")
    
    # Стадия 1: реклассификация
    log("Стадия 1: реклассификация NOISE → HYP для Wave 1 и Wave 2")
    articles, court_log = reclassify_wave1_failures(articles, court_log)
    stats = {"TEXT": 0, "HYP": 0, "NOISE": 0}
    for a in articles:
        stats[a["court"]["status"]] = stats.get(a["court"]["status"], 0) + 1
    log(f"  После реклассификации: TEXT:{stats['TEXT']} HYP:{stats['HYP']} NOISE:{stats['NOISE']}")
    
    # Стадия 2: retry для топ-30
    log("Стадия 2: retry топ-30 с задержкой 4 сек")
    articles = await retry_priority(articles)
    
    # Перестроить court_log по статьям
    log("Пересборка журнала...")
    court_log = []
    for a in articles:
        court_log.append({
            "tool_id": a["id"],
            "tool_name": a["forma"]["name"],
            "status": a["court"]["status"],
            "verified_at": a["court"]["verified_at"],
            "verified_by": a["court"]["verified_by"],
            "signature": a["court"]["signature"],
            "sources_count": a["court"]["sources_count"],
            "search_query": a["court"].get("search_query", ""),
            "wave": "1" if a["court"].get("search_query") else "2"
        })
    
    # Сохранить
    ARTICLES_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    COURT_LOG_PATH.write_text(json.dumps(court_log, ensure_ascii=False, indent=2), encoding="utf-8")
    
    # Финальный отчёт
    stats = {"TEXT": 0, "HYP": 0, "NOISE": 0}
    for a in articles:
        stats[a["court"]["status"]] = stats.get(a["court"]["status"], 0) + 1
    
    print(f"\n{'='*60}")
    print(f"ОТЧЁТ ПОСЛЕ RETRY")
    print(f"{'='*60}")
    print(f"Всего статей:       {len(articles)}")
    print(f"  [ТЕКСТ] (доказано): {stats['TEXT']}")
    print(f"  [ГИП]   (гипотеза): {stats['HYP']}")
    print(f"  [ШУМ]   (только каталог): {stats['NOISE']}")
    print(f"Судовых записей:    {len(court_log)}")
    print(f"\n→ {ARTICLES_PATH}")
    print(f"→ {COURT_LOG_PATH}")

if __name__ == "__main__":
    asyncio.run(main())
