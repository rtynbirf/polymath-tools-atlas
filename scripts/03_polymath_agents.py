#!/usr/bin/env python3
"""
МУЛЬТИАГЕНТНАЯ СИСТЕМА «ПОЛИМАТ» — мастер-оркестратор.
Архитектура по контракту ГОЛОГРАММА v1:

    ПОЛИМАТ (мастер)
      ├─ МАШИНА     → web_search, не трактует
      ├─ ИИ         → LLM-группировка по 6 слоям, не присваивает [ТЕКСТ]
      ├─ СУД        → верификация и подпись: дата + URL + запрос
      └─ СЛОВАРЬ    → граф цепочек, не удаляет шум

Data-схема статьи (JSON):
{
  "id": "cursor",
  "forma": {
    "name": "Cursor",
    "aliases": ["cursor.com", "cursor-ide"],
    "url": "https://cursor.com",
    "license": "Proprietary",
    "category": "4. Программирование",
    "subcategory": "4.1 IDE",
    "version": "0.42",
    "release_date": "2024-XX-XX"
  },
  "text": [
    {"quote": "...", "source": "https://...", "date": "2025-XX-XX", "agent": "MACHINE"}
  ],
  "field": {
    "collocations": ["AI IDE", "VS Code fork", "Claude"],
    "competitors": ["Windsurf", "Continue.dev", "Zed"],
    "replaces": ["VS Code", "JetBrains"]
  },
  "whole": {
    "chain_in": ["anthropic-api", "vscode-fork"],
    "chain_out": ["claude-3.5-sonnet", "gpt-4o"]
  },
  "noise": [
    {"claim": "Лучший AI-редактор всех времён", "source": "marketing", "agent": "COURT", "verdict": "noise"}
  ],
  "court": {
    "status": "TEXT",  // TEXT | NOISE | HYP
    "verified_at": "2026-09-05",
    "verified_by": "POLYMATH",
    "search_query": "Cursor AI IDE Anthropic",
    "sources_count": 3,
    "signature": "polymath-2026-09-05-cursor-TEXT"
  }
}
"""
import asyncio
import json
import os
import re
import subprocess
import sys
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# Константы
# ─────────────────────────────────────────────
ROOT = Path("/home/z/my-project")
SCRIPTS = ROOT / "scripts"
DOWNLOAD = ROOT / "download"
DOWNLOAD.mkdir(parents=True, exist_ok=True)

CATALOG_PATH = SCRIPTS / "catalog_full.json"
ARTICLES_PATH = SCRIPTS / "articles.json"
COURT_LOG_PATH = DOWNLOAD / "court-log.json"

TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")
VERIFY_SEMAPHORE = asyncio.Semaphore(3)  # параллелизм web-search

# ─────────────────────────────────────────────
# Утилиты
# ─────────────────────────────────────────────
def slug(name: str) -> str:
    """Превращает имя в slug для id статьи."""
    s = name.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s).strip('-')
    return s[:64]

def signature(tool_id: str, status: str) -> str:
    """Судовая подпись: polymath-DATE-ID-STATUS."""
    return f"polymath-{TODAY}-{tool_id}-{status}"

