"""Дособираем конфигурации — секция DNA не сматчилась."""
import json
import re
import html
from pathlib import Path

ROOT = Path("/home/z/my-project")
template_path = ROOT / "download" / "polymath-hardware.html"
template = template_path.read_text(encoding="utf-8")

# Проверим — если есть DNA section, заменим её на configs_section
# Шаблон: <section ...id="dna"...>...</section>
dna_match = re.search(r'<section[^>]*id="dna"[^>]*>.*?</section>', template, re.DOTALL)
print(f"DNA section found: {bool(dna_match)}")

# Конфиги — те же что были
data = json.loads((ROOT / "scripts" / "hardware_calc.json").read_text(encoding="utf-8"))

configs_section = '''
    <!-- ═══ 3 КОНФИГУРАЦИИ ═══ -->
    <section class="section container" id="configs" aria-label="3 конфигурации железа">
      <div class="container">
        <div class="sec-head reveal">
          <p class="kicker">polymath · hardware configs</p>
          <h2>Три конфигурации — от Tower до Rack Beast</h2>
          <p>Ресурсы не ограничены. Цель — локальность, быстродействие, полная автономия. Выбрал три варианта: <b>Tower Pro</b> для домашней/офисной сборки с водянкой (4× 5090, $30K), <b>Rack Beast</b> для 235B MoE без компромиссов (8× 5090, $52K), <b>Mac Studio Ultra</b> для тех кто не терпит шум (192GB unified, $11K, 270W).</p>
        </div>
        
        <div class="config-grid reveal">
          
          <article class="config-card tower reveal">
            <h3>Tower Pro — рабочая станция</h3>
            <p class="tagline">4× RTX 5090 / 128GB VRAM / Threadripper 7995WX / 512GB DDR5 ECC</p>
            <p class="use-case"><b>Сценарий A+B</b> (70B + видео + все агенты). Домашняя/офисная сборка. Водянка на 4 GPU, тишина 38 дБ. Помещается под столом. Меняет игру: 128GB VRAM в одной коробке за $30K — это уровень 1.5× H100, но в 4× дешевле.</p>
            
            <div class="config-stats">
              <div class="config-stat"><div class="label">Цена</div><div class="value">$30,249</div></div>
              <div class="config-stat"><div class="label">VRAM</div><div class="value">128 GB</div></div>
              <div class="config-stat"><div class="label">RAM</div><div class="value">512 GB</div></div>
              <div class="config-stat"><div class="label">CPU</div><div class="value">96C</div></div>
              <div class="config-stat"><div class="label">Потребление</div><div class="value">2.4 kW</div></div>
              <div class="config-stat"><div class="label">Шум</div><div class="value">38 дБ</div></div>
            </div>
            
            <p style="font-size:13px;line-height:1.6;margin-top:1rem;"><b>Что потянет параллельно:</b></p>
            <ul style="font-size:12px;line-height:1.7;padding-left:1.2rem;">
              <li>LLM 70B Q4 (СУД) — 48GB ✓</li>
              <li>LLM 8B Q8 ×3 (агенты) — 24GB ✓</li>
              <li>SDXL/Flux dev — 16GB ✓</li>
              <li>Whisper + F5-TTS + embeddings — 12GB ✓</li>
              <li>KV cache — 20GB ✓</li>
              <li><b>Запас: 8GB</b> — Wan 2.5 видео по очереди</li>
            </ul>
            <p style="font-size:13px;margin-top:1rem;padding:0.5rem;background:rgba(74,222,128,0.08);border-radius:6px;"><b>Вердикт:</b> оптимально для 95% задач Polymat. Видео — по очереди.</p>
          </article>
          
          <article class="config-card rack reveal">
            <h3>Rack Beast — серверный монстр</h3>
            <p class="tagline">8× RTX 5090 / 256GB VRAM / EPYC 9755 128C / 1.15TB DDR5 ECC</p>
            <p class="use-case"><b>Сценарий C</b> (235B MoE + 70B + видео + всё параллельно). 4U rackmount, нужен 19" шкаф или гараж. Шум 65 дБ — отдельная комната. 256GB VRAM позволяет запустить Qwen3-235B-A22B Q4 + одновременно 70B для судьи + видео + голос.</p>
            
            <div class="config-stats">
              <div class="config-stat"><div class="label">Цена</div><div class="value">$51,700</div></div>
              <div class="config-stat"><div class="label">VRAM</div><div class="value">256 GB</div></div>
              <div class="config-stat"><div class="label">RAM</div><div class="value">1.15 TB</div></div>
              <div class="config-stat"><div class="label">CPU</div><div class="value">128C</div></div>
              <div class="config-stat"><div class="label">Потребление</div><div class="value">3.8 kW</div></div>
              <div class="config-stat"><div class="label">Шум</div><div class="value">65 дБ</div></div>
            </div>
            
            <p style="font-size:13px;line-height:1.6;margin-top:1rem;"><b>Что потянет параллельно:</b></p>
            <ul style="font-size:12px;line-height:1.7;padding-left:1.2rem;">
              <li>LLM 235B MoE Q4 — 130GB ✓</li>
              <li>LLM 70B Q4 (СУД) — 48GB ✓</li>
              <li>SDXL/Flux — 16GB ✓</li>
              <li>Wan 2.5 видео — 40GB ✓</li>
              <li>Whisper + F5-TTS + embeddings — 12GB ✓</li>
              <li><b>Запас: 10GB</b> — всё в параллель</li>
            </ul>
            <p style="font-size:13px;margin-top:1rem;padding:0.5rem;background:rgba(239,68,68,0.08);border-radius:6px;"><b>Вердикт:</b> единственный вариант для 235B MoE. Нужна отдельная комната (3.8kW тепла).</p>
          </article>
          
          <article class="config-card mac reveal">
            <h3>Mac Studio M3 Ultra</h3>
            <p class="tagline">Apple M3 Ultra 32C / 192GB unified / 80-core GPU / 270W</p>
            <p class="use-case"><b>Сценарий A</b> (70B + картинки + голос, без видео). Тихая альтернатива: 18 дБ, 270W (в 9× меньше Tower), помещается на столе. Минус: нет CUDA, vLLM не работает, только Metal/MLX. Скорость в 2-3× ниже RTX 5090.</p>
            
            <div class="config-stats">
              <div class="config-stat"><div class="label">Цена</div><div class="value">$10,649</div></div>
              <div class="config-stat"><div class="label">Unified</div><div class="value">192 GB</div></div>
              <div class="config-stat"><div class="label">GPU</div><div class="value">80 core</div></div>
              <div class="config-stat"><div class="label">CPU</div><div class="value">32C</div></div>
              <div class="config-stat"><div class="label">Потребление</div><div class="value">270 W</div></div>
              <div class="config-stat"><div class="label">Шум</div><div class="value">18 дБ</div></div>
            </div>
            
            <p style="font-size:13px;line-height:1.6;margin-top:1rem;"><b>Что потянет параллельно:</b></p>
            <ul style="font-size:12px;line-height:1.7;padding-left:1.2rem;">
              <li>LLM 70B Q4 (через MLX) — 48GB ✓</li>
              <li>LLM 8B Q8 ×3 — 24GB ✓ (медленнее CUDA)</li>
              <li>SDXL/Flux (DiffusersBee) — 16GB ✓</li>
              <li>Whisper.cpp + F5-TTS — 12GB ✓</li>
              <li><b>Запас: 92GB</b> — много места, скорость ниже</li>
              <li>235B MoE — только с offload, очень медленно</li>
            </ul>
            <p style="font-size:13px;margin-top:1rem;padding:0.5rem;background:rgba(168,85,247,0.08);border-radius:6px;"><b>Вердикт:</b> для тех кто ценит тишину. Не для 235B, не для видео. Лучшая начальная точка.</p>
          </article>
          
        </div>
        
        <p class="stack-note reveal"><span class="k">правило:</span> 1× RTX 5090 (32GB, $2200) по VRAM эквивалентен 1.3× Mac Studio (192GB unified, но shared). По скорости CUDA в 2-3× быстрее Metal. Tower Pro — оптимум цена/производительность для Polymat.</p>
      </div>
    </section>
'''

if dna_match:
    template = template[:dna_match.start()] + configs_section + template[dna_match.end():]
    print("✓ DNA секция заменена на configs_section")
else:
    print("✗ DNA секция не найдена!")

template_path.write_text(template, encoding="utf-8")
print(f"Размер: {template_path.stat().st_size:,} байт")
print(f"config-card tower: {'config-card tower' in template}")
print(f"config-card rack: {'config-card rack' in template}")
print(f"config-card mac: {'config-card mac' in template}")
