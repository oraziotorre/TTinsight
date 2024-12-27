import asyncio
import os
import pandas as pd
import re
from playwright.async_api import async_playwright, Page

"""
Questo programma ha il compito di completare le informazioni del dataset a nostra disposizione
"""


async def get_console_logs(page: Page, event_id: str, doc_code: str, n_games: int):
    logs = []

    def handle_console_message(msg):
        # Controlla se il log della console è del tipo [.........]
        if re.match(r'^\[.*\]$', msg.text):
            logs.append(f"{msg.text}")

    # Ascolta gli eventi di log della console
    page.on("console", handle_console_message)

    try:
        # Naviga al sito usando gli identificativi forniti
        url = f"https://worldtabletennis.com/PostMatchCenter?eventId={event_id}&docCode={doc_code}"
        print(f"Navigating to: {url}")
        await page.goto(url)

        # Aspetta che la pagina finisca di caricarsi
        await page.wait_for_load_state("networkidle")

        # Interagisce con i bottoni per ottenere i dati dei game G
        for i in range(2, n_games + 1):  # Itera da G2 a Gn(G1 già è stampato)
            game_label = f"G{i}"
            buttons = page.locator("span.tabHeader", has_text=game_label)
            count = await buttons.count()

            if count == 1:
                # Se c'è un solo bottone, cliccalo
                await buttons.nth(0).click()
                print(f"Clicked on the only '{game_label}' button.")
            elif count > 1:
                # Se ci sono più bottoni, clicca sul secondo
                await buttons.nth(1).click()
                print(f"Clicked on the second '{game_label}' button.")
            else:
                # Nessun bottone trovato
                print(f"No '{game_label}' buttons found.")

    except Exception as e:
        print(f"Error navigating to {url}: {e}")

    finally:
        # Salva i log in un file o stampa a schermo
        if len(logs) > 2:
            logs_path = f"logs/{event_id}_{doc_code}_console_logs.txt"
            os.makedirs(os.path.dirname(logs_path), exist_ok=True)

            with open(logs_path, "w", encoding="utf-8") as log_file:
                log_file.write(f"{n_games}\n")
                log_file.write("\n".join(logs))

            print(f"Match stats saved to: {logs_path}")


async def process_files(page: Page):
    """Elabora tutti i file TSV nella cartella data/tournaments."""
    base_path = 'data/tournaments'
    for file_name in os.listdir(base_path):
        if file_name.endswith('.tsv'):
            file_path = os.path.join(base_path, file_name)
            print(f"Processing file: {file_path}")

            # Lettura del file TSV
            df = pd.read_csv(file_path, sep='\t')
            for _, row in df.iterrows():
                event_id = row.iloc[0]
                doc_code = row.iloc[1]
                n_games = int(row.iloc[12]) + int(row.iloc[13])
                await get_console_logs(page, str(event_id), str(doc_code), int(n_games))


async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        page = await browser.new_page()

        # Elabora i file TSV
        await process_files(page)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
