"""WWE.com Career Highlights vs real_title_catalog 대조."""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.request

from kayfabe.app.services.real_title_catalog import individual_title_acquisitions

WWE_SLUGS: dict[str, str] = {
    "AJ Lee": "aj-lee",
    "AJ Styles": "aj-styles",
    "Alexa Bliss": "alexa-bliss",
    "Andrade": "andrade",
    "Angelo Dawkins": "angelo-dawkins",
    "Asuka": "asuka",
    "Austin Theory": "austin-theory",
    "Axiom": "axiom",
    "Bayley": "bayley",
    "Becky Lynch": "becky-lynch",
    "Bo Dallas": "bo-dallas",
    "Brie Bella": "brie-bella",
    "Brock Lesnar": "brock-lesnar",
    "Bron Breakker": "bron-breakker",
    "CM Punk": "cm-punk",
    "Charlotte Flair": "charlotte-flair",
    "Cody Rhodes": "cody-rhodes",
    "Dexter Lumis": "dexter-lumis",
    "Dominik Mysterio": "dominik-mysterio",
    "Dragon Lee": "dragon-lee",
    "Drew McIntyre": "drew-mcintyre",
    "Ethan Page": "ethan-page",
    "Finn Bálor": "finn-balor",
    "Gunther": "gunther",
    "IYO SKY": "iyo-sky",
    "JD McDonagh": "jd-mcdonagh",
    "Jacy Jayne": "jacy-jayne",
    "Jey Uso": "jey-uso",
    "Jimmy Uso": "jimmy-uso",
    "Joe Gacy": "joe-gacy",
    "John Cena": "john-cena",
    "Johnny Gargano": "johnny-gargano",
    "Karrion Kross": "karrion-kross",
    "LA Knight": "la-knight",
    "Lash Legend": "lash-legend",
    "Liv Morgan": "liv-morgan",
    "Logan Paul": "logan-paul",
    "Lyra Valkyria": "lyra-valkyria",
    "Montez Ford": "montez-ford",
    "Myles Borne": "myles-borne",
    "Naomi": "naomi",
    "Nathan Frazer": "nathan-frazer",
    "Nia Jax": "nia-jax",
    "Oba Femi": "oba-femi",
    "Paige": "paige",
    "Penta": "penta",
    "Randy Orton": "randy-orton",
    "Rey Mysterio": "rey-mysterio",
    "Rhea Ripley": "rhea-ripley",
    "Roman Reigns": "roman-reigns",
    "Rusev": "rusev",
    "Sami Zayn": "sami-zayn",
    "Seth Rollins": "seth-rollins",
    "Solo Sikoa": "solo-sikoa",
    "Stephanie Vaquer": "stephanie-vaquer",
    "Tiffany Stratton": "tiffany-stratton",
    "Tommaso Ciampa": "tommaso-ciampa",
    "Tony D'Angelo": "tony-dangelo",
    "Trick Williams": "trick-williams",
    "The Miz": "the-miz",
}

# WWE Career Highlights 라벨 → 카탈로그 belt normalize 키
LABEL_TO_KEY: list[tuple[str, str]] = [
    ("women's intercontinental champion", "women's intercontinental"),
    ("women's united states champion", "women's united states"),
    ("women's world champion", "women's world"),
    ("women's tag team champion", "women's tag"),
    ("wwe women's tag team champion", "women's tag"),
    ("wwe women's champion", "wwe women's"),
    ("raw women's champion", "raw women's"),
    ("smackdown women's champion", "smackdown women's"),
    ("nxt uk women's champion", "nxt uk women's"),
    ("first-ever nxt uk women's champion", "nxt uk women's"),
    ("nxt women's champion", "nxt women's"),
    ("nxt women's north american champion", "nxt women's north american"),
    ("nxt north american champion", "nxt north american"),
    ("nxt tag team champion", "nxt tag"),
    ("undisputed wwe universal champion", "undisputed universal"),
    ("undisputed wwe tag team champion", "undisputed tag"),
    ("world tag team champion", "world tag"),
    ("wwe tag team champion", "wwe tag"),
    ("raw tag team champion", "raw tag"),
    ("smackdown tag team champion", "smackdown tag"),
    ("universal champion", "universal"),
    ("world heavyweight champion", "world heavyweight"),
    ("wwe crown jewel champion", "wwe crown jewel"),
    ("crown jewel champion", "wwe crown jewel"),
    ("wwe champion", "wwe championship"),
    ("undisputed wwe champion", "undisputed wwe"),
    ("intercontinental champion", "intercontinental"),
    ("united states champion", "united states"),
    ("nxt champion", "nxt championship"),
    ("divas champion", "divas"),
    ("wwe divas champion", "divas"),
    ("money in the bank winner", "mitb"),
    ("royal rumble winner", "royal rumble"),
]


def fetch_html(slug: str) -> str:
    url = f"https://www.wwe.com/superstars/{slug}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


