# Pattern Atlas: быстрый старт

1. Откройте [галерею](../gallery.html) локально, чтобы посмотреть индекс паттернов и схемы.
2. Установите скилл: `python scripts/install.py --project PATH --agent codex`. Для OpenCode укажите `--agent opencode`.
3. Попросите агента: «Используй Pattern Atlas. Проанализируй эти OHLCV/скриншот, выдели возможные формации, альтернативы, уровни подтверждения и отмены. Укажи ограничения проверки исходного сайта».
4. Термин из индекса можно искать без LLM: `python skills/pattern-atlas/scripts/search_catalog.py "double bottoms"`.
5. Демонстрация OHLCV: `python skills/pattern-atlas/scripts/scan_ohlcv.py examples/demo_ohlcv.csv`.

Полный состав описан в [README](../README.md), а ограничения первоисточника — в [аудите](SOURCE_AUDIT.md).
