import pandas as pd
import os
from collections import Counter

# Funzione per validare la correttezza dei punteggi inseriti nel csv
def check_points_error(points_a, points_x):

    """

        Questa funzione tenta di rimuovere il più rumore possibile nei dati,
        con l'obiettivo di individuare i casi in cui i punteggi non sono validi

    """

    len_a = len(points_a)
    len_x = len(points_x)

    # Un set non può avere meno di 11 punti di gioco(minimo 11-0)
    if len_a < 11 or len_x < 11:
        return True

    # Un set deve avere lo stesso numero di istanti per entrambi i set dei giocatori
    if len(points_a) != len(points_x):
        return True

    # Un set deve finire con almeno uno dei due giocatori a 11 punti minimo
    if points_a[-1] < 11 and points_x[-1] < 11:
        return True

    # Un set deve finire con almeno due punti di distacco
    if abs(points_a[-1] - points_x[-1]) < 2:
        return True

    for i in range(1, len_a):

        # Un set non può avere un balzo di più di un punto fra un istante e un altro
        if abs(points_a[i - 1] - points_a[i]) > 1:
            return True

        if abs(points_x[i - 1] - points_x[i]) > 1:
            return True

        # Un set non può avere un punteggio decrescente
        if points_a[i] < points_a[i - 1]:
            return True
        elif points_x[i] < points_x[i - 1]:
            return True

        # Se un giocatore fa un punto in un istante "i" allora l'altro giocatore non farà punto
        if points_a[i] > points_a[i - 1]:
            if points_x[i] > points_x[i - 1]:
                return True

        if points_x[i] > points_x[i - 1]:
            if points_a[i] > points_a[i - 1]:
                return True

        # Se un giocatore non fa un punto in un istante "i" allora l'altro giocatore non può non fare un punto
        if points_a[i] == points_a[i - 1]:
            if points_x[i] == points_x[i - 1]:
                return True

        if points_x[i] == points_x[i - 1]:
            if points_a[i] == points_a[i - 1]:
                return True

    return False


def points_transformer(points_a, index):

    """

        Consideriamo i punti fatti da un giocatore come il numero
        di istanti in cui il giocatore si trova al punteggio i

    """

    frequency = Counter(points_a)
    result = []
    for i, val in enumerate(sorted(frequency.keys())):
        if i >= index:
            break
        result.append(frequency[val])

    return result


def process_match_log(file_path):

    """

        Questa funzione legge i file di .txt generati dallo scraper download_matches.py
        e genera le righe del dataset rimuovendo i dati errati

    """

    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_sets = int(lines[0].strip())
    match_data = []  # Conterrà le righe da mettere nel dataset
    match_state = [0, 0]  # Stato iniziale dei set del match
    match_points_a = 0  # Numero di punti vinti da "a"
    match_points_x = 0  # Numero di punti vinti da "x"

    for i in range(num_sets):
        try:
            # Prende i puteggi del set "i" presenti nel file .txt considerato
            points_a = eval(lines[2 + i * 2].strip()) if lines[2 + i * 2].strip() else []
            points_x = eval(lines[1 + i * 2].strip()) if lines[1 + i * 2].strip() else []

            # Se nei punteggi è presente un errore allora genera una eccezione
            if check_points_error(points_a, points_x):
                raise ValueError("Errore nei punteggi")

            match_points_a += points_a[-1]  # Prendo il numero di punti fatti da a
            match_points_x += points_x[-1]  # Prendo il numero di punti fatti da x

            # Aggiunge al dataset temporaneo i punteggi dei giocatori e lo stato attuale dei set
            match_data.append({
                "points_a": points_a[1:-1] if len(points_a) > 2 else [],    # Non considero il primo e l'ultimo istante dei punteggi
                "points_x": points_x[1:-1] if len(points_x) > 2 else [],    # Perchè il primo istante è sempre 0 mentre l'ultimo ci dice il risultato finale della partita(DATA LEAKAGE!)
                "match_state": f"{match_state[0]}-{match_state[1]}"
            })

            # In base ai punteggi vedo chi ha vinto il set
            if points_a[-1] > points_x[-1]:
                match_state[0] += 1  # A vince il set
            else:
                match_state[1] += 1  # X vince il set

        except Exception as e:
            # In caso di errore, aggiungo dati vuoti per il set corrente e blocco l'analisi della partita incriminata
            match_data.append({
                "points_a": "",
                "points_x": "",
                "match_state": f"{match_state[0]}-{match_state[1]}"
            })
            break


    # Se il match ha punteggi troppo contrastanti allora lo tolgo dal dataset
    # Assumo che uno dei giocatori deve fare almeno 7 punti in tutta la partita per considerare il match come "equilibrato"
    if match_points_a < 7 or match_points_x < 7:
        match_data = []

    return match_data


def process_file(file_path, skip_header):
    """
    Funzione per leggere e processare un singolo file .tsv.
    """
    try:
        # Leggo il CSV contenente i dati su tutte le partite di un torneo tranne i punteggi che dovrò prendere dai file .txt
        data = pd.read_csv(file_path, sep='\t', skiprows=0 if skip_header else 0)

        all_match_data = []  # Conterrà tutte le righe del torneo analizzato

        # Per ciascuna partita del torneo inserisce il all_match_data le righe complete
        for idx, row in data.iterrows():
            event_id = row['event_id']
            doc = row['doc']
            filename_to_search = f"{event_id}_{doc}_console_logs.txt"
            matches_dir = '../data/matches'
            file_path_in_matches = os.path.join(matches_dir, filename_to_search)

            if os.path.exists(file_path_in_matches):
                print(f"File trovato: {file_path_in_matches}")
                match_data = process_match_log(file_path_in_matches)

                if match_data:
                    sets_to_win = max(row['res_a'], row['res_x'])  # Calcola i set necessari per vincere
                    for set_data in match_data:
                        all_match_data.append({
                            "event_id": event_id,
                            "match_id": doc,
                            "match_format": row['fmt'],
                            "players_gender": row['gender'],
                            "match_stage": row['stage'],
                            "stage_id": row['stage_id'],
                            "match_duration": row['duration'],
                            "match_start_time": row['start'],
                            "player_id": row['a_id'],
                            "player_2_id": row['b_id'],
                            "opponent_id": row['x_id'],
                            "opponent_2_id": row['y_id'],
                            "player_sets_won": row['res_a'],
                            "opponent_sets_won": row['res_x'],
                            "match_scores": row['scores'],
                            "sets_required_to_win": sets_to_win,
                            "current_match_state": set_data["match_state"],
                            "points_progression": set_data["points_a"],
                            "opponent_points": set_data["points_x"],
                        })

        return pd.DataFrame(all_match_data)

    except Exception as e:
        print(f"Errore durante la lettura del file {file_path}: {e}")
        return pd.DataFrame()


def main():
    tournaments_dir = '../data/tournaments'
    output_file = '../data/datasets/raw_dataset.csv'

    if os.path.exists(output_file):
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