_HIGHLIGHT_START = (
    r"(?="
    r"WWE Champion|WWE Women's Champion|WWE Women's Tag Team Champion|WWE Tag Team Champion|"
    r"World Heavyweight Champion|World Tag Team Champion|"
    r"Raw Women's Champion|Raw Tag Team Champion|"
    r"SmackDown Women's Champion|SmackDown Tag Team Champion|"
    r"NXT UK Women's Champion|NXT Women's Champion|NXT Women's Tag Team Champion|"
    r"NXT Champion|NXT Tag Team Champion|NXT North American Champion|"
    r"NXT Women's North American Champion|NXT Cruiserweight Champion|"
    r"Women's World Champion|Women's Tag Team Champion|"
    r"Women's Intercontinental Champion|Women's United States Champion|"
    r"Universal Champion|Intercontinental Champion|United States Champion|"
    r"Undisputed WWE Universal Champion|Undisputed WWE Tag Team Champion|"
    r"Divas Champion|WWE Divas Champion|"
    r"Money in the Bank|Royal Rumble|Crown Jewel Champion|"
    r"First-ever NXT UK Women's Champion|"
    r"\d{4} WWE"
    r")"
)


def parse_career_highlights(page_html: str) -> list[tuple[str, int]]:
    text = re.sub(r"<[^>]+>", " ", page_html)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text)
    m = re.search(r"Career Highlights\s*(.*?)\s*close\s", text, flags=re.I)
    if not m:
        return []
    block = m.group(1)
    titles: list[tuple[str, int]] = []
    for part in re.split(_HIGHLIGHT_START, block, flags=re.I):
        part = part.strip(" ,;")
        if not part or part.lower().startswith("wwe hall of fame"):
            continue
        count = 1
        cm = (
            re.search(r"\(x(\d+)[^)]*\)", part, flags=re.I)
            or re.search(r"\((\d+)x\)", part, flags=re.I)
            or re.search(r"Champion\s*\((\d+)\)\s*$", part, flags=re.I)
        )
        if cm:
            count = int(cm.group(1))
            part = re.sub(r"\(x\d+[^)]*\)|\(\d+x\)|Champion\s*\(\d+\)\s*$", "", part, flags=re.I).strip()
        if re.search(r"\d{4}\s+and\s+\d{4}", part):
            count = max(count, 2)
        # "2024 WWE Women's Crown Jewel Champion" 등 연도 접두 유지
        part = re.sub(r"\band\b.*$", "", part, flags=re.I).strip()
        part = re.sub(r"\bWinner\b.*$", "", part, flags=re.I).strip()
        part = re.sub(r"\b\d{4}\b(?!\s*WWE)", "", part).strip()
        if not part:
            continue
        titles.append((part, count))
    return titles


def label_to_key(label: str) -> str:
    s = label.lower().strip()
    if "women's" in s and "intercontinental" in s:
        return "women's intercontinental"
    if "women's" in s and "united states" in s:
        return "women's united states"
    # 긴(구체적) 패턴을 먼저 매칭해 세부 벨트명 오분류 방지
    for needle, key in sorted(LABEL_TO_KEY, key=lambda item: len(item[0]), reverse=True):
        if needle in s:
            return key
    return s


def count_map(items: list[tuple[str, int]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for label, count in items:
        key = label_to_key(label)
        out[key] = out.get(key, 0) + count
    return out


# Career Highlights에 있으나 챔피언십 획득 이력이 아닌 항목 (대조 제외)
IGNORE_WWE_KEYS = frozenset(
    {
        "royal rumble",
        "royal rumble match",
        "money in the bank",
        "money in the bank ladder match",
        "mitb",
        "king of the ring",
        "24/7",
        "first-ever",
        "wwe hall of fame",
    }
)


def catalog_count_map(reigns: list[tuple[str, str]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for belt, _ in reigns:
        key = label_to_key(belt)
        out[key] = out.get(key, 0) + 1
    return out


def main() -> int:
    catalog = individual_title_acquisitions()
    mismatches: list[dict] = []
    missing_slug: list[str] = []
    ok: list[str] = []

    for name in sorted(catalog):
        slug = WWE_SLUGS.get(name)
        if not slug:
            missing_slug.append(name)
            continue
        try:
            html = fetch_html(slug)
            wwe_titles = parse_career_highlights(html)
        except Exception as exc:  # noqa: BLE001
            mismatches.append({"name": name, "error": str(exc)})
            continue
        if not wwe_titles:
            mismatches.append({"name": name, "slug": slug, "error": "no Career Highlights parsed"})
            continue

        cat_counts = catalog_count_map(catalog[name])
        wwe_counts = count_map(wwe_titles)
        # 파서가 Women's IC를 intercontinental으로 쪼개는 경우 보정
        if "women's intercontinental" in cat_counts and wwe_counts.get("intercontinental"):
            wwe_counts["women's intercontinental"] = wwe_counts.pop("intercontinental")
        if "women's united states" in cat_counts and wwe_counts.get("united states"):
            wwe_counts["women's united states"] = wwe_counts.pop("united states")
        all_keys = set(cat_counts) | set(wwe_counts)
        diff = {
            k: {"catalog": cat_counts.get(k, 0), "wwe": wwe_counts.get(k, 0)}
            for k in sorted(all_keys)
            if cat_counts.get(k, 0) != wwe_counts.get(k, 0)
            and k not in IGNORE_WWE_KEYS
            and not any(k.startswith(p) for p in IGNORE_WWE_KEYS)
        }
        if diff:
            mismatches.append(
                {
                    "name": name,
                    "slug": slug,
                    "catalog_reigns": catalog[name],
                    "wwe_highlights": wwe_titles,
                    "diff": diff,
                }
            )
        else:
            ok.append(name)

    report = {"ok_count": len(ok), "mismatches": mismatches, "missing_slug": missing_slug}
    sys.stdout.buffer.write(json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8"))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
