import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QRadioButton, QGroupBox, QPushButton, QGraphicsView,
    QGraphicsScene, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Imposta dimensioni della finestra
        self.setWindowTitle("Div con form e colori personalizzati")
        self.setGeometry(100, 100, 1400, 700)  # x, y, larghezza, altezza

        self.is_fullscreen = False

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
        main_layout.addWidget(self.left_div)
        main_layout.addWidget(self.right_div)

        # Imposta proporzioni dei "div"
        main_layout.setStretch(0, 1)  # Div sinistro occupa il 2/3 dello spazio
        main_layout.setStretch(1, 1)  # Div destro occupa il 1/3 dello spazio

        # Imposta il layout principale nella finestra
        self.setLayout(main_layout)

        # Crea la lista per i punteggi
        self.scores = [[0, 0]]  # Lista che contiene i punteggi precedenti

    def keyPressEvent(self, event):
        """Gestisce la pressione dei tasti"""
        if event.key() == Qt.Key_Escape:
            if self.is_fullscreen:
                self.showNormal()  # Passa alla modalità finestra normale
            else:
                self.showFullScreen()  # Passa alla modalità fullscreen
            # Inverte lo stato della finestra
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

        # Aggiungi il contenitore al layout principale
        layout.addWidget(form_container)

    def add_form_sections(self, layout):

        # Sezione Gender
        gender_group = QGroupBox("")
        gender_layout = QVBoxLayout()
        gender_layout.setSpacing(10)
        gender_layout.addWidget(QLabel("Gender_Utente:"))
        gender_layout.addWidget(QRadioButton("M"))
        gender_layout.addWidget(QRadioButton("W"))
        gender_layout.addWidget(QLabel("Gender_Avversario:"))
        gender_layout.addWidget(QRadioButton("M"))
        gender_layout.addWidget(QRadioButton("W"))
        gender_group.setLayout(gender_layout)
        gender_group.setStyleSheet("color: white;")

        # Sezione Is_Final_Set
        final_set_group = QGroupBox("")
        final_set_layout = QVBoxLayout()
        final_set_layout.setSpacing(10)
        final_set_layout.addWidget(QLabel("Is_Final_Set_Utente:"))
        final_set_layout.addWidget(QRadioButton("True"))
        final_set_layout.addWidget(QRadioButton("False"))
        final_set_layout.addWidget(QLabel("Is_Final_Set_Avversario:"))
        final_set_layout.addWidget(QRadioButton("True"))
        final_set_layout.addWidget(QRadioButton("False"))
        final_set_group.setLayout(final_set_layout)
        final_set_group.setStyleSheet("color: white;")

        # Sezione Is_Final
        is_final_group = QGroupBox("")
        is_final_layout = QVBoxLayout()
        is_final_layout.setSpacing(10)
        is_final_layout.addWidget(QLabel("Is_Final:"))
        is_final_layout.addWidget(QRadioButton("True"))
        is_final_layout.addWidget(QRadioButton("False"))
        is_final_layout.addWidget(QLabel(""))

        is_final_group.setLayout(is_final_layout)
        is_final_group.setStyleSheet("color: white;")

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
        gender_group.setVisible(False)
        final_set_group.setVisible(False)
        is_final_group.setVisible(False)

        # Memorizza i gruppi in una lista per gestire visibilità
        self.radio_groups = [gender_group, final_set_group, is_final_group]

        # Layout per i bottoni di "Mostra Tutto" e "Reset"
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.toggle_button)
        button_layout.addWidget(self.reset_button)

        # Aggiungere i gruppi e i bottoni al layout
        layout.addWidget(gender_group)
        layout.addWidget(final_set_group)
        layout.addWidget(is_final_group)
        layout.addLayout(button_layout)

    def toggle_radio_buttons(self):
        """Mostra o nasconde i radio button"""
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

        # Codice esistente per la creazione di `bottom_div`
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

        # Layout per il nuovo div
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
        bottom_div.setFixedHeight(450)
        # Layout verticale per il div
        vertical_layout = QVBoxLayout()
        vertical_layout.setContentsMargins(0, 0, 0, 0)
        vertical_layout.setSpacing(10)
        vertical_layout.setAlignment(Qt.AlignCenter)

        # Crea il layout orizzontale per i numeri centrati
        horizontal_layout = QHBoxLayout()
        horizontal_layout.setContentsMargins(0, 0, 0, 0)
        horizontal_layout.setAlignment(Qt.AlignCenter)
        # Crea i QLabel
        self.label1 = QLabel("0")
        self.label2 = QLabel("0")
        self.label3 = QLabel("-")

        # Imposta larghezza fissa per ciascun QLabel
        max_width = 240
        self.label1.setFixedWidth(max_width)
        self.label2.setFixedWidth(max_width)
        self.label3.setFixedWidth(max_width)

        # Aggiungi gli stili per tutte le etichette
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

                # Pulsante blu
        self.plus_button1.setStyleSheet(""" 
            background-color:#013FB3;
            font-size: 15px;
            color: white;
            font-weight: bold;
            padding: 0;
            border: 2px solid #1a1f23;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            margin-right: 100px;
            margin-left: 100px;
        """)

        # Pulsante rosso
        self.plus_button2.setStyleSheet(""" 
            background-color: #FF6600;
            font-size: 15px;
            color: white;
            font-weight: bold;
            padding: 0;
            border: 2px solid #1a1f23;
            width: 40px;
            height: 40px;
            border-radius: 20px;
            margin-right: 100px;
            margin-left: 100px;
        """)

        # Pulsante verde
        self.back_button.setStyleSheet(""" 
            background-color:#000000;
            font-size: 15px;
            color: white;
            font-weight: bold;
            padding: 0;
            border: 2px solid #1a1f23;
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

        # Aggiungi il div dei bottoni al layout verticale
        vertical_layout.addWidget(button_div)

        # Imposta il layout verticale sul div principale
        vertical_div.setLayout(vertical_layout)

        # Aggiungi il div verticale al layout principale
        bottom_layout.addWidget(vertical_div)

        # Imposta il layout del bottom_div
        bottom_div.setLayout(bottom_layout)

        # Aggiungi il bottom_div al layout principale
        layout.addWidget(bottom_div)

        # Connetti i bottoni alle funzioni
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

    def add_graph(self, layout):
        """Aggiunge un grafico sotto i numeri"""

        # Crea il canvas del grafico
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        # Impostazioni iniziali del grafico
        self.update_graph()

        # Aggiungi il canvas al layout
        layout.addWidget(self.canvas)

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
        self.axes.plot(x_values, y1_values, label="Player 1", marker='o', color="#013FB3")
        self.axes.plot(x_values, y2_values, label="Player 2", marker='o', color="#FF6600")

        self.axes.set_title("Score Progression")
        self.axes.set_xlabel("Points Played")
        self.axes.set_ylabel("Points Won")
        self.axes.legend()

        # Aggiorna il canvas
        self.canvas.draw()

    def increment_label1(self):
        """Incrementa il valore del primo numero"""
        value1 = int(self.label1.text())
        value2 = int(self.label2.text())
        if value1 < 11 and value1 + value2 < 20:
            self.label1.setText(str(value1 + 1))
            self.scores.append([value1 + 1, value2])
            self.update_graph()

    def increment_label2(self):
        """Incrementa il valore del secondo numero"""
        value1 = int(self.label1.text())
        value2 = int(self.label2.text())
        if value2 < 11 and value1 + value2 < 20:
            self.label2.setText(str(value2 + 1))
            self.scores.append([value1, value2 + 1])
            self.update_graph()

    def reset_labels(self):
        """Resetta entrambi i valori a zero"""
        self.label1.setText("0")
        self.label2.setText("0")
        self.scores = [[0, 0]]
        self.update_graph()

    def go_back(self):
        """Torna indietro di un passo nei punteggi"""
        if len(self.scores) > 1:
            self.scores.pop()
            last_score = self.scores[-1]
            self.label1.setText(str(last_score[0]))
            self.label2.setText(str(last_score[1]))
            self.update_graph()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
