#pragma once
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <err.h>
#include <vector>

class Server {
    public:
        Server();
        int run();
    private:
        int one = 1;
        int client_fd;
        struct sockaddr_in svr_addr;
        struct sockaddr_in cli_addr;
        socklen_t sin_len = sizeof(cli_addr);
        int sock;
        int port = 8080;
};

