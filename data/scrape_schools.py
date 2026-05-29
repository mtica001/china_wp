#!/usr/bin/env python3
"""
Scrape nisshinkyo.org school detail pages and output schools.json
Only extracts objective factual data (copyright-safe).
"""

import json
import time
import re
import sys
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

BASE_URL = "https://www.nisshinkyo.org/search/college.php?id="
OUTPUT = "/Users/mervyn/Claude_Web/data/schools.json"

SCHOOL_IDS = [
    {"id": "179", "name": "文化外国語専門学校", "location": "東京都渋谷区"},
    {"id": "71", "name": "水野外語学院", "location": "千葉県市川市"},
    {"id": "35", "name": "国際情報ビジネス専門学校", "location": "栃木県宇都宮市"},
    {"id": "463", "name": "浜松日本語学院", "location": "静岡県浜松市中区"},
    {"id": "509", "name": "はぴねす外語学院", "location": "愛媛県新居浜市"},
    {"id": "48", "name": "与野学院日本語学校", "location": "埼玉県さいたま市大宮区"},
    {"id": "260", "name": "富山国際学院", "location": "富山県富山市"},
    {"id": "59", "name": "中央情報専門学校", "location": "埼玉県新座市"},
    {"id": "279", "name": "国際ことば学院日本語学校", "location": "静岡県静岡市駿河区"},
    {"id": "178", "name": "青山スクールオブジャパニーズ", "location": "東京都渋谷区"},
    {"id": "121", "name": "ミッドリーム日本語学校", "location": "東京都新宿区"},
    {"id": "498", "name": "富士山日本語学校", "location": "静岡県富士市"},
    {"id": "106", "name": "東京外語専門学校", "location": "東京都新宿区"},
    {"id": "54", "name": "山手日本語学校", "location": "埼玉県川越市"},
    {"id": "278", "name": "静岡インターナショナルスクール", "location": "静岡県静岡市葵区"},
    {"id": "89", "name": "ＹＭＣＡ東京日本語学校", "location": "東京都千代田区"},
    {"id": "508", "name": "行知学園日本語学校", "location": "東京都新宿区"},
    {"id": "448", "name": "熊本YMCA学院日本語科", "location": "熊本県熊本市中央区"},
    {"id": "150", "name": "専門学校東京国際ビジネスカレッジ日本語科", "location": "東京都台東区"},
    {"id": "127", "name": "新宿平和日本語学校", "location": "東京都新宿区"},
    {"id": "194", "name": "学校法人サンシャイン学園東京福祉保育専門学校", "location": "東京都豊島区"},
    {"id": "83", "name": "明友日本語学院", "location": "千葉県柏市"},
    {"id": "262", "name": "専門学校アリス学園", "location": "石川県金沢市"},
    {"id": "76", "name": "日本国際工科専門学校日本語科", "location": "千葉県松戸市"},
    {"id": "288", "name": "名古屋福徳日本語学院", "location": "愛知県名古屋市中区"},
    {"id": "296", "name": "ECC日本語学院名古屋校", "location": "愛知県名古屋市中区"},
    {"id": "393", "name": "岡山外語学院", "location": "岡山県岡山市北区"},
    {"id": "392", "name": "長船日本語学院", "location": "岡山県岡山市北区"},
    {"id": "305", "name": "コウブンインターナショナル", "location": "愛知県新城市"},
    {"id": "307", "name": "四日市日本語学校", "location": "三重県四日市市"},
    {"id": "502", "name": "異文化間コミュニケーションセンター附属日本語学校", "location": "沖縄県宜野湾市"},
    {"id": "224", "name": "ISIランゲージスクール大阪校", "location": "大阪府大阪市中央区"},
    {"id": "214", "name": "国書日本語学校", "location": "東京都板橋区"},
    {"id": "97", "name": "青山国際教育学院", "location": "東京都港区"},
    {"id": "228", "name": "東洋言語学院", "location": "東京都江戸川区"},
    {"id": "343", "name": "清風情報工科学院日本語科", "location": "大阪府大阪市阿倍野区"},
    {"id": "364", "name": "国際語学学院", "location": "兵庫県神戸市長田区"},
    {"id": "351", "name": "日中語学専門学院", "location": "大阪府大阪市北区"},
    {"id": "166", "name": "ウエストコースト語学院", "location": "東京都大田区"},
    {"id": "276", "name": "スバル学院本巣校", "location": "岐阜県本巣市"},
    {"id": "456", "name": "日亜外語学院", "location": "沖縄県那覇市"},
    {"id": "47", "name": "埼玉日本語学校", "location": "埼玉県さいたま市大宮区"},
    {"id": "341", "name": "アジアハウス附属海風日本語学舎", "location": "大阪府大阪市生野区"},
    {"id": "333", "name": "エール学園日本語教育学科", "location": "大阪府大阪市浪速区"},
    {"id": "202", "name": "亜細亜友之会外語学院", "location": "東京都北区"},
    {"id": "325", "name": "J国際学院", "location": "大阪府大阪市西区"},
    {"id": "404", "name": "専門学校さくら国際言語学院", "location": "山口県下関市"},
    {"id": "282", "name": "A.C.C.国際交流学園", "location": "静岡県富士宮市"},
    {"id": "462", "name": "ホツマインターナショナルスクール東京校", "location": "東京都新宿区"},
    {"id": "511", "name": "湘南日本語学園浜松校", "location": "静岡県浜松市西区"},
    {"id": "388", "name": "和歌山YMCA国際福祉専門学校日本語科", "location": "和歌山県和歌山市"},
    {"id": "301", "name": "YAMASA言語文化学院", "location": "愛知県岡崎市"},
    {"id": "298", "name": "名古屋国際日本語学校", "location": "愛知県名古屋市昭和区"},
    {"id": "372", "name": "神戸東洋日本語学院", "location": "兵庫県神戸市中央区"},
    {"id": "286", "name": "名古屋SKY日本語学校", "location": "愛知県名古屋市中区"},
    {"id": "405", "name": "専門学校さくら国際言語教育学院", "location": "山口県萩市"},
    {"id": "516", "name": "SANWA外国語学院", "location": "大阪府大阪市平野区"},
    {"id": "207", "name": "ジェット日本語学校", "location": "東京都北区"},
    {"id": "319", "name": "京都励学国際学院", "location": "京都府京都市伏見区"},
    {"id": "128", "name": "日本学生支援機構東京日本語教育センター", "location": "東京都新宿区"},
    {"id": "125", "name": "エリート日本語学校", "location": "東京都新宿区"},
    {"id": "310", "name": "公益財団法人京都日本語教育センター京都日本語学校", "location": "京都府京都市上京区"},
    {"id": "327", "name": "日本学生支援機構大阪日本語教育センター", "location": "大阪府大阪市天王寺区"},
    {"id": "246", "name": "飛鳥学院", "location": "神奈川県横浜市中区"},
    {"id": "144", "name": "公益財団法人 アジア学生文化協会", "location": "東京都文京区"},
    {"id": "88", "name": "九段日本文化研究所日本語学院", "location": "東京都千代田区"},
    {"id": "176", "name": "東京中央日本語学院", "location": "東京都新宿区"},
    {"id": "206", "name": "中央工学校附属日本語学校", "location": "東京都北区"},
    {"id": "123", "name": "サム教育学院", "location": "東京都新宿区"},
    {"id": "402", "name": "専門学校広島国際ビジネスカレッジ", "location": "広島県福山市"},
    {"id": "317", "name": "京都民際日本語学校", "location": "京都府京都市右京区"},
    {"id": "495", "name": "大阪日本語アカデミー", "location": "大阪府大阪市平野区"},
    {"id": "406", "name": "徳山総合ビジネス専門学校", "location": "山口県周南市"},
    {"id": "102", "name": "東京国際日本語学院", "location": "東京都新宿区"},
    {"id": "455", "name": "国際言語文化センター附属日本語学校", "location": "沖縄県那覇市"},
    {"id": "277", "name": "静岡日本語教育センター", "location": "静岡県静岡市葵区"},
    {"id": "518", "name": "相模国際学院", "location": "神奈川県相模原市"},
    {"id": "116", "name": "ヨシダ日本語学院", "location": "東京都新宿区"},
    {"id": "33", "name": "日本語学校つくばスマイル", "location": "茨城県取手市"},
    {"id": "167", "name": "東京教育専門学院・多摩川校", "location": "東京都大田区"},
    {"id": "438", "name": "さくら日本語学院", "location": "福岡県新宮町"},
    {"id": "284", "name": "名古屋経営会計専門学校日本語科", "location": "愛知県名古屋市"},
    {"id": "466", "name": "倉敷外語学院", "location": "岡山県倉敷市"},
    {"id": "555", "name": "日本東京国際学院", "location": "東京都新宿区"},
    {"id": "285", "name": "外語学院アドバンスアカデミー", "location": "愛知県名古屋市東区"},
    {"id": "297", "name": "ＡＲＭＳ日本語学校", "location": "愛知県名古屋市中区"},
    {"id": "44", "name": "NIPPON語学院", "location": "群馬県前橋市"},
    {"id": "326", "name": "クローバー学院", "location": "大阪府大阪市西区"},
    {"id": "94", "name": "UJS Language Institute", "location": "東京都港区"},
    {"id": "237", "name": "早稲田言語学院", "location": "東京都新宿区"},
    {"id": "371", "name": "コミュニカ学院", "location": "兵庫県神戸市"},
    {"id": "533", "name": "ＡＳＡＨＩ文化学院", "location": "愛知県名古屋市"},
    {"id": "330", "name": "大阪YMCA学院", "location": "大阪府大阪市天王寺区"},
    {"id": "34", "name": "セントメリー日本語学院", "location": "栃木県宇都宮市"},
    {"id": "507", "name": "ＫＩＪ語学院東京校", "location": "東京都文京区"},
    {"id": "141", "name": "早稲田外語専門学校", "location": "東京都新宿区"},
    {"id": "291", "name": "ノースリバー日本語スクール", "location": "愛知県名古屋市中村区"},
    {"id": "164", "name": "エヴァグリーンランゲージスクール", "location": "東京都目黒区"},
    {"id": "324", "name": "大阪ＹＭＣＡ国際専門学校", "location": "大阪府大阪市西区"},
    {"id": "103", "name": "新宿御苑学院", "location": "東京都新宿区"},
    {"id": "131", "name": "東京ワールド日本語学校", "location": "東京都新宿区"},
    {"id": "536", "name": "ＴＬＳ袋井", "location": "静岡県袋井市"},
    {"id": "243", "name": "学校法人石川学園横浜デザイン学院", "location": "神奈川県横浜市西区"},
]

