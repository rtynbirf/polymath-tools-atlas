#!/usr/bin/env python3
"""
Дополнение #2 от ПОЛИМАТа — критическое:
1. Добавляем растовые/зиговые/го-шные супербыстрые инструменты
2. Расширяем схему статьи: stack, autonomy, lifecycle, supersedes
3. Пометим legacy-инструменты (устаревшие)
4. Разметим cloud vs local
"""
import json
import re
from pathlib import Path
from datetime import datetime, timezone

ARTICLES = Path("/home/z/my-project/scripts/articles.json")
OUT = Path("/home/z/my-project/scripts/articles_v2.json")
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

articles = json.loads(ARTICLES.read_text(encoding="utf-8"))
print(f"Загружено: {len(articles)} статей")

# ─────────────────────────────────────────────
# 1. Расширение схемы: добавляем поля во все существующие статьи
# ─────────────────────────────────────────────
def infer_stack(name: str, desc: str, url: str = "") -> str:
    """Определяет стек по имени/описанию."""
    text = (name + " " + desc + " " + url).lower()
    rust_hints = ["rust", "звук", " Cargo", "crates.io", "rewritten in rust", "на rust"]
    if any(h in text for h in ["zoxide", "starship", "delta", "yazi", "ripgrep", "rg ", "fd-find", "fd ", "bat ", "eza", "lsd", "broot", "zellij", "wezterm", "atuin", "sd ", "dust", "procs", "xh", "dog", "difftastic", "tokei", "hyperfine", "just ", "bottom", "glances", "skim", "television", "gum", "navi", "btop"]):
        return "Rust"
    if any(h in text for h in ["uv ", "ruff", "polars", "biome", "oxc", "rspack", "rolldown", "turbopack", "deno", "bun", "mise", "rye", "uvicorn", "pydantic"]):
        return "Rust"
    if "go " in text or "golang" in text or any(h in text for h in ["lazygit", "fzf", "lazydocker", "dive", "ctop", "oh-my-posh", "go-"]):
        return "Go"
    if "zig" in text:
        return "Zig"
    if "c++" in text or "cpp" in text:
        return "C++"
    if "python" in text or "django" in text or "flask" in text or "pyramid" in text:
        return "Python"
    if "typescript" in text or "javascript" in text or "node" in text or "deno" in text or "bun " in text:
        return "TypeScript"
    return "Mixed"

def infer_autonomy(name: str, desc: str, url: str = "") -> str:
    """Определяет автономность: local/cloud/hybrid."""
    text = (name + " " + desc).lower()
    # Cloud — нужны API, сервер
    cloud_hints = ["openai", "anthropic", "claude", "gpt-", "chatgpt", "gemini", "grok", "deepseek api", "mistral api", "perplexity", "elevenlabs api", "midjourney", "dall-e", "adobe firefly", "suno", "udio", "runway", "synthesia", "heygen", "grammarly", "krisp", "otter.ai", "fireflies", "salesforce", "hubspot"]
    if any(h in text for h in cloud_hints):
        return "cloud"
    # Local — работает офлайн
    local_hints = ["ollama", "lm studio", "llamafile", "llama.cpp", "gpt4all", "localai", "vllm", "mlc", "whisper.cpp", "stable diffusion", "sdxl", "flux ", "kandinsky", "шедеврум", "tabby", "open-webui", "open webui", "aider", "continue.dev", "cline", "openhands", "void", "pearai", "ollama", "koboldcpp", "fastchat", "text-generation-webui"]
    if any(h in text for h in local_hints):
        return "local"
    # CLI-утилиты — локальные
    cli_hints = ["zoxide", "starship", "delta", "btop", "yazi", "ripgrep", "fd", "bat", "eza", "lazygit", "thefuck", "tldr", "atuin", "sd ", "dust", "procs", "xh", "hyperfine", "just", "bottom", "fzf", "navi", "gum"]
    if any(h in text for h in cli_hints):
        return "local"
    # По умолчанию hybrid
    return "hybrid"

def infer_lifecycle(name: str, desc: str) -> str:
    """Жизненный статус: active/maintenance/legacy/archived."""
    text = (name + " " + desc).lower()
    # Legacy — заменены современными
    legacy_map = {
        "flake8": "ruff",
        "pylint": "ruff",
        "black": "ruff format",
        "isort": "ruff",
        "webpack": "turbopack/vite/rspack",
        "eslint": "biome (для новых проектов)",
        "prettier": "biome",
        "httpie": "xh (Rust)",
        "curl ": "xh для JSON API",
        "top ": "btop/htop",
        "htop": "btop",
        "ls ": "eza/lsd (Rust)",
        "cat ": "bat (Rust)",
        "find ": "fd (Rust)",
        "grep ": "ripgrep (Rust)",
        "sed ": "sd (Rust)",
        "du ": "dust (Rust)",
        "df ": "duf (Rust)",
        "cd ": "zoxide (Rust)",
        "make": "just (Rust)",
        "ps ": "procs (Rust)",
        "hexdump": "hexyl (Rust)",
        "ncdu": "gdu/dust (Rust)",
    }
    for legacy, modern in legacy_map.items():
        if legacy.strip() == name.lower().strip():
            return "legacy"
    return "active"

