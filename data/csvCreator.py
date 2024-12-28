import pandas as pd
import os

def determine_sets_to_win(file_path):
    """
    Determina il numero di set necessari per vincere leggendo il file di log.
    Ritorna:
    - 3 se un giocatore ha vinto almeno 3 set ma non più di 3.
    - 4 se un giocatore ha vinto almeno 4 set.
    - 0 se il file è vuoto o non ci sono vincitori.
    """

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        if not lines:
            print("Il file è vuoto.")
            return 0

        player1_wins = 0
        player2_wins = 0

        # Determina il numero di set
        num_sets = int(lines[0].strip())

        for i in range(num_sets):
            try:
                # Leggi i punteggi dei giocatori
                player1_scores = eval(lines[1 + i * 2].strip())
                player2_scores = eval(lines[2 + i * 2].strip())

                # Conta i set vinti da ciascun giocatore
                if 11 in player1_scores:
                    player1_wins += 1
                if 11 in player2_scores:
                    player2_wins += 1
            except Exception:
                # Ignora errori nel parsing del set
                continue

        # Determina il numero di set necessari per vincere
        if player1_wins >= 4 or player2_wins >= 4:
            return 4
        elif player1_wins >= 3 or player2_wins >= 3:
            return 3
        else:
            return 0  # Nessun vincitore

    except Exception as e:
        print(f"Errore durante la lettura del file {file_path}: {e}")
        return 0


def process_match_log(file_path):
    """
    Funzione per leggere il file di log dei match e analizzare i punteggi.
    """


    try:
        sets_to_win = determine_sets_to_win(file_path)
        with open(file_path, 'r') as file:
            lines = file.readlines()

        num_sets = int(lines[0].strip())
        print(f"Numero di set totali in questo match: {num_sets}")

        player1_wins = 0
        player2_wins = 0

        match_data = []  # Conterrà le righe dei dati dei set

        for i in range(num_sets):
            try:
                player1_scores = eval(lines[1 + i * 2].strip())
                player2_scores = eval(lines[2 + i * 2].strip())

                if 11 in player1_scores:
                    player1_wins += 1
                    set_winner = f"{player1_wins}-{player2_wins}"
                elif 11 in player2_scores:
                    player2_wins += 1
                    set_winner = f"{player1_wins}-{player2_wins}"
                else:
                    # Caso di errore o nessun vincitore
                    set_winner = None
                    player1_scores = []
                    player2_scores = []
            except Exception:
                # In caso di errore nei punteggi, aggiungiamo una riga vuota
                set_winner = None
                player1_scores = []
                player2_scores = []

            print(f"Set {i + 1} Giocatore 1: {player1_scores}, Giocatore 2: {player2_scores}")

            # Dati del set (vuoti se c'è un errore o nessun vincitore)
            match_data.append({
                "set_number": i + 1,
                "points_a": ", ".join(map(str, player1_scores)) if player1_scores else "",
                "points_x": ", ".join(map(str, player2_scores)) if player2_scores else "",
                "sets_to_win": sets_to_win,
                "set_winner": set_winner or ""
            })

        # Resetta i contatori per i prossimi match
        player1_wins, player2_wins = 0, 0

        return match_data

    except Exception as e:
        print(f"Errore durante l'elaborazione del file {file_path}: {e}")
        # Se c'è un errore generale, aggiungiamo righe vuote per il numero di set
        return [{"set_number": i + 1, "points_a": "", "points_b": "", "set_winner": ""} for i in range(num_sets)]


def process_file(file_path, skip_header):
    """
    Funzione per leggere e processare un singolo file .tsv.
    """
    try:
        data = pd.read_csv(file_path, sep='\t', skiprows=0 if skip_header else 0)

        all_match_data = []  # Conterrà tutte le righe

        for idx, row in data.iterrows():
            event_id = row['event_id']
            doc = row['doc']
            filename_to_search = f"{event_id}_{doc}_console_logs.txt"
            matches_dir = 'matches'
            file_path_in_matches = os.path.join(matches_dir, filename_to_search)

            if os.path.exists(file_path_in_matches):
                print(f"File trovato: {file_path_in_matches}")
                match_data = process_match_log(file_path_in_matches)

                if match_data:
                    for set_data in match_data:
                        all_match_data.append({
                            "event_id": event_id,
                            "doc": doc,
                            "fmt": row['fmt'],
                            "gender": row['gender'],
                            "stage": row['stage'],
                            "stage_id": row['stage_id'],
                            "duration": row['duration'],
                            "start": row['start'],
                            "a_id": row['a_id'],
                            "b_id": row['b_id'],
                            "x_id": row['x_id'],
                            "y_id": row['y_id'],
                            "res_a": row['res_a'],
                            "res_x": row['res_x'],
                            "scores": row['scores'],
                            "set_number": set_data["set_number"],
                            "sets_to_win": set_data["sets_to_win"],
                            "set_winner": set_data["set_winner"],
                            "points_a": set_data["points_a"],
                            "points_x": set_data["points_x"]
                        })

        return pd.DataFrame(all_match_data)

    except Exception as e:
        print(f"Errore durante la lettura del file {file_path}: {e}")
        return pd.DataFrame()

import time

def main():
    tournaments_dir = 'tournaments'
    output_file = 'file_output.csv'

    if os.path.exists(output_file):
        try:
            os.remove(output_file)
        except PermissionError:
            print(f"Il file {output_file} è in uso. Riprovo...")
            time.sleep(1)  # Attendi un secondo e riprova
            os.remove(output_file)

    if not os.path.exists(tournaments_dir):
        print(f"Errore: La cartella '{tournaments_dir}' non esiste.")
        return

    first_file = True

    for filename in os.listdir(tournaments_dir):
        if filename.endswith('.tsv'):
            file_path = os.path.join(tournaments_dir, filename)
            data = process_file(file_path, not first_file)

            if not data.empty:
                data.to_csv(output_file, mode='a', index=False, header=first_file)
                first_file = False

if __name__ == '__main__':
    main()
