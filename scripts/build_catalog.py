#!/usr/bin/env python3
"""Build an original educational knowledge base from a manually reviewed index transcription.
No third-party page text or images are scraped, downloaded or republished.
"""
from __future__ import annotations
import json, re, unicodedata, hashlib
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/pattern-atlas'
INDEX='https://www.thepatternsite.com/chartpatterns.html'
VISUAL='https://www.thepatternsite.com/visualcpindex.html'
# URLs independently confirmed via public search; missing detail URLs deliberately not fabricated.
VERIFIED={
'cup with handle':'cup.html','cup with handle, inverted':'icup.html','inverted cup with handle':'icup.html',
'adam & adam double bottoms':'aadb.html','double bottoms, adam & adam':'aadb.html',
'head-and-shoulders tops':'hst.html','head-and-shoulders complex tops':'chst.html','complex head-and-shoulders tops':'chst.html',
'ascending triangles':'at.html','triangles, ascending':'at.html','descending triangles':'dt.html','triangles, descending':'dt.html',
'symmetrical triangles':'st.html','triangles, symmetrical':'st.html',
'falling wedge':'fallwedge.html','wedge, falling':'fallwedge.html',
'rising wedge':'risewedge.html','wedge, rising':'risewedge.html',
'pennants':'pennants.html','rectangle bottoms':'rectbots.html',
'descending broadening wedges':'dbw.html','broadening wedge, descending':'dbw.html',
'wedge, descending broadening':'dbw.html',
 '2b':'2B.html','roof':'roof.html','cloud banks':'Cloudbank.html', 'cat\'s ears':'CatsEars.html',
 'diving board':'DivingBoard.html','pothole':'Pothole.html','adam white setup':'AdamWhiteSetup.html',
 'three peaks and spike':'MultiPeak2B.html','3-peaks and spike':'MultiPeak2B.html',
 'three peaks and domed house':'3peaksdome.html','3 peaks and domed house':'3peaksdome.html','domed house and three peaks':'3peaksdome.html',
}
# Original concise analysis framework shared by each family; no claim of proprietary statistical replication.
FAMILIES={
 'triangles':('Треугольники', 'Сжатие диапазона между двумя границами: горизонтальная и наклонная либо две сходящиеся.', 'Отмечайте последовательные экстремумы, проводите верхнюю/нижнюю границы только по сформированным точкам. Для восходящего варианта верх близок к горизонтали, для нисходящего горизонтален низ; симметричный сходится с двух сторон.', 'Закрытие вне границы после достаточного числа касаний — кандидат на пробой; направление нельзя надёжно вывести из названия.', 'Возврат внутрь границ, ложный выход перед апексом, слишком мало независимых касаний.', 'Для целей иногда используют высоту основания, отложенную от пробоя; это сценарий, не обещание.', 'triangle'),
 'wedges':('Клинья', 'Две наклонённые в одну сторону, но сходящиеся трендовые линии.', 'Сравните наклоны верхней и нижней границы. Растущий клин направлен вверх, падающий — вниз; нужны чередующиеся касания обеих сторон.', 'Пробой внешней границы подтверждают закрытием и последующей структурой цены.', 'Короткая длительность делает фигуру похожей на вымпел; расширяющиеся линии указывают на иную формацию.', 'Цели оценивать по высоте формации или ближайшим уровням ликвидности с явным риском.', 'wedge'),
 'broadening':('Расширяющиеся формации', 'Волатильность увеличивается: максимумы и минимумы расходятся, вместо схождения образуя рупор.', 'Ищите чередующиеся экстремумы и две расходящиеся границы; прямоугольные разновидности имеют одну почти горизонтальную сторону.', 'Необходим фактический выход за крайнюю границу; до этого устойчивое направление неизвестно.', 'Шум и одиночные шпильки могут имитировать расширение; низкая ликвидность и гэпы мешают идентификации.', 'Измерять диапазон и учитывать расширение волатильности при стопе.', 'broadening'),
 'double':('Двойные вершины и основания', 'Два теста близкой зоны максимума или минимума с откатом между ними.', 'Для двойного дна зафиксируйте две впадины и промежуточный максимум; вершина зеркальна. Adam — узкий острый экстремум, Eve — более широкий и округлый.', 'Подтверждение дна — закрытие выше промежуточного максимума; вершины — ниже промежуточного минимума.', 'Без пробоя разделяющего экстремума это гипотеза, а не подтверждённый разворот. Различие Adam/Eve субъективно.', 'Обычное геометрическое правило: высота от экстремума до линии подтверждения; риск за защитным локальным экстремумом.', 'double'),
 'triple':('Тройные вершины и основания', 'Три близких по уровню теста сопротивления либо поддержки.', 'Разделите три экстремума промежуточными откатами; убедитесь, что это не одно шумное плато.', 'Подтверждение обычно требует прохода противоположной границы диапазона после третьего касания.', 'Третий экстремум может оказаться частью более широкой проторговки; без подтверждения модель остаётся предварительной.', 'Высота диапазона даёт грубый ориентир, обязательно проверять другие уровни.', 'triple'),
 'head_shoulders':('Голова и плечи', 'Три области разворота; средняя выражена сильнее, крайние формируют плечи.', 'Для вершины голова выше обоих плеч, линия шеи соединяет промежуточные впадины; основание зеркально. Сложная форма допускает повторные плечи/головы.', 'Подтверждающий выход за линию шеи в сторону разворота.', 'Слишком асимметричная структура, отсутствие тренда до модели и быстрый возврат за шею.', 'Высота головы над/под шеей — ориентир сценария; без статтеста не считать ожидаемой доходностью.', 'head_shoulders'),
 'cup':('Чашка с ручкой', 'Плавная закруглённая коррекция с возвратом к области края; ручка — последняя небольшая пауза.', 'Отличайте округлое U от резкого V, проверьте расположение ручки вблизи края. Перевёрнутая модель зеркальна.', 'Для бычьей модели — закрытие выше верхней границы ручки/края, для перевёрнутой — ниже соответствующего уровня.', 'Слишком глубокая ручка, несходство краёв или V-образная коррекция снижают сходство.', 'Глубина чашки — лишь исходная оценка амплитуды; стоп и ликвидность проверять отдельно.', 'cup'),
 'rounding':('Закруглённые развороты', 'Длительное плавное изменение наклона цены, U-образная или перевёрнутая U-образная траектория.', 'Проверяйте постепенное замедление исходного тренда и медленный переход к противоположному; избегайте подмены разового гэпа.', 'Для оценки смены фазы ждите устойчивого ухода от зоны краёв и новых максимумов/минимумов.', 'Без явного изменения тренда фигура может быть частью широкого боковика.', 'Сценарные уровни задаются границами предшествующей базы и волатильностью.', 'rounding'),
 'diamond':('Ромб', 'Сначала границы расходятся, затем сходятся: условная огранка ромба.', 'Выделите две фазы экстремумов, расширение и сжатие; нужны симметричные колебания.', 'Закрытие за конечной сужающейся границей — кандидат на завершение фигуры.', 'Необоснованно короткая формация часто оказывается просто шумом.', 'Высота максимального расширения — условный ориентир, не гарантия.', 'diamond'),
 'flags':('Флаги и консолидации после импульса', 'Резкий флагшток, затем компактный наклонный канал коррекции или плоская база.', 'Сначала установите предыдущий импульс; внутри небольшой паузы ищите две почти параллельные границы. High-and-tight требует особенно мощного импульса.', 'Пробой края паузы в направлении импульса — лишь торговая гипотеза.', 'Долгий боковик перестаёт быть краткосрочным флагом; слабый импульс не образует флагшток.', 'Флагшток иногда используют как измеритель продолжения; учитывайте невыполнение и откаты.', 'flag'),
 'pennants':('Вымпелы', 'После резкого движения формируется маленький симметричный треугольник.', 'Обязателен выраженный флагшток перед коротким сжатием; оцените время существования, а не только угол линий.', 'Подтверждающее закрытие за одной из сторон; продолжение тренда не гарантировано.', 'Форма без флагштока — скорее треугольник; поздний пробой может потерять смысл.', 'Сценарий может использовать часть длины флагштока, но проверяйте вероятность достижения отдельно.', 'pennant'),
 'rectangles':('Прямоугольники', 'Повторные подходы к двум почти горизонтальным границам, диапазон поддержка–сопротивление.', 'Для tops/bottoms учитывайте направление входа цены, не путайте с гарантией исхода.', 'Пробой границы по закрытию; ретест границы возможен, но необязателен.', 'Бесчисленные короткие зазубрины без устойчивой зоны не образуют корректный диапазон.', 'Высота прямоугольника — возможный масштаб, а не прогноз с определённой вероятностью.', 'rectangle'),
 'gaps':('Ценовые разрывы', 'Разрыв между диапазонами соседних баров или торговых сессий.', 'Отделите истинный гэп high/low от разницы только между закрытием и открытием; классификация area/breakaway/continuation/exhaustion требует контекста тренда.', 'Сигнал зависит от типа: пробой с гэпом, продолжение или возможное истощение.', 'Сплиты, дивиденды, FX-сессии и ошибки данных могут создать искусственный гэп.', 'Размер разрыва и движение до него требуют поправки на корпоративные действия.', 'gap'),
 'islands':('Островные развороты', 'Группа баров оказывается изолирована ценовыми гэпами по обе стороны.', 'Проверьте два разрыва противоположного направления и отделённую ими область торговли.', 'Только второй гэп подтверждает замкнутую островную структуру.', 'Отмена второго разрыва и частичное перекрытие диапазонов делает фигуру сомнительной.', 'Работайте с уровнем второго гэпа и волатильностью.', 'island'),
 'vturn':('V-развороты и экстремумы', 'Резкая смена направления с минимальной горизонтальной базой.', 'Ищите ускорение исходного тренда, единичную область экстремума и энергичный разворот; extended добавляет постразворотную паузу.', 'Подтверждение только после устойчивого движения против исходного тренда.', 'Раннее распознавание подвержено ретроспективному смещению; фаза сильных колебаний похожа на V.', 'Ориентиры ставятся на последующих уровнях, исходный экстремум важен для риска.', 'vturn'),
 'scallops':('Скаллопы', 'Повторяющиеся плавные дугообразные участки; инвертированная форма меняет ориентацию дуги.', 'Проверьте ритмическую округлость и направленность последовательных минимумов/максимумов.', 'Ориентиром служит обновление границы предыдущего элемента.', 'Скаллоп легко перепутать с любыми волнами тренда — нужен ясный повторяемый контур.', 'Измеряйте амплитуду дуги, не приписывайте точных целей без валидации.', 'scallop'),
 'pipes_horns':('Трубные и роговые образования', 'Короткие сочетания заметных соседних пиков/провалов или длинных теней на смежных барах.', 'Для pipe важно соседство выраженных экстремальных свечей; для horn — две заметные тени при промежуточном баре. Проверяйте таймфрейм.', 'Сигнал только после закрытия за ближайшей структурной границей.', 'Спред и низкий объём могут создать ложные длинные тени.', 'Оцените ближайшие уровни и фактический риск по теням.', 'pipes'),
 'harmonics':('Гармонические модели', 'Набор поворотных точек X-A-B-C-D и пропорций откатов/расширений Фибоначчи.', 'Для AB=CD, Gartley, Bat, Butterfly, Crab отдельно сравните отношения длин соседних сегментов; допуски нужно задавать заранее.', 'Предполагаемая зона разворота D сама по себе не сигнал: ждите реакцию цены.', 'Подгонка точек под идеальные коэффициенты после движения — серьёзный риск.', 'Невыполнение зон отмены и геометрия дают сценарный риск; не предсказывайте исход.', 'harmonic'),
 'waves':('Волновые структуры', 'Волновые последовательности Эллиотта: импульсы, коррекции, диагонали, плоскости и зигзаги.', 'Сформулируйте одну конкретную разметку и альтернативу; явно укажите степень волны и правила нарушений.', 'Подтверждение зависит от завершения фазы по заранее заявленному правилу.', 'Несколько допустимых волновых разметок создают субъективность; нельзя выдавать одну за объективный факт.', 'Сценарий основан на уровне отмены волнового счёта и независимых данных.', 'wave'),
 'measured':('Измеренные движения', 'Два приблизительно сходных импульса, разделённых промежуточной коррекцией.', 'Замерьте первый отрезок, откат и второй отрезок в тех же единицах цены и масштабе.', 'Кандидат на завершение после формирования второго сопоставимого движения; это ретроспективная оценка.', 'Не любой зигзаг обязан воспроизводить длину первого импульса.', 'Пропорция первого участка — гипотетический ориентир, не обязательно целевой уровень.', 'measured'),
 'deadcat':('Событийный обвал и отскок', 'Сильное падение, краткосрочный отскок и риск возобновления слабости; инверсия зеркальна.', 'Определите первичную аномальную амплитуду и контекст новостей, затем измерьте отскок.', 'Второе движение через локальный уровень подтверждает развитие сценария.', 'Отскок может оказаться устойчивым восстановлением; нельзя уверенно классифицировать до новых данных.', 'Учитывайте гэпы, корпоративные новости и невозможность исполнения по прежним ценам.', 'deadcat'),
 'bars':('Краткие OHLC-паттерны', 'Правила нескольких соседних баров по диапазонам high/low/open/close.', 'Проверьте конкретную последовательность баров и предшествующий тренд; inside, outside, NR4 и NR7 различаются формальными условиями.', 'Триггер задавайте по максимуму/минимуму сигнального бара, закрытию и контексту.', 'Единичный бар без контекста может часто давать ложные совпадения.', 'Не использовать без точного алгоритма и без проверки на собственной выборке.', 'bars'),
 'volume':('Объёмные структуры', 'Форма, наклон и относительная активность торговых объёмов.', 'Нормализуйте объём по инструменту и торговому календарю; сравните с предыдущим горизонтом.', 'Объём подтверждает или опровергает гипотезу о цене, но сам по себе не предсказывает направление.', 'Сплиты, неполные дни, непрозрачный внебиржевой оборот и фьючерсные роллы мешают сопоставлению.', 'Показывайте относительный объём и качество исходных данных.', 'volume'),
 'trend':('Тренды, уровни и каналы', 'Вспомогательные методы описания направления и динамических границ.', 'Стройте линии только по исторически доступным экстремумам, фиксируйте подтверждение касания.', 'Смена структуры swing high/swing low или закрытие за каналом — возможный сигнал.', 'Линия, проведённая задним числом с использованием будущих точек, вызывает look-ahead bias.', 'Сценарные уровни важнее произвольных идеально точных линий.', 'trend'),
 'event':('Событийные паттерны', 'Реакция цены на известное корпоративное, регуляторное или рейтинговое событие.', 'Фиксируйте точное время и дату публикации, тип события, неожиданность относительно консенсуса, корпоративные действия.', 'Событие — условие выборки, а не автоматический сигнал; реакцию проверяют после известного времени.', 'Survivorship bias, переиздания новостей, пересмотр данных, неликвидность и выбор удачных примеров.', 'Нужны event study, бенчмарк, затраты, окно события и альтернативные объяснения.', 'event'),
 'risk':('Риск и торговые приёмы', 'Материалы о выходе, стопах, защите капитала и типовых ошибках.', 'Опишите правило до сделки, приоритет ликвидности, размер позиции, комиссии и проскальзывание.', 'Не формирует самостоятельного графического сигнала.', 'Размытые правила риска приводят к переобучению и неуправляемым убыткам.', 'Использовать как ограничение стратегии, а не обещание доходности.', None),
 'research':('Методология и исследования', 'Обзорные материалы, рейтинги, учебные страницы, квизы и сравнения результатов.', 'Установите выборку, период, направление пробоя, правила подтверждения и единицу измерения.', 'Самостоятельного триггера нет: это справочные сведения.', 'Исторический рейтинг не переносится на другую выборку и рынок автоматически.', 'Не приводите статистику без идентифицируемого источника и методологии.', None),
 'misc':('Редкие/специальные формации', 'Специальная именованная фигура или метод автора; требует сверки с первоисточником.', 'Не переводите узнаваемое название в произвольные правила. Запросите полную спецификацию: геометрию, входной тренд, подтверждение и недействительность.', 'Неопределён до независимой проверки конкретной методики.', 'Риск ложной конкретизации особенно высок для авторских редких названий.', 'Не генерировать торговый сигнал по одному имени.', None),
}

