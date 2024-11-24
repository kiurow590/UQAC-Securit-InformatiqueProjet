#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/fanotify.h>
#include <unistd.h>
#include <linux/limits.h>
#include <errno.h>
#include <string.h>
#include <signal.h>

// Liste blanche des programmes autorisés
const char *whitelisted_programs[] = {
    "/bin/sh",       // Shell par défaut
    "/usr/bin/vim",  // Exemple d'éditeur autorisé
    "/usr/bin/nano", // Exemple d'éditeur autorisé
    "/bin/busybox",
    "/usr/bin/top",
    NULL             // Fin de la liste
};

// Vérifier si un programme est dans la liste blanche
int is_program_whitelisted(const char *program) {
    for (int i = 0; whitelisted_programs[i] != NULL; i++) {
        if (strcmp(program, whitelisted_programs[i]) == 0) {
            return 1; // Programme trouvé dans la liste blanche
        }
    }
    return 0; // Programme non trouvé dans la liste blanche
}

// Obtenir le chemin de l'exécutable d'un processus
int get_process_executable(pid_t pid, char *resolved_path, size_t size) {
    char exe_path[PATH_MAX];
    snprintf(exe_path, sizeof(exe_path), "/proc/%d/exe", pid);
    ssize_t len = readlink(exe_path, resolved_path, size - 1);
    if (len == -1) {
        perror("readlink");
        return -1; // Erreur lors de la lecture du lien symbolique
    }
    resolved_path[len] = '\0'; // Terminer le chemin par un caractère nul
    return 0;
}

// Fonction pour sauvegarder le fichier
void backup_file(const char *file_path) {
    char backup_path[PATH_MAX];
    snprintf(backup_path, sizeof(backup_path), "%s.bak", file_path);

    FILE *src = fopen(file_path, "r");
    FILE *dst = fopen(backup_path, "w");

    if (!src || !dst) {
        perror("fopen");
        exit(EXIT_FAILURE); // Erreur lors de l'ouverture des fichiers
    }

    char buffer[4096];
    size_t n;
    while ((n = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        if (fwrite(buffer, 1, n, dst) != n) {
            perror("fwrite");
            fclose(src);
            fclose(dst);
            exit(EXIT_FAILURE); // Erreur lors de l'écriture dans le fichier de sauvegarde
        }
    }

    fclose(src);
    fclose(dst);
}

// Fonction pour restaurer le fichier
void restore_file(const char *file_path) {
    char backup_path[PATH_MAX];
    snprintf(backup_path, sizeof(backup_path), "%s.bak", file_path);

    FILE *src = fopen(backup_path, "r");
    FILE *dst = fopen(file_path, "w");

    if (!src || !dst) {
        perror("fopen");
        exit(EXIT_FAILURE); // Erreur lors de l'ouverture des fichiers
    }

    char buffer[4096];
    size_t n;
    while ((n = fread(buffer, 1, sizeof(buffer), src)) > 0) {
        if (fwrite(buffer, 1, n, dst) != n) {
            perror("fwrite");
            fclose(src);
            fclose(dst);
            exit(EXIT_FAILURE); // Erreur lors de l'écriture dans le fichier original
        }
    }

    fclose(src);
    fclose(dst);
}

// Fonction principale de surveillance
void watch_directory(const char *path) {
    int fan_fd = fanotify_init(FAN_CLASS_CONTENT | FAN_NONBLOCK, 0);
    if (fan_fd < 0) {
        perror("fanotify_init");
        exit(EXIT_FAILURE); // Erreur lors de l'initialisation de fanotify
    }

    if (fanotify_mark(fan_fd, FAN_MARK_ADD | FAN_MARK_MOUNT,
                      FAN_OPEN | FAN_MODIFY | FAN_EVENT_ON_CHILD,
                      AT_FDCWD, path) < 0) {
        perror("fanotify_mark");
        close(fan_fd);
        exit(EXIT_FAILURE); // Erreur lors de l'ajout de la marque fanotify
    }

    printf("Monitoring directory: %s\n", path);

    char buf[4096];
    struct fanotify_event_metadata *metadata;

    while (1) {
        ssize_t len = read(fan_fd, buf, sizeof(buf));
        if (len <= 0) {
            if (errno != EAGAIN) perror("read");
            continue; // Continuer en cas d'erreur de lecture non bloquante
        }

        metadata = (struct fanotify_event_metadata *)buf;

        while (FAN_EVENT_OK(metadata, len)) {
            if (metadata->fd >= 0) {
                // Obtenir le chemin de l'exécutable du processus
                char resolved_path[PATH_MAX];
                if (get_process_executable(metadata->pid, resolved_path, sizeof(resolved_path)) == 0) {
                    // Vérifier si le processus est dans la liste blanche
                    if (!is_program_whitelisted(resolved_path)) {
                        printf("!!! ALERT: Suspicious modification by %s (PID %d) !!!\n",
                               resolved_path, metadata->pid);

                        // Tuer le processus
                        if (kill(metadata->pid, SIGKILL) == 0) {
                            printf("Process %d killed.\n", metadata->pid);
                        } else {
                            perror("kill");
                        }

                    }
                }

                close(metadata->fd);
            }
            metadata = FAN_EVENT_NEXT(metadata, len);
        }
    }

    close(fan_fd);
}

// Entrée principale
int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <directory>\n", argv[0]);
        exit(EXIT_FAILURE); // Afficher l'utilisation correcte du programme
    }

    // Sauvegarder le fichier avant de commencer la surveillance
    backup_file(argv[1]);

    watch_directory(argv[1]);

    return 0;
}