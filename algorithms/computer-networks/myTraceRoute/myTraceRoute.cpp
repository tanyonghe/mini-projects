/*
 TRACEROUTE USING ICMP MESSAGES
 (c) Author: Tan Yong He
 Last Modified: 2019 Sept
 Course: CS3103
 School of Computing, NUS
 */


#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <netinet/ip.h>
#include <netinet/ip_icmp.h>
#include <netdb.h>
#include <fcntl.h>


int main(int argc, char *argv[]) {


    int i, ttl;
    int sockfd, tcp_socket, rst_socket;
    long n, m;
    char buf[10000], buf_rst[10000];
    socklen_t clilen;
    struct hostent *host;
    struct sockaddr_in cliaddr, serv_addr;
    struct timeval timeout;


    if (argc < 3) {
        printf("\nFormat %s <destination address> <destination port> <set -h if using website>\n", argv[0]); 
        return 0; 
    }

    if (argc == 4 && strcmp(argv[3], "-h") == 0) {
        host = gethostbyname(argv[1]);
        serv_addr.sin_addr = *((struct in_addr *)host->h_addr);
        argv[1] = inet_ntoa(serv_addr.sin_addr);
    }

    else {
        inet_pton(AF_INET, argv[1], &(serv_addr.sin_addr));
    }


    // Set up destination address to send TCP SYN packets
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(strtol(argv[2], NULL, 10));
    bzero(&(serv_addr.sin_zero), 8);


    // Create a socket (connectionless) to send TCP SYN packets
    tcp_socket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (tcp_socket < 0) {
        perror("Error creating socket tcp_socket");
        exit(1);
    }

    // Create a socket (connectionless) to receive TCP RST packets
    rst_socket = socket(AF_INET, SOCK_RAW, IPPROTO_TCP);
    if (rst_socket < 0) {
        perror("Error creating socket rst_socket");
        exit(1);
    }

    // Create a RAW socket (connectionless) to receive ICMP messages
    sockfd = socket(PF_INET, SOCK_RAW, IPPROTO_ICMP);
    if (sockfd < 0) {
        perror("Error creating socket sockfd");
        exit(1);
    }


    // Set sender socket (tcp_socket) and receiver socket (rst_socket) to non-blocking
    fcntl(tcp_socket, F_SETFL, O_NONBLOCK);
    //fcntl(rst_socket, F_SETFL, O_NONBLOCK);


    // Set timeout value for receiver sockets (rst_socket & sockfd)
    timeout.tv_sec = 1;
    timeout.tv_usec = 0;  // 1 sec = 1000000 usec
    if (setsockopt(rst_socket, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) < 0) {
        perror("Error using setsockopt on sockfd");
        exit(1);
    }
    if (setsockopt(sockfd, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout)) < 0) {
        perror("Error using setsockopt on rst_socket");
        exit(1);
    }


    clilen = sizeof(struct sockaddr_in);

    printf("TTL:\tSender IP:\t\tICMP Reply Protocol:\n");

    // Send TCP SYN packets with increasing TTL values
    for (ttl = 1; ttl < 256; ttl++) {

        // Set increasing TTL value for TCP SYN packets sent by tcp_socket
        if (setsockopt(tcp_socket, IPPROTO_IP, IP_TTL, &ttl, sizeof(ttl)) < 0) {
            perror("Error using setsockopt on tcp_socket");
            exit(1);
        }


        // Send TCP SYN packet to destination address
        connect(tcp_socket, (struct sockaddr *)&serv_addr, sizeof(serv_addr));


        // Receive TCP data on socket rst_socket and store in 'buf_rst'
        m = recvfrom(rst_socket, buf_rst, 10000, 0, (struct sockaddr *)&cliaddr, &clilen);


        // Extract TCP IP header from the buffer 'buf_rst'
        struct ip *ip_hdr_rst = (struct ip *)buf_rst;


        // if TCP packet was received
        if (m > 0) {
            // check if RST ACK packet by checking for bytes `50 14`
            if ( (uint8_t)buf_rst[32] == 80 && (uint8_t)buf_rst[33] == 20 ) {
                // check if sender is from our destination address and return if it is
                if ( strcmp(argv[1], inet_ntoa(ip_hdr_rst->ip_src)) == 0 ) {
                    printf("%d\t%s\t\t%d\n", ttl, inet_ntoa(ip_hdr_rst->ip_src), (uint8_t)buf[37]);
                    printf("\"TCP RST\" message received from %s, program will now terminate.\n", inet_ntoa(ip_hdr_rst->ip_src));
                    return 0;
                }
            }
        }


        // Send TCP SYN packet to destination address
        connect(tcp_socket, (struct sockaddr *)&serv_addr, sizeof(serv_addr));


        // Receive ICMP data on socket sockfd and store in 'buf'
        n = recvfrom(sockfd, buf, 10000, 0, (struct sockaddr *)&cliaddr, &clilen);


        // Extract ICMP IP header from the buffer 'buf'
        struct ip *ip_hdr = (struct ip *)buf;


        // if ICMP packet was received
        if (n > 0) {
            // check for TCP protocol in ICMP packet using the byte `06`
            if ( (uint8_t)buf[37] == 6 ) {
                // print out source IP address of ICMP packet
                printf("%d\t%s\t\t%d\n", ttl, inet_ntoa(ip_hdr->ip_src), (uint8_t)buf[37]);

                // Extract ICMP header part
                struct icmp *icmp_hdr = (struct icmp *)((char *)ip_hdr + (4 * ip_hdr->ip_hl));

                // terminate if ICMP packet contains error type 3
                if (icmp_hdr->icmp_code == 3) {
                    printf("\"Destination Port Unreachable\" message received from %s, program will now terminate.\n", inet_ntoa(ip_hdr->ip_src));
                    return 0;
	        }
            }
        }
        // if no ICMP packet was received
        else {
            printf("%d\trequest timed out\t-\n", ttl);
        }
    }
    return 0;
}