FAMILIES.update({
 'bump_run':('Bump-and-run reversal','Сначала умеренный тренд, затем ускоренный участок («bump») с чрезмерно крутым наклоном и последующим возвратом через исходную линию.', 'Разделите базовую наклонную линию и фазу ускорения; важна смена угла, а не только один экстремум.', 'Слом исходной линии после ускорения и подтверждение контртрендовым ходом.', 'Весьма субъективный угол наклона и ошибки выбора точки начала.', 'Разметьте базовую линию, экстремум bump и цену фактического нарушения тренда.', 'bump_run'),
 'roof':('Крыша / перевёрнутая крыша','Формация с плоской нижней границей, подъёмом до центрального гребня и спадом обратно; инверсия зеркальна.', 'Выявите многократные подходы к горизонтальной базе и симметричную двухскатную верхнюю границу.', 'Закрытие вне ограничивающей стороны, возможно в любую сторону.', 'Может смешиваться с головой и плечами; важно не приписывать результат до подтверждения.', 'Высота между гребнем и горизонтальной базой задаёт ориентир.', 'roof'),
 'cloud_bank':('Облачная зона исторического сопротивления','Широкая длительная область прежних проторговок над текущей ценой выступает зоной потенциального сопротивления при восстановлении.', 'Отметьте исторический плотный торговый диапазон, резкий выход цены вниз и последующую попытку возвращения снизу.', 'Переход к росту требует отдельного сигнала; касание нижнего края «облака» не является подтверждением прибыли.', 'Нельзя считать каждый горизонтальный кластер cloud bank; избегайте выживших примеров.', 'Измеряйте ширину зоны и область следующего сопротивления.', 'cloud_bank'),
 'lindsay':('Три пика и куполообразный дом','Редкая длинная последовательность по Джорджу Линдсею: серия трёх пиков, разделительное снижение, закруглённый крупный подъём и новый разворот.', 'Структура обычно требует длительного периода и последовательных участков, а не простого тройного верха.', 'Не пытайтесь прогнозировать стадию без полной нумерованной разметки; нужна ссылка на метод Линдсея.', 'Высокая свобода ретроспективной подгонки, предсказательная ценность не установлена.', 'Не применять к торговле без независимой разметки и проверки.', 'lindsay'),
 'two_b':('Ложное обновление экстремума (2B)','После теста предыдущего экстремума цена кратко обновляет его, но не удерживает уровень и возвращается обратно.', 'Сравните два последовательных максимума или минимума; второй немного выходит за первый и быстро возвращается.', 'Возврат под прежний максимум для 2B top или выше прежнего минимума для 2B bottom.', 'Сильное продолжение тренда после нового экстремума опровергает предположение о ложном пробое.', 'Зона первого экстремума — ключ к сценарию и отмене.', 'two_b'),
 'steps':('Последовательность трёх уровней','Три последовательно понижающихся пика либо повышающихся минимума отражают смену структуры swing.', 'Каждый новый локальный экстремум должен быть явно ниже/выше предыдущего; проверяйте промежуточные откаты.', 'Триггер привязан к завершению третьей волны и пробою соответствующей локальной границы.', 'Случайные колебания в диапазоне не являются последовательностью устойчивых swing.', 'Устанавливайте стопы по последнему локальному экстремуму.', 'steps'),
})


