#include <stdio.h>
#include <string.h>

int main(int argc, char** argv) {
    const char* const allowed_speeds[] = {"0", "1", "2", "3", "4", "5", "6", "7",
                                          "automatic", "disengaged"};
    const int num_options = 10;
    const int max_option_length = 10;
    int allowed_option = 0;
    if (argc != 2) {
        return 1;
    }
    for (int i = 0; i < num_options; i++) {
        allowed_option = (0 == strncmp(allowed_speeds[i], argv[1], max_option_length));
        if (allowed_option) {
            break;
        }
    }
    if (!allowed_option) {
        return 2;
    }
    FILE* fandev = fopen("/proc/acpi/ibm/fan", "wb");
    if (fandev == NULL) {
        return 3;
    }
    fprintf(fandev,"level %s", argv[1]);
    fclose(fandev);
    return 0;
}
