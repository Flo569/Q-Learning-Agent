# Q-Learning-Agent

Dieses Repository ist im Rahmen einer Seminarfacharbeit entstanden.
Es enthält die Implementierung eines einfachen Q-Learning-Agenten,
der für mehrere Experimente genutzt wurde.

---

![Beispiel eines Labyrinths](docs/images/pre-view.png)

---

## Inhalt

- Implementierung eines Q-Learning-Agenten
- verwendete Umgebungen
- Visualisierung des Trainings
- Labyrinth-Generator
- Labyrinth-Visualisierung


## Voraussetzungen

- Python 3
- Flask


## Installation

### 1. Python installieren

Falls Python noch nicht installiert ist, kann es von der
offiziellen Seite heruntergeladen werden.

[Python herunterladen](https://www.python.org/downloads/)

Bei der Installation unter Windows sollte die Option
**„Add Python to PATH“** aktiviert werden.

### 2. Repository herunterladen

**Hinweis:** Das Repository enthält mehrere Branches. Jeder Branch enthält ein
Experiment.  Vor dem Herunterladen muss daher auf der GitHub-Seite der 
gewünschte Branch ausgewählt werden.

Das Repository kann über den Button **Code → Download ZIP** heruntergeladen
werden. Danach muss die ZIP-Datei entpackt werden.

Alternativ kann das Repository über Git mit folgenden Befehl im Terminal installiert
werden:

```bash
git clone https://github.com/Flo569/Q-Learning-Agent
```

### 3. Virtuelle Umgebung einrichten

Öffne ein Terminal im Ordner des heruntergeladenen Repositories:

#### 1. Virtuelle Umgebung erstellen

**Windows**
```bash
python -m venv .venv
```

**macOS / Linux**
```bash
python3 -m venv .venv
```

#### 2. Virtuelle Umgebung aktivieren

**Windows**
```bash
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Nach erfolgreicher Aktivierung wird im Terminal normalerweise
(.venv) vor der Eingabezeile angezeigt.

### 4. Flask installieren

Flask wird benötigt, um die Weboberfläche des Projekts auszuführen.

**Windows**
```bash
python -m pip install flask
```

**macOS / Linux**
```bash
python3 -m pip install flask
```


## Anwendung

Nach der Installation kann das Programm gestartet werden.

1. Gehe in den heruntergeladenen Ordner
2. Wechsel in den Unterordner **q_learning**
3. Starte ein Terminal aus diesem Ordner
4. Das Programm kann mit und ohne Visualisierung gestartet werden

**Hinweis:** In der Datei `q_learning/utils/settings.py` können verschiedene
Parameter vor dem Start angepasst werden.

### Start

#### Ohne Visualisierung

**Windows**
```bash
python main.py
```

**macOS / Linux**
```bash
python3 main.py
```

Nach Abschluss des Trainings wird ein Ordner mit den Trainingsdaten und Ergebnissen
erstellt.


#### Mit Visualisierung 

**Windows**
```bash
python visualizer_main.py
```

**macOS / Linux**
```bash
python3 visualizer_main.py
```

Im Terminal erscheint eine Nachricht. Öffne den angezeigten Link:
* Running on http://127.0.0.1:8080

Ein Fenster im Browser öffnet sich. Von dort aus kann der Start-Knopf gedrückt
werden und das Training beginnt.

### Beenden

Um das Programm während der Laufzeit vorzeitig zu beenden, drücke im
Terminal **Strg + C** oder auf macOS **Control (^) + C** 

## Branches
Dieses Repository beinhaltet verschiedene Branches für verschiedene Experimente.

|         Branch         |                     Zustandswissen                     | Bonuselemente |
|:----------------------:|:------------------------------------------------------:|:-------------:|
| main / size_comparison |                  x- und y-Koordinate                   |     nein      |
|    bonus_knowledge     | x- und y-Koordinate;<br/> Einsammelstatus der Elemente |      ja       |
|   no_bonus_knowledge   |                  x- und y-Koordinate                   |      ja       |

Jeder Branch kommt mit einem eigenen Set an vorgebauten Labyrinthen.

## Lizenz

Dieses Projekt steht unter der [MIT License](LICENSE).