FAMILIES.update({
 'cats_ears':('Кошачьи уши','Медвежья комбинация двух вершин после падения: две локальные «ушные» вершины разделены областью «scalp».', 'Проверьте нисходящий подход, паузу и два отчётливых пика; отдельно оцените 14-периодный RSI как вспомогательное условие оригинального описания.', 'Закрытие ниже разделяющего минимума; до пробоя не считать подтверждённой фигурой.', 'Автор сайта отдельно сообщает, что самостоятельно не тестировал результативность Cat’s Ears.', 'Измерение высоты между ухом и разделяющим минимумом — геометрический сценарий.', 'cats_ears'),
 'pothole':('Яма и трамплин (Pothole / Diving Board)','Относительно ровный участок цены сменяется локальным глубоким провалом и последующим восстановлением к исходной области.', 'Для Pothole использовалась дневная шкала; для Diving Board исследовалась недельная. Проверьте фоновый рост до рисунка.', 'Следите за устойчивым возвращением из провала в базовую область, а не просто за первой растущей свечой.', 'Разворот без исходного плоского участка не идентичен описываемой структуре; смешение таймфреймов некорректно.', 'Ориентир — предыдущая горизонтальная база, провал определяет риск.', 'pothole'),
 'multipeak':('Многократные вершины со всплеском','Несколько пиков у похожего уровня и заключительный более высокий шпиль, за которым следует риск снижения.', 'Отметьте минимум три сопоставимые вершины и последнюю более высокую; отделите от обычного тройного верха.', 'Снижение ниже минимума всей группы вершин является подтверждением, верхний выход противоречит сценарию.', 'Не назначайте четвёртую вершину «шпилем» задним числом до завершения структуры.', 'Высота от максимума до нижней границы даёт сценарный масштаб, но не статистическую вероятность.', 'multipeak'),
 'setup':('Формализованные торговые системы','Правила скрининга, входа и выхода, потенциально содержащие несколько индикаторов.', 'Требуются точные окна, формулы OHLC, таймфрейм и правила исполнения.', 'Отдельное выполнение всех правил стратегии; одиночная картинка не доказывает сигнал.', 'Оптимизированные настройки и исторические тесты легко подгоняются, особенно на малой выборке.', 'Backtest с out-of-sample, издержками и ограничениями риска.', None),
})

