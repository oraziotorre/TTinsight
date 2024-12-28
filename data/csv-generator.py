import pandas as pd
import os

#Funzione per validare la correttezza dei punteggi inseriti nel csv
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

def process_match_log(file_path):
    """
    Funzione per leggere il file di log dei match e analizzare i punteggi.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_sets = int(lines[0].strip())
    match_data = []  # Conterrà le righe dei dati dei set
    match_state = [0, 0]  # Stato iniziale dei set del match

    for i in range(num_sets):
        try:
            # Ottieni i punteggi dei giocatori, con fallback a liste vuote per evitare errori
            points_a = eval(lines[2 + i * 2].strip()) if lines[2 + i * 2].strip() else []
            points_x = eval(lines[1 + i * 2].strip()) if lines[1 + i * 2].strip() else []

            if check_points_error(points_a, points_x):
                raise ValueError("Errore nei punteggi")

            # Aggiungi i dati del match con i punteggi in formato stringa
            match_data.append({
                "points_a": ", ".join(map(str, points_a)) if points_a else "",
                "points_x": ", ".join(map(str, points_x)) if points_x else "",
                "match_state": f"{match_state[0]}-{match_state[1]}"
            })

            if points_a[-1] > points_x[-1]:
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
                            "sets_to_win": sets_to_win,
                            "match_state": set_data["match_state"],
                            "points_a": set_data["points_a"],
                            "points_x": set_data["points_x"]
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
