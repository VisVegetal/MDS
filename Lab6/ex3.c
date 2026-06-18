// Compile: gcc -g -o ex3 ex3.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char* name;
    int*  grades;
    int   count;
} Student;

Student* new_student(const char* name, int grades[], int n) {
    Student* s = malloc(sizeof(Student));
    s->name = malloc(strlen(name));  
    strcpy(s->name, name);
    s->grades = malloc(n * sizeof(int));
    memcpy(s->grades, grades, n * sizeof(int));
    s->count = n;
    return s;
}

float average(Student* s) {
    int sum = 0;
    for (int i = 0; i <= s->count; i++) {  
        sum += s->grades[i];
    }
    return (float)sum / s->count;
}

void free_student(Student* s) {
    free(s->name);
    free(s);
}

int main() {
    int grades[] = {85, 90, 78, 92};
    Student* alice = new_student("Alice", grades, 4);
    printf("%s: avg = %.1f\n", alice->name, average(alice));
    free_student(alice);
    return 0;
}
