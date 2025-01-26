import math
import sys
import numpy as np
import os
from keras.src.utils import pad_sequences
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
TF_ENABLE_ONEDNN_OPTS = 0
import sklearn
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QPushButton
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QWidget):
    is_going_back = False
    points_progression = []
    lstm_values = [0, 0]
    scores = [[0, 0]]
    def __init__(self):
        super().__init__()

        self.model_lstm = load_model('../data/models/LSTM.keras')  # Carica il modello LSTM

        # Imposta dimensioni della finestra
        self.probabilities = None
        self.setWindowTitle("Div con form e colori personalizzati")
        self.setGeometry(100, 100, 1400, 700)  # x, y, larghezza, altezza

        # Mostra la finestra a tutto schermo
        self.showFullScreen()
        self.is_fullscreen = True
        self.setFocus()

        main_layout = QHBoxLayout()
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
        self.add_left_div(left_layout)

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

    # Predizione quando ci troviamo nel punteggio corrente
    def pred1(self):
        num_ones = self.points_progression.count(1)
        num_zeros = self.points_progression.count(0)
        if len(self.points_progression) > 18 or len(self.points_progression) < 7 or abs(num_ones - num_zeros) > 3 or num_ones == 10 or num_zeros == 10:
            '''Caso in cui le condizioni non sono verificate
            print("Non possibile")
            '''
            self.current_prob_label_left.setText(f"Punteggio Corrente: NAN")
            return None
        else:
            X_seq = pad_sequences([self.points_progression], maxlen=18, padding='post', truncating='post',
                                  value=-1)
            X_global_lstm = np.array([self.lstm_values])
            y_pred_prob_lstm = self.model_lstm.predict([X_seq, X_global_lstm])
            y_pred_lstm = (y_pred_prob_lstm > 0.5).astype(int)

            ''' Debug LSTM
            print(f"Sequenza di Punti (LSTM): {self.points_progression}")
            print(f"Caratteristiche Globali (LSTM): {self.lstm_values}")
            print(f"Probabilità previste (LSTM): {y_pred_prob_lstm[0][0]:.4f}")
            print(f"Predizione (LSTM - classe): {y_pred_lstm[0]}")
            print("-" * 50)
            '''
            self.current_prob_label_left.setText(f"Punteggio Corrente: {y_pred_prob_lstm[0][0] * 100:.4f}%")

    # Predizione quando ci troviamo nel caso in cui playerA fa punto a partire dal punteggio corrente
    def pred2(self):
        points_progression_playerA = self.points_progression.copy()
        points_progression_playerA.append(1)
        num_ones = points_progression_playerA.count(1)
        num_zeros = points_progression_playerA.count(0)
        if len(points_progression_playerA) > 18 or len(points_progression_playerA) < 7 or abs(num_ones - num_zeros) > 3 or num_ones == 10 or num_zeros == 10:
            '''Caso in cui le condizioni non sono verificate
            print("Non possibile")
            '''
            self.playerA_prob_label_left.setText(f"playerA fa punto: NAN")
            return None
        else:
            X_seq = pad_sequences([points_progression_playerA], maxlen=18, padding='post', truncating='post',
                                  value=-1)
            X_global_lstm = np.array([self.lstm_values])
            y_pred_prob_lstm = self.model_lstm.predict([X_seq, X_global_lstm])
            y_pred_lstm = (y_pred_prob_lstm > 0.5).astype(int)

            ''' Debug LSTM playerA
            print(f"Sequenza di Punti (LSTM): {points_progression_playerA}")
            print(f"Caratteristiche Globali (LSTM): {self.lstm_values}")
            print(f"Probabilità previste (LSTM): {y_pred_prob_lstm[0][0]:.4f}")
            print(f"Predizione (LSTM - classe): {y_pred_lstm[0]}")
            print("-" * 50) '''

            self.playerA_prob_label_left.setText(f"Player A fa punto: {y_pred_prob_lstm[0][0] * 100:.4f}%")
            return y_pred_prob_lstm[0][0]

    # Predizione quando ci troviamo nel caso in cui playerB fa punto a partire dal punteggio corrente
    def pred3(self):
        points_progression_playerB = self.points_progression.copy()
        points_progression_playerB.append(0)
        num_ones = points_progression_playerB.count(1)
        num_zeros = points_progression_playerB.count(0)
        if len(points_progression_playerB) > 18 or len(points_progression_playerB) < 7 or abs(num_ones - num_zeros) > 3 or num_ones == 10 or num_zeros == 10:
            '''Caso in cui le condizioni non sono verificate
            print("Non possibile")
            '''
            self.playerB_prob_label_left.setText(f"Player B fa punto: NAN")
            return None
        else:
            X_seq = pad_sequences([points_progression_playerB], maxlen=18, padding='post', truncating='post',
                                  value=-1)
            X_global_lstm = np.array([self.lstm_values])
            y_pred_prob_lstm = self.model_lstm.predict([X_seq, X_global_lstm])
            y_pred_lstm = (y_pred_prob_lstm > 0.5).astype(int)

            ''' Debug LSTM playerB
            print(f"Sequenza di Punti (LSTM): {points_progression_playerB}")
            print(f"Caratteristiche Globali (LSTM): {self.lstm_values}")
            print(f"Probabilità previste (LSTM): {y_pred_prob_lstm[0][0]:.4f}")
            print(f"Predizione (LSTM - classe): {y_pred_lstm[0]}")
            print("-" * 50)
            '''
            self.playerB_prob_label_left.setText(f"playerB fa punto: {y_pred_prob_lstm[0][0] * 100:.4f}%")
            return y_pred_prob_lstm[0][0]

    # Gestisce la pressione dei tasti
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            if self.is_fullscreen:
                self.showNormal()  # Passa alla modalità finestra normale
            else:
                self.showFullScreen()  # Passa alla modalità fullscreen
            self.is_fullscreen = not self.is_fullscreen

    # Contenitore form
    def add_form_container(self, layout):
        # Contenitore per il form
        form_container = QWidget()
        form_container.setStyleSheet(""" 
            background-color: #1a1f23;  
            color: white;  
            border: 0px solid #444; 
            border-radius: 5px;
        """)
        form_layout = QHBoxLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(10)
        self.add_form_sections(form_layout)
        form_container.setLayout(form_layout)
        layout.addWidget(form_container)

    # Raggruppamento dentro il form_container
    def add_form_sections(self, layout):
        # Gruppo per Utente
        utente_group = QGroupBox("")
        utente_layout = QVBoxLayout()
        utente_layout.setSpacing(5)
        utente_layout.addWidget(QLabel("Final_Set_A", alignment=Qt.AlignCenter))  # Centrare il titolo
        self.utente_radio_true = QRadioButton("1")
        self.utente_radio_false = QRadioButton("0")
        utente_layout.addWidget(self.utente_radio_true, alignment=Qt.AlignCenter)  # Centrare i radio button
        utente_layout.addWidget(self.utente_radio_false, alignment=Qt.AlignCenter)
        utente_group.setLayout(utente_layout)
        utente_group.setStyleSheet("color: white;")
        self.utente_radio_true.toggled.connect(self.update_lstm_values)

        # Gruppo per Avversario
        avversario_group = QGroupBox("")
        avversario_layout = QVBoxLayout()
        avversario_layout.setSpacing(5)
        avversario_layout.addWidget(QLabel("Final_Set_B", alignment=Qt.AlignCenter))  # Centrare il titolo
        self.avversario_radio_true = QRadioButton("1")
        self.avversario_radio_false = QRadioButton("0")
        avversario_layout.addWidget(self.avversario_radio_true, alignment=Qt.AlignCenter)  # Centrare i radio button
        avversario_layout.addWidget(self.avversario_radio_false, alignment=Qt.AlignCenter)
        avversario_group.setLayout(avversario_layout)
        avversario_group.setStyleSheet("color: white;")
        self.avversario_radio_true.toggled.connect(self.update_lstm_values)

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

        # Aggiungere i gruppi e il bottone al layout principale
        layout.addWidget(utente_group, alignment=Qt.AlignCenter)  # Centrare il gruppo Final_Set_A
        layout.addWidget(avversario_group, alignment=Qt.AlignCenter)  # Centrare il gruppo Final_Set_B
        layout.addWidget(self.reset_button)  # Centrare il pulsante Reset

    # Aggiorna i valori in lstm_values in base ai radio button selezionati
    def update_lstm_values(self):
        self.lstm_values[0] = 1 if self.utente_radio_true.isChecked() else 0
        self.lstm_values[1] = 1 if self.avversario_radio_true.isChecked() else 0
        '''Debug per verificare che i radio button funzionino 
        print(f"Updated lstm_values: {self.lstm_values}")
        '''

    # Inserimento di un altro div al di sotto del contenitore dei form
    def add_left_div(self, layout):
        if not hasattr(self, 'scores'):
            self.scores = [[0, 0]]

        left_div = QWidget()
        left_div.setStyleSheet(""" 
            background-color: #1a1f23;  /* Nuovo colore di sfondo */
            color: white;  /* Testo bianco */
            border-radius: 5px;
            margin-top: 5px;
            padding: 10px;
            border: none;
        """)

        left_div.setMinimumHeight(100)
        left_div.setFixedHeight(450)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(20)
        left_layout.setAlignment(Qt.AlignCenter)

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


        left_layout.addWidget(vertical_div)
        left_div.setLayout(left_layout)
        layout.addWidget(left_div)

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

        graph_layout = QVBoxLayout()
        graph_layout.setContentsMargins(0, 0, 0, 0)
        graph_layout.setSpacing(10)

        # Aggiungere il grafico usando la funzione esistente
        self.add_graph(graph_layout)
        graph_div.setFixedHeight(400)
        graph_div.setLayout(graph_layout)
        layout.addWidget(graph_div)

    # Inserimento di un div destro
    def add_right_div(self, layout):
        # Creazione di un layout verticale principale
        main_layout = QVBoxLayout()

        # Creazione del primo div (Probabilità LSTM)
        left_div = QWidget()
        left_div.setStyleSheet("""
            background-color: #1a1f23;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 10px;
            padding: 10px;
            border: 0px solid;
        """)
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(0)

        # Titolo per le probabilità LSTM
        title_label_left = QLabel("Probabilità LSTM")
        title_label_left.setAlignment(Qt.AlignCenter)
        title_label_left.setStyleSheet("""
            font-size: 18px;
            color: #f0f0f0;
            font-weight: bold;
        """)

        # Etichette delle probabilità LSTM
        self.current_prob_label_left = QLabel("Probabilità Corrente: NAN")
        self.playerA_prob_label_left = QLabel("Player A fa punto: NAN")
        self.playerB_prob_label_left = QLabel("Player B fa punto: NAN")

        # Aggiungo il titolo e le label al layout del div LSTM
        left_layout.addWidget(title_label_left)
        for label in [self.current_prob_label_left, self.playerA_prob_label_left, self.playerB_prob_label_left]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                font-size: 14px;
                color: white;
            """)
            left_layout.addWidget(label)

        left_div.setLayout(left_layout)

        # Creazione del secondo div per la probabilità matematica
        text_div = QWidget()
        text_div.setStyleSheet("""
            background-color: #1a1f23;
            border-radius: 5px;
            margin-top: 10px;
            margin-bottom: 10px;
            padding: 10px;
            border: 0px solid;
        """)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(10, 10, 10, 10)
        text_layout.setSpacing(0)

        # Titolo per le probabilità Matematiche
        title_label = QLabel("Probabilità Matematica")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 18px;
            color: #f0f0f0;
            font-weight: bold;
        """)

        # Etichette delle probabilità Matematiche
        self.current_prob_label = QLabel("Probabilità Corrente: 50%")
        self.current_prob_vant_label = QLabel("Probabilità Corrente: 50%")
        self.playerA_prob_label = QLabel("Player A fa punto: 50%")
        self.playerB_prob_label = QLabel("Player B fa punto: 50%")


        text_layout.addWidget(title_label)
        for label in [self.current_prob_label,self.current_prob_vant_label,  self.playerA_prob_label, self.playerB_prob_label]:
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("""
                font-size: 14px;
                color: white;
            """)
            text_layout.addWidget(label)

        text_div.setLayout(text_layout)

        # Div inferiore che contiene il grafico
        lower_div = QWidget()
        lower_div.setStyleSheet("""
            background-color: #1a1f23;
            border-radius: 5px;
            margin: 10px;
            padding: 10px;
        """)
        lower_div.setFixedHeight(500)
        lower_layout = QVBoxLayout()
        lower_layout.setContentsMargins(10, 10, 10, 10)
        lower_layout.setSpacing(0)

        # Aggiungere il grafico usando la funzione esistente
        self.add_probability_graph(lower_layout)
        lower_div.setLayout(lower_layout)

        # Aggiungere i div al layout verticale principale
        main_layout.addWidget(left_div)
        main_layout.addWidget(text_div)

        # Aggiungere il div inferiore per il grafico
        layout.addLayout(main_layout)
        layout.addWidget(lower_div)

        # Rimuovere lo spazio residuo per non occupare tutto lo spazio
        layout.addStretch()

    # Aggiunge un grafo che mostra l'andamento della partita
    def add_graph(self, layout):

        # Crea il canvas del grafico
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # Impostazioni iniziali del grafico
        self.update_graph()
        layout.addWidget(self.canvas)

    # Aggiunge un grafico per la probabilità di vincere
    def add_probability_graph(self, layout):
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
        self.axes.plot(x_values, y1_values, label="Player A", marker = 'o', color="#013FB3")
        self.axes.plot(x_values, y2_values, label="Player B", marker='o', color="#FF6600")
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
        lstm_scenario1 = None # Probabilità di vincita nel caso playerA fa punto
        lstm_scenario2 = None # Probabilità di vincita nel caso playerB fa punto

        # Caso speciale: Se value1 == 11, la probabilità è 1
        if value1 == 11:
            prob_value = 1.0
            prob_vantaggio = 0  # Probabilità di raggiungere i vantaggi
        elif value2 == 11:
            prob_value = 0.0
            prob_vantaggio = 0  # Probabilità di raggiungere i vantaggi
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

        if value1 + value2 == 20:
            prob_vantaggio = 1

        # Calcola le probabilità per gli scenari futuri
        elif value1 + value2 < 20 and value1 < 11 and value2 < 11:  # Solo se non siamo alla fine del gioco
            prob_vantaggio = self.prob_vant(p, value1, value2)
            if value1 == 10:
                prob_scenario1 = 1
                prob_scenario2 = self.prob(p, value1, value2 + 1)
            elif value2 == 10:
                prob_scenario1 = self.prob(p, value1 + 1, value2)
                prob_scenario2 = 0
            else:
                prob_scenario1 = self.prob(p, value1 + 1, value2)
                lstm_scenario1 = self.pred2()
                prob_scenario2 = self.prob(p, value1, value2 + 1)
                lstm_scenario2 = self.pred3()

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

            offset_increment = 5

            # Annotazioni per gli scenari lstm
            if lstm_scenario1 is not None:
                self.axes_probability.plot(
                    [current_x, future_x],
                    [prob_value, lstm_scenario1],
                    linestyle="--", color="orange", label="Punto_Player_1_Lstm"
                )
                if abs(prob_scenario1 - lstm_scenario1) < 0.1:
                    # Aggiungi la percentuale a destra del pallino
                    y_offset = (lstm_scenario1 > prob_scenario1) * offset_increment * 2 or (
                            prob_scenario1 > lstm_scenario1) * offset_increment * -2
                    self.axes_probability.annotate(f"{lstm_scenario1:.4f}", (future_x, lstm_scenario1),
                                                   textcoords="offset points", xytext=(10, y_offset), ha='left',
                                                   color="orange")

            if lstm_scenario2 is not None:
                self.axes_probability.plot(
                    [current_x, future_x],
                    [prob_value, lstm_scenario2],
                    linestyle="--", color="purple", label="Punto_Player_2_Lstm"
                )
                if abs(prob_scenario2 - lstm_scenario2) < 0.1:
                    # Aggiungi la percentuale a destra del pallino
                    y_offset = (lstm_scenario2 > prob_scenario2) * offset_increment * 2 or (
                            prob_scenario2 > lstm_scenario2) * offset_increment * -2
                    self.axes_probability.annotate(f"{lstm_scenario2:.4f}", (future_x, lstm_scenario2),
                                                   textcoords="offset points", xytext=(10, y_offset), ha='left',
                                                   color="purple")

            # Aggiungi i pallini alle estremità delle linee tratteggiate
            self.axes_probability.scatter([future_x], [prob_scenario1], color="green", marker='o')
            self.axes_probability.scatter([future_x], [prob_scenario2], color="red", marker='o')
            self.axes_probability.scatter([future_x], [lstm_scenario1], color="orange", marker='o')
            self.axes_probability.scatter([future_x], [lstm_scenario2], color="purple", marker='o')

            # Aggiungi la percentuale a destra del pallino per gli scenari futuri
            self.axes_probability.annotate(f"{prob_scenario1:.4f}", (future_x, prob_scenario1),
                                           textcoords="offset points", xytext=(10,-3), ha='left', color="green")
            self.axes_probability.annotate(f"{prob_scenario2:.4f}", (future_x, prob_scenario2),
                                           textcoords="offset points", xytext=(10,-3), ha='left', color="red")
            self.playerA_prob_label.setText(f"Player A fa punto: {prob_scenario1 * 100:.4f}%")
            self.playerB_prob_label.setText(f"Player B fa punto: {prob_scenario2 * 100:.4f}%")

        total_points = value1 + value2
        half_visible = 5  # Range minimo visibile
        buffer = half_visible // 2  # Valore a cui iniziare ad espandere

        # Determina il range dinamico
        start_x = max(0, total_points - buffer)  # Espande solo dopo aver superato metà del range
        end_x = min(20, start_x + half_visible)  # Mantiene sempre almeno 8 punti visibili

        # Configurazione dell'asse
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
        self.current_prob_label.setText(f"Probabilità Corrente: {prob_value * 100:.4f} %")
        if prob_vantaggio != None:
            self.current_prob_vant_label.setText(f"Probabilità Vantaggio: {prob_vantaggio * 100:.4f}%")
        else:
            self.current_prob_vant_label.setText(f"Probabilità Vantaggio: NAN")

        # Aggiorna il canvas
        self.canvas_probability.draw()

    # Funzione matematica per calcolare la probabilità di vittoria
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

    # Probabilità di arrivare 10-10
    def prob_vant(self, p, x, y):
        total = p ** (10 - x) * math.comb(20 - x - y, 10 - x) * (1 - p) ** (10 - y)
        return total

    # Funzione per incrementare lo score del playerA
    def increment_label1(self):
        value1 = int(self.label1.text())
        value2 = int(self.label2.text())
        '''Verifica del corretto funzionamento della funzione 
        print(f"Incrementing label1. Current values: label1 = {value1}, label2 = {value2}")
        '''
        if value1 < 11 and value1 + value2 < 20 and value2 < 11:
            self.label1.setText(str(value1 + 1))
            self.scores.append([value1 + 1, value2])
            '''Verifica del corretto funzionamento della funzione 
            print(f"label1 incremented. Current values: label1 = {value1}, label2 = {value2}")
            '''
            self.points_progression.append(1)  # Aggiungi 1 per incrementare il comeback
            '''
            print(f"Appended 1 to points_progression: {self.points_progression}")
            '''
            self.pred1()
            self.update_graph()
            self.update_probability_graph()

    # Funzione per incrementare lo score del playerB
    def increment_label2(self):
        value1 = int(self.label1.text())
        value2 = int(self.label2.text())
        '''Verifica del corretto funzionamento della funzione 
        print(f"Incrementing label2. Current values: label1 = {value1}, label2 = {value2}")
        '''
        if value2 < 11 and value1 + value2 < 20 and value1 < 11:
            self.label2.setText(str(value2 + 1))
            self.scores.append([value1, value2 + 1])
            '''Verifica del corretto funzionamento della funzione 
            print(f"label2 incremented. Current values: label1 = {value1}, label2 = {value2}")
            '''
            self.points_progression.append(0)
            '''
            print(f"Appended 0 to points_progression: {self.points_progression}")
            '''
            self.pred1()
            self.update_graph()
            self.update_probability_graph()

    # Funzione per poter reiniziare da capo
    def reset_labels(self):
        '''Verifica del corretto funzionamento della funzione
        print("Resetting labels...")
        '''
        self.label1.setText("0")
        self.label2.setText("0")
        self.probabilities = []
        self.points_progression = []
        self.scores = [[0, 0]]
        self.pred1()
        '''
        print(f"points_progression reset: {self.points_progression}") '''
        self.update_graph()
        self.update_probability_graph()

    # Funzione per poter tornare indietro di un'istanza
    def go_back(self):
        if len(self.scores) > 1:
            self.scores.pop() # Rimozione dell'ultimo scores valore inserito
            self.points_progression.pop() # Rimozione dell'ultimo elemento nella progressione dello score
            ''' Verifica delle rimozioni eseguite con successo
            print(f"Removed last score. Current scores: {self.scores}")
            print(f"Removed last point from points_progression. Current points_progression: {self.points_progression}")
            '''
            self.pred1()
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
    sys.exit(app.exec_())
