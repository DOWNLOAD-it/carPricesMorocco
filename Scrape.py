import csv
import time
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

COLUMNS = [
    "Title",
    "Secteur",
    "Ville",
    "Price",
    "Année-Modèle",
    "Boite de vitesses",
    "Type de carburant",
    "Kilométrage",
    "Marque",
    "Modèle",
    "Nombre de portes",
    "Origine",
    "Première main",
    "Puissance fiscale",
    "État",
]


def get_text_or_none(soup, selector, index=0):
    elements = soup.select(selector)  # Select all matching elements
    if 0 <= index < len(elements):  # Check if index is within valid range
        return elements[index].get_text(strip=True)  # Extract text with strip
    return None  # Return None if no matching element at the given index


def get_value_by_label(soup, target_label):
    label_spans = soup.select("span.sc-1x0vz2r-0.bXFCIH")  # all label spans

    for label_span in label_spans:
        if label_span.get_text(strip=True) == target_label:
            # find previous sibling that contains the value
            value_span = label_span.find_previous_sibling(
                "span", class_="sc-1x0vz2r-0 fjZBup"
            )
            if value_span:
                return value_span.get_text(strip=True)
    return None  # if not found


def clean_price(raw):
    if not raw:
        return None
    raw = raw.replace(" ", "").replace("\u202f", "").replace("DH", "")
    try:
        return int(raw)
    except Exception:
        return None


def clean_puissance(raw):
    if not raw:
        return None
    raw = raw.replace(" ", "").replace("\u202f", "").replace("CV", "")
    try:
        return int(raw)
    except Exception:
        return None


def clean_kilometrage(price_range_str):
    if not isinstance(price_range_str, str) or "-" not in price_range_str:
        return None
    try:
        parts = price_range_str.split("-")
        min_price = int(parts[0].replace(" ", "").strip())
        max_price = int(parts[1].replace(" ", "").strip())
        avg_price = (min_price + max_price) // 2
        return avg_price
    except Exception:
        return None


def split_location(location_str):
    if not isinstance(location_str, str) or "," not in location_str:
        return None, None
    try:
        parts = [part.strip() for part in location_str.split(",")]
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return None, None
    except Exception:
        return None, None


def scrape_listing(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=8)
        if r.status_code != 200:
            print(f"⚠️ {url} status {r.status_code}")
            return None
    except Exception as e:
        print(f"Erreur requête {url} : {e}")
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Step 1: extract all raw values
    values = [
        get_text_or_none(soup, "h1", 0),
        get_text_or_none(soup, ".sc-1x0vz2r-0.iKguVF", 0),
        get_text_or_none(soup, ".sc-1x0vz2r-0.iKguVF", 0),
        get_text_or_none(soup, ".sc-1x0vz2r-0.lnEFFR.sc-1veij0r-10.jdRkSM", 0),
        get_value_by_label(soup, COLUMNS[4]),
        get_value_by_label(soup, COLUMNS[5]),
        get_value_by_label(soup, COLUMNS[6]),
        get_value_by_label(soup, COLUMNS[7]),
        get_value_by_label(soup, COLUMNS[8]),
        get_value_by_label(soup, COLUMNS[9]),
        get_value_by_label(soup, COLUMNS[10]),
        get_value_by_label(soup, COLUMNS[11]),
        get_value_by_label(soup, COLUMNS[12]),
        get_value_by_label(soup, COLUMNS[13]),
        get_value_by_label(soup, COLUMNS[14]),
    ]

    # Step 2: Further processing (e.g. cleaning price)
    values[3] = clean_price(values[3])
    values[13] = clean_puissance(values[13])
    values[7] = clean_kilometrage(values[7])
    values[1], values[2] = split_location(values[1])

    print(f"Scraped: {values[0] or url.split('/')[-1]}")
    return values


def get_listing_links_from_page(page_url):
    try:
        r = requests.get(page_url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"Page {page_url} indisponible ({r.status_code})")
            return []
    except Exception as e:
        print(f"Erreur page {page_url}: {e}")
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    # Find all <a> with BOTH classes
    links = []
    for a in soup.find_all("a", class_="sc-1jge648-0 jZXrfL"):
        href = a.get("href")
        if href:
            # Normalize relative links
            if href.startswith("/"):
                href = "https://www.avito.ma" + href
            links.append(href)
    # Also: if Avito sometimes uses only the first class, you can try:
    # links = [a['href'] for a in soup.select('a.sc-1jge648-0.jZXrfL') if a.get('href')]
    return list(set(links))  # remove possible duplicates


def main(start_page=1, nb_pages=100, output_csv="avito_data.csv"):
    for i in range(start_page, start_page + nb_pages):
        page_url = f"https://www.avito.ma/fr/maroc/voitures?o={i}"
        print(f"==> Page {i}")
        links = get_listing_links_from_page(page_url)
        print(f"   {len(links)} annonces trouvées")
        rows_to_append = []
        for link in links:
            row = scrape_listing(link)
            if row:
                rows_to_append.append(row)
        # Append to CSV if any data scraped
        if rows_to_append:
            # Use append mode, write header only if file does not exist
            try:
                with open(output_csv, "x", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(COLUMNS)
            except FileExistsError:
                pass
            with open(output_csv, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows_to_append)
        time.sleep(1)
    print(f"✅ scraping completed, data appended to {output_csv}")


if __name__ == "__main__":
    main(start_page=801, nb_pages=100, output_csv="avito_data.csv")
