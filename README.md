#Détection d'Équipement avec YOLOv8 et Flask
Ce projet utilise le modèle YOLO (You Only Look Once) pour détecter les personnes, les casques et les gilets dans un flux vidéo en direct. Il utilise Flask pour créer une interface web permettant de visualiser le flux vidéo en direct avec les boîtes de détection superposées et un message de conformité en temps réel.

Prérequis
Python 3.x
Ultralytics YOLO : Assurez-vous d'installer les dépendances requises en suivant les instructions du projet YOLO.
OpenCV : Vous pouvez l'installer avec pip install opencv-python.
Flask : Vous pouvez l'installer avec pip install Flask.
Installation
Clonez ce dépôt sur votre machine locale :

bash
Copy code
git clone https://github.com/votre-utilisateur/detection-equipement.git
Accédez au répertoire du projet :

bash
Copy code
cd detection-equipement
Installez les dépendances nécessaires :

Copy code
pip install -r requirements.txt
Utilisation
Lancez l'application Flask :

Copy code
python app.py
Accédez à l'application dans votre navigateur à l'adresse http://localhost:5000.

Soumettez une image ou accédez au flux vidéo en direct pour voir la détection en action.

Personnalisation
Vous pouvez personnaliser les classes détectées et leurs alias dans le fichier aliases.py.
La logique de détection et de traitement d'image se trouve dans la fonction detect_objects du fichier app.py.
