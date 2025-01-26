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

<h3>Breve Descrizione dei File Principali</h3>

<h3>Breve Descrizione dei File Principali</h3>
<div style="font-family: monospace; padding: 10px; margin-bottom: 20px;">
  <ul>
    <li><strong>data/</strong>:
      <ul>
        <li><strong>additional_data</strong>:
          <ul>
            <li><strong>players_metadata.tsv</strong>: Contains information about players such as their ID and nationality, which have not yet been incorporated into our project but may be added later.</li>
            <li><strong>tournaments_metadata.tsv</strong>: Similar to players_metadata.tsv, it contains information that is not currently relevant to the problem at hand.</li>
          </ul>
        </li>
        <li><strong>datasets</strong>:
          <ul>
            <li><strong>cleaned_dataset.csv</strong>: This dataset is used for training and testing the model. It is derived from various modifications made to the raw dataset. The fields it contains include:
            </li>
            <li><strong>raw_dataset.csv</strong>: The raw dataset obtained from various matches played. It contains several inaccurate or unnecessary features that need to be modified.</li>
          </ul>
        </li>
        <li><strong>models/</strong>:
          <ul>
            <li><strong>LogReg.pkl</strong>:
              <p>This model predicts match set outcomes (win/loss) based on features like scores and match dynamics.</p>
              <p><strong>Training:</strong> Logistic Regression is used with standardized data.</p>
              <p><strong>Evaluation:</strong> Cross-validation checks Log Loss and Brier Score for performance.</p>
              <p><strong>Hyperparameter Tuning:</strong> <code>GridSearchCV</code> optimizes parameters (e.g., regularization strength) based on Log Loss.</p>
              <p><strong>Saving:</strong> The best model is saved as a <code>.pkl</code> file for future predictions.</p>
            </li>
            <li><strong>LSTM.keras</strong>:
              <p>This LSTM model captures temporal dependencies in match sequences, which logistic regression couldn’t handle. It uses point progression sequences (<code>points_progression</code>) and two global features (<code>final_set_a</code>, <code>final_set_b</code>) for prediction.</p>
              <p><strong>Data Preparation:</strong> Sequences are padded to a fixed length of 18, and global features are combined for context.</p>
               <ul>
                  <li><strong>LSTM Layers:</strong> Process the sequence of points.</li>
                  <li><strong>Dense Layer:</strong> Integrates the global features.</li>
                  <li><strong>Dropout Layer:</strong> Outputs are combined and passed through a Dropout layer before the final Dense layer with a sigmoid activation for binary classification.</li>
                </ul>
              </p>
              <p><strong>Training and Evaluation:</strong> The model is trained for 20 epochs with binary cross-entropy loss, and evaluated using Log Loss and Brier Score.</p>
              <p><strong>Testing:</strong> The model correctly identifies comeback situations as negative, unlike the logistic regression model, showcasing its ability to capture time-dependent dynamics.</p>
            </li>
          </ul>
        </li>
        <li><strong>data_preprocessing/</strong>:
          <ul>
            <li><strong>dataset-generator.py</strong>:
              <p>This program processes match logs from a tournament, validates scores, and creates a dataset for analysis.</p>
              <p><strong>check_points_error:</strong> Validates scores for consistency, ensuring minimum points and correct score differences.</p>
              <p><strong>points_transformer:</strong> Converts a player's scores into frequency sequences.</p>
              <p><strong>process_match_log:</strong> Reads a match's log, validates the scores, and prepares data for the dataset.</p>
              <p><strong>process_file:</strong> Reads tournament files, associates match scores, and prepares the data.</p>
              <p><strong>main:</strong> Processes all tournament files and generates a final CSV dataset with valid match data.</p>
              <p>The goal is to clean and create a comprehensive dataset for match analysis.</p>
            </li>
            <li><strong>downloader-scores.py</strong>:
              <p>This program asynchronously scrapes match data from a website using Playwright. It processes TSV files containing event IDs and document codes, navigates to the corresponding match pages, interacts with the page to gather game data, and logs relevant console messages.</p>
              <p><strong>get_console_logs:</strong> Navigates to a match URL, interacts with buttons for game data, and collects console logs.</p>
              <p><strong>process_files:</strong> Reads TSV files, extracts event IDs, and calls get_console_logs for each event.</p>
              <p><strong>main:</strong> Launches the browser, processes files, and closes the browser once done.</p>
              <p>The logs are saved to text files for later use.</p>
            </li>
          </ul>
        </li>
      </ul>
    </li>
    <li><strong>TTinsight/</strong>:
      <ul>
        <li><strong>TTinsight_DataPreprocessing.ipynb</strong>: A colab notebook that demonstrates the steps for cleaning, transforming, and preparing data for training.</li>
        <li><strong>TTinsight_ModelDevelopment.ipynb</strong>: A colab notebook containing scripts for training, evaluating, and fine-tuning the model.</li>
      </ul>
    </li>
    <li><strong>README.md</strong>: The main documentation file that provides an overview of the project, installation instructions, and usage guidelines.</li>
    <li><strong>requirements.txt</strong>: A file listing all the dependencies required for running the project.</li>
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



