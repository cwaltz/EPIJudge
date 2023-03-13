"""
#19.4 IMPLEMENT A THREAD POOL

The following program, implements part of a simple HTTP server:
"""

import concurrent.futures
import socket
import threading

SERVERPORT = 8080


def process_req(sock):
    raise NotImplementedError


def main():
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.bind(('', SERVERPORT))
    serversock.listen(5)
    while True:
        sock, addr = serversock.accept()
        process_req(sock)


"""
Suppose you find that the program has poor performance because it frequently
blocks on I/O. What steps could you take to improve the program's performance?
Feel free to use any utilities from the standard library, including concurrency
classes.


Hint: Use multithreading, but control the number of threads.


Solution: The first attempt to solve this problem might be to launch a new
thread per request rather than process the request itself:
"""

# SERVERPORT = 8080  # Redeclared 'SERVERPORT' defined above without usage

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind(('', SERVERPORT))
serversock.listen(5)
while True:
    sock, addr = serversock.accept()
    threading.Thread(target=process_req, args=(sock, )).start()


"""
The problem with this approach is that we do not control the number of threads
launched. A thread consumes a nontrivial amount of resources, such as the 
time taken to start & end the thread & the memory used by the thread. For a 
lightly-loaded server this may not be an issue but under load, it can result 
in exceptions that are challenging, if not impossible, to handle.

The right trade-off is to use a thread pool. As the name implies, this is a 
collection of threads, the size of which is bounded. A thread pool can be 
implemented relatively easily using a blocking queue/ i.e., a queue which 
blocks the writing thread on a put until the queue is empty. However,
since the problem statement explicitly allows us to use library routines, 
we can use:
"""

# SERVERPORT = 8080  # Redeclared 'SERVERPORT' defined above without usage
NTHREADS = 2

executor = concurrent.futures.ThreadPoolExecutor(max_workers=NTHREADS)
serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversock.bind(('', SERVERPORT))
serversock.listen(5)
while True:
    sock, addr = serversock.accept()
    executor.submit(process_req, sock)
