import math
import sys
import joblib
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QPushButton
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QWidget):
    is_going_back = False

    def __init__(self):
        super().__init__()

        self.model_logreg = joblib.load('models/LogReg.pkl')  # Carica il modello di regressione logistica

        # self.model_lstm = load_model('models/LSTMboolean+3.keras')  # Carica il modello LSTM

        # Imposta dimensioni della finestra
        self.probabilities = None
        self.setWindowTitle("Div con form e colori personalizzati")
        self.setGeometry(100, 100, 1400, 700)  # x, y, larghezza, altezza

        # Mostra la finestra a tutto schermo
        self.showFullScreen()
        self.is_fullscreen = True
        self.setFocus()


        main_layout = QHBoxLayout()

        # Rimuovi margini e spaziatura dal layout principale
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Div sinistro
        self.left_div = QWidget()
        self.left_div.setStyleSheet(""" 
            background-color: #2a2f33;  /* Sfondo grigio scuro */
            border-right: 2px solid black;
        """)
        left_layout = QVBoxLayout()
        self.add_form_container(left_layout)
        self.add_bottom_div(left_layout)

        self.left_div.setLayout(left_layout)

        # Div destro
        self.right_div = QWidget()
        self.right_div.setStyleSheet(""" 
            background-color: #2a2f33;  /* Sfondo grigio scuro */
        """)
        right_layout = QVBoxLayout()
        self.add_right_div(right_layout)
        self.right_div.setLayout(right_layout)

        # Aggiungere i due "div" al layout principale
        main_layout.addWidget(self.left_div)
        main_layout.addWidget(self.right_div)

        # Imposta proporzioni dei "div"
        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 1)

        self.setLayout(main_layout)

        self.scores = [[0, 0]]
        self.points_progression = []
        self.log_reg_values = [0, 0]
        self.comeback_count = 0
        self.lstm_values = [0, 0, 0]

    def predict(self):


        logreg_input = np.array(self.points_progression + self.log_reg_values).reshape(1,-1)
        logreg_prob = self.model_logreg.predict_proba(logreg_input)[0]
        print(f"LogReg Probabilities: {logreg_prob}")

        '''
        lstm_input = np.array(self.lstm_values + self.points_progression).reshape(1, -1)
        lstm_prob = self.model_lstm.predict(lstm_input)
        print(f"LSTM Probabilities: {lstm_prob}")
        '''

    def keyPressEvent(self, event):
        """Gestisce la pressione dei tasti"""
        if event.key() == Qt.Key_Escape:
            if self.is_fullscreen:
                self.showNormal()  # Passa alla modalità finestra normale
            else:
                self.showFullScreen()  # Passa alla modalità fullscreen
            self.is_fullscreen = not self.is_fullscreen

    def add_form_container(self, layout):
        """Aggiunge il contenitore per il form"""

        # Contenitore per il form
        form_container = QWidget()
        form_container.setStyleSheet(""" 
            background-color: #1a1f23;  /* Colore di sfondo scuro per il contenitore */
            color: white;  /* Testo bianco */
            border: 0px solid #444;  /* Bordo sottile per il contenitore */
            border-radius: 5px;
        """)
        form_layout = QHBoxLayout()
        form_layout.setContentsMargins(10, 10, 10, 10)
        form_layout.setSpacing(20)
        self.add_form_sections(form_layout)
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

    def add_form_sections(self, layout):
        final_set_group = QGroupBox("")
        final_set_layout = QVBoxLayout()

        # Gruppo per Utente
        utente_group = QGroupBox("")
        utente_layout = QVBoxLayout()
        utente_layout.setSpacing(5)
        utente_layout.addWidget(QLabel("Final_Set_A"))
        self.utente_radio_true = QRadioButton("1")
        self.utente_radio_false = QRadioButton("0")
        utente_layout.addWidget(self.utente_radio_true)
        utente_layout.addWidget(self.utente_radio_false)
        utente_group.setLayout(utente_layout)
        utente_group.setStyleSheet("color: white;")
        self.utente_radio_true.toggled.connect(self.update_lstm_values)

        # Gruppo per Avversario
        avversario_group = QGroupBox("")
        avversario_layout = QVBoxLayout()
        avversario_layout.setSpacing(5)
        avversario_layout.addWidget(QLabel("Final_Set_B"))
        self.avversario_radio_true = QRadioButton("1")
        self.avversario_radio_false = QRadioButton("0")
        avversario_layout.addWidget(self.avversario_radio_true)
        avversario_layout.addWidget(self.avversario_radio_false)
        avversario_group.setLayout(avversario_layout)
        avversario_group.setStyleSheet("color: white;")
        self.avversario_radio_true.toggled.connect(self.update_lstm_values)

        # Aggiungi i gruppi al layout finale
        final_set_layout.addWidget(utente_group)
        final_set_layout.addWidget(avversario_group)

        # Settiamo il layout per il QGroupBox finale
        final_set_group.setLayout(final_set_layout)
        final_set_group.setStyleSheet("color: white;")

        # Sezione Is_Final
        is_final_group = QGroupBox("")
        is_final_layout = QVBoxLayout()
        is_final_layout.setSpacing(10)
        is_final_layout.addWidget(QLabel("Is_Final:"))
        self.is_final_radio_true = QRadioButton("1")
        self.is_final_radio_false = QRadioButton("0")
        is_final_layout.addWidget(self.is_final_radio_true)
        is_final_layout.addWidget(self.is_final_radio_false)
        is_final_layout.addWidget(QLabel(""))

        is_final_group.setLayout(is_final_layout)
        is_final_group.setStyleSheet("color: white;")
        self.is_final_radio_true.toggled.connect(self.update_lstm_values)

        # Bottone per mostrare/nascondere tutto
        self.toggle_button = QPushButton("Mostra Tutto")
        self.toggle_button.setStyleSheet(""" 
            background-color: #768a89; 
            color: white; 
            font-size: 14px; 
            border-radius: 5px;
            padding: 5px;
        """)

        # Bottone di reset
        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet(""" 
            background-color: black; 
            color: white; 
            font-size: 14px; 
            border-radius: 5px;
            padding: 5px;
        """)
        self.reset_button.clicked.connect(self.reset_labels)

        # Connessione del toggle_button per mostrare/nascondere i gruppi
        self.toggle_button.clicked.connect(self.toggle_radio_buttons)

        # Nascondi inizialmente i gruppi di radio button
        final_set_group.setVisible(False)
        is_final_group.setVisible(False)

        # Memorizza i gruppi in una lista per gestire visibilità
        self.radio_groups = [final_set_group, is_final_group]

        # Layout per i bottoni di "Mostra Tutto" e "Reset"
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.reset_button)

        # Aggiungere i gruppi e i bottoni al layout
        layout.addWidget(final_set_group)
        layout.addWidget(is_final_group)
        layout.addLayout(button_layout)

    def update_lstm_values(self):
        """Aggiorna i valori in lstm_values in base ai radio button selezionati"""
        self.lstm_values[0] = 1 if self.is_final_radio_true.isChecked() else 0
        self.lstm_values[1] = 1 if self.utente_radio_true.isChecked() else 0
        self.lstm_values[2] = 1 if self.avversario_radio_true.isChecked() else 0

        print(f"Updated lstm_values: {self.lstm_values}")

    def toggle_radio_buttons(self):
        """Mostra o nascondi i radio button"""
        if self.radio_groups[0].isVisible():
            for group in self.radio_groups:
                group.setVisible(False)
            self.toggle_button.setText("Mostra Tutto")
        else:
            for group in self.radio_groups:
                group.setVisible(True)
            self.toggle_button.setText("Nascondi Tutto")

    def add_bottom_div(self, layout):

        if not hasattr(self, 'scores'):
            self.scores = [[0, 0]]

        bottom_div = QWidget()
        bottom_div.setStyleSheet(""" 
            background-color: #1a1f23;  /* Nuovo colore di sfondo */
            color: white;  /* Testo bianco */
            border-radius: 5px;
            margin-top: 5px;
            padding: 10px;
            border: none;
        """)

        bottom_div.setMinimumHeight(100)
        bottom_div.setFixedHeight(450)
        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(20)
        bottom_layout.setAlignment(Qt.AlignCenter)

        vertical_div = QWidget()
        vertical_div.setStyleSheet(""" 
            background-color: #1a1f23; 
            color: white;
            border-radius: 5px;
            padding: 10px;
        """)
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(10)
        vertical_layout.setAlignment(Qt.AlignCenter)

        # Crea il layout orizzontale per i numeri centrati
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setAlignment(Qt.AlignCenter)
        self.label1 = QLabel("0")
        self.label2 = QLabel("0")
        self.label3 = QLabel("-")

        # Imposta larghezza fissa per ciascun QLabel
        max_width = 240
        self.label1.setFixedWidth(max_width)
        self.label2.setFixedWidth(max_width)
        self.label3.setFixedWidth(max_width)

        self.label1.setStyleSheet("""
            font-size: 170px;
            color: white;
        """)
        self.label2.setStyleSheet("""
            font-size: 170px;
            color: white;
        """)
        self.label3.setStyleSheet("""                      
            font-size: 170px;
            color: white;
        """)

        # Allinea il testo al centro in ogni QLabel
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2.setAlignment(Qt.AlignCenter)
        self.label3.setAlignment(Qt.AlignCenter)

        horizontal_layout.addWidget(self.label1)
        horizontal_layout.addWidget(self.label3)
        horizontal_layout.addWidget(self.label2)

        vertical_layout.addLayout(horizontal_layout)

        button_div = QWidget()
        button_div.setStyleSheet(""" 
            background-color: #1a1f23;
            padding: 10px;
            margin-bottom: 20px;
        """)

        # Layout per i bottoni
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setAlignment(Qt.AlignCenter)

        self.plus_button1 = QPushButton("")
        self.back_button = QPushButton("←")
        self.plus_button2 = QPushButton("")

        self.plus_button1.setStyleSheet(""" 
            background-color:#013FB3;
            font-size: 15px;
            color: white;
            font-weight: bold;
            padding: 0;
            border: 4px solid black;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            margin-right: 100px;
            margin-left: 100px;
        """)

        self.plus_button2.setStyleSheet(""" 
            background-color: #FF6600;
            font-size: 15px;
            color: white;
            font-weight: bold;
            padding: 0;
            border: 4px solid black;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            margin-right: 100px;
            margin-left: 100px;
        """)

        self.back_button.setStyleSheet(""" 
            background-color:#000000;
            font-size: 15px;
            color: white;
            font-weight: bold;
            padding: 0;
            border: 4px solid black;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            margin-right: 100px;
            margin-left: 100px;
        """)

        # Aggiungi i bottoni nell'ordine specificato
        button_layout.addWidget(self.plus_button1)
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.plus_button2)

        button_div.setLayout(button_layout)


        vertical_layout.addWidget(button_div)
        vertical_div.setLayout(vertical_layout)


        bottom_layout.addWidget(vertical_div)
        bottom_div.setLayout(bottom_layout)
        layout.addWidget(bottom_div)

        self.plus_button1.clicked.connect(self.increment_label1)
        self.plus_button2.clicked.connect(self.increment_label2)
        self.back_button.clicked.connect(self.go_back)

        # Div del Grafico
        graph_div = QWidget()
        graph_div.setStyleSheet(""" 
            background-color: #1a1f23;  /* Colore di sfondo del div grafico */
            border-radius: 5px;
            margin-top: 10px;
            padding: 10px;
        """)

        # Layout per il div del grafico
        graph_layout = QVBoxLayout()
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.setSpacing(10)

        self.add_graph(graph_layout)
        graph_div.setFixedHeight(400)
        graph_div.setLayout(graph_layout)
        layout.addWidget(graph_div)

    def add_right_div(self, layout):
        # Creazione di un layout orizzontale principale
        main_layout = QHBoxLayout()

        # Creazione del primo div verticale (sinistra)
        left_div = QWidget()
        left_div.setStyleSheet("""
            background-color: #1a1f23;
            border-radius: 5px;
            margin-top: 60px;
            margin-bottom: 10px;
            padding: 10px;
            border: 0px solid;
        """)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        # Titolo per le probabilità (a sinistra)
        title_label_left = QLabel("Probabilità Matematica")
        title_label_left.setAlignment(Qt.AlignCenter)
        title_label_left.setStyleSheet("""
            font-size: 18px;
            color: #f0f0f0;
            font-weight: bold;
        """)

        # Etichette delle probabilità (a sinistra)
        current_prob_label_left = QLabel("Probabilità Corrente: 0.0%")
        player1_prob_label_left = QLabel("Player 1 fa punto: 0.0%")
        player2_prob_label_left = QLabel("Player 2 fa punto: 0.0%")

        # Aggiungo il titolo e le label al layout del div a sinistra
        left_layout.addWidget(title_label_left)
        for label in [current_prob_label_left, player1_prob_label_left, player2_prob_label_left]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                font-size: 14px;
                color: white;
            """)
            left_layout.addWidget(label)

        left_div.setLayout(left_layout)

        # Creazione del div centrale (già esistente)
        text_div = QWidget()
        text_div.setStyleSheet("""
            background-color: #1a1f23;
            border-radius: 5px;
            margin-top: 60px;
            margin-bottom: 10px;
            padding: 10px;
            border: 0px solid;
        """)

        # Layout verticale per il testo
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(10)

        # Titolo per le probabilità
        title_label = QLabel("Probabilità Matematica")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            color: #f0f0f0;
            font-weight: bold;
        """)

        # Etichette delle probabilità
        self.current_prob_label = QLabel("Probabilità Corrente: 0.0%")
        self.player1_prob_label = QLabel("Player 1 fa punto: 0.0%")
        self.player2_prob_label = QLabel("Player 2 fa punto: 0.0%")

        # Aggiungo il titolo e le label al layout verticale
        text_layout.addWidget(title_label)
        for label in [self.current_prob_label, self.player1_prob_label, self.player2_prob_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                font-size: 14px;
                color: white;
            """)
            text_layout.addWidget(label)

        text_div.setLayout(text_layout)

        # Creazione del div destro (a destra)
        right_div = QWidget()
        right_div.setStyleSheet("""
            background-color: #1a1f23;
            border-radius: 5px;
            margin-top: 60px;
            margin-bottom: 10px;
            padding: 10px;
            border: 0px solid;
        """)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # Titolo per le probabilità (a destra)
        title_label_right = QLabel("Probabilità Matematica")
        title_label_right.setAlignment(Qt.AlignCenter)
        title_label_right.setStyleSheet("""
            font-size: 18px;
            color: #f0f0f0;
            font-weight: bold;
        """)

        # Etichette delle probabilità (a destra)
        current_prob_label_right = QLabel("Probabilità Corrente: 0.0%")
        player1_prob_label_right = QLabel("Player 1 fa punto: 0.0%")
        player2_prob_label_right = QLabel("Player 2 fa punto: 0.0%")

        # Aggiungo il titolo e le label al layout del div a destra
        right_layout.addWidget(title_label_right)
        for label in [current_prob_label_right, player1_prob_label_right, player2_prob_label_right]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                font-size: 14px;
                color: white;
            """)
            right_layout.addWidget(label)

        right_div.setLayout(right_layout)

        # Div inferiore - grafico (come nel codice originale)
        lower_div = QWidget()
        lower_div.setStyleSheet("""
            background-color: #1a1f23;
            border-radius: 5px;
            margin: 10px;
            padding: 10px;
        """)
        lower_div.setFixedHeight(500)  # Occupa circa il 55% dello spazio verticale

        # Layout per il grafico
        lower_layout = QVBoxLayout()
        lower_layout.setContentsMargins(10, 10, 10, 10)
        lower_layout.setSpacing(10)

        # Aggiungere il grafico usando la funzione esistente
        self.add_probability_graph(lower_layout)
        lower_div.setLayout(lower_layout)

        # Aggiungere i div al layout orizzontale principale
        main_layout.addWidget(left_div)
        main_layout.addWidget(text_div)
        main_layout.addWidget(right_div)

        # Aggiungere il div inferiore per il grafico
        layout.addLayout(main_layout)
        layout.addWidget(lower_div)

        # Rimuovere lo spazio residuo per non occupare tutto lo spazio
        layout.addStretch()

    def add_graph(self, layout):
        """Aggiunge un grafico sotto i numeri"""

        # Crea il canvas del grafico
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # Impostazioni iniziali del grafico
        self.update_graph()
        layout.addWidget(self.canvas)

    def add_probability_graph(self, layout):
        """Aggiunge un grafico per la probabilità di vincere"""
        self.figure_probability = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas_probability = FigureCanvas(self.figure_probability)
        self.axes_probability = self.figure_probability.add_subplot(111)

        self.update_probability_graph()
        layout.addWidget(self.canvas_probability)

    def update_graph(self):
        """Aggiorna il grafico con i punteggi correnti"""
        if not hasattr(self, 'scores'):  # Controlla che `self.scores` esista
            self.scores = [[0, 0]]

        self.axes.clear()

        # Estrai i valori per l'asse X e Y
        x_values = list(range(len(self.scores)))
        y1_values = [score[0] for score in self.scores]
        y2_values = [score[1] for score in self.scores]

        # Disegna le linee
        self.axes.plot(x_values, y1_values, label="Player 1", marker = 'o', color="#013FB3")
        self.axes.plot(x_values, y2_values, label="Player 2", marker='o', color="#FF6600")
        self.axes.set_xticks(range(len(self.scores)))
        max_score = max(max(y1_values), max(y2_values))
        self.axes.set_yticks(range(0, max_score + 1, max(1, max_score // 5)))

        self.axes.set_title("Score Progression")
        self.axes.set_xlabel("Points Played")
        self.axes.set_ylabel("Points Won")
        self.axes.legend()

        # Aggiorna il canvas
        self.canvas.draw()

    def update_probability_graph(self):
        """Aggiorna il grafico con le probabilità correnti, includendo righe tratteggiate per scenari futuri"""
        self.axes_probability.clear()

        # Parametri iniziali
        p = 0.5  # Probabilità di vincere un punto
        value1 = int(self.label1.text())  # Punti vinti dal giocatore
        value2 = int(self.label2.text())  # Punti vinti dall'avversario

        # Caso speciale: Se value1 == 11, la probabilità è 1
        if value1 == 11:
            prob_value = 1.0
        elif value2 == 11:
            prob_value = 0.0
        else:
            prob_value = self.prob(p, value1, value2)

        if self.is_going_back:
            del self.probabilities[-1]
            self.is_going_back = False
        elif not hasattr(self, 'probabilities') or not self.probabilities:
            self.probabilities = [(value1 + value2, prob_value)]  # Aggiunge il primo valore
        else:
            self.probabilities.append((value1 + value2, prob_value))  # Aggiunge il valore corrente

        # Estrai gli x e y per disegnare la linea e i punti
        x_values = [item[0] for item in self.probabilities]  # Punti totali (value1 + value2)
        y_values = [item[1] for item in self.probabilities]  # Probabilità calcolate

        # Disegna la linea continua
        self.axes_probability.plot(x_values, y_values, label="Probabilità", color="blue")

        # Aggiungi i pallini per evidenziare i punti calcolati
        self.axes_probability.scatter(x_values, y_values, color="blue", marker='o')

        # Aggiungi la percentuale sopra ogni pallino
        for i, (x, y) in enumerate(zip(x_values, y_values)):
            # Percentuale sopra ogni pallino
            self.axes_probability.annotate(f"{y:.4f}%", (x, y),
                                           textcoords="offset points", xytext=(0, 10), ha='center', color="blue")

        # Calcola le probabilità per gli scenari futuri
        if value1 + value2 < 20 and value1 < 11 and value2 < 11:  # Solo se non siamo alla fine del gioco
            if value1 == 10:
                prob_scenario1 = 1
                prob_scenario2 = self.prob(p, value1, value2 + 1)
            elif value2 == 10:
                prob_scenario1 = self.prob(p, value1 + 1, value2)
                prob_scenario2 = 0
            else:
                # Scenario 1: Giocatore 1 vince il prossimo punto (value1 + 1, value2)
                prob_scenario1 = self.prob(p, value1 + 1, value2)
                # Scenario 2: Giocatore 2 vince il prossimo punto (value1, value2 + 1)
                prob_scenario2 = self.prob(p, value1, value2 + 1)

            # Coordinate per i due scenari
            current_x = value1 + value2  # Ascissa attuale
            future_x = current_x + 1  # Ascissa del futuro passo

            # Disegna le linee tratteggiate per i due scenari
            self.axes_probability.plot(
                [current_x, future_x],
                [prob_value, prob_scenario1],
                linestyle="--", color="green", label="Punto_Player_1"
            )
            self.axes_probability.plot(
                [current_x, future_x],
                [prob_value, prob_scenario2],
                linestyle="--", color="red", label="Punto_Player_2"
            )

            # Aggiungi i pallini alle estremità delle linee tratteggiate
            self.axes_probability.scatter([future_x], [prob_scenario1], color="green", marker='o')
            self.axes_probability.scatter([future_x], [prob_scenario2], color="red", marker='o')

            # Aggiungi la percentuale sopra ogni pallino per gli scenari futuri
            self.axes_probability.annotate(f"{prob_scenario1:.4f}%", (future_x, prob_scenario1),
                                           textcoords="offset points", xytext=(0, 10), ha='center', color="green")
            self.axes_probability.annotate(f"{prob_scenario2:.4f}%", (future_x, prob_scenario2),
                                           textcoords="offset points", xytext=(0, 10), ha='center', color="red")
            self.player1_prob_label.setText(f"Player 1 fa punto: {prob_scenario1:.8f}%")
            self.player2_prob_label.setText(f"Player 2 fa punto: {prob_scenario2:.8f}%")

        total_points = value1 + value2
        half_visible = 8  # Range minimo visibile
        buffer = half_visible // 2  # Valore a cui iniziare ad espandere

        # Determina il range dinamico
        start_x = max(0, total_points - buffer)  # Espandi l'inizio solo dopo aver superato metà del range
        end_x = min(20, start_x + half_visible)  # Mantieni sempre almeno 8 punti visibili

        # Configurazione dell'asse (solo una porzione dei dati sarà visibile)
        self.axes_probability.set_xlim(start_x, end_x)  # Rendi visibile la parte dinamica
        self.axes_probability.set_xticks(range(start_x, end_x + 1))  # Imposta le tacche dell'asse X

        self.axes_probability.set_yticks([i * 0.1 for i in range(11)])  # Probabilità da 0 a 1 (step 0.1)

        # Titoli e etichette
        self.axes_probability.set_title(
            f"Probabilità di Vincita (Punti Giocatore: {value1}, Punti Avversario: {value2})"
        )
        self.axes_probability.set_xlabel("Punti Totali (Giocatore 1 + Giocatore 2)")
        self.axes_probability.set_ylabel("Probabilità")
        self.axes_probability.legend()

        # Aggiorna le label con le probabilità calcolate
        self.current_prob_label.setText(f"Probabilità Corrente: {prob_value:.8f}%")

        # Aggiorna il canvas
        self.canvas_probability.draw()

    def prob(self, p, x, y):
        """Funzione che calcola la probabilità di vincere un punto."""
        # Somma della prima parte
        sum_part1 = 0
        for i in range(0, 10 - y):
            sum_part1 += p ** (11 - x) * math.comb(10 + i - x, i) * (1 - p) ** i

        # Seconda parte della formula
        part2 = p ** (10 - x) * math.comb(20 - x - y, 10 - x) * (1 - p) ** (10 - y)
        part2 *= (p ** 2) / (1 - 2 * p * (1 - p))

        # Somma totale
        total = sum_part1 + part2
        return total

    def update_comeback_and_length(self):
        """Aggiorna il comeback e la lunghezza in base a points_progression"""
        print(f"Updating comeback and length. Current points_progression: {self.points_progression}")

        self.log_reg_values[1] = len(self.points_progression)
        print(f"Updated length (log_reg_values[1]): {self.log_reg_values[1]}")

        if self.log_reg_values[1] == 1:
            if self.points_progression[-1] == 0:
                self.log_reg_values[0] = -1
            else:
                self.log_reg_values[0] = 1
        else:
            # Controlliamo il valore corrente di comeback
            last_value = self.points_progression[-1]
            secondtolast_value = self.points_progression[-2]

            if last_value == 1:
                if last_value == secondtolast_value:
                    self.log_reg_values[0] += 1
                else:
                    self.log_reg_values[0] = 1
            elif last_value == 0:
                if last_value == secondtolast_value:
                    self.log_reg_values[0] -= 1
                else:
                    self.log_reg_values[0] = -1

        print(f"Updated comeback (log_reg_values[0]): {self.log_reg_values[0]}")

    def increment_label1(self):
        """Incrementa il valore del primo numero"""
        value1 = int(self.label1.text())
        value2 = int(self.label2.text())
        print(f"Incrementing label1. Current values: label1 = {value1}, label2 = {value2}")

        if value1 < 11 and value1 + value2 < 20 and value2 < 11:
            self.label1.setText(str(value1 + 1))
            self.scores.append([value1 + 1, value2])
            self.points_progression.append(1)  # Aggiungi 1 per incrementare il comeback
            print(f"Appended 1 to points_progression: {self.points_progression}")
            self.update_comeback_and_length()
            self.update_graph()
            self.update_probability_graph()

    def increment_label2(self):
        """Incrementa il valore del secondo numero"""
        value1 = int(self.label1.text())
        value2 = int(self.label2.text())
        print(f"Incrementing label2. Current values: label1 = {value1}, label2 = {value2}")

        if value2 < 11 and value1 + value2 < 20 and value1 < 11:
            self.label2.setText(str(value2 + 1))
            self.scores.append([value1, value2 + 1])
            self.points_progression.append(0)  # Aggiungi 0 per diminuire il comeback
            print(f"Appended 0 to points_progression: {self.points_progression}")
            self.update_comeback_and_length()
            self.update_graph()
            self.update_probability_graph()

    def reset_labels(self):
        """Resetta entrambi i valori a zero"""
        print("Resetting labels...")
        self.label1.setText("0")
        self.label2.setText("0")
        self.probabilities = []
        self.points_progression = []
        self.log_reg_values = [0, 0]  # Reset both comeback and length
        self.scores = [[0, 0]]
        print(f"points_progression reset: {self.points_progression}")
        self.update_graph()
        self.update_probability_graph()

    def go_back(self):
        """Torna indietro di un passo nei punteggi"""
        print("Going back one step...")
        if len(self.scores) > 1:
            self.scores.pop()
            self.points_progression.pop()
            print(f"Removed last score. Current scores: {self.scores}")
            print(f"Removed last point from points_progression. Current points_progression: {self.points_progression}")
            self.update_comeback_and_length()
            last_score = self.scores[-1]
            self.label1.setText(str(last_score[0]))
            self.label2.setText(str(last_score[1]))
            self.axes_probability.clear()
            self.is_going_back = True
            self.update_graph()
            self.update_probability_graph()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    logreg_prob, lstm_prob = main_window.predict()
    sys.exit(app.exec_())