def infer_supersedes(name: str, desc: str) -> list:
    """Что заменяет этот инструмент."""
    text = (name + " " + desc).lower()
    supersedes_map = {
        "ruff": ["flake8", "pylint", "black", "isort", "pyupgrade"],
        "uv": ["pip", "pip-tools", "poetry", "virtualenv", "pyenv"],
        "rye": ["poetry", "pdm", "pip"],
        "mise": ["asdf", "pyenv", "nvm", "rbenv"],
        "biome": ["eslint", "prettier", "dprint"],
        "oxc": ["eslint", "babel", "terser"],
        "rspack": ["webpack"],
        "rolldown": ["rollup", "vite"],
        "turbopack": ["webpack"],
        "deno": ["node"],
        "bun": ["node", "npm", "yarn"],
        "zoxide": ["cd", "fasd", "autojump"],
        "starship": ["powerlevel10k", "oh-my-zsh themes"],
        "delta": ["git diff", "diff-so-fancy"],
        "btop": ["top", "htop"],
        "yazi": ["ranger", "vifm", "nnn"],
        "ripgrep": ["grep", "ag", "ack"],
        "fd-find": ["find"],
        "bat": ["cat", "batcat"],
        "eza": ["ls", "exa"],
        "lsd": ["ls"],
        "lazygit": ["git CLI"],
        "atuin": ["shell history (ctrl-r)"],
        "sd": ["sed"],
        "dust": ["du", "ncdu"],
        "procs": ["ps"],
        "xh": ["curl", "httpie"],
        "dog": ["dig"],
        "difftastic": ["diff"],
        "tokei": ["cloc"],
        "hyperfine": ["time", "bench"],
        "just": ["make", "npm scripts"],
        "bottom": ["btop", "htop"],
        "skim": ["fzf"],
        "television": ["fzf"],
        "gum": ["glow", "gum"],
        "navi": ["cheat", "tldr"],
        "zellij": ["tmux", "screen"],
        "wezterm": ["iterm2", "alacritty"],
        "hexyl": ["hexdump", "xxd"],
        "duf": ["df"],
        "gdu": ["ncdu", "du"],
        "thefuck": ["manual correction"],
        "tldr": ["man"],
        "ripgrep-all": ["ripgrep"],
        "glances": ["top", "htop"],
        "lazydocker": ["docker CLI"],
        "dive": ["docker history"],
        "ctop": ["docker stats"],
    }
    name_lower = name.lower().strip()
    for k, v in supersedes_map.items():
        if k == name_lower or name_lower.startswith(k + " "):
            return v
    return []

# Применяем расширение к существующим статьям
for a in articles:
    name = a["forma"]["name"]
    desc = a.get("noise", [{}])[0].get("claim", "") if a.get("noise") else ""
    url = a["forma"].get("url", "")
    
    a["forma"]["stack"] = infer_stack(name, desc, url)
    a["forma"]["autonomy"] = infer_autonomy(name, desc, url)
    a["forma"]["lifecycle"] = infer_lifecycle(name, desc)
    a["forma"]["supersedes"] = infer_supersedes(name, desc)

print(f"Расширено: {len(articles)} статей получили поля stack/autonomy/lifecycle/supersedes")

