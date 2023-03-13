"""
#19.7 THE READERS-WRITERS PROBLEM WITH WRITE PREFERENCE

Suppose we have an object s as in Problem 19.6 on the preceding page. In the
solution to Problem 19.6 on the facing page, a reader R1 may have the lock;
if a writer W is waiting for the lock & then a reader R2 requests access,
R2 will be given priority over W. If this happens often enough, W will starve.
Instead, suppose we want W to start as soon as possible.

This motivates the second readers-writers problem: protect s with
"writer-preference", i.e., no writer, once added to the queue, is to be kept
waiting longer than absolutely necessary.

Implement a synchronization mechanism for the second readers-writers problem.


Hint: Force readers to acquire a write lock.


Solution: We want to give writers the preference. We achieve this by modifying
Solution 19.6 on the previous page to have a reader start by locking the write
lock & then immediately releasing it. In this way, a writer who acquires the
write lock is guaranteed to be ahead of the subsequent readers.


Variant: The specifications to Problems 19.6 on Page 296 & 19.7 on the previous
page allow starvation - the first may starve writers, the second may starve
readers. The third readers-writers problem adds the constraint that neither
readers nor writers should starve. Implement a synchronization mechanism for
the third readers-writers problem.
"""
