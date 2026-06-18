#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int* data;
    int size;
    int capacity;
} Vec;

Vec* vec_new(int capacity) {
    Vec* v = malloc(sizeof(Vec));
    v->data = malloc(capacity * sizeof(int));
    v->size = 0;
    v->capacity = capacity;
    return v;
}

void vec_push(Vec* v, int value) {
    if (v->size == v->capacity) {
        v->capacity *= 2;
        int* new_data = malloc(v->capacity * sizeof(int));
        memcpy(new_data, v->data, v->size * sizeof(int));
        free(v->data);
        v->data = new_data;
    }
    v->data[v->size++] = value;
}

void vec_free(Vec* v) {
    free(v->data);
    free(v);
}

int main() {
    Vec* scores = vec_new(2);
    vec_push(scores, 85);
    vec_push(scores, 92);

    int* top_score = &scores->data[1];

    vec_push(scores, 78);
    vec_push(scores, 95);
    vec_push(scores, 61);

    printf("Top score was: %d\n", *top_score);

    vec_free(scores);
    return 0;
}