def log(msg: str, *, agent: str = "POLYMATH", level: str = "INFO"):
    """Лог в stderr."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{agent}] {level}: {msg}", file=sys.stderr, flush=True)

# ─────────────────────────────────────────────
# z-ai CLI обёртки
# ─────────────────────────────────────────────
def web_search(query: str, num: int = 5) -> List[Dict[str, str]]:
    """МАШИНА: синхронный web-search через z-ai CLI."""
    cmd = ["z-ai", "function", "-n", "web_search",
           "-a", json.dumps({"query": query, "num": num}),
           "-o", "/tmp/_search_result.json"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            log(f"web_search failed: {r.stderr[:200]}", agent="MACHINE", level="WARN")
            return []
        data = json.loads(Path("/tmp/_search_result.json").read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data[:num]
        return []
    except Exception as e:
        log(f"web_search exception: {e}", agent="MACHINE", level="WARN")
        return []

def llm_chat(prompt: str, system: str = "") -> str:
    """ИИ: chat completion через z-ai CLI."""
    cmd = ["z-ai", "chat", "-p", prompt]
    if system:
        cmd.extend(["-s", system])
    cmd.extend(["-o", "/tmp/_chat_result.json"])
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            log(f"llm_chat failed: {r.stderr[:200]}", agent="AI", level="WARN")
            return ""
        data = json.loads(Path("/tmp/_chat_result.json").read_text(encoding="utf-8"))
        # Формат: {"content": "...", ...}
        if isinstance(data, dict):
            return data.get("content", "") or data.get("text", "") or ""
        return str(data)
    except Exception as e:
        log(f"llm_chat exception: {e}", agent="AI", level="WARN")
        return ""

# ─────────────────────────────────────────────
# АГЕНТ: МАШИНА (сбор цитат из веба)
# ─────────────────────────────────────────────
class MachineAgent:
    """Собирает цитаты из веба. Не трактует."""
    
    async def search_tool(self, name: str, category: str) -> List[Dict]:
        async with VERIFY_SEMAPHORE:
            queries = self._build_queries(name, category)
            all_results = []
            for q in queries[:2]:  # максимум 2 запроса на инструмент
                results = await asyncio.to_thread(web_search, q, 4)
                for r in results:
                    r["query"] = q
                    all_results.append(r)
                await asyncio.sleep(0.3)  # мягкий таймаут
            
            # Дедупликация по URL
            seen = set()
            unique = []
            for r in all_results:
                u = r.get("url", "")
                if u and u not in seen:
                    seen.add(u)
                    unique.append(r)
            return unique[:6]  # максимум 6 цитат
    
    def _build_queries(self, name: str, category: str) -> List[str]:
        """Строит поисковые запросы для инструмента."""
        clean = re.sub(r'\s*\(.*?\)', '', name).strip()
        queries = [
            f"{clean} AI tool official",
            f"{clean} documentation 2025",
        ]
        # Спец-запросы для конкретных категорий
        if "LLM" in category or "модели" in category:
            queries.insert(0, f"{clean} model release 2025")
        elif "IDE" in category or "code" in category.lower():
            queries.insert(0, f"{clean} AI coding agent")
        elif "Изображения" in category or "Видео" in category:
            queries.insert(0, f"{clean} AI generation 2025")
        return queries

# ─────────────────────────────────────────────
# АГЕНТ: ИИ (группировка по 6 слоям)
# ─────────────────────────────────────────────
class AIAgent:
    """Группирует находки по 6 слоям. Не присваивает [ТЕКСТ]."""
    
    def build_article_skeleton(self, tool: Dict, search_results: List[Dict]) -> Dict:
        """Строит скелет статьи из находок МАШИНЫ."""
        name = tool["name"]
        tool_id = slug(name)
        
        # ФОРМА — из каталога
        forma = {
            "name": name,
            "aliases": self._extract_aliases(name, tool.get("description", "")),
            "url": self._extract_url(search_results, name),
            "license": "UNKNOWN",
            "category": tool.get("category", ""),
            "subcategory": tool.get("subcategory", ""),
            "version": "UNKNOWN",
            "release_date": "UNKNOWN",
        }
        
        # ТЕКСТ — живые цитаты с датами (готовит ИИ, утверждает СУД)
        text_layer = []
        for r in search_results:
            quote = (r.get("snippet") or "").strip()
            if not quote:
                continue
            text_layer.append({
                "quote": quote[:400],
                "source": r.get("url", ""),
                "source_name": r.get("name", "")[:200],
                "date": r.get("date", ""),
                "agent": "MACHINE",
                "query": r.get("query", "")
            })
        
        # ПОЛЕ — коллокации, конкуренты, замены (ИИ группирует)
        field = self._infer_field(tool, search_results)
        
        # ЦЕЛОЕ — карта словаря (строится позже СЛОВАРЁМ)
        whole = {"chain_in": [], "chain_out": []}
        
        # ШУМ — авторские пересказы без пруфа
        noise = []
        desc = tool.get("description", "")
        if desc and len(desc) > 30:
            noise.append({
                "claim": desc[:300],
                "source": tool.get("source", "user_catalog"),
                "agent": "AI",
                "verdict": "noise"
            })
        
        # СУД — пока пусто, заполнит СУД
        court = {
            "status": "HYP",  # по умолчанию гипотеза
            "verified_at": TODAY,
            "verified_by": "POLYMATH",
            "search_query": "; ".join(set(r.get("query", "") for r in search_results if r.get("query"))),
            "sources_count": len(text_layer),
            "signature": signature(tool_id, "HYP")
        }
        
        return {
            "id": tool_id,
            "forma": forma,
            "text": text_layer,
            "field": field,
            "whole": whole,
            "noise": noise,
            "court": court
        }
    
    def _extract_aliases(self, name: str, desc: str) -> List[str]:
        aliases = []
        # Из скобок в имени
        for m in re.finditer(r'\(([^)]+)\)', name):
            for part in m.group(1).split(','):
                p = part.strip()
                if p and p not in aliases and len(p) < 40:
                    aliases.append(p)
        # Из описания (markdown-bolds)
        for m in re.finditer(r'\*\*([^*]+)\*\*', desc):
            p = m.group(1).strip()
            if p and p not in aliases and len(p) < 30:
                aliases.append(p)
        return aliases[:5]
    
    def _extract_url(self, search_results: List[Dict], name: str) -> str:
        clean = re.sub(r'\s*\(.*?\)', '', name).strip().lower()
        # Prefer official domains
        for r in search_results:
            url = r.get("url", "")
            host = r.get("host_name", "").lower()
            if clean.replace(' ', '') in host.replace('.', '').replace('-', ''):
                return url
        # Fallback: first result
        if search_results:
            return search_results[0].get("url", "")
        return ""
    
    def _infer_field(self, tool: Dict, search_results: List[Dict]) -> Dict:
        """ИИ группирует коллокации из текстов."""
        collocations = []
        competitors = []
        replaces = []
        
        all_text = " ".join([r.get("snippet", "") for r in search_results]).lower()
        
        # Паттерны конкуренции
        for pattern in [r'(?:vs\.?|versus|alternative to|instead of|replaces?)\s+([a-z0-9 .,/-]{3,40})']:
            for m in re.finditer(pattern, all_text):
                for part in m.group(1).split(','):
                    p = part.strip().rstrip('.')
                    if 2 < len(p) < 30 and p not in competitors:
                        competitors.append(p)
        
        return {
            "collocations": collocations[:10],
            "competitors": competitors[:8],
            "replaces": replaces[:5]
        }

# ─────────────────────────────────────────────
# АГЕНТ: СУД (верификация и подпись)
# ─────────────────────────────────────────────
class CourtAgent:
    """Утверждает статус, подписывает. Не создаёт цитаты."""
    
    def verify_and_sign(self, article: Dict) -> Dict:
        """Присваивает финальный статус на основе слоя ТЕКСТ."""
        text_count = len(article.get("text", []))
        has_official_url = bool(article["forma"].get("url"))
        
        # Правило: ≥2 цитат с URL и датой → [ТЕКСТ]
        # 1 цитата или только URL → [ГИП]
        # 0 цитат → [ШУМ] (только описание из каталога)
        if text_count >= 2 and has_official_url:
            status = "TEXT"
        elif text_count >= 1:
            status = "HYP"
        else:
            status = "NOISE"
        
        tool_id = article["id"]
        article["court"] = {
            "status": status,
            "verified_at": TODAY,
            "verified_by": "POLYMATH",
            "search_query": article["court"].get("search_query", ""),
            "sources_count": text_count,
            "signature": signature(tool_id, status)
        }
        return article

# ─────────────────────────────────────────────
# АГЕНТ: СЛОВАРЬ (граф цепочек, не удаляет шум)
# ─────────────────────────────────────────────
class DictionaryAgent:
    """Строит граф цепочек. Не удаляет шум."""
    
    def build_chains(self, articles: List[Dict]) -> List[Dict]:
        """Строит связи между статьями на основе общих упоминаний."""
        # Индекс: slug → id статьи
        name_to_id = {}
        for a in articles:
            name_to_id[a["forma"]["name"].lower()] = a["id"]
            for alias in a["forma"].get("aliases", []):
                name_to_id[alias.lower()] = a["id"]
        
        for a in articles:
            # Ищем упоминания других инструментов в текстах этой статьи
            chain_out = set()
            all_text = " ".join([t.get("quote", "") for t in a.get("text", [])]).lower()
            all_text += " " + " ".join([n.get("claim", "") for n in a.get("noise", [])]).lower()
            
            for name, target_id in name_to_id.items():
                if target_id == a["id"]:
                    continue
                if len(name) < 4:  # короткие имена пропускаем
                    continue
                if name in all_text:
                    chain_out.add(target_id)
            
            a["whole"]["chain_out"] = sorted(chain_out)[:15]
        
        # Обратные связи
        for a in articles:
            chain_in = []
            for other in articles:
                if a["id"] in other["whole"].get("chain_out", []):
                    chain_in.append(other["id"])
            a["whole"]["chain_in"] = chain_in[:15]
        
        return articles

# ─────────────────────────────────────────────
# МАСТЕР: ПОЛИМАТ
# ─────────────────────────────────────────────
class Polymath:
    """Мастер-оркестратор. Подписывает финальный судовой журнал."""
    
    def __init__(self):
        self.machine = MachineAgent()
        self.ai = AIAgent()
        self.court = CourtAgent()
        self.dictionary = DictionaryAgent()
        self.court_log: List[Dict] = []
    
    async def process_tool(self, tool: Dict, do_web_verify: bool) -> Optional[Dict]:
        """Полный конвейер: МАШИНА → ИИ → СУД → (позже) СЛОВАРЬ."""
        name = tool["name"]
        try:
            # МАШИНА: веб-поиск
            if do_web_verify:
                search_results = await self.machine.search_tool(name, tool.get("category", ""))
            else:
                search_results = []
            
            # ИИ: построение скелета статьи
            article = self.ai.build_article_skeleton(tool, search_results)
            
            # СУД: верификация и подпись
            article = self.court.verify_and_sign(article)
            
            # Лог судовой записи
            self.court_log.append({
                "tool_id": article["id"],
                "tool_name": name,
                "status": article["court"]["status"],
                "verified_at": article["court"]["verified_at"],
                "verified_by": article["court"]["verified_by"],
                "signature": article["court"]["signature"],
                "sources_count": article["court"]["sources_count"],
                "search_query": article["court"]["search_query"],
                "wave": "1" if do_web_verify else "2"
            })
            
            return article
        except Exception as e:
            log(f"Failed: {name} — {e}", agent="POLYMATH", level="ERROR")
            return None
    
    async def run(self, catalog: List[Dict], wave1_ids: set) -> Tuple[List[Dict], List[Dict]]:
        """Запуск двух волн: 1 (с веб-верификацией) и 2 (без)."""
        articles = []
        total = len(catalog)
        
        log(f"Каталог: {total} инструментов. Волна 1: {len(wave1_ids)} на верификацию.", agent="POLYMATH")
        
        # Волна 1: с веб-верификацией (батчами по 5 параллельно)
        wave1_tools = [t for t in catalog if slug(t["name"]) in wave1_ids]
        wave2_tools = [t for t in catalog if slug(t["name"]) not in wave1_ids]
        
        log(f"Волна 1: {len(wave1_tools)} инструментов с веб-пруфом", agent="POLYMATH")
        BATCH = 5
        for i in range(0, len(wave1_tools), BATCH):
            batch = wave1_tools[i:i+BATCH]
            tasks = [self.process_tool(t, do_web_verify=True) for t in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for t, r in zip(batch, results):
                if isinstance(r, Exception):
                    log(f"Wave1 error {t['name']}: {r}", agent="POLYMATH", level="ERROR")
                elif r:
                    articles.append(r)
                    log(f"Wave1 ✓ {t['name']:30s} → {r['court']['status']}", agent="POLYMATH")
            await asyncio.sleep(0.5)
        
        log(f"Волна 2: {len(wave2_tools)} инструментов — ФОРМА + [ГИП]", agent="POLYMATH")
        for i, t in enumerate(wave2_tools):
            r = await self.process_tool(t, do_web_verify=False)
            if r:
                articles.append(r)
            if (i+1) % 50 == 0:
                log(f"  ... {i+1}/{len(wave2_tools)}", agent="POLYMATH")
        
        # СЛОВАРЬ: построение цепочек
        log(f"СЛОВАРЬ: построение цепочек для {len(articles)} статей...", agent="POLYMATH")
        articles = self.dictionary.build_chains(articles)
        
        # Статистика по статусам
        stats = {"TEXT": 0, "HYP": 0, "NOISE": 0}
        for a in articles:
            stats[a["court"]["status"]] = stats.get(a["court"]["status"], 0) + 1
        log(f"Итог: {len(articles)} статей — TEXT:{stats['TEXT']} HYP:{stats['HYP']} NOISE:{stats['NOISE']}", agent="POLYMATH")
        
        return articles, self.court_log


# ─────────────────────────────────────────────
# Точка входа
# ─────────────────────────────────────────────
def select_wave1(catalog: List[Dict], n: int = 40) -> set:
    """Выбирает n приоритетных инструментов для Волны 1."""
    # Ключевые слова приоритета
    priority_keywords = [
        # LLM
        "chatgpt", "claude", "gemini", "grok", "deepseek", "llama", "qwen", "mistral", "glm", "kimi", "hunyuan", "ernie", "perplexity",
        # IDE / Code
        "cursor", "claude code", "windsurf", "github copilot", "aider", "cline", "zed", "devin", "openhands", "continue.dev", "tabnine", "codex cli", "goose",
        # CLI (топ)
        "zoxide", "starship", "delta", "btop", "yazi", "ripgrep", "fd-find", "fzf", "bat", "eza", "lazygit", "thefuck",
        # Мультимедиа топ
        "midjourney", "dall", "stable diffusion", "flux", "suno", "elevenlabs", "runway", "sora", "veo", "kling", "synthesia", "heygen",
        # MISC
        "notion ai", "figma ai", "canva ai", "gamma", "adobe firefly"
    ]
    
    selected = set()
    for kw in priority_keywords:
        for t in catalog:
            name = t["name"].lower()
            if kw in name and slug(t["name"]) not in selected:
                selected.add(slug(t["name"]))
                if len(selected) >= n:
                    return selected
                break
    return selected


async def main():
    # Загрузка каталога
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    log(f"Загружен каталог: {len(catalog)} инструментов", agent="POLYMATH")
    
    # Выбор Волны 1
    wave1_ids = select_wave1(catalog, n=40)
    log(f"Волна 1: {len(wave1_ids)} приоритетных инструментов", agent="POLYMATH")
    
    # Запуск мультиагента
    polymath = Polymath()
    articles, court_log = await polymath.run(catalog, wave1_ids)
    
    # Сохранение
    ARTICLES_PATH.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    COURT_LOG_PATH.write_text(json.dumps(court_log, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"Статьи: {ARTICLES_PATH}", agent="POLYMATH")
    log(f"Судовой журнал: {COURT_LOG_PATH}", agent="POLYMATH")
    
    # Краткий отчёт
    stats = {"TEXT": 0, "HYP": 0, "NOISE": 0}
    for a in articles:
        stats[a["court"]["status"]] = stats.get(a["court"]["status"], 0) + 1
    print(f"\n{'='*60}")
    print(f"ОТЧЁТ ПОЛИМАТа")
    print(f"{'='*60}")
    print(f"Всего статей:       {len(articles)}")
    print(f"  [ТЕКСТ] (доказано): {stats['TEXT']}")
    print(f"  [ГИП]   (гипотеза): {stats['HYP']}")
    print(f"  [ШУМ]   (только каталог): {stats['NOISE']}")
    print(f"Судовых записей:    {len(court_log)}")


if __name__ == "__main__":
    asyncio.run(main())
