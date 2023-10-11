
# 👷 Détection d'objet avec YOLO et Flask

Ce projet utilise le modèle YOLO (You Only Look Once) pour détecter les personnes, les casques et les gilets dans un flux vidéo en direct. Il utilise Flask pour créer une interface web permettant de visualiser le flux vidéo en direct avec les boîtes de détection superposées et un message de conformité en temps réel.

## Prérequis

- Python 3.x
- [Ultralytics YOLO](https://github.com/ultralytics/yolov5) : Assurez-vous d'installer les dépendances requises en suivant les instructions du projet YOLO.
- OpenCV : Vous pouvez l'installer avec `pip install opencv-python`.
- Flask : Vous pouvez l'installer avec `pip install Flask`.

## Installation

1. Clonez ce dépôt sur votre machine locale :

   ```shell
   git clone https://https://github.com/Artemis-IA/YOLOv8_Detection/.git
   ```

2. Accédez au répertoire du projet :

   ```shell
   cd detection-equipement
   ```

3. Installez les dépendances nécessaires :

   ```shell
   pip install -r requirements.txt
   ```

## Utilisation

1. Lancez l'application Flask :

   ```shell
   flask run
   ```

2. Accédez à l'application dans votre navigateur à l'adresse `http://localhost:5000`.

3. Soumettez une image ou accédez au flux vidéo en direct pour voir la détection en action.

## Personnalisation

- Vous pouvez personnaliser les classes détectées et leurs alias dans le fichier `aliases.py`.
- La logique de détection et de traitement d'image se trouve dans la fonction `detect_objects` du fichier `app.py`.

## Auteur

[Artemisia](https://github.com/Artemis-IA)

## Licence

Ce projet est sous licence [MIT License](LICENSE).

---
