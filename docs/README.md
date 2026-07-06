# Q-Learning-Agent

Dieses Repository ist in Folge einer Seminarfacharbeit entstanden.
Es kann genutzt werden, um den Lernprozess und das Lernergebnis eines
Q-Learning-Agenten zu erfassen.

## Funktionen

- Simulation mit Q-Learning
- Live-Visualisierung
- Logging der Ergebnisse in externe Dateien
- vorgebaute Labyrinthe
- Labyrinth-Generator
- Labyrinth-Visualisierung

## Anwendung

1. Nutze die `settings.py`, um zentrale Parameter anzupassen und zu verändern.   
2. Um einen Durchlauf zu starten, nutze `main.py` oder `visualizer_main.py`.
3. Klicke auf den, in der Konsole ausgegebenen, Link.

## Branches
Dieses Repository beinhaltet verschiedene branches für verschiedene Experimente.

|         Branch         |                     Zustandswissen                     | Bonuselemente |
|:----------------------:|:------------------------------------------------------:|:-------------:|
| main / size_comparison |                  x- und y-Koordinate                   |     nein      |
|    bonus_knowledge     | x- und y-Korrdinate;<br/> Einsammelstatus der Elemente |      ja       |
|   no_bonus_knowledge   |                  x- und y-Koordinate                   |      ja       |

Jeder branch kommt mit einem eigenen Set an vorgebauten Labyrinthen.

## Weitere Tools

**Labyrinth-Generator**: Nutze die `maze_generator` Datei, um neue zufällige Labyrinthe zu erstellen.  
**Labyrinth-Visualisierung**: Nutze die `maze_viwer` Datei, um ein Labyrinth anzuzeigen.  