REGION_MAP = {
    "北海道": "北海道・東北", "青森県": "北海道・東北", "岩手県": "北海道・東北",
    "宮城県": "北海道・東北", "秋田県": "北海道・東北", "山形県": "北海道・東北",
    "福島県": "北海道・東北",
    "茨城県": "関東", "栃木県": "関東", "群馬県": "関東", "埼玉県": "関東",
    "千葉県": "関東", "東京都": "関東", "神奈川県": "関東",
    "新潟県": "中部", "富山県": "中部", "石川県": "中部", "福井県": "中部",
    "山梨県": "中部", "長野県": "中部", "岐阜県": "中部", "静岡県": "中部",
    "愛知県": "中部",
    "三重県": "近畿", "滋賀県": "近畿", "京都府": "近畿", "大阪府": "近畿",
    "兵庫県": "近畿", "奈良県": "近畿", "和歌山県": "近畿",
    "鳥取県": "中国・四国", "島根県": "中国・四国", "岡山県": "中国・四国",
    "広島県": "中国・四国", "山口県": "中国・四国", "徳島県": "中国・四国",
    "香川県": "中国・四国", "愛媛県": "中国・四国", "高知県": "中国・四国",
    "福岡県": "九州・沖縄", "佐賀県": "九州・沖縄", "長崎県": "九州・沖縄",
    "熊本県": "九州・沖縄", "大分県": "九州・沖縄", "宮崎県": "九州・沖縄",
    "鹿児島県": "九州・沖縄", "沖縄県": "九州・沖縄",
}


