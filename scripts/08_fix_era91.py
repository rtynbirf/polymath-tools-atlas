"""Дофикс era91 (UNIX) — прямая замена содержимого."""
from pathlib import Path
import re

P = Path("/home/z/my-project/download/polymath-catalog.html")
html = P.read_text(encoding="utf-8")

# Прямая замена блока era91
old_era91 = '''<div class="era91">
                <h1>ἰδιώτης</h1>
                <p class="meta">https://en.wiktionary.org/wiki/ἰδιώτης — запись эпохи: V век до н. э.</p>
                <hr>
                <p>Идиот — гражданин, не принимающий участия в общественных, государственных, общих делах; человек частный. Брани в слове нет: это вопрос гражданства, а не ума.</p>
                <p>Происходит от ἴδιος «свой, частный». Статус записи — [ТЕКСТ]: живая цитата с датой, начало цепочки. Выберите, куда идти дальше.</p>
                <ul>
                  <li><a href="#top" onclick="return false">Даль, 1863—1866 [ШУМ]</a></li>
                  <li><a href="#top" onclick="return false">Ожегов—Шведова, 1992 [ТЕКСТ]</a></li>
                  <li><a href="#top" onclick="return false">Закон цепочек</a></li>
                  <li><a href="#top" onclick="return false">О проекте ГОЛОГРАММА</a></li>
                </ul>
                <hr>
                <p class="fin">© V в. до н. э., ἰдиóτovис · греческий первоисточник · статус [ТЕКСТ]</p>
              </div>'''

# Находим любой вариант era91
new_era91 = '''<div class="era91">
                <h1>UNIX &amp; CLI</h1>
                <p class="meta">https://www.bell-labs.com — UNIX epoch: 1969–1973</p>
                <hr>
                <p>UNIX — операционная система Bell Labs (Ken Thompson, Dennis Ritchie, 1969). Философия: «делай одну вещь и делай хорошо». Каждый инструмент — фильтр, читающий stdin и пишущий в stdout. cat, grep, sed, awk, ls, cd — словарь CLI, который не устарел за 55 лет.</p>
                <p>Статус записи — [ТЕКСТ]: живая цитата с датой, начало цепочки. Каждый современный AI-CLI-агент — наследник UNIX-философии: одна задача, текстовый ввод/вывод, композитность через пайпы. Выберите, куда идти дальше.</p>
                <ul>
                  <li><a href="#top" onclick="return false">Web 2.0, 2005 [ШУМ]</a></li>
                  <li><a href="#top" onclick="return false">LLM-эра, 2022 [ТЕКСТ]</a></li>
                  <li><a href="#top" onclick="return false">Закон цепочек</a></li>
                  <li><a href="#top" onclick="return false">О проекте ПОЛИМАТ</a></li>
                </ul>
                <hr>
                <p class="fin">© 1969–1973, Bell Labs · UNIX · статус [ТЕКСТ]</p>
              </div>'''

# Также обновляем era-desc для era91
old_desc = '<b>V в. до н.э. · ἰδιóτovис · [ТЕКСТ]</b><p>Так слово выглядело до всякого словаря: ἰδιóτovис — гражданин вне дел, человек частный, от ἴδιος «свой». Синие подчёркнутые ссылки, ноль графики, ноль брани. Цепочка слова начинается здесь — с текста, у которого есть дата. Это и есть статус [ТЕКСТ]: живая цитата, а не пересказ умника, и ни один автор не заменит её собой.</p>'
new_desc = '<b>1969–1973 · UNIX · [ТЕКСТ]</b><p>Так выглядело начало цепочки: UNIX и его утилиты — cat, grep, sed, awk. Философия «одна программа — одна задача» оказалась длиннее всех остальных эпох вместе взятых. Современные AI-CLI-агенты (Aider, Claude Code, OpenHands) — те же UNIX-утилиты, только с LLM внутри. Цепочка начинается здесь — с текста, у которого есть дата.</p>'

# Имя вкладки
html = html.replace(
    '<label class="tm-tab" for="e1991" role="tab" aria-selected="true" tabindex="-1"><b>V до н.э.</b><em>ἰδιώτης</em></label>',
    '<label class="tm-tab" for="e1991" role="tab" aria-selected="true" tabindex="-1"><b>1969</b><em>UNIX</em></label>'
)
html = html.replace(
    '<label class="tm-tab" for="e1996" role="tab" aria-selected="false" tabindex="-1"><b>1863</b><em>Шум Даля</em></label>',
    '<label class="tm-tab" for="e1996" role="tab" aria-selected="false" tabindex="-1"><b>2005</b><em>Web 2.0</em></label>'
)
html = html.replace(
    '<label class="tm-tab" for="e2005" role="tab" aria-selected="false" tabindex="-1"><b>1987</b><em>Корпус</em></label>',
    '<label class="tm-tab" for="e2005" role="tab" aria-selected="false" tabindex="-1"><b>2022</b><em>ChatGPT</em></label>'
)
html = html.replace(
    '<label class="tm-tab" for="e2013" role="tab" aria-selected="false" tabindex="-1"><b>1992</b><em>Бранное</em></label>',
    '<label class="tm-tab" for="e2013" role="tab" aria-selected="false" tabindex="-1"><b>2026</b><em>Полимат</em></label>'
)

# Заменяем содержимое era91 через regex (включая unicode)
pattern = re.compile(r'<div class="era91">.*?</div>\s*</div>\s*</div>\s*</div>\s*<div class="era-desc"><b>V в\. до н\.э\..*?</p></div>', re.DOTALL)
match = pattern.search(html)
if match:
    replacement = new_era91 + '''
            </div>
          </div>
        </div>
        <div class="era-desc">' + new_desc + '</div>'''
    html = html[:match.start()] + replacement + html[match.end():]
    print("✓ era91 заменена")
else:
    print("✗ era91 НЕ найдена, пробуем альтернативный паттерн")
    # Альтернатива: ищем от '<div class="era91">' до '<b>V в. до н.э.'
    alt_pattern = re.compile(r'<div class="era91">.*?<b>V в\. до н\.э\..*?</p></div>', re.DOTALL)
    m2 = alt_pattern.search(html)
    if m2:
        # Найдём границы блока era91
        start_idx = html.find('<div class="era91">')
        end_idx = html.find('<div class="era-desc"><b>V в. до н.э.')
        if start_idx >= 0 and end_idx >= 0:
            # Найдём конец </div> после era-desc
            block_end = html.find('</div>', end_idx + len('<div class="era-desc"><b>V в. до н.э.'))
            block_end = html.find('</div>', block_end + 6)  # ещё один </div>
            # Заменяем весь блок
            old_block = html[start_idx:block_end + 6]
            new_block = new_era91 + '\n            </div>\n          </div>\n        </div>\n        <div class="era-desc">' + new_desc + '</div>'
            html = html[:start_idx] + new_block + html[block_end + 6:]
            print("✓ era91 заменена (alt)")
        else:
            print(f"  start_idx={start_idx}, end_idx={end_idx}")
    else:
        print("✗ Альтернативный паттерн тоже не сработал")

P.write_text(html, encoding="utf-8")
print(f"\nРазмер: {P.stat().st_size:,} байт")
print(f"UNIX & CLI: {html.count('UNIX &')} раз")
print(f"ἰδιώτης: {html.count('ἰδιώτης')} раз (должно быть 0 или 1 в text)")