RESEARCH_WORDS=['book reviews','book value','best buy','best chart','candlestick patterns','price mountain','mountain, price','ten bagger','10 bagger','three trading','3 trading','performance','rank','quizzes','slider quizzes','small patterns','trading mistakes','trading tips','tips','patterns, overview','patterns, daily','event patterns','busted patterns','pattern pairs','market bottoms','finding market bottoms','nature of bottoms','the nature','corrective phase','basic motive','elliott waves','double bottoms, overview','double tops, overview','adam and eve patterns','support','resistance','divergence','averaging down','asset protection','12 month moving average']
RISK_WORDS=['stop','exit','money management','averaging down','asset protection','three trading mistakes','3 trading mistakes']
EVENT_WORDS=['surprise','same-store','fda','upgrades','downgrades','dutch auction','stock rating','earnings flag','flags, earnings']
SMALL_WORDS=['2-close','2-dance','2-did','2-tall','2-step','3-bar','3dc','3l-r','fakey','hook reversal','inside day','outside day','one day reversal','open-close reversal','closing price reversal','pivot point reversal','key reversal','turn-key','wide ranging','weekly reversal','weekly reversals','nr4','nr7','narrow range','failure swing','shark-32','gap2h']

def family_of(raw:str):
 n=raw.lower()
 if any(x in n for x in EVENT_WORDS): return 'event'
 if any(x in n for x in RISK_WORDS): return 'risk'
 if any(x in n for x in RESEARCH_WORDS): return 'research'
 if 'dead-cat' in n: return 'deadcat'
 if n=='2b':return 'two_b'
 if n in ['adam white setup','the cpsetup']:return 'setup'
 if 'cat\'s ear' in n:return 'cats_ears'
 if n in ['diving board','pothole']:return 'pothole'
 if '3-peaks and spike' in n or 'three peaks and spike' in n or n=='multi-peaks':return 'multipeak'
 if 'bump-and-run' in n:return 'bump_run'
 if 'cloud bank' in n:return 'cloud_bank'
 if n in ['roof','roof, inverted','inverted roof']:return 'roof'
 if 'three peaks and domed house' in n or 'domed house and three peaks' in n or '3 peaks and domed house' in n:return 'lindsay'
 if 'three falling peak' in n or '3 falling peaks' in n or 'three rising valley' in n or '3 rising valleys' in n:return 'steps'
 if n=='bottoms, finding market':return 'research'
 if any(x in n for x in SMALL_WORDS):return 'bars'
 if 'volume' in n:return 'volume'
 if 'gap' in n:return 'gaps'
 if 'island' in n:return 'islands'
 if any(x in n for x in ['bat,','bat','butterfly','crab,','crab','gartley','ab=cd']):return 'harmonics'
 if any(x in n for x in ['wave','zigzag','flat (3-3-5)','flat, expanded','flat, running','leading diagonal','ending diagonal','truncation','motive phase','running flat','running triangle','abc correction','corrective phase']):return 'waves'
 if 'head-and-shoulders' in n:return 'head_shoulders'
 if 'triangle' in n:
  if 'reverse symmetrical' in n or 'broadening' in n: return 'broadening'
  return 'triangles'
 if 'broadening' in n:return 'broadening'
 if 'wedge' in n:return 'wedges'
 if 'double' in n or n in ['big m','big w','ugly double bottoms']:return 'double'
 if 'triple' in n:return 'triple'
 if 'cup' in n:return 'cup'
 if 'rounding' in n:return 'rounding'
 if 'diamond' in n:return 'diamond'
 if 'pennant' in n:return 'pennants'
 if 'flag' in n or 'flat base' in n:return 'flags'
 if 'rectangle' in n:return 'rectangles'
 if any(x in n for x in ['scallop']):return 'scallops'
 if any(x in n for x in ['pipe','horn']):return 'pipes_horns'
 if any(x in n for x in ['v-bottom','v top','v-top','v pivot','pivot, v','carl v','vertical run']):return 'vturn'
 if any(x in n for x in ['measured move','measure','price mirror']):return 'measured'
 if any(x in n for x in ['trendline','channel','trend change','trend compression','trend','partial decline','partial rise','spike','tails','pullback','throwback','minor highs','mirror','knots']):return 'trend'
 if any(x in n for x in ['roof','mountain','pothole','three peaks','3 peaks','3-peaks','cloud bank','cat\'s ear','diving board']):return 'misc'
 return 'misc'

