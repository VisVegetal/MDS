#include <stdio.h>
#include <pthread.h>

int counter = 0;
#define N 100000

void* increment(void* arg) {
    for (int i = 0; i < N; i++)
        counter++;
    return NULL;
}

int main(void) {
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("counter = %d (expected %d)\n", counter, 2 * N);
    return 0;
}
