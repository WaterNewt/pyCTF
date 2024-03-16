#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/bio.h>
#include <openssl/evp.h>

int verify() {
    char password[256];
    printf("Password: ");
    scanf("%s", password);

    // Encode the password using base64
    BIO *b64 = BIO_new(BIO_f_base64());
    BIO_set_flags(b64, BIO_FLAGS_BASE64_NO_NL);
    BIO *bio = BIO_new(BIO_s_mem());
    bio = BIO_push(b64, bio);
    BIO_write(bio, password, strlen(password));
    BIO_flush(bio);

    BUF_MEM *bptr;
    BIO_get_mem_ptr(bio, &bptr);

    // Check if the encoded password matches the expected value
    int result = strcmp(bptr->data, "c3VwZXJzZWNyZXRwYXNzd29yZDEyMw==") == 0;

    BIO_free_all(bio);
    return result;
}

int main() {
    int verification = verify();
    if (verification == 1) {
        // Decode and print the message
        BIO *b64 = BIO_new(BIO_f_base64());
        BIO *bio = BIO_new_mem_buf("cHlDVEZ7Y29uZ3JhdHVsYXRpb25zX29uX3ZpY3Rvcnl9", -1);
        bio = BIO_push(b64, bio);

        char buffer[1024];
        memset(buffer, 0, sizeof(buffer));
        BIO_read(bio, buffer, sizeof(buffer));
        printf("%s\n", buffer);

        BIO_free_all(bio);
    } else {
        printf("Invalid password\n");
        return 1;
    }
    return 0;
}
