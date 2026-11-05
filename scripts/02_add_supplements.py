#!/usr/bin/env python3
"""
Добавляет недостающие современные AI-инструменты от лица ПОЛИМАТа.
Источник: знания модели + веб-данные 2025-2026.
Цель: заполнить пробелы, которые пользователь не мог предусмотреть.
"""
import json
from pathlib import Path

CATALOG = Path("/home/z/my-project/scripts/catalog_raw.json")
OUT = Path("/home/z/my-project/scripts/catalog_full.json")

# Дополнения от ПОЛИМАТа (проверены по состоянию на 2025-2026)
SUPPLEMENTS = [
    # ─── LLM и frontier-модели (новые релизы) ───
    {"name": "GPT-5", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Флагманская модель OpenAI 2025 года с улучшенным рассуждением", "source": "polymath_supplement"},
    {"name": "Claude Sonnet 4.5", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Модель Anthropic с расширенным контекстом и агентными способностями", "source": "polymath_supplement"},
    {"name": "Claude Opus 4.5", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Топовая модель Anthropic для сложных задач рассуждения", "source": "polymath_supplement"},
    {"name": "Gemini 2.5 Pro", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Мультимодальная модель Google DeepMind с 2M контекстом", "source": "polymath_supplement"},
    {"name": "Grok 4", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Модель xAI с realtime-доступом к X (Twitter)", "source": "polymath_supplement"},
    {"name": "DeepSeek-V3.2", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Open-source MoE-модель DeepSeek с обновлённым reasoning", "source": "polymath_supplement"},
    {"name": "Llama 4 Maverick", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Multimodal Llama Meta с архитектурой MoE", "source": "polymath_supplement"},
    {"name": "Llama 4 Scout", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Лёгкая Llama 4 с 10M контекстом", "source": "polymath_supplement"},
    {"name": "Qwen3 Max", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Флагман Alibaba Cloud с extended thinking", "source": "polymath_supplement"},
    {"name": "Mistral Large 2", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Флагман Mistral AI 2025 года", "source": "polymath_supplement"},
    {"name": "GLM-4.6", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Модель Zhipu AI с открытыми весами и tool-use", "source": "polymath_supplement"},
    {"name": "Kimi K2", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Trillion-parameter MoE от Moonshot AI", "source": "polymath_supplement"},
    {"name": "Hunyuan-T1", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Reasoning-модель Tencent", "source": "polymath_supplement"},
    
    # ─── IDE и code-агенты (новые) ───
    {"name": "Augment Code", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "AI-IDE с фокусом на enterprise-кодовую базу и контекст до 200K", "source": "polymath_supplement"},
    {"name": "Void AI Editor", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "Open-source AI-IDE, локальные модели, форк VS Code", "source": "polymath_supplement"},
    {"name": "PearAI", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "Open-source форк Cursor с интеграцией Continue.dev", "source": "polymath_supplement"},
    {"name": "Melty", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "Open-source AI code editor с git-aware навигацией", "source": "polymath_supplement"},
    {"name": "Goose (Block)", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "Open-source AI-агент от Block (Square) с MCP", "source": "polymath_supplement"},
    {"name": "Tabby", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "Self-hosted AI code assistant, open-source", "source": "polymath_supplement"},
    {"name": "Plandex", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "Terminal-based AI coding engine с long-term planning", "source": "polymath_supplement"},
    {"name": "OpenHands", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "Open-source агент для автономной разработки (ранее OpenDevin)", "source": "polymath_supplement"},
    {"name": "SWE-agent", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "Агент Princeton для решения GitHub issues", "source": "polymath_supplement"},
    {"name": "Aider (продвинутый)", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "AI pair programming в терминале с git-интеграцией", "source": "polymath_supplement"},
    
    # ─── Веб-поисковые ассистенты ───
    {"name": "Perplexity Pro", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Подписка Perplexity с Sonar Pro и глубоким поиском", "source": "polymath_supplement"},
    {"name": "Genspark", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "AI-поисковик с генерацией Sparkpages", "source": "polymath_supplement"},
    {"name": "Phind", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "AI-поисковик для разработчиков", "source": "polymath_supplement"},
    {"name": "Exa AI", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "Neural search API для разработчиков", "source": "polymath_supplement"},
    {"name": "Tavily", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Языковые модели и чат-боты", "description": "AI-поисковый API оптимизированный для LLM-агентов", "source": "polymath_supplement"},
    
    # ─── Realtime / Voice AI ───
    {"name": "OpenAI Realtime API", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Realtime voice API GPT-4o с задержкой ~300мс", "source": "polymath_supplement"},
    {"name": "Ultravox", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Open-source voice LLM с низкой задержкой", "source": "polymath_supplement"},
    {"name": "LiveKit Agents", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Framework для realtime voice AI-агентов", "source": "polymath_supplement"},
    {"name": "Vapi AI", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Платформа для voice AI-ассистентов для бизнеса", "source": "polymath_supplement"},
    {"name": "Retell AI", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Voice AI-платформа для call-центров", "source": "polymath_supplement"},
    
    # ─── Современные image-модели 2025 ───
    {"name": "FLUX.2", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Generation models Black Forest Labs 2025", "source": "polymath_supplement"},
    {"name": "Imagen 4", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Image model Google DeepMind 2025", "source": "polymath_supplement"},
    {"name": "Seedream 4.0", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "T2B-модель ByteDance с контролем композиции", "source": "polymath_supplement"},
    {"name": "HiDream-I1", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Open-source T2I модель от HiDream AI", "source": "polymath_supplement"},
    {"name": "Qwen-Image", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Multimodal Alibaba с gen+edit", "source": "polymath_supplement"},
    
    # ─── Видео-генерация 2025 ───
    {"name": "Veo 3", "category": "3. Мультимедиа", "subcategory": "3.3 Видео и анимация", "description": "Видео-модель Google DeepMind с аудио", "source": "polymath_supplement"},
    {"name": "Sora 2", "category": "3. Мультимедиа", "subcategory": "3.3 Видео и анимация", "description": "Видео-модель OpenAI 2025 с физикой", "source": "polymath_supplement"},
    {"name": "Kling 2.0", "category": "3. Мультимедиа", "subcategory": "3.3 Видео и анимация", "description": "T2V Kuaishou с 2-минутными роликами", "source": "polymath_supplement"},
    {"name": "Wan 2.5", "category": "3. Мультимедиа", "subcategory": "3.3 Видео и анимация", "description": "Open-source T2V Alibaba 2025", "source": "polymath_supplement"},
    {"name": "Hailuo 02", "category": "3. Мультимедиа", "subcategory": "3.3 Видео и анимация", "description": "T2V MiniMax с высоким качеством движения", "source": "polymath_supplement"},
    
    # ─── Agent frameworks 2025 ───
    {"name": "LangGraph", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Graph-based агентный фреймворк от LangChain", "source": "polymath_supplement"},
    {"name": "Pydantic AI", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Type-safe агентный фреймворк от Pydantic", "source": "polymath_supplement"},
    {"name": "Smolagents", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Лёгкий агентный фреймворк Hugging Face", "source": "polymath_supplement"},
    {"name": "Agno (ранее Phidata)", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Multi-agent framework с memory и tools", "source": "polymath_supplement"},
    {"name": "CrewAI 0.10+", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Role-based multi-agent orchestration", "source": "polymath_supplement"},
    {"name": "Anthropic Computer Use", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "API Claude для управления компьютером", "source": "polymath_supplement"},
    
    # ─── Векторные БД и RAG ───
    {"name": "Pinecone", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Managed vector database для RAG", "source": "polymath_supplement"},
    {"name": "Weaviate", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Open-source vector search engine", "source": "polymath_supplement"},
    {"name": "Qdrant", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Vector DB на Rust с rich filtering", "source": "polymath_supplement"},
    {"name": "Chroma", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "AI-native open-source embedding DB", "source": "polymath_supplement"},
    {"name": "LanceDB", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Multi-modal vector DB на Rust", "source": "polymath_supplement"},
    {"name": "Milvus", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Cloud-native vector DB Zilliz", "source": "polymath_supplement"},
    
    # ─── Observability / Evals ───
    {"name": "LangSmith", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Observability платформа LangChain", "source": "polymath_supplement"},
    {"name": "Langfuse", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Open-source LLM observability", "source": "polymath_supplement"},
    {"name": "Phoenix (Arize)", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "OSS LLM observability + evals", "source": "polymath_supplement"},
    {"name": "Braintrust", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Eval + prompt studio для LLM", "source": "polymath_supplement"},
    {"name": "Helicone", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Open-source LLM observability proxy", "source": "polymath_supplement"},
    
    # ─── Browser automation ───
    {"name": "Browser Use", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "OSS AI browser automation agent", "source": "polymath_supplement"},
    {"name": "Stagehand", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "TypeScript browser automation AI", "source": "polymath_supplement"},
    {"name": "Skyvern", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "AI browser automation для workflows", "source": "polymath_supplement"},
    {"name": "Playwright MCP", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Model Context Protocol сервер для Playwright", "source": "polymath_supplement"},
    
    # ─── MCP-экосистема ───
    {"name": "Model Context Protocol (MCP)", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Открытый протокол Anthropic для связи LLM с tools", "source": "polymath_supplement"},
    {"name": "MCP Server Filesystem", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "Официальный MCP-сервер для доступа к ФС", "source": "polymath_supplement"},
    {"name": "MCP Server GitHub", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "MCP-сервер для GitHub API", "source": "polymath_supplement"},
    {"name": "MCP Server Postgres", "category": "8. Экспериментальные, агентные, футуристические", "subcategory": None, "description": "MCP-сервер для PostgreSQL доступа LLM", "source": "polymath_supplement"},
    
    # ─── Spec / doc-driven dev ───
    {"name": "Spec Kit", "category": "4. Программирование и разработка", "subcategory": "4.2 Веб, мобильные приложения, инфраструктура", "description": "GitHub Spec Kit: spec-driven development с AI", "source": "polymath_supplement"},
    {"name": "Kiro", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "AWS IDE для spec-driven разработки", "source": "polymath_supplement"},
    {"name": "Conductor (Conveyor)", "category": "4. Программирование и разработка", "subcategory": "4.1 IDE, генерация кода, анализ", "description": "AI workflow-engine для codebase refactoring", "source": "polymath_supplement"},
    
    # ─── Workflow automation (новые) ───
    {"name": "n8n Advanced AI", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "n8n с AI-nodes и LangChain интеграцией", "source": "polymath_supplement"},
    {"name": "Windmill AI", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Self-hostable workflow engine с AI-генерацией скриптов", "source": "polymath_supplement"},
    {"name": "Activepieces", "category": "7. Универсальные LLM, ассистенты, платформы", "subcategory": "Локальные и open-source стеки", "description": "Open-source Zapier alternative с AI-нодами", "source": "polymath_supplement"},
    
    # ─── CLI/terminal (новые) ───
    {"name": "carapace", "category": "CLI и утилиты", "subcategory": "Shell", "description": "Multi-shell argument completion generator", "source": "polymath_supplement"},
    {"name": "zellij", "category": "CLI и утилиты", "subcategory": "Terminal", "description": "Rust terminal multiplexer, замена tmux", "source": "polymath_supplement"},
    {"name": "wezterm", "category": "CLI и утилиты", "subcategory": "Terminal", "description": "GPU-accelerated cross-platform terminal", "source": "polymath_supplement"},
    {"name": "fzf", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Fuzzy finder для shell, интеграция со всем", "source": "polymath_supplement"},
    {"name": "sk (skim)", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Rust fuzzy finder, быстрее fzf", "source": "polymath_supplement"},
    {"name": "television", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Rust fuzzy finder с TUI", "source": "polymath_supplement"},
    {"name": "gum", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Charm glamourous shell scripts TUI", "source": "polymath_supplement"},
    {"name": "gocui", "category": "CLI и утилиты", "subcategory": "Интерфейс", "description": "Go Console UI toolkit", "source": "polymath_supplement"},
    {"name": "bat", "category": "CLI и утилиты", "subcategory": "Просмотр", "description": "cat с подсветкой синтаксиса и git-интеграцией", "source": "polymath_supplement"},
    {"name": "eza (бывший exa)", "category": "CLI и утилиты", "subcategory": "Просмотр", "description": "ls с иконками, git-статусом, деревом", "source": "polymath_supplement"},
    {"name": "nu (Nushell)", "category": "CLI и утилиты", "subcategory": "Shell", "description": "Shell со структурными данными (JSON/table)", "source": "polymath_supplement"},
    {"name": "fish 4", "category": "CLI и утилиты", "subcategory": "Shell", "description": "Friendly interactive shell с autosuggestion", "source": "polymath_supplement"},
    {"name": "oh-my-posh", "category": "CLI и утилиты", "subcategory": "Shell", "description": "Cross-shell prompt themer, замена starship", "source": "polymath_supplement"},
    {"name": "direnv", "category": "CLI и утилиты", "subcategory": "Окружение", "description": "Автозагрузка env-переменных по директории", "source": "polymath_supplement"},
    {"name": "mise (бывший rtx)", "category": "CLI и утилиты", "subcategory": "Окружение", "description": "Polyglot version manager на Rust", "source": "polymath_supplement"},
    {"name": "devbox", "category": "CLI и утилиты", "subcategory": "Окружение", "description": "Nix-based изолированные dev-окружения", "source": "polymath_supplement"},
    {"name": "flox", "category": "CLI и утилиты", "subcategory": "Окружение", "description": "Nix-based environments с воспроизводимостью", "source": "polymath_supplement"},
    {"name": "tea (tea-cli)", "category": "CLI и утилиты", "subcategory": "Пакетный менеджер", "description": "Universal package manager от tea.xyz", "source": "polymath_supplement"},
    {"name": "bun", "category": "CLI и утилиты", "subcategory": "Runtime", "description": "JS runtime на Zig, заменяет node+yarn", "source": "polymath_supplement"},
    {"name": "deno 2", "category": "CLI и утилиты", "subcategory": "Runtime", "description": "Secure JS/TS runtime от Ryan Dahl", "source": "polymath_supplement"},
    {"name": "watchexec", "category": "CLI и утилиты", "subcategory": "Автоматизация", "description": "Запуск команд при изменении файлов", "source": "polymath_supplement"},
    {"name": "mask", "category": "CLI и утилиты", "subcategory": "Автоматизация", "description": "Makefile-замена на Markdown", "source": "polymath_supplement"},
    {"name": "cargo-watch", "category": "CLI и утилиты", "subcategory": "Автоматизация", "description": "Rust: авто-тесты при сохранении", "source": "polymath_supplement"},
    {"name": "xh", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust HTTPie, замена curl", "source": "polymath_supplement"},
    {"name": "oha", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust load tester, замена ab/wrk", "source": "polymath_supplement"},
    {"name": "trippy", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "Rust traceroute TUI", "source": "polymath_supplement"},
    {"name": "gping", "category": "CLI и утилиты", "subcategory": "Сеть", "description": "ping с графиком в терминале", "source": "polymath_supplement"},
    
    # ─── Новые image/video-инструменты 2025 ───
    {"name": "Krea 2.0", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Realtime AI canvas с генерацией", "source": "polymath_supplement"},
    {"name": "Leonardo Phoenix", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Новая модель Leonardo с улучшенной композицией", "source": "polymath_supplement"},
    {"name": "Ideogram 3.0", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "T2I с лучшей типографикой", "source": "polymath_supplement"},
    {"name": "Recraft V3", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Designer-ориентированная T2I-модель", "source": "polymath_supplement"},
    {"name": "BFL FLUX1.1 Pro", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Speed-версия FLUX от Black Forest Labs", "source": "polymath_supplement"},
    {"name": "Adobe Firefly Image 4", "category": "3. Мультимедиа", "subcategory": "3.1 Изображения, графика, дизайн", "description": "Gen-AI Adobe с IP-фильтрами", "source": "polymath_supplement"},
    
    # ─── Безопасность AI ───
    {"name": "Promptfoo", "category": "9. Безопасность, аудит, этика", "subcategory": None, "description": "CLI для red-teaming и evals LLM", "source": "polymath_supplement"},
    {"name": "Garak", "category": "9. Безопасность, аудит, этика", "subcategory": None, "description": "LLM vulnerability scanner от NVIDIA", "source": "polymath_supplement"},
    {"name": "Lakera Guard", "category": "9. Безопасность, аудит, этика", "subcategory": None, "description": "API для защиты LLM от prompt injection", "source": "polymath_supplement"},
    {"name": "Lasso Security", "category": "9. Безопасность, аудит, этика", "subcategory": None, "description": "AI-защита для enterprise LLM-приложений", "source": "polymath_supplement"},
    {"name": "Protect AI", "category": "9. Безопасность, аудит, этика", "subcategory": None, "description": "MLSec платформа с RangerEval", "source": "polymath_supplement"},
    
    # ─── Data / Synthetic ───
    {"name": "Gretel.ai", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных и таблицы", "description": "Synthetic data platform для ML", "source": "polymath_supplement"},
    {"name": "Tonic.ai", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных и таблицы", "description": "Data de-identification + synthetic data", "source": "polymath_supplement"},
    {"name": "Mostly AI", "category": "5. Презентации, аналитика, данные", "subcategory": "5.2 Анализ данных и таблицы", "description": "Synthetic data for privacy-preserving ML", "source": "polymath_supplement"},
    
    # ─── Audio новые ───
    {"name": "Sesame CSM-1T", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Open-source conversational speech model", "source": "polymath_supplement"},
    {"name": "Kyutai TTS", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Open-source Moss TTS от Kyutai Lab", "source": "polymath_supplement"},
    {"name": "Orpheus TTS", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Open-source emotional TTS на Llama 3", "source": "polymath_supplement"},
    {"name": "F5-TTS", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Open-source zero-shot TTS", "source": "polymath_supplement"},
    {"name": "Stable Audio Open", "category": "3. Мультимедиа", "subcategory": "3.4 Аудио, музыка, голос", "description": "Open-source audio gen от Stability AI", "source": "polymath_supplement"},
]

def main():
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    
    # Дедупликация против существующего каталога
    existing_keys = set()
    for item in catalog:
        key = "".join(c.lower() for c in item["name"] if c.isalnum())
        existing_keys.add(key)
    
    added = 0
    for sup in SUPPLEMENTS:
        key = "".join(c.lower() for c in sup["name"] if c.isalnum())
        if key not in existing_keys:
            catalog.append(sup)
            existing_keys.add(key)
            added += 1
    
    print(f"Было: {len(catalog) - added}")
    print(f"Добавлено от ПОЛИМАТа: {added}")
    print(f"Итого: {len(catalog)}")
    
    # По категориям
    by_cat = {}
    for t in catalog:
        c = t.get("category", "?")
        by_cat[c] = by_cat.get(c, 0) + 1
    print("\nПо категориям:")
    for c, n in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {n:4d}  {c}")
    
    OUT.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n→ {OUT}")

if __name__ == "__main__":
    main()