def norm(s):
 s=unicodedata.normalize('NFKC',s).strip().lower()
 s=re.sub(r'\([^)]*\)\s*','',s) if s.startswith('(three-') or s.startswith('(two-') else s
 s=s.strip(' .');s=re.sub(r'\s+',' ',s)
 return s

def variation(name,fam):
 n=name.lower()
 out=[]
 if any(x in n for x in ['bullish','bottom','uptrend','ascending','upside','up breakout','move up']):out.append('В названии обозначена бычья/восходящая ориентация; проверяйте направление фактического пробоя, а не предполагайте его.')
 if any(x in n for x in ['bearish','top','downtrend','descending','downside','move down']):out.append('В названии обозначена медвежья/нисходящая ориентация; фактическая динамика может её опровергнуть.')
 if 'busted' in n:out.append('Busted — первоначальный пробой оказался неустойчивым, затем цена пересекла противоположный уровень; нужен контроль двух последовательных событий.')
 if 'inverted' in n or 'reverse' in n:out.append('Инверсия означает зеркальную ориентацию эталонной геометрии; не путайте её с противоположным последующим пробоем.')
 if 'monthly' in n or 'weekly' in n:out.append('Используйте строго соответствующий календарный масштаб; нельзя смешивать недельные и дневные свечи.')
 if 'adam' in n or 'eve' in n:out.append('Adam — узкие остроконечные экстремумы; Eve — относительно широкие округлые. Смешанные случаи бывают неоднозначны.')
 if 'elliott' in n:out.append('Это волновая интерпретация, она не тождественна стандартному определению одноимённой геометрической модели.')
 if 'event' == fam:out.append('Событийный тип зависит от timestamp новости и состава выборки, а не только формы графика.')
 if 'harmonics'==fam:out.append('Соотношения Фибоначчи нельзя подгонять после знания движения; правила должны быть сформулированы до теста.')
 if 'bars'==fam:out.append('Для конкретного авторского short-pattern нужна явная формула по OHLC; категория не заменяет точное условие.')
 return ' '.join(out) or 'Вариант определяется спецификацией первоисточника; не подменять форму похожими фигурами.'

