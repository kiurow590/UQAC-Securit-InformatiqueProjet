#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void append_comment_to_file(const char *file_path) {
    // Open the file in append mode
    FILE *file = fopen(file_path, "a");
    if (!file) {
        perror("fopen");
        exit(EXIT_FAILURE);
    }

    // Add a comment to the end of the file
    const char *comment = "\n// Comment added by the modifier program\n";
    if (fputs(comment, file) == EOF) {
        perror("fputs");
        fclose(file);
        exit(EXIT_FAILURE);
    }

    printf("Comment added to %s\n", file_path);
    fclose(file);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <path_to_target_c_file>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *target_file = argv[1];

    // Check if the file exists
    if (access(target_file, F_OK) != 0) {
        perror("access");
        exit(EXIT_FAILURE);
    }

    // Modify the file
    append_comment_to_file(target_file);

    return 0;
}