# ─────────────────────────────────────────────
# 2. Новые инструменты — РУСТОВЫЕ И СУПЕРБЫСТРЫЕ
# ─────────────────────────────────────────────
NEW_TOOLS = [
    # Python ecosystem на Rust
    {"name": "uv", "category": "CLI и утилиты", "subcategory": "Python", "description": "Astral: package manager на Rust, в 10-100× быстрее pip/pip-tools/poetry. Заменяет pip+virtualenv+pyenv", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["pip", "pip-tools", "poetry", "virtualenv", "pyenv"]},
    {"name": "ruff", "category": "CLI и утилиты", "subcategory": "Python", "description": "Astral: Python linter+formatter на Rust. 10-100× быстрее flake8+pylint+black+isort. Один инструмент вместо пяти", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["flake8", "pylint", "black", "isort", "pyupgrade"]},
    {"name": "ruff format", "category": "CLI и утилиты", "subcategory": "Python", "description": "Formatter в ruff, заменяет black. Скорость 100×+", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["black", "autopep8"]},
    {"name": "polars", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных", "description": "DataFrame на Rust, замена pandas. В 5-50× быстрее, многопоточный, lazy evaluation", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["pandas", "dask"]},
    {"name": "duckdb", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных", "description": "OLAP DB на C++, в процессе SQL прямо на CSV/Parquet. 10× быстрее PostgreSQL для аналитики", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": ["pandas", "sqlite для аналитики"]},
    {"name": "datafusion", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных", "description": "Rust query engine от Apache, основа polars и других", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "rye", "category": "CLI и утилиты", "subcategory": "Python", "description": "Armin Ronacher's Python manager на Rust, сейчас использует uv внутри", "stack": "Rust", "autonomy": "local", "lifecycle": "maintenance", "supersedes": ["poetry", "pdm"]},
    {"name": "pixi", "category": "CLI и утилиты", "subcategory": "Python/Multi", "description": "prefix.dev: пакетный менеджер на Rust для conda+PyPI, репродьюсибл окружения", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["conda", "mamba"]},
    {"name": "mamba", "category": "CLI и утилиты", "subcategory": "Python", "description": "C++/Rust реализация conda, в 10× быстрее", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": ["conda"]},
    
    # JS/TS ecosystem на Rust
    {"name": "biome", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Rust linter+formatter для JS/TS/JSON/CSS. Заменяет eslint+prettier, в 25× быстрее", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["eslint", "prettier", "dprint"]},
    {"name": "oxc (Oxidation Compiler)", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Rust JS toolchain: parser/linter/minifier. Самый быстрый JS linter", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["eslint", "babel", "terser"]},
    {"name": "rspack", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "ByteDance: bundler на Rust, совместим с webpack API. В 10× быстрее webpack", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["webpack"]},
    {"name": "rolldown", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Vite: bundler на Rust, замена rollup. Будет внутри Vite 6", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["rollup", "esbuild"]},
    {"name": "turbopack", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Vercel: bundler на Rust от автора webpack, в Next.js 15", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["webpack"]},
    {"name": "esbuild", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Go bundler, в 100× быстрее webpack. Сделал эру быстрых bundler", "stack": "Go", "autonomy": "local", "lifecycle": "maintenance", "supersedes": ["webpack"]},
    {"name": "swc", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Rust JS/TS compiler, основа Next.js и Turbopack", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["babel"]},
    {"name": "vite 6", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Dev server + bundler на Rolldown (Rust). Стандарт frontend-разработки 2025", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["webpack", "parcel"]},
    {"name": "parcel 2", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Zero-config bundler на Rust/SWC", "stack": "Rust", "autonomy": "local", "lifecycle": "maintenance", "supersedes": ["webpack"]},
    
    # JS runtimes
    {"name": "bun", "category": "CLI и утилиты", "subcategory": "Runtime", "description": "JavaScript runtime на Zig, в 4× быстрее Node.js. Включает bundler+test runner+package manager", "stack": "Zig", "autonomy": "local", "lifecycle": "active", "supersedes": ["node", "npm", "yarn", "jest"]},
    {"name": "deno 2", "category": "CLI и утилиты", "subcategory": "Runtime", "description": "Secure JS/TS runtime на Rust от Ryan Dahl, с npm-совместимостью", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["node"]},
    {"name": "workerd", "category": "CLI и утилиты", "subcategory": "Runtime", "description": "Cloudflare: JS runtime на C++, основа Workers", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Terminals на Rust/Zig
    {"name": "ghostty", "category": "CLI и утилиты", "subcategory": "Terminal", "description": "Mitchell Hashimoto: terminal на Zig, GPU-ускоренный, кросс-платформенный", "stack": "Zig", "autonomy": "local", "lifecycle": "active", "supersedes": ["alacritty", "kitty"]},
    {"name": "alacritty", "category": "CLI и утилиты", "subcategory": "Terminal", "description": "Rust GPU-accelerated terminal, чистый фокус на скорость", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["iterm2", "gnome-terminal"]},
    {"name": "kitty", "category": "CLI и утилиты", "subcategory": "Terminal", "description": "C+Python GPU terminal с graphics support", "stack": "C", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "wezterm", "category": "CLI и утилиты", "subcategory": "Terminal", "description": "Rust GPU terminal, mux, Lua config", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["iterm2", "alacritty"]},
    {"name": "zellij", "category": "CLI и утилиты", "subcategory": "Terminal multiplexer", "description": "Rust terminal multiplexer, замена tmux с более дружелюбным UX", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["tmux", "screen"]},
    
    # Современные CLI на Rust
    {"name": "bat", "category": "CLI и утилиты", "subcategory": "Просмотр", "description": "Rust: cat с подсветкой синтаксиса, git-интеграцией, нумерацией строк", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["cat"]},
    {"name": "eza", "category": "CLI и утилиты", "subcategory": "Просмотр", "description": "Rust: форк exa, ls с иконками, git-статусом, деревом", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["ls", "exa"]},
    {"name": "lsd", "category": "CLI и утилиты", "subcategory": "Просмотр", "description": "Rust: ls Deluxe с иконками и цветами", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["ls"]},
    {"name": "skim", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Rust fuzzy finder, быстрее fzf", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["fzf"]},
    {"name": "television", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Rust fuzzy finder с TUI, новая волна", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["fzf"]},
    {"name": "gum", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Charm: Rust TUI для glamourous shell scripts", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "atuin", "category": "CLI и утилиты", "subcategory": "Shell", "description": "Rust: sync shell history, поиск по дате/директории/exit code", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["shell history (ctrl-r)"]},
    {"name": "mcfly", "category": "CLI и утилиты", "subcategory": "Shell", "description": "Rust: умная история команд с ML-ранжированием", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["shell history"]},
    {"name": "sd", "category": "CLI и утилиты", "subcategory": "Текст", "description": "Rust: замена sed, регулярные выражения без головной боли", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["sed"]},
    {"name": "dust", "category": "CLI и утилиты", "subcategory": "Диск", "description": "Rust: du с визуализацией дерева", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["du", "ncdu"]},
    {"name": "duf", "category": "CLI и утилиты", "subcategory": "Диск", "description": "Rust: df с цветным выводом", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["df"]},
    {"name": "gdu", "category": "CLI и утилиты", "subcategory": "Диск", "description": "Rust: очень быстрый disk usage analyzer, в 5× быстрее ncdu", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["ncdu", "du"]},
    {"name": "procs", "category": "CLI и утилиты", "subcategory": "Процессы", "description": "Rust: ps с цветом, фильтрацией, деревом", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["ps"]},
    {"name": "xh", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust: HTTPie-замена для HTTP-запросов, быстрее curl", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["httpie", "curl для API"]},
    {"name": "oha", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust: load tester, замена ab/wrk с TUI", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["ab", "wrk"]},
    {"name": "dog", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust: DNS-клиент, замена dig с цветом", "stack": "Rust", "autonomy": "local", "lifecycle": "maintenance", "supersedes": ["dig"]},
    {"name": "trippy", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust: traceroute TUI, в реальном времени", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["traceroute", "mtr"]},
    {"name": "gping", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust: ping с графиком в терминале", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["ping"]},
    {"name": "bandwhich", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust: мониторинг сети по процессам в реальном времени", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["iftop"]},
    {"name": "difftastic", "category": "CLI и утилиты", "subcategory": "Diff", "description": "Rust: структурный diff с учётом синтаксиса", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["diff"]},
    {"name": "tokei", "category": "CLI и утилиты", "subcategory": "Метрики", "description": "Rust: подсчёт строк кода, мгновенно", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["cloc"]},
    {"name": "hyperfine", "category": "CLI и утилиты", "subcategory": "Бенчмарки", "description": "Rust: бенчмаркинг команд с warmup и статистикой", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["time"]},
    {"name": "just", "category": "CLI и утилиты", "subcategory": "Автоматизация", "description": "Rust: замена make с человеческим синтаксисом", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["make"]},
    {"name": "mask", "category": "CLI и утилиты", "subcategory": "Автоматизация", "description": "Rust: task runner на Markdown-файлах", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["make"]},
    {"name": "bottom", "category": "CLI и утилиты", "subcategory": "Мониторинг", "description": "Rust: системный монитор, замена btop/htop с графиками", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["btop", "htop"]},
    {"name": "glances", "category": "CLI и утилиты", "subcategory": "Мониторинг", "description": "Python: кросс-платформенный системный монитор", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": ["top"]},
    {"name": "hexyl", "category": "CLI и утилиты", "subcategory": "Просмотр", "description": "Rust: hex viewer с цветом по типам байтов", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["hexdump", "xxd"]},
    {"name": "ripgrep-all", "category": "CLI и утилиты", "subcategory": "Поиск", "description": "Rust: ripgrep + PDF/epub/office/db/sqlite — поиск во всём", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["ripgrep"]},
    {"name": "ack", "category": "CLI и утилиты", "subcategory": "Поиск", "description": "Perl: поиск по коду для программистов, уважает .gitignore", "stack": "Perl", "autonomy": "local", "lifecycle": "maintenance", "supersedes": ["grep"]},
    {"name": "broot", "category": "CLI и утилиты", "subcategory": "Навигация", "description": "Rust: интерактивный браузер директорий с поиском", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["tree", "ranger"]},
    {"name": "fff", "category": "CLI и утилиты", "subcategory": "Навигация", "description": "Bash: минималистичный файловый менеджер", "stack": "Bash", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "nnn", "category": "CLI и утилиты", "subcategory": "Навигация", "description": "C: лёгкий и быстрый файловый менеджер", "stack": "C", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "ranger", "category": "CLI и утилиты", "subcategory": "Навигация", "description": "Python: файловый менеджер с vim-биндингами", "stack": "Python", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "vifm", "category": "CLI и утилиты", "subcategory": "Навигация", "description": "C: двухпанельный файловый менеджер с vim-ключами", "stack": "C", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Go CLI
    {"name": "lazydocker", "category": "CLI и утилиты", "subcategory": "Docker", "description": "Go: TUI для Docker как lazygit для git", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["docker CLI"]},
    {"name": "lazygit", "category": "CLI и утилиты", "subcategory": "Git", "description": "Go: TUI для git, самый популярный", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["git CLI"]},
    {"name": "dive", "category": "CLI и утилиты", "subcategory": "Docker", "description": "Go: анализ слоёв Docker-образов", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["docker history"]},
    {"name": "ctop", "category": "CLI и утилиты", "subcategory": "Docker", "description": "Go: top для контейнеров", "stack": "Go", "autonomy": "local", "lifecycle": "maintenance", "supersedes": ["docker stats"]},
    {"name": "fzf", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Go: fuzzy finder, классика, интегрируется со всем", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "oh-my-posh", "category": "CLI и утилиты", "subcategory": "Shell", "description": "Go: cross-shell prompt themer, альтернатива starship", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["powerlevel10k"]},
    
    # Zig ecosystem
    {"name": "Zig compiler", "category": "4. Программирование и разработка", "subcategory": "4.1 Языки", "description": "Zig: C-совместимый язык, drop-in замена gcc/clang для сборки", "stack": "Zig", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Git-инструменты
    {"name": "gitui", "category": "CLI и утилиты", "subcategory": "Git", "description": "Rust: TUI для git с async, альтернатива lazygit", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["lazygit"]},
    {"name": "tig", "category": "CLI и утилиты", "subcategory": "Git", "description": "C: TUI для git, классика", "stack": "C", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "gh (GitHub CLI)", "category": "CLI и утилиты", "subcategory": "Git", "description": "Go: официальный CLI GitHub", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "glab (GitLab CLI)", "category": "CLI и утилиты", "subcategory": "Git", "description": "Go: официальный CLI GitLab", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "tea (Gitea CLI)", "category": "CLI и утилиты", "subcategory": "Git", "description": "Go: CLI для Gitea/Forgejo", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "jujutsu (jj)", "category": "CLI и утилиты", "subcategory": "Git", "description": "Rust: DVCS совместимая с git, проще UX", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["git"]},
    {"name": "sapling", "category": "CLI и утилиты", "subcategory": "Git", "description": "Meta: SCM на OCaml, совместимая с git", "stack": "OCaml", "autonomy": "local", "lifecycle": "active", "supersedes": ["git"]},
    
    # Контейнерные и K8s
    {"name": "k9s", "category": "CLI и утилиты", "subcategory": "Kubernetes", "description": "Go: TUI для Kubernetes", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["kubectl"]},
    {"name": "lazygit for k8s", "category": "CLI и утилиты", "subcategory": "Kubernetes", "description": "TUI для K8s, упрощённый", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["kubectl"]},
    {"name": "stern", "category": "CLI и утилиты", "subcategory": "Kubernetes", "description": "Go: logs из нескольких pod'ов одновременно", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["kubectl logs"]},
    {"name": "kubectx", "category": "CLI и утилиты", "subcategory": "Kubernetes", "description": "Go: переключение контекстов и неймспейсов K8s", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Self-hosted / автономные LLM-инструменты (ВАЖНО для ПОЛИМАТа)
    {"name": "llama.cpp", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "C++: основа всех локальных LLM-инференсов. GGUF-формат, CPU/GPU/Apple Silicon", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "Ollama", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Go: Docker для LLM. Самый простой способ запустить локальные модели", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "llamafile", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "C: один .exe-файл с моделью внутри, кросс-платформенный", "stack": "C", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "vLLM", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Python/C++: high-throughput LLM server, PagedAttention", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "TGI (Text Generation Inference)", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Rust/Python: HF сервер для LLM-инференса", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "LM Studio", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Closed-source desktop app: GUI для локальных LLM, OpenAI-совместимый API", "stack": "Closed", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "GPT4All", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "C++/Python: запуск LLM на CPU, обученные модели Nomic AI", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "Open WebUI", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Python/Svelte: самохостящийся UI для Ollama/llama.cpp, как ChatGPT", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": ["ChatGPT UI"]},
    {"name": "LocalAI", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Go: drop-in замена OpenAI API, локально", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["OpenAI API"]},
    {"name": "koboldcpp", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "C++: форк llama.cpp с UI и lorebook'ами", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "text-generation-webui (oobabooga)", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Python: Gradio UI для LLM, классика локального запуска", "stack": "Python", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "MLC-LLM", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Python/C++: LLM на любых GPU, включая мобильные", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "llama-cpp-python", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Python: биндинги llama.cpp, основа большинства Python-локалок", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Whisper локально
    {"name": "whisper.cpp", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио", "description": "C++: порт Whisper на C/C++, в 4× быстрее, без Python", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": ["openai-whisper"]},
    {"name": "faster-whisper", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио", "description": "Python: CTranslate2-версия Whisper, в 4× быстрее оригинала", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": ["openai-whisper"]},
    {"name": "whisperX", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио", "description": "Python: Whisper + diarization + alignment, точные тайм-коды", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Local TTS
    {"name": "Piper TTS", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио", "description": "C++: нейро-TTS для Raspberry Pi и не только, очень быстрый", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "Coqui TTS", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио", "description": "Python: XTTS — клонирование голоса за 6 секунд, 17 языков", "stack": "Python", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "F5-TTS", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио", "description": "Python: zero-shot TTS, open-source, качество на уровне ElevenLabs", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "StyleTTS2", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио", "description": "Python: TTS с переносом стиля, open-source SOTA", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Local image gen
    {"name": "ComfyUI", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения", "description": "Python: node-based UI для SD/Flux, де-факто стандарт локальной генерации", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": ["Automatic1111"]},
    {"name": "Automatic1111 (A1111)", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения", "description": "Python: классический webUI для Stable Diffusion, медленно развивается", "stack": "Python", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "Forge (sd-webui-forge)", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения", "description": "Python: оптимизированный форк A1111, в 2-4× быстрее", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": ["Automatic1111"]},
    {"name": "Fooocus", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения", "description": "Python: SDXL с UX как у Midjourney, ноль настроек", "stack": "Python", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "SwarmUI", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения", "description": "C#: ComfyUI-бэкенд с удобным UI", "stack": "C#", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "diffusers", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения", "description": "Python: HF библиотека для diffusion моделей, программный API", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "SD WebUI reForge", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения", "description": "Python: современный форк A1111 с оптимизациями", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": ["Automatic1111"]},
    
    # Embedding / Vector (локальные)
    {"name": "infinity (embedding server)", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "Vector", "description": "Rust: high-throughput embedding server, в 10× быстрее text-embeddings-inference", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "text-embeddings-inference (TEI)", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "Vector", "description": "Rust/C++: HF server для embeddings, быстрый", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "sentence-transformers", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "Vector", "description": "Python: классика для embeddings, медленно но точно", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Observability на Rust
    {"name": "GreptimeDB", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "Observability", "description": "Rust: time-series DB, замена InfluxDB/Prometheus", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["InfluxDB"]},
    {"name": "Vector", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "Observability", "description": "Rust: log/metric/trace pipeline, замена Logstash/Fluentd", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["Logstash", "Fluentd"]},
    
    # Self-hosted сервера
    {"name": "Coolify", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "Self-hosted", "description": "PHP/Svelte: open-source Heroku/Netlify/Vercel self-hosted", "stack": "PHP", "autonomy": "local", "lifecycle": "active", "supersedes": ["Vercel", "Heroku"]},
    {"name": "Dokploy", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "Self-hosted", "description": "TypeScript: open-source Vercel alternative на Docker", "stack": "TypeScript", "autonomy": "local", "lifecycle": "active", "supersedes": ["Vercel"]},
    {"name": "CapRover", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "Self-hosted", "description": "Node.js: self-hosted PaaS на Docker", "stack": "TypeScript", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Супербыстрые базы данных
    {"name": "SurrealDB", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "DB", "description": "Rust: multi-model DB (relational+document+graph), в одном бинарнике", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "Turso (libSQL)", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "DB", "description": "Rust/C: форк SQLite с replication, edge-DB", "stack": "Rust", "autonomy": "hybrid", "lifecycle": "active", "supersedes": []},
    {"name": "Redb", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "DB", "description": "Rust: embedded key-value DB, проще than SQLite", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "FoundationDB", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": "DB", "description": "C++: distributed transactional DB от Apple", "stack": "C++", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Супербыстрые веб-серверы
    {"name": "Caddy", "category": "CLI и утилиты", "subcategory": "Сервер", "description": "Go: веб-сервер с авто-HTTPS, проще nginx", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["nginx"]},
    {"name": "Pingora", "category": "CLI и утилиты", "subcategory": "Сервер", "description": "Rust: Cloudflare's reverse-proxy framework", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["nginx"]},
    {"name": "axum", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Rust: web framework от tokio team, ergonomics+type safety", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "actix-web", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Rust: высокопроизводительный web framework", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "pavex", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Rust: compiler-driven web framework, от Luca Palmieri", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Async Python на Rust
    {"name": "uvicorn", "category": "CLI и утилиты", "subcategory": "Python", "description": "Python/Cython: ASGI server, стандарт для FastAPI", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "granian", "category": "CLI и утилиты", "subcategory": "Python", "description": "Rust: ASGI/WSGI server, в 2-5× быстрее uvicorn", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["uvicorn", "gunicorn"]},
    {"name": "hypercorn", "category": "CLI и утилиты", "subcategory": "Python", "description": "Python: ASGI server с HTTP/2 и HTTP/3", "stack": "Python", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "robyn", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Rust+Python: web framework, в 2× быстрее FastAPI", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["FastAPI"]},
    {"name": "litestar", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб", "description": "Python: ASGI framework, развитие Starlette", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": ["FastAPI"]},
    
    # Супербыстрая Data Engineering
    {"name": "dlt (data loading tool)", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных", "description": "Python: ELT в несколько строк кода, source-to-warehouse", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "dagster", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных", "description": "Python: data orchestrator с asset-oriented model", "stack": "Python", "autonomy": "local", "lifecycle": "active", "supersedes": ["Airflow"]},
    {"name": "prefect 3", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных", "description": "Python: workflow orchestration с dev-опытом", "stack": "Python", "autonomy": "hybrid", "lifecycle": "active", "supersedes": ["Airflow"]},
    
    # Cargo-экосистема (Rust)
    {"name": "cargo-nextest", "category": "CLI и утилиты", "subcategory": "Rust", "description": "Rust: более быстрый и_feature-rich test runner для cargo", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["cargo test"]},
    {"name": "cargo-machete", "category": "CLI и утилиты", "subcategory": "Rust", "description": "Rust: поиск неиспользуемых зависимостей", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "cargo-deny", "category": "CLI и утилиты", "subcategory": "Rust", "description": "Rust: аудит лицензий и уязвимостей зависимостей", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "cargo-binstall", "category": "CLI и утилиты", "subcategory": "Rust", "description": "Rust: установка бинарников вместо компиляции", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["cargo install"]},
    {"name": "cargo-metrics", "category": "CLI и утилиты", "subcategory": "Rust", "description": "Rust: метрики компиляции crate'ов", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # LSP/языковые серверы
    {"name": "rust-analyzer", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE", "description": "Rust: LSP для Rust, де-факто стандарт", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "pyright", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE", "description": "TypeScript: type checker для Python от Microsoft", "stack": "TypeScript", "autonomy": "local", "lifecycle": "active", "supersedes": ["mypy"]},
    {"name": "basedpyright", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE", "description": "TypeScript: форк pyright с доп. фичами и open-source", "stack": "TypeScript", "autonomy": "local", "lifecycle": "active", "supersedes": ["pyright"]},
    {"name": "ruff-lsp", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE", "description": "Rust: LSP обёртка над ruff", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Yaml/TOML/JSON
    {"name": "yq (mikefarah)", "category": "CLI и утилиты", "subcategory": "Текст", "description": "Go: jq для YAML, самый современный", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "yq (kislyuk)", "category": "CLI и утилиты", "subcategory": "Текст", "description": "Python: jq-обёртка для YAML", "stack": "Python", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
    {"name": "jq", "category": "CLI и утилиты", "subcategory": "Текст", "description": "C: классика для JSON, как sed для текста", "stack": "C", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "dasel", "category": "CLI и утилиты", "subcategory": "Текст", "description": "Go: jq для JSON/YAML/TOML/XML/CSV", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["jq", "yq"]},
    {"name": "toml-cli", "category": "CLI и утилиты", "subcategory": "Текст", "description": "Rust: TOML-парсер CLI", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Markdown
    {"name": "glow", "category": "CLI и утилиты", "subcategory": "Markdown", "description": "Rust: Markdown renderer в терминале, от Charm", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "mdcat", "category": "CLI и утилиты", "subcategory": "Markdown", "description": "Rust: cat для Markdown с подсветкой", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    
    # Secrets / Security
    {"name": "age", "category": "9. Безопасность, аудит, этика", "subcategory": "Crypto", "description": "Go: простой file encryption от Filippo Valsorda", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["gpg"]},
    {"name": "sops", "category": "9. Безопасность, аудит, этика", "subcategory": "Secrets", "description": "Go: Mozilla, secrets ops, шифрование значений в YAML/JSON", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": []},
    {"name": "gopass", "category": "9. Безопасность, аудит, этика", "subcategory": "Secrets", "description": "Go: password manager, форк pass на Go с фичами", "stack": "Go", "autonomy": "local", "lifecycle": "active", "supersedes": ["pass"]},
    {"name": "bitwarden-cli (rbw)", "category": "9. Безопасность, аудит, этика", "subcategory": "Secrets", "description": "Rust: альтернативный CLI для Bitwarden", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["bitwarden-cli"]},
    
    # System info
    {"name": "fastfetch", "category": "CLI и утилиты", "subcategory": "Система", "description": "C: замена neofetch, в 10× быстрее", "stack": "C", "autonomy": "local", "lifecycle": "active", "supersedes": ["neofetch"]},
    {"name": "macchina", "category": "CLI и утилиты", "subcategory": "Система", "description": "Rust: system info, альтернатива neofetch", "stack": "Rust", "autonomy": "local", "lifecycle": "active", "supersedes": ["neofetch"]},
    {"name": "ahoy", "category": "CLI и утилиты", "subcategory": "Автоматизация", "description": "Go: аналог make на YAML", "stack": "Go", "autonomy": "local", "lifecycle": "maintenance", "supersedes": []},
]

# Конвертируем в полный формат статьи
def slug(name):
    s = name.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s).strip('-')
    return s[:64]

TODAY = "2026-09-05"
def signature(tool_id, status):
    return f"polymath-{TODAY}-{tool_id}-{status}"

new_articles = []
existing_keys = set(a["forma"]["name"].lower().strip() for a in articles)

for t in NEW_TOOLS:
    name = t["name"]
    if name.lower().strip() in existing_keys:
        continue
    existing_keys.add(name.lower().strip())
    
    aid = slug(name)
    desc = t["description"]
    
    article = {
        "id": aid,
        "forma": {
            "name": name,
            "aliases": [],
            "url": "",
            "license": "UNKNOWN",
            "category": t["category"],
            "subcategory": t.get("subcategory", ""),
            "version": "UNKNOWN",
            "release_date": "UNKNOWN",
            "stack": t.get("stack", "Mixed"),
            "autonomy": t.get("autonomy", "local"),
            "lifecycle": t.get("lifecycle", "active"),
            "supersedes": t.get("supersedes", [])
        },
        "text": [],
        "field": {
            "collocations": [],
            "competitors": [],
            "replaces": t.get("supersedes", [])
        },
        "whole": {"chain_in": [], "chain_out": []},
        "noise": [{
            "claim": desc,
            "source": "polymath_supplement_v2",
            "agent": "AI",
            "verdict": "noise"
        }],
        "court": {
            "status": "HYP",
            "verified_at": TODAY,
            "verified_by": "POLYMATH",
            "search_query": "",
            "sources_count": 0,
            "signature": signature(aid, "HYP")
        }
    }
    new_articles.append(article)

print(f"Добавлено новых: {len(new_articles)} статей")
all_articles = articles + new_articles

# ─────────────────────────────────────────────
# 3. Помечаем legacy для существующих
# ─────────────────────────────────────────────
LEGACY_NAMES = {
    "flake8": "ruff",
    "pylint": "ruff", 
    "black": "ruff format",
    "isort": "ruff",
    "webpack": "turbopack/vite/rspack",
    "eslint": "biome (для новых проектов)",
    "prettier": "biome",
    "httpie": "xh (Rust)",
    "ncdu": "gdu/dust (Rust)",
    "htop": "btop",
    "neofetch": "fastfetch",
    "sed": "sd (Rust)",
    "cat": "bat (Rust)",
    "ls": "eza/lsd (Rust)",
    "find": "fd (Rust)",
    "grep": "ripgrep (Rust)",
    "ps": "procs (Rust)",
    "du": "dust (Rust)",
    "df": "duf (Rust)",
    "cd": "zoxide (Rust)",
    "make": "just (Rust)",
    "curl": "xh для JSON API",
    "dig": "dog (Rust)",
    "hexdump": "hexyl (Rust)",
    "traceroute": "trippy (Rust)",
    "iftop": "bandwhich (Rust)",
    "ping": "gping (Rust)",
    "ab": "oha (Rust)",
    "wrk": "oha (Rust)",
    "cloc": "tokei (Rust)",
    "time": "hyperfine (Rust)",
    "git diff": "delta (Rust)",
    "git CLI": "lazygit (Go)",
    "docker CLI": "lazydocker (Go)",
    "docker history": "dive (Go)",
    "docker stats": "ctop (Go)",
    "kubectl logs": "stern (Go)",
    "pass": "gopass (Go)",
    "gpg": "age (Go)",
    "tmux": "zellij (Rust)",
    "screen": "zellij (Rust)",
    "node": "bun/deno",
    "npm": "bun/pnpm",
    "yarn": "bun/pnpm",
    "Logstash": "Vector (Rust)",
    "Fluentd": "Vector (Rust)",
    "InfluxDB": "GreptimeDB (Rust)",
    "Airflow": "dagster/prefect",
    "Automatic1111": "ComfyUI/Forge",
    "iterm2": "ghostty/wezterm",
    "alacritty": "ghostty",
    "powerlevel10k": "starship/oh-my-posh",
    "pyright": "basedpyright",
    "mypy": "pyright",
    "conda": "pixi/mamba",
    "poetry": "uv",
    "pdm": "uv",
    "pip": "uv",
    "pyenv": "mise",
    "asdf": "mise",
    "nvm": "mise",
    "rbenv": "mise",
    "fasd": "zoxide",
    "autojump": "zoxide",
    "exa": "eza",
    "rollup": "rolldown",
    "babel": "swc",
    "fastapi": "litestar/robyn",
    "uvicorn": "granian",
    "gunicorn": "granian",
    "openai-whisper": "whisper.cpp/faster-whisper",
}

# Помечаем существующие
marked_legacy = 0
for a in all_articles:
    name_lower = a["forma"]["name"].lower().strip()
    if name_lower in LEGACY_NAMES:
        a["forma"]["lifecycle"] = "legacy"
        # Если supersedes пустой, заполнить
        modern = LEGACY_NAMES[name_lower]
        if not a["forma"].get("supersedes"):
            a["forma"]["supersedes"] = []
        if not a["forma"]["supersedes"]:
            a["forma"]["supersedes"] = [{"replaced_by": modern, "reason": "Современная замена"}]
        marked_legacy += 1

print(f"Помечено legacy: {marked_legacy} статей")

# Сохраняем
OUT.write_text(json.dumps(all_articles, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\nИтого: {len(all_articles)} статей → {OUT}")

# Статистика
from collections import Counter
stack_stats = Counter(a["forma"].get("stack", "?") for a in all_articles)
auto_stats = Counter(a["forma"].get("autonomy", "?") for a in all_articles)
life_stats = Counter(a["forma"].get("lifecycle", "?") for a in all_articles)
print("\nПо стеку:")
for k, n in stack_stats.most_common():
    print(f"  {n:4d}  {k}")
print("\nПо автономности:")
for k, n in auto_stats.most_common():
    print(f"  {n:4d}  {k}")
print("\nПо жизненному циклу:")
for k, n in life_stats.most_common():
    print(f"  {n:4d}  {k}")
