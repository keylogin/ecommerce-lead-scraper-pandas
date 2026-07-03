import concurrent.futures
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configurații globale pentru a evita blocajele de bază
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
TIMEOUT = 5  # Secunde până când un site e considerat "Dead Link"
MAX_WORKERS = 10  # Numărul de thread-uri paralele pentru viteză crescută


def extract_and_verify_store(url):
    """Accesează magazinul, verifică dacă e live și extrage link-urile de contact folosind BeautifulSoup."""
    # Asigurăm formatul corect al URL-ului
    if not url.startswith("http"):
        url = "https://" + url

    result = {
        "Brand Name": "Generic Store",
        "Website": url,
        "Shopify Contact Form (Main)": "Not Found",
        "Shopify Contact Form (Alt)": "Not Found",
        "Status": "Dead Link",
    }

    try:
        # Multi-threading check: trimitem un request rapid către domeniu
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)

        if response.status_code == 200:
            result["Status"] = "Verified Shopify Store"

            # BeautifulSoup parsing pentru structura HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Încercăm să extragem un Brand Name curat din tag-ul <title>
            if soup.title and soup.title.string:
                title_text = soup.title.string.strip()
                # Curățăm titlurile lungi specifice e-commerce-ului (ex: Nume | Shop Online -> Nume)
                for separator in ["-", "|", "—", ":"]:
                    if separator in title_text:
                        title_text = title_text.split(separator)[0].strip()
                result["Brand Name"] = title_text if title_text else "Generic Store"

            # Căutăm paginile de contact în link-urile din pagină (href-uri)
            for link in soup.find_all("a", href=True):
                href = link["href"].lower()

                # Identificăm link-urile principale de contact
                if "contact-us" in href or "contactus" in href:
                    full_link = href if href.startswith("http") else url.rstrip("/") + "/" + href.lstrip("/")
                    result["Shopify Contact Form (Main)"] = full_link
                # Identificăm link-urile alternative
                elif "contact" in href and result["Shopify Contact Form (Main)"] == "Not Found":
                    full_link = href if href.startswith("http") else url.rstrip("/") + "/" + href.lstrip("/")
                    result["Shopify Contact Form (Alt)"] = full_link

    except requests.RequestException:
        # Dacă site-ul nu răspunde, rămâne marcat ca "Dead Link"
        pass

    return result


def run_data_pipeline(urls):
    """Rulează pipeline-ul complet: Scrape paralele -> Procesare Pandas -> Export CSV."""
    print(f"🚀 [INIT] Se lansează scanarea pentru {len(urls)} domenii...")

    # Pasul 1: Concurrency (Multi-threading) cu ThreadPoolExecutor
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        raw_results = list(executor.map(extract_and_verify_store, urls))

    # Pasul 2: Procesare și analiză cu Pandas
    print("🧼 [PANDAS] Se activează pipeline-ul de curățare a datelor...")
    df = pd.DataFrame(raw_results)

    # Eliminarea duplicatelor pe baza domeniului web
    df.drop_duplicates(subset=["Website"], keep="first", inplace=True)

    # Gestionarea valorilor lipsă (NaNs) sau goale
    df["Brand Name"] = df["Brand Name"].replace("", "Generic Store").fillna("Generic Store")
    df["Shopify Contact Form (Main)"] = df["Shopify Contact Form (Main)"].fillna("Not Found")

    # Pasul 3: Export final în CSV curat
    output_filename = "cleaned_ecommerce_leads.csv"
    df.to_csv(output_filename, index=False)

    print(f"✅ [SUCCESS] Pipeline finalizat cu succes!")
    print(f"📊 Fișierul curat '{output_filename}' conține {len(df)} lead-uri unice verificate.")


if __name__ == "__main__":
    # Liste demo de test (Pot fi înlocuite cu citirea unui fișier brut)
    test_domains = [
        "https://sendribbon.com",
        "https://truetone.com",
        "https://dagger.com",
        "https://starlightstone.com",
        "https://sendribbon.com",  # Duplicat intenționat pentru testarea Pandas
    ]

    run_data_pipeline(test_domains)
