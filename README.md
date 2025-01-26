# TTinsight

<div align="center">
  <img src="https://github.com/user-attachments/assets/65354228-520d-400d-aeeb-59dc69f6a848" alt="TTinsight logo" width="250">
</div>

**TTinsight** is an advanced system for predicting table tennis set outcomes. It leverages sequential LSTM neural networks to analyze score progression patterns and deliver accurate set result predictions.

---

## Key Features

<div>
  <ul>
    <li><strong>Outcome Prediction</strong>: Real-time predictions for set results.</li>
    <li><strong>Sequence Analysis</strong>: Utilizes LSTMs to identify recurring score patterns.</li>
    <li><strong>Data Flexibility</strong>: Compatible with custom score progression datasets.</li>
  </ul>
</div>

**This project is currently under active development. Features and functionality may change as the system evolves.**

---

## Repository Structure

The general structure of the **TTinsight** project is as follows:

```bash
.
├── data
│   ├── additional_data
│   │   ├── unavailable_score_tournaments
│   │   │   ├── ...
│   │   ├── players_metadata.tsv
│   │   └── tournaments_metadata.tsv
│   ├── datasets
│   │   ├── cleaned_dataset.csv
│   │   ├── raw_dataset.csv
│   │   └── single_matches_dataset.csv
│   ├── matches
│   │   ├── ...
│   ├── models
│   │   ├── LogReg.pkl
│   │   └── LSTM.keras
│   └── tournaments
│       ├── ...
├── data_preprocessing
│   ├── dataset-generator.py
│   └── downloader-scores.py
├── gui
│   ├── gui-test.py
│   └── TTinsight_GUI_explanation.png
├── README.md
├── requirements.txt
├── TTinsight_DataPreprocessing.ipynb
└── TTinsight_ModelDevelopment.ipynb
```

<h3>Summary of some files</h3>

<div style="font-family: monospace; padding: 10px; margin-bottom: 20px;">
  <ul>
    <li><strong>data/</strong>
      <ul>
        <li><strong>additional_data</strong>
          <ul>
            <li><code>players_metadata.tsv</code>: Contains player IDs and nationality, <em>not yet included in the project but may be added later.</em></li>
            <li><code>tournaments_metadata.tsv</code>: Holds metadata <em>not relevant for the current analysis.</em></li>
          </ul>
        </li>
        <li><strong>datasets</strong>
          <ul>
            <li><code>cleaned_dataset.csv</code>: Used for model training and testing, <em>derived from modifications made to the raw dataset.</em> Contains relevant match data.</li>
            <li><code>raw_dataset.csv</code>: Initial dataset with inaccuracies and irrelevant features that need to be cleaned and adjusted.</li>
          </ul>
        </li>
        <li><strong>models/</strong>
          <ul>
            <li><code>LogReg.pkl</code>: 
              <p>Predicts match set outcomes (<em>win/loss</em>) based on scores and match dynamics.</p>
              <p><strong>Training:</strong> Logistic Regression on standardized data.</p>
              <p><strong>Evaluation:</strong> Cross-validation with Log Loss and Brier Score for performance check.</p>
              <p><strong>Hyperparameter Tuning:</strong> Optimized using GridSearchCV with regularization and solver adjustments.</p>
              <p><strong>Saving:</strong> Best model saved as a <code>.pkl</code> file for future predictions.</p>
            </li>
            <li><code>LSTM.keras</code>: 
              <p>Captures temporal match dynamics, predicting outcomes from point sequences and global features.</p>
              <p><strong>Data Preparation:</strong> Sequences padded to a fixed length and global features integrated.</p>
              <ul>
                <li><strong>LSTM Layers:</strong> Handle point sequences.</li>
                <li><strong>Dense Layer:</strong> Combine global features.</li>
                <li><strong>Dropout Layer:</strong> Prevents overfitting, followed by final Dense layer with sigmoid for binary classification.</li>
              </ul>
              <p><strong>Training and Evaluation:</strong> 20 epochs, binary cross-entropy loss, evaluated with Log Loss and Brier Score.</p>
              <p><strong>Testing:</strong> Detects comeback scenarios <em>effectively, unlike Logistic Regression.</em></p>
            </li>
          </ul>
        </li>
        <li><strong>data_preprocessing/</strong>
          <ul>
            <li><code>dataset-generator.py</code>
              <p>Processes match logs, validates scores, and creates a cleaned dataset for analysis.</p>
              <ul>
                <li><em>Validates scores ensuring minimum standards and valid score differences.</em></li>
                <li>Transforms player scores into frequency sequences.</li>
                <li>Reads match logs, validates scores, and prepares data for analysis.</li>
                <li>Handles tournament data, associating match scores with details.</li>
                <li>Processes all tournament files, generating a final CSV dataset with valid match data.</li>
              </ul>
            </li>
            <li><code>dowloader-scores.py</code>
              <p>Scrapes match data asynchronously, gathering game details from a website and logging console output.</p>
              <ul>
                <li>Interacts with the webpage, collects game data, and logs relevant details.</li>
                <li>Processes event IDs from TSV files, extracting match data from the website.</li>
                <li><em>Launches the scraper, processes files, and saves the logs for future use.</em></li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
    <li><strong>TTinsight/</strong>
      <ul>
        <li><code>TTinsight_DataPreprocessing.ipynb</code>: Colab notebook showing steps for data cleaning and transformation.</li>
        <li><code>TTinsight_ModelDevelopment.ipynb</code>: Colab notebook for model training, evaluation, and fine-tuning.</li>
      </ul>
    </li>
    <li><code>README.md</code>: Documentation with project overview, installation, and usage instructions.</li>
    <li><code>requirements.txt</code>: Lists dependencies required to run the project.</li>
  </ul>
