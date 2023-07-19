# Parameter Injection II

## Where is I ?
first thing first, why is it **II**? because there was a **I** in the Qualification phase which, we did not solve during the Quals, but we solved similar challenges while preparing for the final phase.

*Let us discuss real quick as a background*. Although, that challenge was a black box with no source code, and no real attempts were done to that challenge, but we found similar ones on other platforms like [CryptoHack](https://cryptohack.org/challenges/diffie-hellman/) and with some help from other awesome writeups like the [one](https://s00ra.github.io/ctfs/icmtccrypto/#parameter-injection) of 50r4 from 0xl4ugh, I could figure out how was it like.

In brief, it was man-in-the-middle attack on Diffie-Hellman, while you are given access to intercept communication and modify them. Alice gives you her public key, you take it get a shared secret with her, poor Bob asks you and you don't even have to give him a valid public key; then Alice gives you the flag encrypted with your shared key with her and *voila*. (if that was not the case please notify me)

## What about II?
This challenge is a sequel for the previous one (and the instance were down so I could not mimic it correctly); this challenge is a black box too. Now, Alice and poor Bob communicate so fast that we could not modify the intercepted request, we could only eavdrop on them then communicate only with Bob (he is poor no more -.-). 

The json requests from Alice contained: 1) P, a prime number, 2) g, a base number, 3) A, Alice's public key

The json requests from Bob contained: 1) B, Bob's public key only (it is still you poor Bob)

then Alice sends the flag encrypted with their shared key.

At that occassion, we get to communicate with Bob.


## Bob isn't just poor, he is dummy small brain too

Bob expects from us a json like the first one from Alice. First, I tried to change the A, public key paramter, so that Bob can give me data encrypted with out shared secret or something, but almost forgot he is poor, he got no data.

He only sends his public key to me, which should be the same right? right?

In fact, it was the same in that case yes, but when we try to change other paramters like the P, the prime number, to something like 1, so we can leak Bob's secret we get an alert *"Hacking Detected"*. 

hmm, maybe we can change the only left paramter g, the base, ? then we can find Bob's public key changes. poor Bob, now you are officially small brain too.


## What is really happening here?
Okay let's think of what is happening. Bob takes whatever *A* and nothing changes, but when we change g, which was 2, to any other number his outputs change.

Let's address his output which is his public, that is calculated by raising his secret key to a common base, which in that case was g, or 2 to be exact.

same thing applies to Alice, but Alice or the party communicating with Bob gets to send him the common base in order to unify it.

Afterwards, when the public keys get exchanged, both parties can forge their shared secret key happily by raising the public key of the other party with their own secret key again like the following:

$$\displaystyle{\displaylines{Alice's\hspace{0.1cm}Secret\hspace{0.1cm}key = g^{a} \newline Bob's\hspace{0.1cm}Secret\hspace{0.1cm}key = g^{b} \newline Alices's\hspace{0.1cm}Shared\hspace{0.1cm}Secret\hspace{0.1cm}key = g^{b^{a}} = g^{b*a}  \newline Bob's\hspace{0.1cm}Shared\hspace{0.1cm}Secret\hspace{0.1cm}key = g^{a^{b}} = g^{a*b}}}$$

so when we change *A*, Bob's shared secret changes but we don't see it because it is secret. However, when we change *g*, the base, the calculation of Bob's public key changes as it depends on it, or Bob raise it to his secret number to be percise.

think of how we can exploit this to leak the shared secret 🤔

## Leaking Alice-Bob Shared Secret

let's say we sent A, the public key, as Alice's public key $g^{a}$ , we will make poor Bob forge the same shared secret $g^{a*b}$ and his public key is the same, but we got two problems here that makes this irrelevant: first, we do not have Alice's secret keys in the first place; if Bob encrypts anything with it, I will not be able to decrypt it still. second, Bob is **poor**, he has no data to encrypt (gottem!) 

Hmm, what if we use Alice's public key as the base. I mean no certain law or anything makes me use Alice's public key, just my CTF instinict. when we try to do this, Bob's shared secret of course changes too but no his public too.

let's simulate it. we send to $g^{a}$ as $g$, so when he calculates his public key it is now $g^{a^{b}}$ instead of just $g^{b}$.

if $g^{a^{b}}$ sounds familiar, that's because it is. that's how we calculate the shared secret key 🤩.

so now when small brain Bob sends us his public key he is sending us his shared secret with Alice too, since Bob's secret is the same.

Bingo. Now, we can decrypt the flag sent from Alice.


if you want to practice I suggest all man-in-the-middle attacks on [CryptoHack's Diffie-Hellman Module](https://cryptohack.org/challenges/diffie-hellman/) specially the one named Static Client and maybe Static Client 2 (what is it with the sequels?)


Don't forget to check the sol.py script ;) 