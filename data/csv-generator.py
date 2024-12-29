import pandas as pd
import os
from collections import Counter

# Funzione per validare la correttezza dei punteggi inseriti nel csv
def check_points_error(points_a, points_x):
    len_a = len(points_a)
    len_x = len(points_x)

    if len_a < 11 or len_x < 11:
        return True

    if len(points_a) != len(points_x):
        return True

    for i in range(len_a - 1):
        if abs(points_a[i] - points_a[i + 1]) > 1:
            return True

    for i in range(len_x - 1):
        if abs(points_x[i] - points_x[i + 1]) > 1:
            return True

    if points_a[-1] < 11 and points_x[-1] < 11:
        return True

    if abs(points_a[-1] - points_x[-1]) < 2:
        return True

    for i in range(1, len_a):
        if points_a[i] > points_a[i - 1]:
            if points_x[i] > points_x[i - 1]:
                return True
        elif points_x[i] > points_x[i - 1]:
            if points_a[i] > points_a[i - 1]:
                return True

    return False


def points_transformer(points_a):
    """
    Consideriamo i punti fatti da un giocatore come il numero
    di istanti in cui il giocatore si trova al punteggio i
    """
    frequency = Counter(points_a)

    result = [frequency[val] for val in sorted(frequency.keys())]

    return result


def process_match_log(file_path):
    """
    Funzione per leggere il file di log dei match e analizzare i punteggi.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_sets = int(lines[0].strip())
    match_data = []  # Conterrà le righe dei dati dei set
    match_state = [0, 0]  # Stato iniziale dei set del match
    match_points_a = 0  # numero totale di punteggio
    match_points_x = 0  # numero totale di punteggio

    for i in range(num_sets):
        try:
            # Ottieni i punteggi dei giocatori, con fallback a liste vuote per evitare errori
            points_a = eval(lines[2 + i * 2].strip()) if lines[2 + i * 2].strip() else []
            points_x = eval(lines[1 + i * 2].strip()) if lines[1 + i * 2].strip() else []

            if check_points_error(points_a, points_x):
                raise ValueError("Errore nei punteggi")

            points_a = points_transformer(points_a)
            points_x = points_transformer(points_x)
            match_points_a += len(points_a)
            match_points_x += len(points_x)

            # Aggiungi i dati del match con i punteggi in formato stringa
            match_data.append({
                "points_a": ", ".join(map(str, points_a)) if points_a else "",
                "points_x": ", ".join(map(str, points_x)) if points_x else "",
                "match_state": f"{match_state[0]}-{match_state[1]}"
            })

            if len(points_a) > len(points_x):
                match_state[0] += 1  # A vince il set
            else:
                match_state[1] += 1  # X vince il set


        except Exception as e:
            # In caso di errore, aggiungi dati vuoti per il set corrente
            match_data.append({
                "points_a": "",
                "points_x": "",
                "match_state": f"{match_state[0]}-{match_state[1]}"
            })
            break

    # Se il match ha punteggi troppo contrastanti allora lo tolgo dal dataset
    if match_points_a < 7 or match_points_x < 7:
        match_data = []

    return match_data


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
                            "player_points": set_data["points_a"],
                            "opponent_points": set_data["points_x"],
                            "match_result": 'W' if sets_to_win == row['res_a'] else 'L'
                        })

                        all_match_data.append({
                            "event_id": event_id,
                            "match_id": doc,
                            "match_format": row['fmt'],
                            "players_gender": row['gender'],
                            "match_stage": row['stage'],
                            "stage_id": row['stage_id'],
                            "match_duration": row['duration'],
                            "match_start_time": row['start'],
                            "player_id": row['x_id'],
                            "player_2_id": row['y_id'],
                            "opponent_id": row['a_id'],
                            "opponent_2_id": row['b_id'],
                            "player_sets_won": row['res_x'],
                            "opponent_sets_won": row['res_a'],
                            "match_scores": ','.join(['-'.join(reversed(score.split('-'))) for score in row['scores'].split(',')]),
                            "sets_required_to_win": sets_to_win,
                            "current_match_state": '-'.join(reversed(set_data["match_state"].split('-'))),
                            "player_points": set_data["points_x"],
                            "opponent_points": set_data["points_a"],
                            "match_result": 'W' if sets_to_win == row['res_x'] else 'L'
                        })

        return pd.DataFrame(all_match_data)

    except Exception as e:
        print(f"Errore durante la lettura del file {file_path}: {e}")
        return pd.DataFrame()


def main():
    tournaments_dir = 'tournaments'
    output_file = 'raw_data.csv'

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
