"""실제 WWE 챔피언십 획득 이력 (WWE.com / 공식 방송 기준, PLE 게임 결과와 무관)."""

from __future__ import annotations

from kayfabe.app.services.competitor_roster import unique_individuals

CATALOG_REVISION = 11

# (belt_name, won_at) — won_at: 실제 획득 이벤트·방송·날짜
# 키는 로스터명(태그팀 포함) — sync 시 개인 링네임으로 펼친다.
REAL_TITLE_ACQUISITIONS: dict[str, list[tuple[str, str]]] = {
    "#DIY": [
        ("NXT Tag Team Championship", "NXT TakeOver: Toronto — November 19, 2016"),
        ("NXT Tag Team Championship", "NXT TakeOver: Chicago II — May 20, 2017"),
        ("NXT Tag Team Championship", "NXT TakeOver: New Orleans — April 7, 2018"),
    ],
    "AJ Lee": [
        ("WWE Divas Championship", "Payback — June 16, 2013"),
        ("WWE Divas Championship", "Raw — June 30, 2014"),
        ("WWE Divas Championship", "Night of Champions — September 21, 2014"),
        ("Women's Intercontinental Championship", "Elimination Chamber — February 28, 2026"),
    ],
    "AJ Styles": [
        ("WWE Championship", "SmackDown Live — September 11, 2016"),
        ("United States Championship", "WrestleMania 33 — April 2, 2017"),
        ("WWE Championship", "Battleground — July 23, 2017"),
        ("Intercontinental Championship", "Extreme Rules — July 15, 2018"),
    ],
    "Alexa Bliss": [
        ("SmackDown Women's Championship", "TLC — December 4, 2016"),
        ("SmackDown Women's Championship", "Money in the Bank — June 18, 2017"),
        ("Raw Women's Championship", "Payback — April 30, 2017"),
        ("Raw Women's Championship", "Raw — August 28, 2017"),
        ("Raw Women's Championship", "Raw — June 17, 2018"),
        ("Women's Tag Team Championship", "Raw — August 5, 2019"),
        ("Women's Tag Team Championship", "Halloween Havoc — October 25, 2020"),
        ("Women's Tag Team Championship", "Raw — July 31, 2022"),
        ("Women's Tag Team Championship", "SummerSlam — August 2, 2025"),
    ],
    "Alexa Bliss & Charlotte Flair": [],
    "Austin Theory": [
        ("United States Championship", "WrestleMania 38 Night 2 — April 3, 2022"),
        ("World Tag Team Championship", "Raw — March 30, 2026"),
    ],
    "Asuka": [
        ("NXT Women's Championship", "NXT TakeOver: Dallas — April 1, 2016"),
        ("Raw Women's Championship", "WrestleMania 34 — April 8, 2018"),
        ("Raw Women's Championship", "Money in the Bank — July 18, 2020"),
        ("Women's Tag Team Championship", "WrestleMania 39 Night 2 — April 2, 2023"),
    ],
    "Bayley": [
        ("NXT Women's Championship", "NXT TakeOver: Respect — October 7, 2015"),
        ("Raw Women's Championship", "Elimination Chamber — March 8, 2020"),
        ("SmackDown Women's Championship", "WrestleMania 36 Night 1 — April 5, 2020"),
    ],
    "Bayley & Lyra Valkyria": [],
    "Becky Lynch": [
        ("SmackDown Women's Championship", "Backlash — September 11, 2016"),
        ("SmackDown Women's Championship", "Hell in a Cell — September 16, 2018"),
        ("Raw Women's Championship", "WrestleMania 35 — April 7, 2019"),
        ("SmackDown Women's Championship", "WrestleMania 35 — April 7, 2019"),
        ("SmackDown Women's Championship", "SummerSlam — August 21, 2021"),
        ("Raw Women's Championship", "SmackDown — October 22, 2021"),
        ("Women's Tag Team Championship", "Raw — February 27, 2023"),
        ("NXT Women's Championship", "Raw — September 12, 2023"),
        ("SmackDown Women's Championship", "Raw — April 22, 2024"),
        ("Women's Tag Team Championship", "WrestleMania 41 Night 1 — April 19, 2025"),
        ("Women's Intercontinental Championship", "Money in the Bank — June 7, 2025"),
        ("Women's Intercontinental Championship", "Raw on Netflix Anniversary Show — January 5, 2026"),
        ("Women's Intercontinental Championship", "WrestleMania 42 Night 1 — April 18, 2026"),
    ],
    "Brock Lesnar": [
        ("WWE Championship", "King of the Ring — June 23, 2002"),
        ("WWE Championship", "WrestleMania XIX — March 30, 2003"),
        ("WWE Championship", "SummerSlam — August 17, 2014"),
        ("WWE Championship", "WrestleMania 31 — March 29, 2015"),
        ("WWE Championship", "Survivor Series — November 20, 2016"),
        ("Universal Championship", "SummerSlam — August 20, 2017"),
        ("Universal Championship", "WrestleMania 34 — April 8, 2018"),
        ("Universal Championship", "Extreme Rules — July 14, 2019"),
        ("WWE Championship", "Crown Jewel — October 31, 2019"),
        ("WWE Championship", "Day 1 — January 1, 2022"),
    ],
    "Bron Breakker": [
        ("NXT Championship", "New Year's Evil — January 4, 2022"),
        ("NXT Championship", "NXT Stand & Deliver — April 2, 2023"),
        ("NXT Tag Team Championship", "NXT — February 13, 2024"),
        ("World Tag Team Championship", "Raw — May 25, 2026"),
    ],
    "CM Punk": [
        ("World Heavyweight Championship", "Money in the Bank — July 17, 2011"),
        ("WWE Championship", "Survivor Series — November 20, 2011"),
        ("WWE Championship", "Royal Rumble — January 27, 2013"),
        ("Intercontinental Championship", "Raw — November 8, 2024"),
        ("World Heavyweight Championship", "Saturday Night's Main Event — December 7, 2024"),
    ],
    "Charlotte Flair": [
        ("NXT Women's Championship", "NXT TakeOver: Charlotte — May 29, 2014"),
        ("WWE Divas Championship", "Night of Champions — September 20, 2015"),
        ("Raw Women's Championship", "WrestleMania 32 — April 3, 2016"),
        ("Raw Women's Championship", "SummerSlam — August 21, 2016"),
        ("Raw Women's Championship", "Hell in a Cell — October 30, 2016"),
        ("Raw Women's Championship", "Roadblock — December 18, 2016"),
        ("SmackDown Women's Championship", "SmackDown — November 14, 2017"),
        ("SmackDown Women's Championship", "SummerSlam — August 19, 2018"),
        ("SmackDown Women's Championship", "SmackDown — March 26, 2019"),
        ("SmackDown Women's Championship", "Money in the Bank — May 19, 2019"),
        ("SmackDown Women's Championship", "Super Show-Down — October 6, 2019"),
        ("NXT Women's Championship", "NXT — March 26, 2020"),
        ("Women's Tag Team Championship", "Raw — December 20, 2020"),
        ("Raw Women's Championship", "Raw — July 18, 2021"),
        ("SmackDown Women's Championship", "SmackDown — October 22, 2021"),
        ("Raw Women's Championship", "SummerSlam — August 21, 2021"),
        ("SmackDown Women's Championship", "SmackDown — December 30, 2022"),
        ("WWE Women's Championship", "WrestleMania 38 Night 2 — April 3, 2022"),
        ("WWE Women's Championship", "WrestleMania 39 Night 2 — April 2, 2023"),
        ("Women's Tag Team Championship", "SummerSlam — August 2, 2025"),
    ],
    "Cody Rhodes": [
        ("Intercontinental Championship", "Night of Champions — June 17, 2013"),
        ("Undisputed WWE Championship", "WrestleMania 40 Night 2 — April 7, 2024"),
    ],
    "Dominik Mysterio": [
        ("NXT North American Championship", "NXT — July 18, 2023"),
        ("WWE Tag Team Championship", "WrestleMania 39 Night 1 — April 1, 2023"),
        ("Intercontinental Championship", "WrestleMania 41 Night 2 — April 20, 2025"),
    ],
    "Dragon Lee": [
        ("NXT North American Championship", "NXT No Mercy — September 30, 2023"),
    ],
    "Drew McIntyre": [
        ("NXT Championship", "NXT TakeOver: Brooklyn III — August 19, 2017"),
        ("WWE Championship", "WrestleMania 36 Night 2 — April 5, 2020"),
        ("WWE Championship", "Money in the Bank — November 22, 2020"),
    ],
    "Finn Bálor": [
        ("NXT Championship", "NXT TakeOver: R Evolution — February 11, 2015"),
        ("Universal Championship", "SummerSlam — August 21, 2016"),
        ("Intercontinental Championship", "WrestleMania 34 — April 8, 2018"),
        ("Undisputed WWE Tag Team Championship", "Payback — September 2, 2023"),
        ("World Tag Team Championship", "Raw — June 24, 2024"),
        ("World Tag Team Championship", "Raw — June 30, 2025"),
    ],
    "Fraxiom": [
        ("NXT Tag Team Championship", "NXT — August 13, 2024"),
    ],
    "Gunther": [
        ("Intercontinental Championship", "WrestleMania 38 Night 1 — April 2, 2022"),
        ("World Heavyweight Championship", "SummerSlam — August 3, 2024"),
        ("World Heavyweight Championship", "Raw — June 9, 2025"),
    ],
    "IYO SKY": [
        ("WWE Women's Championship", "Night of Champions — June 17, 2023"),
        ("Women's Tag Team Championship", "WrestleMania 39 Night 2 — April 2, 2023"),
    ],
    "JD McDonagh": [
        ("World Tag Team Championship", "Raw — June 24, 2024"),
        ("World Tag Team Championship", "Raw — June 30, 2025"),
    ],
    "Jacy Jayne": [
        ("NXT Women's Championship", "NXT — May 27, 2025"),
        ("NXT Women's Championship", "NXT — November 18, 2025"),
    ],
    "Jade Cargill": [],
    "Jey Uso": [
        ("Raw Tag Team Championship", "WrestleMania 34 — April 8, 2018"),
        ("Raw Tag Team Championship", "WrestleMania 35 — April 7, 2019"),
        ("Undisputed WWE Tag Team Championship", "WrestleMania 38 Night 1 — April 2, 2022"),
        ("Undisputed WWE Tag Team Championship", "WrestleMania 39 Night 1 — April 1, 2023"),
        ("Undisputed WWE Tag Team Championship", "WrestleMania 40 Night 1 — April 6, 2024"),
        ("Intercontinental Championship", "Raw — September 23, 2024"),
        ("World Heavyweight Championship", "WrestleMania 41 Night 2 — April 20, 2025"),
    ],
    "John Cena": [
        ("United States Championship", "WrestleMania 20 — March 14, 2004"),
        ("WWE Championship", "WrestleMania 21 — April 3, 2005"),
        ("WWE Championship", "Royal Rumble — January 29, 2006"),
        ("WWE Championship", "WrestleMania 25 — April 5, 2009"),
        ("WWE Championship", "Money in the Bank — July 17, 2013"),
        ("WWE Championship", "Royal Rumble — January 25, 2015"),
        ("WWE Championship", "Royal Rumble — January 29, 2017"),
    ],
    "Johnny Gargano": [
        ("NXT Championship", "NXT TakeOver: Philadelphia — January 27, 2018"),
        ("NXT Championship", "NXT TakeOver: New York — April 4, 2018"),
        ("NXT North American Championship", "NXT TakeOver: New Orleans — April 7, 2018"),
    ],
    "Karrion Kross": [
        ("NXT Championship", "NXT TakeOver: XXX — August 22, 2020"),
        ("NXT Championship", "NXT TakeOver: Stand & Deliver Night 2 — April 8, 2021"),
    ],
    "LA Knight": [
        ("United States Championship", "Crown Jewel — November 4, 2023"),
    ],
    "Liv Morgan": [
        ("Women's World Championship", "Money in the Bank — July 2, 2022"),
        ("Women's Tag Team Championship", "WrestleMania 39 Night 1 — April 1, 2023"),
        ("Women's Tag Team Championship", "Money in the Bank — July 1, 2023"),
        ("Women's Tag Team Championship", "WrestleMania 40 Night 1 — April 6, 2024"),
        ("Women's Tag Team Championship", "Elimination Chamber — March 1, 2025"),
        ("Women's World Championship", "King and Queen of the Ring — May 25, 2024"),
        ("WWE Women's Crown Jewel Championship", "Crown Jewel — November 2, 2024"),
        ("Women's World Championship", "WrestleMania 42 Night 1 — April 18, 2026"),
    ],
    "Logan Paul": [
        ("United States Championship", "Crown Jewel — November 4, 2023"),
    ],
    "Los Americanos": [],
    "Lyra Valkyria": [
        ("NXT Women's Championship", "NXT Halloween Havoc — October 24, 2023"),
        ("Women's Intercontinental Championship", "Raw — January 13, 2025"),
        ("Women's Tag Team Championship", "WrestleMania 41 Night 1 — April 19, 2025"),
    ],
    "Motor City Machine Guns": [
        ("WWE Tag Team Championship", "SmackDown — October 25, 2024"),
    ],
    "Myles Borne": [
        ("NXT North American Championship", "NXT — February 24, 2026"),
    ],
    "Naomi": [
        ("SmackDown Women's Championship", "Elimination Chamber — February 12, 2017"),
    ],
    "Nia Jax & Lash Legend": [
        ("Women's Tag Team Championship", "SmackDown — February 27, 2026"),
    ],
    "Oba Femi": [
        ("NXT Championship", "NXT New Year's Evil — January 7, 2025"),
        ("NXT Championship", "NXT Deadline — December 6, 2025"),
    ],
    "Penta": [
        ("Intercontinental Championship", "Raw — March 2, 2026"),
    ],
    "Randy Orton": [
        ("World Heavyweight Championship", "SummerSlam — August 15, 2004"),
        ("Intercontinental Championship", "Taboo Tuesday — November 9, 2004"),
        ("WWE Championship", "WrestleMania 25 — April 5, 2009"),
        ("World Heavyweight Championship", "Night of Champions — September 15, 2013"),
        ("WWE Championship", "WrestleMania 33 — April 2, 2017"),
        ("WWE Championship", "Hell in a Cell — October 25, 2020"),
    ],
    "Raquel Rodriguez": [],
    "Raquel Rodriguez & Roxanne Perez": [],
    "Rey Mysterio": [
        ("World Heavyweight Championship", "WrestleMania 22 — April 2, 2006"),
        ("Intercontinental Championship", "Judgment Day — May 17, 2009"),
        ("United States Championship", "WrestleMania 34 — April 8, 2018"),
        ("United States Championship", "WrestleMania 38 Night 1 — April 2, 2022"),
    ],
    "Rhea Ripley": [
        ("NXT UK Women's Championship", "NXT UK TakeOver: Blackpool — January 12, 2019"),
        ("NXT Women's Championship", "NXT TakeOver: New York — April 10, 2019"),
        ("WWE Women's Championship", "WrestleMania 37 Night 2 — April 11, 2021"),
        ("Women's Tag Team Championship", "Raw — July 18, 2021"),
        ("WWE Women's Championship", "WrestleMania 39 Night 2 — April 2, 2023"),
        ("Women's World Championship", "WrestleMania 39 Night 2 — April 2, 2023"),
        ("Women's Tag Team Championship", "Raw — January 5, 2025"),
        ("Women's World Championship", "Raw on Netflix — January 6, 2025"),
    ],
    "Roman Reigns": [
        ("WWE Tag Team Championship", "Extreme Rules — October 14, 2013"),
        ("WWE Championship", "Survivor Series — November 22, 2015"),
        ("WWE Championship", "Raw — December 14, 2015"),
        ("United States Championship", "Hell in a Cell — September 25, 2016"),
        ("WWE Championship", "WrestleMania 32 — April 3, 2016"),
        ("Intercontinental Championship", "Raw — November 20, 2017"),
        ("Universal Championship", "WrestleMania 33 — April 2, 2017"),
        ("Universal Championship", "SummerSlam — August 19, 2018"),
        ("WWE Championship", "WrestleMania 38 Night 2 — April 3, 2022"),
        ("World Heavyweight Championship", "WrestleMania 42 Night 2 — April 19, 2026"),
    ],
    "Roman Reigns & Jey Uso": [],
    "Rusev": [
        ("United States Championship", "Night of Champions — September 21, 2014"),
        ("United States Championship", "Raw — November 3, 2014"),
    ],
    "Sami Zayn": [
        ("NXT Championship", "NXT TakeOver: Rival — February 11, 2015"),
        ("Intercontinental Championship", "WrestleMania 34 — April 8, 2018"),
        ("Intercontinental Championship", "WrestleMania 37 Night 1 — April 10, 2021"),
        ("United States Championship", "WrestleMania 38 Night 1 — April 2, 2022"),
        ("Undisputed WWE Tag Team Championship", "WrestleMania 39 Night 1 — April 1, 2023"),
    ],
    "Seth Rollins": [
        ("NXT Championship", "NXT — July 26, 2012"),
        ("Raw Tag Team Championship", "Extreme Rules — May 19, 2013"),
        ("WWE Championship", "WrestleMania 31 — March 29, 2015"),
        ("United States Championship", "SummerSlam — August 23, 2015"),
        ("WWE Championship", "Money in the Bank — June 19, 2016"),
        ("Raw Tag Team Championship", "SummerSlam — August 20, 2017"),
        ("Raw Tag Team Championship", "Raw — December 25, 2017"),
        ("Intercontinental Championship", "WrestleMania 34 — April 8, 2018"),
        ("Intercontinental Championship", "SummerSlam — August 19, 2018"),
        ("Raw Tag Team Championship", "Raw — October 22, 2018"),
        ("Universal Championship", "WrestleMania 35 — April 7, 2019"),
        ("Raw Tag Team Championship", "SummerSlam — August 19, 2019"),
        ("Universal Championship", "SummerSlam — August 11, 2019"),
        ("Raw Tag Team Championship", "Raw — January 20, 2020"),
        ("United States Championship", "Raw — October 10, 2022"),
        ("World Heavyweight Championship", "Night of Champions — July 1, 2023"),
        ("World Heavyweight Championship", "SummerSlam Night 1 — August 2, 2025"),
        ("WWE Crown Jewel Championship", "Crown Jewel — October 11, 2025"),
    ],
    "Solo Sikoa": [
        ("NXT North American Championship", "NXT 2.0 — September 13, 2022"),
        ("United States Championship", "WrestleMania 39 Night 2 — April 2, 2023"),
    ],
    "Stephanie Vaquer": [
        ("NXT Women's Championship", "NXT Roadblock — March 11, 2025"),
        ("Women's World Championship", "Wrestlepalooza — September 20, 2025"),
    ],
    "The Street Profits": [
        ("Raw Tag Team Championship", "WrestleMania 35 — April 7, 2019"),
        ("Raw Tag Team Championship", "SummerSlam — August 11, 2019"),
        ("SmackDown Tag Team Championship", "WrestleMania 38 Night 1 — April 2, 2022"),
    ],
    "The Vanity Project": [
        ("NXT Tag Team Championship", "NXT — February 24, 2026"),
    ],
    "The Wyatt Sicks": [
        ("WWE Tag Team Championship", "Bash in Berlin — August 31, 2024"),
    ],
    "Tiffany Stratton": [
        ("NXT Women's Championship", "NXT Battleground — May 28, 2023"),
        ("WWE Women's Championship", "Saturday Night's Main Event — December 6, 2025"),
    ],
    "Tony D'Angelo": [
        ("NXT Tag Team Championship", "NXT The Great American Bash — July 30, 2023"),
        ("NXT Tag Team Championship", "NXT — November 14, 2023"),
        ("NXT Championship", "NXT Stand & Deliver — April 4, 2026"),
    ],
    "Trick Williams": [
        ("NXT North American Championship", "NXT No Mercy — September 30, 2023"),
        ("NXT Championship", "NXT Stand & Deliver — April 7, 2024"),
    ],
    "Ethan Page": [
        ("NXT Championship", "NXT Heatwave — July 7, 2024"),
    ],
    "Andrade": [
        ("NXT Championship", "NXT TakeOver: Philadelphia — January 26, 2019"),
        ("United States Championship", "WrestleMania 35 — April 7, 2019"),
    ],
    "Andrade & Rey Fénix": [],
    "BirthRight": [],
    "Blake Monroe": [],
    "Bron Breakker & Bronson Reed": [],
    "Danhausen & Minihausen": [],
    "Drew McIntyre & Logan Paul": [],
    "IShowSpeed & The Vision": [],
    "Jacob Fatu": [],
    "Je'Von Evans": [],
    "Joe Hendry": [],
    "Kendal Grey": [],
    "Kiana James": [],
    "LA Knight & The Usos": [],
    "Lola Vice": [],
    "Brie Bella": [
        ("WWE Divas Championship", "Night of Champions — November 20, 2011"),
    ],
    "Paige": [
        ("WWE Divas Championship", "Raw — April 7, 2014"),
    ],
    "Paige & Brie Bella": [],
    "Randy Orton & Jelly Roll": [],
    "Ricky Saints": [],
    "Sinclair, Hank & Tank, EK Prosper, Shiloh Hill": [],
    "Sol Ruca": [
        ("Women's Intercontinental Championship", "Clash in Italy — May 31, 2026"),
    ],
    "Tatum Paxley": [],
    "Jimmy Uso": [
        ("Raw Tag Team Championship", "WrestleMania 34 — April 8, 2018"),
        ("Raw Tag Team Championship", "WrestleMania 35 — April 7, 2019"),
        ("Undisputed WWE Tag Team Championship", "WrestleMania 38 Night 1 — April 2, 2022"),
        ("Undisputed WWE Tag Team Championship", "WrestleMania 39 Night 1 — April 1, 2023"),
        ("Undisputed WWE Tag Team Championship", "WrestleMania 40 Night 1 — April 6, 2024"),
    ],
    "The Miz": [
        ("WWE Championship", "WrestleMania 27 — April 3, 2011"),
        ("WWE Championship", "Money in the Bank — July 17, 2011"),
        ("Intercontinental Championship", "WrestleMania 25 — April 5, 2009"),
        ("Intercontinental Championship", "Extreme Rules — June 4, 2012"),
        ("United States Championship", "WrestleMania 27 — April 3, 2011"),
        ("World Heavyweight Championship", "Survivor Series — November 30, 2024"),
    ],
    "The Miz & Kit Wilson": [],
    "Zaria": [],
}


def individual_title_acquisitions() -> dict[str, list[tuple[str, str]]]:
    """태그팀·스테이블 획득을 멤버 개인 기록으로 합친다."""
    merged: dict[str, list[tuple[str, str]]] = {}
    for competitor, reigns in REAL_TITLE_ACQUISITIONS.items():
        if not reigns:
            continue
        for member in unique_individuals([competitor]):
            bucket = merged.setdefault(member, [])
            for reign in reigns:
                if reign not in bucket:
                    bucket.append(reign)
    return merged