def slug(s):
 s=s.lower().replace('&',' and ').replace('=',' eq ').replace("'",'')
 s=re.sub(r'[^a-z0-9]+','-',s).strip('-')
 return s[:90]

def build():
 raw=[];section=''
 for s in (SKILL/'data/index_names.txt').read_text(encoding='utf-8').splitlines():
  s=s.strip()
  if not s:continue
  if s.startswith('[') and s.endswith(']'): section=s[1:-1];continue
  raw.append({'name':s,'section':section})
 unique={}; repeated=[]
 for rec in raw:
  key=norm(rec['name'])
  if key in unique:
   unique[key]['seen_in_sections'].append(rec['section']); repeated.append(rec)
   continue
  title=rec['name'];f=family_of(title); meta=FAMILIES[f];s=slug(title)
  if s in {r['id'] for r in unique.values()}: s+='-'+hashlib.sha256(title.encode()).hexdigest()[:6]
  detail=VERIFIED.get(title.lower())
  kind='study' if f=='research' else 'method' if f in ('risk','setup') else 'event' if f=='event' else 'pattern'
  status='family_level' if f not in ('misc','research','risk') else 'requires_source_review' if f=='misc' else 'context_only'
  unique[key]={'id':s,'name':title,'family':f,'category':kind,'index_section':rec['section'], 'seen_in_sections':[rec['section']],
    'source_index_url':INDEX,'verified_detail_url':'https://www.thepatternsite.com/'+detail if detail else None,
    'description_ru':meta[1], 'identification_ru':meta[2], 'confirmation_ru':meta[3], 'failure_ru':meta[4],
    'measurement_ru':meta[5], 'variant_note_ru':variation(title,f),
    'confidence':'reference_verified' if detail else status,
    'example':'assets/charts/'+s+'.svg' if kind in ('pattern','event') and meta[6] else None,
    'example_kind':'original_schematic_not_market_data' if kind in ('pattern','event') and meta[6] else None,
    'automatic_detection_implemented':False}
 records=sorted(unique.values(),key=lambda x:x['name'].lower());ids={r['id'] for r in records}
 assert len(ids)==len(records)
 (SKILL/'data/catalog.json').write_text(json.dumps({'schema_version':'1.0','source':INDEX,'source_visual_index':VISUAL,'limitations':['Index names are transcribed from search-indexed page sections; original HTML and per-entry links could not be exhaustively audited in this environment.','All descriptions and diagrams are original educational syntheses; original website images and complete text are not included.','Family-level interpretation is not a verified page-specific rule; confidence tracks that distinction.','Pattern catalog coverage is not detector implementation coverage.'], 'counts':{'index_rows':len(raw),'unique_normalized_entries':len(records),'exact_normalized_repeated_rows':len(repeated),'with_verified_detail_url':sum(bool(r['verified_detail_url']) for r in records),'with_illustration':sum(bool(r['example']) for r in records)},'records':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (SKILL/'data/families.json').write_text(json.dumps({k:dict(zip(['title_ru','summary_ru','identification_ru','confirmation_ru','failure_ru','measurement_ru','illustration'],v)) for k,v in FAMILIES.items()},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 output=['# Alphabetical catalog (curated index transcription)','',f'Index: {INDEX}',f'Unique normalized entries: {len(records)}; original rows: {len(raw)}; verified individual links: {sum(bool(r["verified_detail_url"]) for r in records)}.','', '> Short names are not the original long-form page descriptions. For methodology and exact coverage status see [SOURCE_AUDIT](../../../docs/SOURCE_AUDIT.md).','']
 for c in sorted(set(r['index_section'] for r in records)):
  output.append(f'## {c}')
  for r in records:
   if r['index_section']==c:
    note=f' [verified page]({r["verified_detail_url"]})' if r['verified_detail_url'] else ''
    output.append(f'- **{r["name"]}** — {FAMILIES[r["family"]][0]} ({r["confidence"]}){note}')
  output.append('')
 (SKILL/'references/INDEX.md').write_text('\n'.join(output),encoding='utf-8')
 # For an agent, retrieval should be selective rather than loading a 200KB catalog into prompt.
 for f,m in FAMILIES.items():
  entries=[r for r in records if r['family']==f]
  lines=[f'# {m[0]}','',f'**Раздел:** `{f}` · **Index entries:** {len(entries)}','', '## Описание',m[1],'','## Распознавание',m[2],'','## Подтверждение',m[3],'','## Ошибки, отмена и двусмысленности',m[4],'','## Оценка амплитуды',m[5],'','## Представители', '']
  lines += [f'- [{r["name"]}](../data/catalog.json): `{r["id"]}`' for r in entries]
  lines += ['','**Происхождение:** оригинальное методическое резюме по таксономии ThePatternSite; точные авторские определения и статистику сверять по ссылке в конкретной записи.']
  (SKILL/'references'/f'{f}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
 print(json.dumps({'raw':len(raw),'unique':len(records),'families':len(FAMILIES),'schematic':sum(bool(r['example']) for r in records),'verified':sum(bool(r['verified_detail_url']) for r in records)}))
if __name__=='__main__':build()
