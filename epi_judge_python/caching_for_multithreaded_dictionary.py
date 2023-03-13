"""
#19.1 IMPLEMENT CACHING FOR A MULTI-THREADED DICTIONARY

The program below is part of an online spell correction service. Clients send as
input a string, & the service returns an array of strings in its dictionary that
are closest to the input string (this array could be computed, for example,
using Solution 1.6.2 on Page 239). The service caches results to improve
performance. Critique the implementation & provide a solution that overcomes its
limitations.
"""

import threading


def closest_in_dictionary(word):
    raise NotImplementedError


class SpellCheckService1:  # With race condition
    w_last = closest_to_last_word = None

    @staticmethod
    def service(req, resp):
        word = req.extract_word_to_check_from_request()
        if word != SpellCheckService1.w_last:
            SpellCheckService1.w_last = word
            SpellCheckService1.closest_to_last_word = closest_in_dictionary(
                word)
        resp.encode_into_response(SpellCheckService1.closest_to_last_word)


"""
Hint: Look for races, & lock as little as possible to avoid reducing throughput.


Solution: The solution has a race condition. Suppose clients A & B make 
concurrent requests, & the service launches a thread per request. Suppose the
thread for request A finds that the input string is present in the cache, and
then, immediately after that check, the thread for request B is scheduled. 
Suppose this thread's lookup fails, so it computes the result, & adds it to the
cache. If the cache is full, an entry will be evicted, & this may be the result
for the string passed in request A. Now when request A is scheduled back, it
does a lookup for the value corresponding to its input string, expecting it to
be present (since it checked that that string is a key in the cache). However
the cache will return null.

A thread-safe solution would be to synchronize every call to the service. In
this case, only one thread could be executing the method & there are no races
between cache reads & writes. However, it also leads to poor performance - only
one thread can execute the service call at a time.

The solution is to lock just the part of the code that operates on the cached
values - specifically, the check on the cached value & the updates to the cached
values.

In the program below, multiple threads can be concurrently computing closest 
strings. This is good because the calls take a long time (this is why they 
are cached). Locking ensures that the read assignment on a hit & write
assignment on completion are atomic.
"""


class SpellCheckService:  # Without race condition
    w_last = closest_to_last_word = None
    lock = threading.Lock()

    @staticmethod
    def service(req, resp):
        word = req.extract_word_to_check_from_request()
        result = None
        with SpellCheckService.lock:
            if word != SpellCheckService.w_last:
                result = SpellCheckService.closest_to_last_word.copy()
        if result is None:
            result = closest_in_dictionary(word)
            with SpellCheckService.lock:
                SpellCheckService.w_last = word
                SpellCheckService.closest_to_last_word = result
        resp.encode_into_response(result)


"""
Variant:

Threads 1 to n execute a method called critical(). Before this, they
execute a method called rendezvous(). The synchronization constraint is that 
only one thread can execute critical() at a time, & all threads must have 
completed executing rendezvous() before critical() can be called. You can assume
n is stored in a variable n that is accessible from all threads. Design a
synchronization mechanism for the threads. All threads must execute the same
code. Threads may call critical() multiple times, & you should ensure that a
thread cannot call critical() a (k + 1)th time until all other threads have 
completed their kth calls to critical().
"""