</div>




---
## Visual Representation

<div align="center">
  <img src="https://github.com/oraziotorre/TTinsight/blob/main/gui/TTinsight_GUI_explanation.png?raw=true" width="600">
</div>


*Figure: A preview of the TTinsight GUI in action.*

---

## Prerequisites

To run this project, you need to have the following installed:

<div>
  <ul>
    <li><strong>Python 3.11</strong> (or higher)</li>
    <li><strong>pip</strong> for dependency management</li>
    <li><strong>A virtual environment</strong> (to manage dependencies in an isolated environment)</li>
    <li><strong>An IDE</strong> like <strong>PyCharm</strong>, <strong>Visual Studio Code</strong>, or any other preferred environment.</li>
  </ul>
</div>

---

## Steps to Run the Project

### 1. **Clone or Copy the Project**

Ensure that you have a copy of the **TTinsight** project on your machine. If you don’t have it yet, you can clone it from a Git repository or simply copy the project folder.

### 2. **Install Python 3.11**

Check that Python 3.11 is installed on your machine. Run the following command:

```bash
python --version
```
If you don’t have Python 3.11, install it by following the instructions for your OS:

<div> <ul> <li><strong>Windows</strong>: <a href="https://www.python.org/downloads/">Download Python 3.11 for Windows</a></li> <li><strong>macOS</strong>: Install via <a href="https://brew.sh/">Homebrew</a> using <code>brew install python@3.11</code></li> <li><strong>Linux</strong>: Use your system’s package manager (e.g., on Ubuntu: <code>sudo apt install python3.11</code>).</li> </ul> </div>

### 3. **Create a Virtual Environment**

After installing Python 3.11, create a virtual environment to isolate the project’s dependencies.
```bash
python3.11 -m venv venv
```

Activate the virtual environment based on your OS:

<div>
  <ul>
    <li><strong>Windows</strong>: 
      <pre><code>.\\venv\\Scripts\\activate</code></pre>
    </li>
    <li><strong>macOS/Linux</strong>: 
      <pre><code>source venv/bin/activate</code></pre>
    </li>
  </ul>
</div>

### 4. **Install the Dependencies**

Ensure that the `requirements.txt` file is present in the project folder (it was generated earlier). If you don't have it, you can generate it by running:

To install all the required dependencies, use the following command:

```bash
pip install -r requirements.txt
```


### 5. **Set Up Your IDE**

Depending on which IDE you’re using, follow these steps to configure it to use the Python 3.11 virtual environment.

#### **Visual Studio Code (VS Code)**

1. **Install VS Code** from the official site: <a href="https://code.visualstudio.com/">https://code.visualstudio.com/</a>
2. **Open the project folder** in VS Code: Go to **File** > **Open Folder...** and select your project folder.
3. **Create or Activate the Virtual Environment**:
   If you haven’t done so already, activate the virtual environment:
   <div>
     <ul>
       <li><strong>On Windows</strong>: 
         <pre><code>.\\venv\\Scripts\\activate</code></pre>
       </li>
       <li><strong>On macOS/Linux</strong>: 
         <pre><code>source venv/bin/activate</code></pre>
       </li>
     </ul>
   </div>
4. **Install the Dependencies** (if you haven't done so):
```bash
pip install -r requirements.txt
```

5. **Select the Python Interpreter**:
Open the **Command Palette** (Ctrl + Shift + P or Cmd + Shift + P on macOS), search for **Python: Select Interpreter**, and choose the interpreter for your virtual environment.
6. **Run the Project**:
You can now run the Python scripts directly in the VS Code terminal, or start the GUI.

#### **PyCharm**

1. **Install PyCharm** from the official site: <a href="https://www.jetbrains.com/pycharm/">https://www.jetbrains.com/pycharm/</a>
2. **Open the Project**: Go to **File** > **Open** and select your project folder.
3. **Set Up the Python Interpreter**:
- Navigate to **File** > **Settings** (or **PyCharm** > **Preferences** on macOS).
- Under **Project: TTinsight**, click on **Python Interpreter**.
- Click the gear icon, then choose **Add**. Select **Existing environment** and point to your virtual environment’s interpreter:
  - **Windows**: `.\\venv\\Scripts\\python.exe`
  - **macOS/Linux**: `venv/bin/python`
4. **Install the Dependencies**:
If you haven't already installed the dependencies, you can open the terminal within PyCharm and run:
```bash
pip install -r requirements.txt
```
5. **Run the Project**:
Now, you can run your Python scripts or the GUI directly from PyCharm.

## Common Issues

### 1. **Incompatible Versions Error**

If you encounter errors related to incompatible library versions, make sure you have Python 3.11 and the versions of libraries specified in the `requirements.txt` file. You can also try creating a new virtual environment and reinstalling the dependencies.

### 2. **Permission Errors**

If you get permission-related errors (e.g., `PermissionError`) while installing libraries, try using `sudo` on macOS/Linux or running as an administrator on Windows.

---

## Contributing

If you would like to contribute to the **TTinsight** project, feel free to submit a **pull request** or open an **issue** on GitHub. All contributions are welcome!



