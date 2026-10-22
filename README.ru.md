<div align="center">
  <img src="docs/assets/pattern-atlas-mark.svg" alt="Pattern Atlas" width="126" height="126">

  # Pattern Atlas

  **Describe. Verify. Falsify.**

  Открытый offline-first Agent Skill для исследования, распознавания и критической проверки графических паттернов.

  [![Agent Skills](https://img.shields.io/badge/Agent_Skills-compatible-4cbfbd)](https://agentskills.io/specification)
  [![skills.sh](https://img.shields.io/badge/skills.sh-Pattern%20Atlas-111111)](https://www.skills.sh/kaigorodovtuskul/pattern-atlas-technical-analysis-agent-skill/pattern-atlas)
  [![MIT](https://img.shields.io/badge/license-MIT-4c6078)](LICENSE)
  [![Python](https://img.shields.io/badge/Python-3.9%2B-4c6078)](#установка)
  [![Source](https://img.shields.io/badge/taxonomy-ThePatternSite-31455f)](https://www.thepatternsite.com/chartpatterns.html)

  [English](README.md) · **Русский** · [Офлайн-галерея](gallery.html) · [Аудит источников](docs/SOURCE_AUDIT.md)
</div>

---

## О проекте

**Pattern Atlas** — открытый Agent Skill с каталогом паттернов технического анализа, оригинальными учебными SVG-схемами и проверяемыми инструментами для OHLCV. Справочник структурирован по именам из [алфавитного каталога Thomas Bulkowski / ThePatternSite](https://www.thepatternsite.com/chartpatterns.html) и написан самостоятельно: **не является зеркалом сайта, точной репродукцией его описаний или источником его статистики**.

Идея: ИИ не только узнаёт внешне похожую фигуру, но и объясняет, почему её можно **опровергнуть**. Агент должен отличать поиск названия в каталоге от подтверждённого на графике сигнала и от доказанной статистической закономерности.

<p align="center"><img src="docs/assets/workflow.svg" alt="Lookup, Classify, Verify, Falsify and Report" width="100%"></p>

### Что входит

| Компонент | Объём | Статус |
|---|---:|---|
| Уникальные записи каталога | **383** | Транскрипция индексных имён; 426 исходных строк, 43 точных повторения |
| Методические семейства | **38** | Авторские русские критерии и аналитические оговорки |
| Индивидуальные страницы | **383** | Одна на каждую запись, с особенностями, ограничениями и ссылкой |
| Оригинальные схемы SVG | **334** | Программно созданные учебные примеры **семейства**, не графики реальных торгов |
| Найденные прямые URL | **35** | Проверены ссылки на страницы, **не** все сведения этих страниц |
| OHLCV-сканер | **ограниченный** | Inside/outside, NR4/NR7, полные гэпы, эвристика подтверждённой двойной вершины/дна |
| Офлайн-галерея | **1 HTML** | Поиск и фильтры, без сервера, CDN и сборщика |

> **Правило точности.** 383 — покрытие *записей индекса*, а не 383 научно проверенных торговых стратегий или 383 реализованных алгоритма распознавания. Некоторые записи — методы, исследования и события, а не фигуры. Многие уникальные определения автора требуют сверки с конкретными страницами; код помечает это явно. См. [SOURCE_AUDIT](docs/SOURCE_AUDIT.md).

## Быстрый просмотр

Откройте [`gallery.html`](gallery.html) прямо в браузере после клонирования репозитория. В галерее доступны поиск, семейства, категории, SVG и переходы к индивидуальным Markdown-описаниям и первоисточнику. Для нормального отображения изображений при просмотре на GitHub лучше открыть локальную копию страницы.

Примеры материалов:

- [Ascending triangles](skills/pattern-atlas/patterns/ascending-triangles.md) — форма, проверка, ложные сигналы, SVG
- [Head-and-shoulders tops](skills/pattern-atlas/patterns/head-and-shoulders-tops.md) — шея/плечи и условия отмены
- [Double bottoms](skills/pattern-atlas/patterns/adam-and-adam-double-bottoms.md) — различие кандидата и пробоя neckline
- [Source audit](docs/SOURCE_AUDIT.md) — что проверено и что НЕ проверено

## Установка

### Агентский установщик

```bash
npx skills add KaigorodovTuskul/Pattern-Atlas-Technical-Analysis-Agent-Skill --skill pattern-atlas
```

Для Codex / Claude Code / Cursor можно выбрать конкретные агенты в [skills CLI](https://github.com/vercel-labs/skills). Команда устанавливает скилл напрямую из этого репозитория.

### Офлайн-установка без сторонних зависимостей

```bash
# Из корня репозитория; Python 3.9+
python scripts/install.py --project /path/to/project --agent codex --dry-run
python scripts/install.py --project /path/to/project --agent codex
```

Поддержаны `codex`, `claude-code`, `cursor`, `opencode`, `gemini`, `copilot`, `generic` — точные пути описаны в [COMPATIBILITY](docs/COMPATIBILITY.md). Установщик не перезаписывает старый скилл без `--force`. Можно также скопировать `skills/pattern-atlas` в поддерживаемую папку вручную.

## Использование

```text
Используй Pattern Atlas для анализа приложенного дневного графика.
Найди 2–3 гипотезы о формации, отметь границы, уровень подтверждения
и критерий отмены. Не выдумывай ни цен, ни вероятностей, ни статистики Bulkowski.
```

```bash
# Поиск оригинального термина или русского методического описания
python skills/pattern-atlas/scripts/search_catalog.py "cup with handle"
python skills/pattern-atlas/scripts/search_catalog.py "клин" --json
python skills/pattern-atlas/scripts/search_catalog.py --families
python skills/pattern-atlas/scripts/search_catalog.py --stats

# Открыть подробную запись по slug
python skills/pattern-atlas/scripts/search_catalog.py --id ascending-triangles

# Ограниченный воспроизводимый скринер OHLCV
python skills/pattern-atlas/scripts/scan_ohlcv.py examples/demo_ohlcv.csv --output results.json
```

Формат CSV: `date,open,high,low,close[,volume]`. Даты должны быть отсортированы в ISO-совместимом формате; volume необязателен. Скринер не получает данные из интернета, не корректирует корпоративные события и **не умеет автоматически обнаруживать все фигуры каталога**. Критерии и покрытие описаны в [DETECTION](skills/pattern-atlas/references/DETECTION.md).

## Структура репозитория

```text
Pattern-Atlas-Technical-Analysis-Agent-Skill/
├── README.md / README.ru.md / AGENTS.md / LICENSE / NOTICE / CHANGELOG.md
├── gallery.html                 # красивый интерактивный автономный каталог
├── skills/pattern-atlas/
│   ├── SKILL.md                # агентские инструкции, progressive disclosure
│   ├── data/
│   │   ├── catalog.json        # 383 записи, URL/доверие/описания/схемы
│   │   ├── families.json       # 38 семейств
│   │   └── index_names.txt     # индексная транскрипция с сохранением повторов
│   ├── patterns/               # 383 отдельных файла с описаниями
│   ├── references/             # 38 методик + индексы + протоколы
│   ├── assets/                 # 334 оригинальные SVG + demo OHLCV
│   └── scripts/                # поиск, OHLCV-сканер
├── scripts/                    # сборка, рендер, инсталляция, проверка
├── docs/                       # исходники, методология, совместимость
├── examples/                   # демоданные, запросы
├── tests/                      # unit/integration + поведенческие сценарии
└── .github/workflows/ci.yml   # CI-проверки
```

## Валидация / воспроизводимость

```bash
python scripts/validate.py
python -m unittest discover -s tests -v

# Пересобрать каталог, учебные SVG, страницы и галерею локально
python scripts/build_catalog.py
python scripts/render_diagrams.py
python scripts/build_docs.py
python scripts/validate.py
```

Проверки удостоверяют целостность файлов, связность ссылок, синтаксис SVG, схему данных и базовые свойства сканера. **Они не удостоверяют исходную достоверность статистики паттернов, превосходство над buy-and-hold или точное соответствие каждой авторской странице.**

## Объём и ограничения

Pattern Atlas — портативный Agent Skill без зависимостей, вдохновлённый **индексом/таксономией** Thomas Bulkowski / ThePatternSite. Для каждой записи индекса есть оригинальное русское объяснение; включены 38 лениво загружаемых методических справочников, 334 самостоятельно сгенерированные синтетические SVG-схемы, офлайн-галерея с поиском и фильтрами и ограниченные проверяемые правила для OHLCV. **Оригинальные описания сайта, исторические графики, фотографии и статистические таблицы не включены.** Используйте проект для структурного исследования и критической интерпретации, а не как доказанное прогнозное преимущество. Точные ограничения — в [аудите происхождения](docs/SOURCE_AUDIT.md).

## Атрибуция, авторские права и риски

**Оригинальный код, схемы и авторские комментарии** этого проекта распространяются по MIT. ThePatternSite, его оригинальный текст, скриншоты, фотографии и таблицы **не** лицензированы по MIT в этом репозитории; переходите по ссылкам, чтобы посмотреть их на исходном сайте. Проект не одобрен Thomas Bulkowski и не аффилирован с ним. Рыночные исходы неопределённы; это образовательный материал, а не персональная инвестиционная рекомендация или доказательство прибыльной стратегии. См. [RESEARCH ETHICS](docs/SOURCE_AUDIT.md), [LICENSE](LICENSE) и [NOTICE](NOTICE).
