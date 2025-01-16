import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Lista per memorizzare i punteggi
punteggi = []

# Variabile per tenere traccia dello stato del gioco (attivo o terminato)
gioco_terminato = False

def aggiorna_grafico():
    """Aggiorna il grafico in base ai punteggi attuali."""
    ax.clear()
    ax.set_title("Andamento del punteggio")
    ax.set_xlabel("Iterazioni")
    ax.set_ylabel("Punti totali")

    # Calcoliamo i punteggi cumulativi
    punteggi_utente = [sum(1 for p in punteggi[:i] if p == 1) for i in range(1, len(punteggi) + 1)]
    punteggi_avversario = [sum(1 for p in punteggi[:i] if p == 0) for i in range(1, len(punteggi) + 1)]

    # Tracciamo i punteggi cumulativi
    ax.plot(range(len(punteggi)), punteggi_utente, label="Utente", color="blue", marker="o")
    ax.plot(range(len(punteggi)), punteggi_avversario, label="Avversario", color="cyan", marker="o")
    ax.legend()
    canvas.draw()

def aggiungi_punto_utente():
    """Aggiunge un punto per l'utente (1) alla lista dei punteggi"""
    global gioco_terminato
    if len(punteggi) < 20 and not gioco_terminato:
        punteggi.append(1)
        aggiorna_punteggi()
        aggiorna_grafico()
        verifica_vittoria()
    elif gioco_terminato:
        messagebox.showinfo("Gioco Terminato", "Il gioco è finito! Premi Reset per iniziare una nuova partita.")
    else:
        mostra_avviso()

def aggiungi_punto_avversario():
    """Aggiunge un punto per l'avversario (0) alla lista dei punteggi"""
    global gioco_terminato
    if len(punteggi) < 20 and not gioco_terminato:
        punteggi.append(0)
        aggiorna_punteggi()
        aggiorna_grafico()
        verifica_vittoria()
    elif gioco_terminato:
        messagebox.showinfo("Gioco Terminato", "Il gioco è finito! Premi Reset per iniziare una nuova partita.")
    else:
        mostra_avviso()

def reset():
    """Resetta la lista dei punteggi e riattiva il gioco"""
    global gioco_terminato
    punteggi.clear()
    gioco_terminato = False
    aggiorna_punteggi()
    aggiorna_grafico()
    bottone_utente.config(state="normal")
    bottone_avversario.config(state="normal")

def annulla_ultimo_punto():
    """Annulla l'ultimo punto aggiunto"""
    if punteggi:
        punteggi.pop()
        aggiorna_punteggi()
        aggiorna_grafico()
    else:
        messagebox.showinfo("Nessuna Azione", "Non ci sono punti da annullare.")

def aggiorna_punteggi():
    """Calcola i punteggi e aggiorna l'etichetta"""
    punteggio_utente = punteggi.count(1)
    punteggio_avversario = punteggi.count(0)
    etichetta_punteggi.config(text=f"{punteggio_utente} - {punteggio_avversario}")

def mostra_avviso():
    """Mostra un messaggio di avviso se il numero di iterazioni supera il limite"""
    messagebox.showinfo("Limite raggiunto", "Il numero massimo di iterazioni (20) è stato raggiunto! Per favore resetta il punteggio.")

def verifica_vittoria():
    """Controlla se uno dei giocatori ha vinto (raggiunto 11 punti)"""
    global gioco_terminato
    punteggio_utente = punteggi.count(1)
    punteggio_avversario = punteggi.count(0)

    if punteggio_utente == 11:
        messagebox.showinfo("Vittoria", "Hai vinto! Complimenti!")
        termina_gioco()
    elif punteggio_avversario == 11:
        messagebox.showinfo("Sconfitta", "Hai perso! Peccato...")
        termina_gioco()

def termina_gioco():
    """Termina il gioco e disabilita i bottoni"""
    global gioco_terminato
    gioco_terminato = True
    bottone_utente.config(state="disabled")
    bottone_avversario.config(state="disabled")

# Creazione della finestra principale
root = tk.Tk()
root.title("Gioco del Punteggio")
root.geometry("1400x900")
root.minsize(1400, 900)

# Configura il layout della finestra per dividere lo spazio in due metà
root.grid_columnconfigure(0, weight=1, uniform="half")
root.grid_columnconfigure(1, weight=1, uniform="half")
root.grid_rowconfigure(0, weight=1)

# Creazione del frame di sinistra
left_frame = tk.Frame(root, bg="#f0f0f0")
left_frame.grid(row=0, column=0, sticky="nsew")

# Configurazione del frame sinistro
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_rowconfigure(1, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

# Bottone di reset piccolo in alto
small_reset_button = tk.Button(left_frame, text="Reset", command=reset, font=("Arial", 12, "bold"), bg="#FFD700", fg="white", width=6, height=1, relief="ridge")
small_reset_button.grid(row=0, column=0, sticky="n", pady=2)

# Parte superiore: punteggi e bottoni
score_frame = tk.Frame(left_frame, bg="#f0f0f0")
score_frame.grid(row=0, column=0, sticky="nsew", pady=(50, 0))

etichetta_punteggi = tk.Label(score_frame, text="0 - 0", font=("Helvetica", 64, "bold"), fg="#333", bg="#f0f0f0")
etichetta_punteggi.place(relx=0.5, rely=0.3, anchor="center")

bottone_utente = tk.Button(score_frame, text="+", command=aggiungi_punto_utente, font=("Arial", 28, "bold"), bg="#77DD77", fg="white", width=3, height=1, relief="ridge")
bottone_utente.place(relx=0.30, rely=0.7, anchor="center")

bottone_annulla = tk.Button(score_frame, text="Annulla", command=annulla_ultimo_punto, font=("Arial", 28, "bold"), bg="#87CEEB", fg="white", width=7, height=1, relief="ridge")
bottone_annulla.place(relx=0.5, rely=0.7, anchor="center")

bottone_avversario = tk.Button(score_frame, text="+", command=aggiungi_punto_avversario, font=("Arial", 28, "bold"), bg="#FF6961", fg="white", width=3, height=1, relief="ridge")
bottone_avversario.place(relx=0.70, rely=0.7, anchor="center")

# Parte inferiore: grafico
graph_frame = tk.Frame(left_frame, bg="#ffffff")
graph_frame.grid(row=1, column=0, sticky="nsew")

fig, ax = plt.subplots(figsize=(8, 1))  # Dimensioni medie per il grafico
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

# Creazione del frame di destra
right_frame = tk.Frame(root, bg="#e0e0e0")
right_frame.grid(row=0, column=1, sticky="nsew")

hello_label = tk.Label(right_frame, text="hello", font=("Helvetica", 64, "italic"), fg="#555", bg="#e0e0e0")
hello_label.place(relx=0.5, rely=0.5, anchor="center")

# Avvio del loop principale della finestra
root.mainloop()

