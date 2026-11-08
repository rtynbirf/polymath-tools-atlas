#!/usr/bin/env python3
# Волна ×3 · W3-E · «Патруль-Мертвецы» (предложение polymath-tools-atlas#1).
# Воскресный обход: URL берутся из файла данных атласа (не из отрендеренного README),
# чтобы слои ГОЛОГРАММЫ и закон цепочек не искажались рендером. Зона записи патруля —
# только liveness-поля у существующих записей + отчёты deadpatrol/; строки каталога
# не удаляются и не переименовываются. Проба: HEAD → GET, таймаут 15 с, 2 повтора
# (параметры lychee из предложения; сама проба — детерминированный python-stdlib).
import argparse, datetime, glob, json, os, re, sys, time
import urllib.error, urllib.request

UA = ("polymath-tools-atlas-deadpatrol/1.0 "
      "(+https://github.com/rtynbirf/polymath-tools-atlas; воскресный патруль ссылок)")
URL_KEYS = ("url", "source_url", "source", "link", "homepage")


def probe(url, timeout, retries):
    last_ms = 0
    for attempt in range(retries + 1):
        for method in ("HEAD", "GET"):
            t0 = time.perf_counter()
            try:
                req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return int(r.status), int((time.perf_counter() - t0) * 1000)
            except urllib.error.HTTPError as e:
                last_ms = int((time.perf_counter() - t0) * 1000)
                if method == "HEAD":
                    break
                if e.code < 500:
                    return e.code, last_ms
            except Exception:
                last_ms = int((time.perf_counter() - t0) * 1000)
                if method == "GET" and attempt == retries:
                    return "error", last_ms
    return "error", last_ms


def collect(node, out, path="$"):
    """Рекурсивный обход JSON: словарь с http-ссылкой в одном из URL_KEYS — запись атласа."""
    if isinstance(node, dict):
        urls = [(k, v) for k, v in node.items()
                if isinstance(v, str) and v.startswith(("http://", "https://"))
                and k.lower() in URL_KEYS]
        if urls:
            kind = "cloud" if any(k.lower() == "url" for k, _ in urls) else "local-source"
            out.append({"node": node, "path": path, "kind": kind,
                        "key": urls[0][0], "url": urls[0][1],
                        "layer": str(node.get("layer") or node.get("type") or "—")})
        for k, v in node.items():
            collect(v, out, "%s.%s" % (path, k))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            collect(v, out, "%s[%d]" % (path, i))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog", default="catalog.json")
    ap.add_argument("--report-dir", default="deadpatrol")
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--retries", type=int, default=2)
    args = ap.parse_args()

    today = datetime.date.today()
    iso_year, week, _ = today.isocalendar()
    tag = "%04d-W%02d" % (iso_year, week)
    raw = open(args.catalog, encoding="utf-8").read()
    ind = 2 if not raw.lstrip().startswith("[") else 2
    m = re.search(r"\n(\s+)", raw)
    if m:
        ind = len(m.group(1).expandtabs(4))
    catalog = json.loads(raw)
    entries = []
    collect(catalog, entries)
    before_count, before_urls = len(entries), sorted(e["url"] for e in entries)

    state_path = os.path.join(args.report_dir, "state.json")
    state = json.load(open(state_path, encoding="utf-8")) if os.path.exists(state_path) else {}
    uniq = sorted(set(e["url"] for e in entries))
    cloud = sorted(set(e["url"] for e in entries if e["kind"] == "cloud"))
    print("Патруль-Мертвецы %s: записей с URL %d, уникальных URL %d (cloud %d)" %
          (tag, len(entries), len(uniq), len(cloud)))
    codes, dead = {}, []
    for n, url in enumerate(uniq):
        code, ms = probe(url, args.timeout, args.retries)
        codes[url] = code
        ok = isinstance(code, int) and code < 400
        if not ok:
            dead.append((url, code))
            if url not in state:
                state[url] = {"first_seen_dead": tag}
            state[url]["last_code"] = str(code)
            state[url]["last_seen"] = today.isoformat()
        elif url in state:
            state[url]["last_code"] = str(code)
            state[url]["last_seen"] = today.isoformat()
        if (n + 1) % 25 == 0:
            print("Патруль: %d/%d проб…" % (n + 1, len(uniq)))

    # Зона записи в файле данных: только liveness-поля (закон цепочек расширяется, не ломается).
    dead_urls = set(u for u, _ in dead)
    for e in entries:
        e["node"]["liveness"] = "dead" if e["url"] in dead_urls else (
            "alive" if isinstance(codes[e["url"]], int) else "unknown")
        e["node"]["liveness_checked_at"] = today.isoformat()
    after = []
    collect(json.loads(json.dumps(catalog)), after)
    assert len(after) == before_count and sorted(e["url"] for e in after) == before_urls, \
        "НАРУШЕНИЕ ЗОНЫ ЗАПИСИ: строки каталога удалены или переименованы"

    os.makedirs(args.report_dir, exist_ok=True)
    with open(args.catalog, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=ind)
        f.write("\n")
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
        f.write("\n")

    rep = os.path.join(args.report_dir, "%s.md" % tag)
    with open(rep, "w", encoding="utf-8") as f:
        f.write("# Мертвецы недели %s\n\n" % tag)
        f.write("- Дата пробы: %s · проверено: %d из %d (cloud: все %d)\n" %
                (today.isoformat(), len(uniq), len(entries), len(cloud)))
        f.write("- Мёртвых: %d · полей liveness обновлено: %d\n\n" % (len(dead), len(entries)))
        f.write("| URL | код | слой | first_seen_dead |\n|---|---|---|---|\n")
        for url, code in dead:
            f.write("| %s | %s | %s | %s |\n" % (url, code,
                    next((e["layer"] for e in entries if e["url"] == url), "—"),
                    state.get(url, {}).get("first_seen_dead", tag)))
        if not dead:
            f.write("(мёртвых ссылок на этой неделе не найдено)\n")

    # Статус-лента (последние 5 недель): счётчики сходятся с файлом данных по построению.
    weeks = sorted(glob.glob(os.path.join(args.report_dir, "20*-W*.md")))[-5:]
    with open(os.path.join(args.report_dir, "FEED.md"), "w", encoding="utf-8") as f:
        f.write("# Статус-лента патруля (последние 5 недель)\n\n")
        f.write("Источники: отчёты deadpatrol/ и поля liveness в catalog.json — "
                "число dead в ленте = число записей с liveness=dead.\n\n")
        for w in weeks:
            txt = open(w, encoding="utf-8").read()
            pv = re.search(r"проверено: (\d+) из (\d+)", txt)
            dv = re.search(r"Мёртвых: (\d+)", txt)
            if pv and dv:
                f.write("- %s — проверено %s/%s, мёртвых %s\n" %
                        (os.path.basename(w)[:-3], pv.group(1), pv.group(2), dv.group(1)))
    print("Патруль-Мертвецы %s: проверено %d/%d (cloud %d), мёртвых %d → %s" %
          (tag, len(uniq), len(entries), len(cloud), len(dead), rep))


if __name__ == "__main__":
    main()
