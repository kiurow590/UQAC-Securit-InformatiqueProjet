# Projet de Sécurité Informatique

Ce projet a été réalisé dans le cadre du cours de sécurité informatique à l'Université du Québec à Chicoutimi (UQAC) pour l'année académique 2024/2025.

## Équipe

- Matéo Hany
- Thomas Le Baron
- Aubry Tonnerre

## Structure du Projet

Le projet est divisé en deux parties principales : Antivirus et Virus.

### Antivirus

#### Antivirus Comportemental

- **CMakeLists.txt** : Fichier de configuration CMake.
- **Dockerfile** : Fichier Docker pour créer l'image de l'antivirus.
- **main.c** : Code source principal de l'antivirus comportemental.
- **modifier.c** : Code source pour modifier des fichiers.
- **Test/** : Répertoire contenant les tests unitaires.
  - **mainTest.c** : Code source des tests unitaires.

```shell
# Déploement du docker a l'aide du dockerfile
docker build -t antivirus .
docker run --privileged -it antivirus /bin/sh 
```

#### Antivirus Hash

- **CMakeLists.txt** : Fichier de configuration CMake.
- **Dockerfile** : Fichier Docker pour créer l'image de l'antivirus.
- **main.c** : Code source principal de l'antivirus basé sur les hash.
- **hash.c** : Code source pour les fonctions de hachage.
- **Test/** : Répertoire contenant les tests unitaires.
  - **mainTest.c** : Code source des tests unitaires.

### Virus

#### BestApp4Ever

- **BestApp4Ever** : Script malveillant conçu pour remplir le disque avec des informations aléatoires pour saturer la mémoire et le CPU.

#### Stonks

- **app.py** : Application Flask pour gérer les clés de chiffrement et les fichiers exfiltrés.
- **Dockerfile** : Fichier Docker pour créer l'image de l'application Flask.
- **Stonks.sh** : Script ransomware qui chiffre les fichiers et demande une rançon.

### Nouveaux Éléments

#### Antivirus

- **Antivirus Comportemental** : Un antivirus basé sur le comportement, avec des fichiers comme `main.c`, `modifier.c`, et des tests dans `mainTest.c`.
- **Antivirus Hash** : Un autre composant de l'antivirus (détails non fournis).

#### Virus

- **BestApp4Ever** : Un script malveillant conçu pour remplir le disque avec des informations aléatoires pour saturer la mémoire et le CPU.
- **Stonks** : Un ransomware qui chiffre les fichiers et demande une rançon. Il inclut des scripts Bash (`Stonks.sh`) et une application Flask (`app.py`) pour gérer les clés de chiffrement et les fichiers exfiltrés.

## Détails des Composants

### Antivirus Comportemental

L'antivirus comportemental surveille les processus et les fichiers pour détecter des comportements suspects. Il utilise `fanotify` pour surveiller les modifications de fichiers et une liste blanche pour autoriser certains programmes.

### Antivirus Hash

L'antivirus basé sur les hash utilise des fonctions de hachage pour vérifier l'intégrité des fichiers et détecter les modifications non autorisées. Il compare les hash des fichiers actuels avec une base de données de hash connus pour identifier les fichiers suspects.

### BestApp4Ever

Un script malveillant qui génère des fichiers aléatoires pour saturer la mémoire et le CPU de la machine cible.

### Stonks

Un ransomware qui chiffre les fichiers de la victime et envoie la clé de chiffrement à un serveur distant. Il demande ensuite une rançon en bitcoin pour déchiffrer les fichiers.

## Avertissement

**DISCLAIMER** : Ne pas exécuter ces programmes sur votre ordinateur personnel ou sur toute autre machine sans comprendre les risques associés.