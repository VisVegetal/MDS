#define OPENSSL_SUPPRESS_DEPRECATED
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <openssl/sha.h>

#define ITERS 2000000

const char* files[4] = {"a.html", "b.html", "c.html", "d.html"};
unsigned long results[4];

unsigned long stretch_hash(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) { perror(path); return 0; }
    fseek(f, 0, SEEK_END);
    long sz = ftell(f);
    fseek(f, 0, SEEK_SET);
    unsigned char* buf = malloc(sz);
    fread(buf, 1, sz, f);
    fclose(f);

    unsigned char digest[32];
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, buf, sz);
    SHA256_Final(digest, &ctx);
    free(buf);

    for (int i = 0; i < ITERS; i++) {
        SHA256_Init(&ctx);
        SHA256_Update(&ctx, digest, 32);
        SHA256_Final(digest, &ctx);
    }

    unsigned long sum = 0;
    for (int i = 0; i < 32; i++) sum += digest[i];
    return sum;
}

void* thread_routine(void* arg) {
    int idx = *(int*)arg;
    results[idx] = stretch_hash(files[idx]);
    return NULL;
}

int main(int argc, char** argv) {
#ifdef MULTI
    pthread_t threads[4];
    int ids[4] = {0, 1, 2, 3};
    for (int i = 0; i < 4; i++)
        pthread_create(&threads[i], NULL, thread_routine, &ids[i]);
    for (int i = 0; i < 4; i++)
        pthread_join(threads[i], NULL);
#else
    for (int i = 0; i < 4; i++)
        results[i] = stretch_hash(files[i]);
#endif
    for (int i = 0; i < 4; i++)
        printf("%s: %lu\n", files[i], results[i]);
    return 0;
}