def fetch_page(school_id):
    url = BASE_URL + school_id
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def cell_text(el):
    return re.sub(r'\s+', ' ', el.get_text()).strip()


def extract_number(text):
    if not text:
        return None
    m = re.search(r'([\d,]+)', text.replace('，', ','))
    return int(m.group(1).replace(',', '')) if m else None


def find_marked_value(soup, marker):
    """Find value after ■marker in any cell, stopping at the next ■."""
    for td in soup.find_all(['td', 'th']):
        t = cell_text(td)
        if marker in t:
            after = re.split(re.escape(marker), t, maxsplit=1)[-1].strip()
            # Stop at next ■ marker
            after = re.split(r'■', after)[0].strip()
            if after:
                return after
            nxt = td.find_next_sibling('td')
            if nxt:
                return cell_text(nxt)
    return ""


def parse_school(html, school_id, name_hint, location_hint):
    soup = BeautifulSoup(html, 'html.parser')

    pref_match = re.match(r'^(.+?(?:都|道|府|県))', location_hint)
    prefecture = pref_match.group(1) if pref_match else location_hint
    # Normalize bare 京都 → 京都府
    if prefecture == '京都':
        prefecture = '京都府'

    data = {
        "id": school_id,
        "name": name_hint,
        "city": location_hint,
        "prefecture": prefecture,
        "region": REGION_MAP.get(prefecture, "その他"),
        "nisshinkyo_url": f"https://www.nisshinkyo.org/search/college.php?id={school_id}",
    }

    # --- Basic contact info from ■-marked cells ---
    addr_raw = find_marked_value(soup, "■所在地")
    # Strip postal code prefix if present
    addr_raw = re.sub(r'^\d{3}-\d{4}\s*', '', addr_raw)
    data["address"] = addr_raw or location_hint

    data["phone"] = find_marked_value(soup, "■電話番号")
    data["fax"] = find_marked_value(soup, "■FAX番号")
    data["nearest_station"] = find_marked_value(soup, "■最寄駅からの道順")

    # Website: find ■URL cell
    url_val = find_marked_value(soup, "■URL")
    if not url_val:
        for a in soup.find_all('a', href=re.compile(r'^http')):
            h = a.get('href', '')
            if 'nisshinkyo' not in h and 'google' not in h:
                url_val = h
                break
    data["website"] = url_val

    # Email
    data["email"] = find_marked_value(soup, "■E-Mail") or find_marked_value(soup, "■メール")

    # --- Org info ---
    data["operator"] = find_marked_value(soup, "■設置者名")
    data["operator_type"] = find_marked_value(soup, "■設置者種別")
    data["principal"] = find_marked_value(soup, "■校長名")
    data["board_chair"] = find_marked_value(soup, "■代表者名")
    data["founded"] = find_marked_value(soup, "■日本語教育開始年月日")
    data["certification_period"] = find_marked_value(soup, "■認定期間")

    # Teachers: "26 名（うち専任：15 名）"
    teachers_raw = find_marked_value(soup, "■教員数")
    data["total_teachers"] = extract_number(teachers_raw)
    ft_match = re.search(r'専任[：:]\s*([\d]+)', teachers_raw)
    data["full_time_teachers"] = int(ft_match.group(1)) if ft_match else None

    # Capacity & enrollment
    cap_raw = find_marked_value(soup, "■収容定員")
    data["capacity"] = extract_number(cap_raw)
    enroll_raw = find_marked_value(soup, "■現員")
    data["current_enrollment"] = extract_number(enroll_raw)

    # Admission
    data["admission_requirement"] = find_marked_value(soup, "■入学資格")
    data["selection_method"] = find_marked_value(soup, "■入学選抜方法")

    # Accommodation: look for 寮 in any cell
    dorm_raw = find_marked_value(soup, "■学生寮") or find_marked_value(soup, "■寮") or find_marked_value(soup, "■宿舎")
    data["has_accommodation"] = bool(dorm_raw and dorm_raw not in ["なし", "無", "×", ""])
    fee_m = re.search(r'([\d,]+)\s*円', dorm_raw)
    data["accommodation_fee"] = int(fee_m.group(1).replace(',', '')) if fee_m else None

    # --- Course table ---
    # Row 0 (th): 認定コース | 目的 | 修業期間 | 授業時数 | 授業週数 | 入学時期(月) | 納付金(5-colspan)
    # Row 1 (th): 選考料 | 入学金 | 授業料 | その他 | 合計
    # Row 2+ (td, 11 cells): コース名 | 目的 | 修業期間 | 時数 | 週数 | 入学月 | 選考料 | 入学金 | 授業料 | その他 | 合計
    courses = []
    for table in soup.find_all('table'):
        all_text = cell_text(table)
        if '修業期間' not in all_text:
            continue
        rows = table.find_all('tr')
        # Data rows: td rows with 11 cells where first cell is non-empty course name
        for row in rows[2:]:
            cells = [cell_text(td) for td in row.find_all('td')]
            if len(cells) < 10 or not cells[0]:
                continue
            # Index mapping: 0=name,1=purpose,2=duration,3=hours,4=weeks,5=start_month,6=fee_exam,7=fee_enroll,8=tuition,9=other,10=total
            total = extract_number(cells[10]) if len(cells) > 10 else extract_number(cells[-1])
            if total and total < 50000:
                total = None  # not a realistic total, skip
            courses.append({
                "name": cells[0],
                "purpose": cells[1] if len(cells) > 1 else "",
                "duration": cells[2] if len(cells) > 2 else "",
                "hours": extract_number(cells[3]) if len(cells) > 3 else None,
                "weeks": extract_number(cells[4]) if len(cells) > 4 else None,
                "start_month": cells[5] if len(cells) > 5 else "",
                "fee_exam": extract_number(cells[6]) if len(cells) > 6 else None,
                "fee_enroll": extract_number(cells[7]) if len(cells) > 7 else None,
                "tuition": extract_number(cells[8]) if len(cells) > 8 else None,
                "fee_other": extract_number(cells[9]) if len(cells) > 9 else None,
                "total": total,
            })
        if courses:
            break

    data["courses"] = courses

    durations = sorted(set(c["duration"] for c in courses if c["duration"]))
    start_months_raw = sorted(set(c["start_month"] for c in courses if c["start_month"]))
    totals = [c["total"] for c in courses if c["total"]]

    data["course_durations"] = durations
    data["start_months"] = start_months_raw
    data["tuition_min"] = min(totals) if totals else None
    data["tuition_max"] = max(totals) if totals else None

    # --- Nationalities table ---
    # Pattern: each cell is "国名 数字" like "中国 39"
    nationalities = []
    for table in soup.find_all('table'):
        cells_text = [cell_text(td) for td in table.find_all('td')]
        # Detect nationality table by checking if first cell matches "X 数字" and contains "中国" or "韓国"
        nation_cells = []
        for ct in cells_text:
            m = re.match(r'^(.+?)\s+(\d+)$', ct)
            if m and m.group(1) not in ('受験者数', '認定者数', '合計', '大学院', '大学', '短期大学'):
                nation_cells.append((m.group(1), int(m.group(2))))
        # Valid nationality table has 合計 as one of the entries or has "中国"
        has_china = any(n[0] in ('中国', '中国大陸') for n in nation_cells)
        if has_china and len(nation_cells) >= 3:
            # Exclude "合計" row
            nationalities = [
                {"country": n, "count": c}
                for n, c in nation_cells
                if n not in ('合計', 'その他') and c > 0
            ]
            nationalities.sort(key=lambda x: -x["count"])
            break

    data["nationalities"] = nationalities[:10]

    # --- JLPT table ---
    # Structure: header row [N1, N2, N3, N4, N5, 計], then 受験者数 row, then 認定者数 row
    jlpt = {}
    for table in soup.find_all('table'):
        rows = table.find_all('tr')
        if len(rows) < 2:
            continue
        header_cells = [cell_text(c) for c in rows[0].find_all(['th', 'td'])]
        if 'N1' in header_cells and 'N2' in header_cells:
            level_indices = {cell: i for i, cell in enumerate(header_cells) if re.match(r'^N[1-5]$', cell)}
            examined_row = None
            passed_row = None
            for row in rows[1:]:
                cells = [cell_text(c) for c in row.find_all(['th', 'td'])]
                label = cells[0] if cells else ''
                if '受験' in label:
                    examined_row = cells
                elif '認定' in label or '合格' in label:
                    passed_row = cells
            if examined_row:
                for level, idx in level_indices.items():
                    jlpt[level] = {
                        "examined": extract_number(examined_row[idx]) if idx < len(examined_row) else None,
                        "passed": extract_number(passed_row[idx]) if passed_row and idx < len(passed_row) else None,
                    }
            break

    data["jlpt"] = jlpt

    # --- Graduate placement table ---
    # Header: 大学院 | 大学 | 短期大学 | 高等専門学校 | 専修学校(専門課程) | 各種学校 | その他
    placement = {}
    for table in soup.find_all('table'):
        rows = table.find_all('tr')
        if len(rows) < 2:
            continue
        header_cells = [cell_text(c) for c in rows[0].find_all(['th', 'td'])]
        if '大学院' in header_cells and '専修学校' in ' '.join(header_cells):
            data_cells = [cell_text(c) for c in rows[1].find_all(['th', 'td'])]
            for i, label in enumerate(header_cells):
                if label and i < len(data_cells):
                    n = extract_number(data_cells[i])
                    if n is not None:
                        placement[label] = n
            break

    data["placement"] = placement

    return data


def main():
    results = []
    total = len(SCHOOL_IDS)
    for i, entry in enumerate(SCHOOL_IDS):
        sid = entry["id"]
        name = entry["name"]
        loc = entry["location"]
        print(f"[{i+1}/{total}] id={sid} {name}", flush=True)
        try:
            html = fetch_page(sid)
            school = parse_school(html, sid, name, loc)
            results.append(school)
        except Exception as e:
            print(f"  ERROR: {e}", flush=True)
            pref_m = re.match(r'^(.+?(?:都|道|府|県))', loc)
            prefecture = pref_m.group(1) if pref_m else loc
            if prefecture == '京都':
                prefecture = '京都府'
            results.append({
                "id": sid, "name": name, "city": loc,
                "prefecture": prefecture,
                "region": REGION_MAP.get(prefecture, "その他"),
                "error": str(e),
                "nisshinkyo_url": f"https://www.nisshinkyo.org/search/college.php?id={sid}"
            })
        time.sleep(0.4)

    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nDone. {len(results)} schools → {OUTPUT}")


if __name__ == "__main__":
    main()
