import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QPushButton, QGraphicsView,
    QGraphicsScene, QMessageBox
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Imposta dimensioni della finestra
        self.setWindowTitle("Div con form e colori personalizzati")
        self.setGeometry(100, 100, 1400, 900)  # x, y, larghezza, altezza

        # Layout orizzontale principale
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
        left_layout = QVBoxLayout()  # Layout verticale per il contenuto del div sinistro
        left_layout.setAlignment(Qt.AlignTop)  # Allinea il contenuto in alto
        self.add_form_container(left_layout)  # Aggiungi il form contenitore
        self.add_bottom_div(left_layout)  # Aggiungi il div sotto il form

        self.left_div.setLayout(left_layout)

        # Div destro
        self.right_div = QWidget()
        self.right_div.setStyleSheet(""" 
            background-color: #2a2f33;  /* Sfondo grigio scuro */
        """)

        # Aggiungere i due "div" al layout principale
        main_layout.addWidget(self.left_div)  # Div sinistro
        main_layout.addWidget(self.right_div)  # Div destro

        # Imposta proporzioni dei "div"
        main_layout.setStretch(0, 2)  # Div sinistro occupa il 2/3 dello spazio
        main_layout.setStretch(1, 1)  # Div destro occupa il 1/3 dello spazio

        # Imposta il layout principale nella finestra
        self.setLayout(main_layout)

        # Crea la lista per i punteggi
        self.scores = [[0, 0]]  # Lista che contiene i punteggi precedenti

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
        form_layout.setContentsMargins(10, 10, 10, 10)  # Margini interni
        form_layout.setSpacing(20)  # Spaziatura tra i gruppi
        self.add_form_sections(form_layout)  # Aggiungi le sezioni del form
        form_container.setLayout(form_layout)

        # Aggiungi il contenitore al layout principale
        layout.addWidget(form_container)

    def add_form_sections(self, layout):
        """Aggiunge le sezioni del form al layout orizzontale"""

        # Sezione Gender
        gender_group = QGroupBox("")
        gender_layout = QVBoxLayout()
        gender_layout.setSpacing(10)  # Spaziatura interna al gruppo
        gender_layout.addWidget(QLabel("Gender_Utente:"))
        gender_layout.addWidget(QRadioButton("M"))
        gender_layout.addWidget(QRadioButton("W"))
        gender_layout.addWidget(QLabel("Gender_Avversario:"))
        gender_layout.addWidget(QRadioButton("M"))
        gender_layout.addWidget(QRadioButton("W"))
        gender_group.setLayout(gender_layout)
        gender_group.setStyleSheet("color: white;")  # Testo bianco nel gruppo

        # Sezione Is_Final_Set
        final_set_group = QGroupBox("")
        final_set_layout = QVBoxLayout()
        final_set_layout.setSpacing(10)  # Spaziatura interna al gruppo
        final_set_layout.addWidget(QLabel("Is_Final_Set_Utente:"))
        final_set_layout.addWidget(QRadioButton("True"))
        final_set_layout.addWidget(QRadioButton("False"))
        final_set_layout.addWidget(QLabel("Is_Final_Set_Avversario:"))
        final_set_layout.addWidget(QRadioButton("True"))
        final_set_layout.addWidget(QRadioButton("False"))
        final_set_group.setLayout(final_set_layout)
        final_set_group.setStyleSheet("color: white;")  # Testo bianco nel gruppo

        # Sezione Is_Final
        is_final_group = QGroupBox("")
        is_final_layout = QVBoxLayout()
        is_final_layout.setSpacing(10)
        is_final_layout.addWidget(QLabel("Is_Final:"))
        is_final_layout.addWidget(QRadioButton("True"))
        is_final_layout.addWidget(QRadioButton("False"))
        is_final_layout.addWidget(QLabel(""))  # Spazio vuoto

        is_final_group.setLayout(is_final_layout)
        is_final_group.setStyleSheet("color: white;")  # Testo bianco nel gruppo

        # Aggiungere le sezioni al layout principale in orizzontale
        layout.addWidget(gender_group)
        layout.addWidget(final_set_group)
        layout.addWidget(is_final_group)

    def add_bottom_div(self, layout):
        """Aggiungi un altro div sotto il form con numeri al centro"""

        # Nuovo div sotto il form con il colore specificato
        bottom_div = QWidget()
        bottom_div.setStyleSheet(""" 
            background-color: #1a1f23;  /* Nuovo colore di sfondo */
            color: white;  /* Testo bianco */
            border-radius: 5px;
            margin-top: 20px;
            padding: 10px;
            border: none; /* Rimuovi eventuali bordi che potrebbero causare la linea */
        """)

        # Imposta un'altezza minima per il bottom_div in modo che non sparisca se vuoto
        bottom_div.setMinimumHeight(100)  # Puoi cambiare il valore a seconda della tua esigenza

        # Layout per il nuovo div
        bottom_layout = QVBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)  # Assicurati che non ci siano margini extra
        bottom_layout.setSpacing(20)  # Impostiamo una spaziatura tra i widget
        bottom_layout.setAlignment(Qt.AlignCenter)  # Centra tutto il contenuto (numeri e bottoni) verticalmente

        # Crea il div verticale
        vertical_div = QWidget()
        vertical_div.setStyleSheet(""" 
            background-color: #1a1f23;  /* Colore di sfondo più scuro per il div verticale */
            color: white;
            border-radius: 5px;
            padding: 10px;
        """)

        # Layout verticale per il div
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)  # Rimuovi i margini
        vertical_layout.setSpacing(10)  # Spaziatura tra gli elementi
        vertical_layout.setAlignment(Qt.AlignCenter)  # Centra verticalmente e orizzontalmente

        # Crea il layout orizzontale per i numeri centrati
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)  # Rimuovi i margini
        horizontal_layout.setAlignment(Qt.AlignCenter)  # Allineamento orizzontale centrato

        # Crea i QLabel per i numeri
        self.label1 = QLabel("0")
        self.label2 = QLabel("0")

        self.label1.setStyleSheet(""" 
                font-size: 200px;  /* Dimensione font enorme per il primo numero */
                color: white;      /* Colore bianco per il testo */
            """)
        self.label2.setStyleSheet(""" 
                        font-size: 200px;  /* Dimensione font enorme per il primo numero */
                        color: white;      /* Colore bianco per il testo */
                    """)

        # Appendi i QLabel al layout orizzontale
        horizontal_layout.addWidget(self.label1)
        horizontal_layout.addWidget(self.label2)

        # Aggiungi il layout orizzontale al layout verticale
        vertical_layout.addLayout(horizontal_layout)

        # Aggiungere un nuovo div sotto i numeri con tre bottoni
        button_div = QWidget()
        button_div.setStyleSheet(""" 
            background-color: #1a1f23;  /* Sfondo simile a quello dei numeri */
            padding: 10px;
            margin-bottom: 20px;
        """)

        # Layout per i bottoni
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setAlignment(Qt.AlignCenter)  # Centra orizzontalmente i bottoni

        # Crea i bottoni a cerchio
        plus_button1 = QPushButton("+")
        plus_button2 = QPushButton("+")
        reset_button = QPushButton("x")
        back_button = QPushButton("←")

        for button in [plus_button1, plus_button2, reset_button, back_button]:
            button.setStyleSheet(""" 
                background-color: #768a89;  /* Colore di sfondo */
                color: white;  /* Testo bianco */
                font-size: 20px;  /* Dimensione del testo più piccola */
                padding: 0;  /* Rimuovi padding extra */
                border: 2px solid #1a1f23;  /* Bordo del cerchio */
                width: 60px;  /* Larghezza del bottone più piccola */
                height: 60px;  /* Altezza del bottone più piccola */
                border-radius: 30px;  /* Border radius per rendere il bottone circolare */
            """)

        # Aggiungi i bottoni nell'ordine specificato
        button_layout.addWidget(plus_button1)
        button_layout.addWidget(back_button)
        button_layout.addWidget(reset_button)
        button_layout.addWidget(plus_button2)

        # Aggiungi i bottoni al nuovo div
        button_div.setLayout(button_layout)

        # Aggiungi il div dei bottoni al layout verticale
        vertical_layout.addWidget(button_div)

        # Imposta il layout verticale sul div principale
        vertical_div.setLayout(vertical_layout)

        # Aggiungi il div verticale al layout principale
        bottom_layout.addWidget(vertical_div)

        # Aggiungi il grafico sotto i numeri
        self.add_graph(bottom_layout)

        # Imposta il layout del bottom_div
        bottom_div.setLayout(bottom_layout)

        # Aggiungi il bottom_div al layout principale
        layout.addWidget(bottom_div)

        # Connetti i bottoni alle funzioni
        plus_button1.clicked.connect(self.increment_label1)
        plus_button2.clicked.connect(self.increment_label2)
        reset_button.clicked.connect(self.reset_labels)
        back_button.clicked.connect(self.go_back)

    def add_graph(self, layout):
        """Aggiunge un grafico sotto i numeri"""

        # Crea il canvas del grafico
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)  # Dimensioni aumentate
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # Impostazioni iniziali del grafico
        self.axes.set_title("Andamento dei Punti")
        self.axes.set_xlabel("Tempo")
        self.axes.set_ylabel("Punti")

        # Linee per i punteggi dell'utente e dell'avversario
        self.user_points, = self.axes.plot([], [], label="Utente", color='blue', lw=2)
        self.opponent_points, = self.axes.plot([], [], label="Avversario", color='red', lw=2)

        # Aggiungi la legenda
        self.axes.legend()

        # Imposta il layout del grafico nel layout principale
        layout.addWidget(self.canvas)

    from PyQt5.QtWidgets import QMessageBox

    def increment_label1(self):
        """Incrementa il primo numero"""
        current_value = int(self.label1.text())
        current_value2 = int(self.label2.text())

        # Se la somma dei due punteggi è minore di 11, si può incrementare
        if current_value < 11 and current_value2 < 11:
            self.label1.setText(str(current_value + 1))
            self.scores.append([int(self.label1.text()), current_value2])
            self.update_graph()

        # Controlla se un giocatore ha raggiunto 11
        if current_value + 1 == 11:
            self.show_victory_message("Utente")
            self.disable_buttons()

    def increment_label2(self):
        """Incrementa il secondo numero"""
        current_value = int(self.label2.text())
        current_value1 = int(self.label1.text())

        # Se la somma dei due punteggi è minore di 11, si può incrementare
        if current_value < 11 and current_value1 < 11:
            self.label2.setText(str(current_value + 1))
            self.scores.append([current_value1, int(self.label2.text())])
            self.update_graph()

        # Controlla se un giocatore ha raggiunto 11
        if current_value + 1 == 11:
            self.show_victory_message("Avversario")
            self.disable_buttons()

    def show_victory_message(self, winner):
        """Mostra il messaggio di vittoria"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Vittoria!")
        msg.setText(f"Ha vinto {winner}!")
        msg.exec_()

    def disable_buttons(self):
        """Disabilita i bottoni dopo la vittoria"""
        for button in [self.plus_button1, self.plus_button2, self.reset_button, self.back_button]:
            button.setEnabled(False)

    def reset_labels(self):
        """Resetta entrambi i numeri"""
        self.label1.setText("0")
        self.label2.setText("0")
        self.scores.append([0, 0])
        self.update_graph()

    def go_back(self):
        """Torna indietro all'ultimo stato"""
        if len(self.scores) > 1:
            self.scores.pop()  # Rimuovi l'ultimo punteggio
            last_score = self.scores[-1]  # Prendi l'ultimo punteggio valido
            self.label1.setText(str(last_score[0]))
            self.label2.setText(str(last_score[1]))
            self.update_graph()

    def update_graph(self):
        """Aggiorna il grafico"""
        # Estrai i punteggi dall'elenco
        user_scores = [score[0] for score in self.scores]
        opponent_scores = [score[1] for score in self.scores]

        # Imposta i dati sulle linee
        self.user_points.set_data(range(len(user_scores)), user_scores)
        self.opponent_points.set_data(range(len(opponent_scores)), opponent_scores)

        # Rendi il grafico dinamico
        self.axes.relim()
        self.axes.autoscale_view()

        # Rende il grafico visibile
        self.canvas.draw()


# Avvio dell'applicazione
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
