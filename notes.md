---
geometry:
-               margin=10mm
-               letterpaper
urlcolor:       blue
fontsize:       11pt
...

# CS 528 Class Notes

## Chapt 2

### Data privacy

- Logical security of data
- It is needed
  - Attributes of of user in a database can be used to identify them

### Data Linkage

- Types of attributes
  - Identifiers (ID), attributes that explicitly identify the user
  - Quasi-Identifier (QID), attributes that *implicitly* identify the user through comparing the attributes in public databases that have exposed IDs.
  - Sensitive Attribute (SA), attributes that we don't want attackers to know about a user

- Removing IDs is not enoughs as QIDs can be used to match the user to databases that do have their ID and then it can be use to match SAs to IDs.
  - 87% of US citizens can be uniquely linked using only (Zip-code, DOB, Sex)

### K-anonymity

- Definition
  - Each record is indistinguishable from at least k-1 other records\
    - In terms of the QIDs, SAs are unchanged
  - k-Anonymity ensures that linking cannot be performed with confidence
- Implementation
  - Randomization, Data swapping, suppression, or generalization of QIDs
    - Generalization Hierarchies - generalization and suppression
      - Achieve k-anonymity by successively generalizing user QIDs until each group has k-1 anonymity

#### Distortion

**k-minimal Distortion**: A k-minimal generalization that has the least distortion

$Distortion\ D=\frac{\sum_{Attrib\ i}\frac{Current\ level\ of\ generalization\ for\ attribute\ i}{Max\ level\ of\ generalization\ for\ attribute\ i}}{Number\ of\ attributes}$

#### Precision

Average height of generalized values, normalized by Value 
Generalization Hierarchy (VGH) depth per attribute per record

$Precision\ P= 1-\frac{
    \sum_{Every\ q*-block}\sum_{Number\ of\ Attributes}\frac{Gen\ level}{Max\ Gen\ level}
}{Data\ Set\ Size\ *\ Number\ of\ Attributes}$

### Attacks

- Unsorted Matching Attack
  - This attack is based on the order in which tuples appear in the released table
  - Sol. Randomly sort the tuples before releasing
- Complementary Release Attack
  - Different releases can be linked together to compromise k-anonymity.
  - Solutions
    - Consider all of the released tables before releasing the new one, and try to avoid linking.
    - Other data holders may release some data that can be used in this kind of attack.
    - Generally, this kind of attack is hard to be prohibited completely.
- Temporal Attack
  - Adding or removing tuples may compromise k-anonymity protection
  - Sol. Subsequent releases must use the already released table.

#### Attacks with BG knowledge or non-diverse SAs

| #   | Zip   | Age    | Nationality | Condition           |
| --- | ----- | ------ | :---------: | ------------------- |
| 1   | 130** | < 30   |      *      | Heart Disease       |
| 2   | 130** | < 30   |      *      | Heart Disease       |
| 3   | 130** | < 30   |      *      | **Viral Infection** |
| 4   | 130** | < 30   |      *      | **Viral Infection** |
| 5   | 1485* | > = 40 |      *      | Cancer              |
| 6   | 1485* | > = 40 |      *      | Heart Disease       |
| 7   | 1485* | > = 40 |      *      | Viral Infection     |
| 8   | 1485* | > = 40 |      *      | Viral Infection     |
| 9   | 130** | 3*     |      *      | **Cancer**          |
| 10  | 130** | 3*     |      *      | **Cancer**          |
| 11  | 130** | 3*     |      *      | **Cancer**          |
| 12  | 130** | 3*     |      *      | **Cancer**          |

BG: Japanese have low incidence of heart disease

| Name  | Zip   | Age | Nationality |
| ----- | ----- | --- | :---------: |
| Umeko | 13068 | 21  |  Japanese   |

**Umeko has Viral Infection!**

| Name | Zip   | Age | Nationality |
| ---- | ----- | --- | :---------: |
| Bob  | 13053 | 31  |  American   |

**Bob has Cancer!**

### L-diversity

Each equivalence class has at least l well-represented sensitive values

- Distinct l-diversity
  - Each equivalence class has at least l distinct sensitive values
  - Probabilistic inference

**Homogeneity Attacks**: k-Anonymity can create groups that leak information due to lack of diversity in the sensitive attribute.

**Background Knowledge Attacks**: k-Anonymity does not protect against attacks based on background knowledge.

- l-diversity principle
  - q*-block: equivalence class
  - A q\*-block is l-diverse if contains at least l *well-represented* values for the sensitive attribute S.
  - A table is l-diverse if every q*-block is l-diverse.

#### Entropy L-Diversity

Entropy of the entire table must be l-diverse

#### Recursive (C, L)-Diversity

Less restrictive than entropy l-diversity

For every q*-block, if the count of each attribute was sorted, q*-block is recursive (c, 2)-diverse if $r_1 < c(r_l+ r_{l+1} + ... + r_m)$ for a specified constant c.

#### Limitations

l-diversity may be difficult and unnecessary to achieve

l-diversity does not consider the overall distribution of sensitive values

- A single sensitive attribute
  - Two values: HIV positive (1%) and HIV negative (99%)
  - Very different degrees of sensitivity
- l-diversity is unnecessary to achieve
  - 2-diversity is unnecessary for an equivalence class that contains only negative records
- l-diversity is difficult to achieve
  - Dataset must be large enough

**Similarity Attack** : Matching QIDs may not give an exact answer but can still give a general answer for SAs

### T-Closeness

#### Principle

The *distance* between Overall distribution Q of sensitive values and Distribution Pi of sensitive values in each equi-class is bounded by a threshold t. *l-diversity only considered Pi*.

t-closeness protects against attribute disclosure but not identity disclosure.

t-closeness requires that the distribution of a sensitive attribute in any equivalence class is close to the distribution of a sensitive attribute in the overall table.

### Types Of Information Disclosure

- Identity Disclosure
  - An individual is linked to a particular record in the published data.
- Attribute Disclosure
  - Sensitive attribute information of an individual is disclosed.
- Membership Disclosure
  - Information about whether an individual's record is in the published data or not.

### GPS location Anonymization

- Anonymization done through *cloaked* regions with at least *k* users.
  - here, *k* depends on context
  - *k* = 100 is very little in a stadium, or a lot in a desert

### Social Network (Graph)

- Social **Net**Works; this data can be represented as a graph
- very difficult to mark what is a QI

#### privacy leak with graphs

- Regardless of identity on a node, the # of connections cab let us know who is what node

#### implement privacy

- graphs can be k-degree anonymous where every node has the same degree as k-1 nodes
- *fake* relations are created to match degrees between nodes, utility is lost.

### Search queries

- Queries can be linked through sensitive values
- Search engines are based on this sensitive data, to give better results
    Modern search engines don't depend on keywords, they focus on what the users do, the links clicked is linked to the query searched.

#### Implement privacy

- cluster up queries that point to the same links
  - queries that users made are clustered if they clicked on the same link

### Whats on the Test?

- Attacks
  - Linkage
  - Homogeneity
  - Background knowledge
  - Skewness
  - Similarity

- k-Anon, l-Div, t-Closeness

## Chapt 3

**Background knowledge!**
Anon methods so far do not protect against BG very well

TDC (Trusted Data Curator) produce anon datasets, like HW1

### Differential Privacy

Promise for protection against arbitrary background knowledge

- Protection relies on the fact that it is not certain if a particular user is part of the dataset
  - Statistical outcome is indistinguishable regardless whether a particular user (record) is included in the data or not.
- Causes a paradox
  - learn nothing about the individual but learn about the population
- Statistical outcome should be indistinguishable if a particular user is included or not
  - Where there are spike, correlations

Cannot determine if a user is in a dataset or not -> plausible deniability

### Probability Div Priv

- Two *users* that differ in one record / attribute should have a very similar probability in being an output
  - An output being a specific user
  - similar *user* entries should not have distinct outputs.

$\log(\frac{Pr[A(D_1)=O]}{Pr[A(D_2)=O]}) <= \epsilon\ (\epsilon>0)$

Noise is added to meet criteria? difficult to distinguish

### Parameter eps

control the degree at which two similar entries could be distinguished between eachother

We care about every output because any output can possibly identify someone.

D_2 neighboor of D_1

p(D_1) / p(D_2) <= e^eps

This is predefined

esp is privacy budget

### Indistinguishably

for every possible neighbor
p(D_1) / p(D_2) <= e^eps

It is difficult to tell whether a user is in or not

### Adding noise

- Laplace Mechanism - Distribution
  - Noise determined on esp
  - Lap(S/esp)
  - keep mean u=0
  - variance 2b^2
  - Is a piecewise func
  - works for any function returning a real number
  - Error
    - E(true ans - noise ans)^2
  - Queries to DB returns request + noise
  - Used for REAL numbers
- Exponential Mechanism
  - What is the most common, what is the most ...
    - Noise cannot be added here, most is most even with noise
  - With any user, whether they are in or not in the DB, the output should be close.
  - Make queries return based off the probability of each attribute
  - e.g.    Given a DB of nationalities, they are set based off the probability that they are most common.
    - Probability is exponential? Accentuating those that are most common.
      - Creates high utility
  - More for categorical data, how often a cat. occurs
- Global sensitivity
  - How sensitive a func is
  - More noise is added if a function is sensitive

### Indistiguishability

Query to a database will return with noise

- We don't know whether a particular use is actually in a database

### Composition Theorems

*Compose* all these building blocks together

Parallel composition has better utility, each query has it's own esp to satisfy

- Can be used with disjoint queries
Sequential composition requires that all queries satisfy esp
- Easier to implement, used when there is overlap

Postprocessing should not lead to any data leaks

- not considered a composition method, does not consume privacy budget

### Differential private k-means

Clustering of users

Noise is added to each step when calculating size, this allows the removal of a person not be noticeable

Each iteration in the algorithm, esp/T, where T is the current iteration and esp is total privacy loss

laplace k-means cannot distinguish small clusters that are close by

### Relaxed DP - Non interactive

The database is pre-modified? ensures DP holds true on the modified database.
no pair of similar people can be differentiated from another.

## Chapt 4 Local Differential Privacy

DP on a local scale; Centralized DP

Reduce trust from the database, produce private data locally

- pre-randomize data? Don't trust the DB
- Each user runs a local DP algorithm
  - Once sent to the DB, it can just be combined

injected noise averages out, however, it is not ideal

### Combinig user data

true answer + sum of N laplace distributions

Example: binary user info 0/1
Error looks like `sqrt(N)/eps` => Larger datasets lose less utility, as N gets higher

Error typically scales `sqrt(N)`, the more the better

### DP vs LDP

LDP works on inputs no datasets

- Ensures that no two similar inputs can be differentiated between
  - e.g. If we get yes or no from a person, we don't know if they specifically said y/n

LDP concerns two values, DP concerns two Data sets

Noise in DP is constant while LDP's aggregate noise is `1/sqrt(n)`

### Random Response

Toss a coin (p = 0.5), send true answer if heads, otherwise, lie

### Google's RAPPOR

- Random Response (RR) for something like favorite URL?

#### Bloom filters can be used for indexing items

- Items are represented as masks of this filter
  - 01001 => Apple
  - Filter 1001101001 has Apple
- Using Bloom filters, each user maps their inputs to at most k bits in the filter
  - With guarantee of 2keps
- Using K bits to encode inputs.
- This data structure is probabilistic, it is not 100% accurate

### Apple Sketches

- Used for capturing frequencies
  - We don't care about who exactly, just identify groups

### Microsoft Telemetry

- Collect app usage
  - Find behavior patterns

#### 1BitMean

For collecting numeric data

#### dBitFlip

For collecting sparse histogram data

### Snap LDP ML

- Send user a randomly chosen model depending on a rand model

### Frequency estimation

- eps-LDP items should be equally probably to be output
- We then remove bias from a RR using estimation

### Generalized RR - Direct encoding

- Random *coin flip* is biased with param `p`
- Other values are reported with probability `q`
- values `p` and `q` are inversely proportional to `d`
  - Very large domains make the probabilities very small
  - solved through unary encodings

### Unary Encoding - Basic RAPPOR

- value is encoded into a bit string
- each user randomizes the true output for each value
- observed value is then *filtered* to get a more accurate result
- accuracy increases with more users
- Better than DE

### Laplacian (gaussian)

- Instead of randomizing each bit, add noise to each bit
- Worse utility than UE

### Heavy Hitter prob

- Find one most frequent values
  - Partition users into groups
  - concatenate most common segments
  - too large concatenates

### Node LDP

- Social graphs are more diffictuly to deal with
- isolated node groups should not be individually identifiable

## Chapt 5 Cryptography

- Data Obfuscation
  - k-anon
  - l-div
  - DP - lap, exp
  - LDP - UE, GRR, RAPPOR
- Encrypt data - Applied Crypto
  - Decrypt data

Crypto techniques for privacy & security

Crypto: Encryption (protect message) and Authentication (protect users id)

### Types of basic crypto techs

- **Fundamental rule: Cipher should still be secure even if everyone knows the complete design**
- Cipher
  - Encrypt
    - Shift data
    - a->d, b->e
    - "hello" -> "khoor"
  - Decrypt
    - Anyone with the cipher can break it
- Caligula - Extended Cipher
  - Encrypt
    - Have sender and receiver agree on what shift to use
    - `key` = shift decided on, is kept private
  - Decrypt
    - Single char is very secure
    - For plain english, shift until there are english words
    - given a known word and it's cipher, we can easily find the key
    - statistical attack
      - exploit regularities in english

### Cryptographic attacks

- Attacker ...
  - Has only ciphertext
  - has plain and cipher text
    - Can find decoding pattern

**Kerckhoff's principle**
Security of an encryption system **Must depend only on the key** not the algorithm itself

Provable security
no such thing as a *provably* secure system

systems are only believed secure

### One-Time pad

Attacks that requires someone to use the same key twice

Breaking One-Time Pad
> `buy` ^ `xqr` = `zmq` --> `zmq` ^ `-xqr` = `buy`
> `zmq` = random without key

### Indistinguishablity - *like DP for messages*

Encryptor flips rand bit `r` to encrypt `M_i` to get `C`

attacker gets `C` and has to guess `r`

### Practical Issues

- One Time pad can get huge; large messages make large keys
- It cannot be reused

How to make the keys smaller?

- 40 bits is pathetic
- 128 is difficult
- 4096 mucho bueno

### Crypto Algorithms

#### Block Ciphers

- given msg and key we get cipher
- Invertibility - everything has to be reversible
  - Given a cipher and key get msg
- Not useful if the key to reverse is public
  - Sol: do it multiple times?
- Feistel network
  - xor with key multiple times
- Still not secure
  - Patterns can still be observed from encrypted values

Rand component - probabilistic encryption

- and randomness to the encryption
  - decrypted msg can still be obtained
- How to add?
  - one time pad trick?

#### Hashes & MAC

crypto hash func -> for data sec. and priv.
> msg `m` -> Hash `h` -> k-bit hash `h(m)`

hash func `H` - maps n bits to k bits where k is security param

- `H` should look like a random function
- Should be hard to find collisions

Collision intractibility

- Should be very difficult to find collisions

#### Public key crypto and Diffie-hellman key exchange

Public key Crypto

- private key only known by individual
- public key known to anyone

Idea

- Confidentiality
  - encipher with public decipher with private
- Auth
  - encipher with priv key, decipher with pub

Requirements

- Easy to de/cipher
- infeasible to get priv from pub
- infeasible to get priv from chosen plaintext attack

Messages are one-way

Known to all : prime `p`, int `g` =/= 0,1, p-1

e.g.
    Alice choses priv `kA`, computes pub `kA` = `g^kA % p`
    com with Bob, alice computes `kS = kB^kA % p`
    com with alice, bob computes `kS = kA^kB % p`

#### RSA

Exponentiation cipher
Relies on the difficulty of determining the number of
numbers relatively prime to a large integer n
> `tot(n)` : number of ints less than n with no factors common with n

e.g.

`tot(10) => |{1,3,7,9}| => 4`

`tot(21) => |{1,2,4,5,8,10,11,13,16,17,19,20}| => 12`

**Algo**
Two large primes `p`,`q`

`n = pq`

`tot(n)=(p-1)(q-1)`

`e => e < n; e relatively prime to tot(n)`

`d => ed % tot(n) = 1`

pub key: `(e,n)`

priv key: `(d,n)`

### Security Services

- Confidentiality
- Authentication
- Integrity
- Non-Repudiation

## Mid-Term

Chapt. 1 - 5
Focus on 2 - 4
6 Questions - Sub Questions

- Open Note - in person
  - NOT open internet
  - Slides work
  - Note sheets / cheatsheets
  - Handouts
  - Only printouts
- 2:00 - 2:30
  - 30 min should be enough tho
- Some questions might be similar to the homework

### Chapt. 1

- Understand how privacy concerns can happen
  - Why users can be de-anonymized
- The trade off between utility v.s. privacy

### Chapt. 2

- Everything regarding the HW
- No source code, just short answer
- QIDs
- How data leakage can happen
- k-anon, l-div, c-l-div
  - Writing pseudo code
  - How to design it
  - Measuring distortion etc.
- Won't ask about an exact algo but describe how to minimize utility loss
- Vulnerabilities to methods
- Skip pgs 57-62
- understand how t-closeness works, not how to implement
- how to generalize k-anon to other applications

### Chapt. 3

- When to use DP vs LDP
- How DP works
  - Why care about neighbors
  - why care about similar outputs
  - how it guarantees privacy
  - When should use DP
- Laplace / exponentiation mechanism
  - skip proofs, only need to know how to inject noise
- Sequential and parallel composition
  - How does that work?
- k-means
- give example of when to use eps-delta

### Chapt. 4

- Why do we use LDP? Vs DP?
- understand Industrial applications
- understand bloom filter
- GRR
- Understand Itemset mining
  - questions how to design
- How to link fundamentals to higher applications

### Chapt. 5

- Questions should be easy?
- Understand what is secure and not secure
- Understand how ciphers works
- Block cipher
  - high level understanding
- Understanding examples might be enough

## Chapt. 6 Secure Multiparty Computation

- Focus on crypto techniques
  - Ensures 100% accuracy

How to Compare values without actually knowing/revealing the values?

- Given two **private** inputs, we want to compute a function of their inputs while maintaining privacy, correctness, and verifiable
  - Function can be as simple as a comparison or as complicated as a ML task

SMC Defines how parties are to exchange messages

### protocol vs algorithm

SMC is a protocol

- protocol
  - Involves more parties
  - interaction with each other
  - LDP is a protocol
- algorithm
  - protocols can be generalized as an algorithm

### How to get rid of a trusted third party?

k inputs (one per party) generates k outputs

We want this protocol to ultimately behave as if there were a trusted third party

### Attackers - What if we are attacking each other?

- If we all were honest, no need for smc
- Semi-honest, honest but curious
  - Follows protocol for the most part
  - Is honest but do what they can to learn more than normal
- Malicious
  - Deviates from protocol, lies about inputs, does whatever

Honest parties should get the correct result from computing f  
Corrupt parties should only get the result of evaluating f

In real world application, the real protocol can simulate the ideal world view.

Instead of passing values to a third party, run values through a protocol function

The real world and idea world views should be *indistinguishable*, the the exact same but *similar*

### Oblivious transfer

i.e. A passes two inputs, B inputs the index of one of A's inputs, A learns nothing but B learns chosen input

B send two pubs, one with knows key. A encyrpts both and returns. B can only decrypt one

Note: Malicious receivers can generate keys for both pubs that are sent, this deviates from the protocol

#### Generalize

For a 1 out of k OT  
Choose k-1 pubs with no keys
Choose 1 pub with a key

### Yao's Protocol

Convert function to boolean circuit

Generate truth table

Garbled circuit

Encrypt truth table, where each gate's inputs and outputs are encrypted

randomize rows and send to receiver

Can convert overall truth table to circuit

#### Against Active Adversaries

What can they do?

Sender: encrypt different circuit  
Receiver: report different output

### Open Source Tools

First started with Fairpaly, written in Java. Only made for two parties

May tools now that support multiple parties and some can deal with the malicious model

## Chapt. 7 Holomorphic Encryption

### RSA History

Most popular asymmetric encryption

$E(m)=m^e(mod\ n)$  
$D(c)=c^d(mod\ n)$

#### Multiplicative Homomorphism

RSA is multiplicatively homomorphic, but not additively

$E(m_1)\cdot{}E(m_2)=E(m_1\cdot{}m_2)$

### Homomorphic encryption

Homomorphic encryption is a form of encryption that allows computation on ciphertexts, generating an encrypted result which, when decrypted, matches the result of the operations as if they had been performed on the plaintext

From $E[A]$, $E[B]$, can compute $E[f(A,B)]$

Where $f$ is +, x, xor, ...

A division operation is very difficult

Running functions on encrypted values will result in a final encrypted value that does result in the actual answer.

Allows analysis of data without actually looking at the data

*What about multiplying different encryption algorithms?*

#### Applying HE

In Fairplay, HE can be applied when passing arguments through gates. AND gate can multiply the encrypted value of A and B

Initial implementations were partially homomorphic, not just any computation was possible.

### Fully HE

#### Computing on encrypted data

implementing XOR and AND makes us turing complete, in the sense that we can perform any operation using these two operations.

#### How secure

With no noise, GCD can be used to find the private key

It seems that, when given non zero noise, no attack has broken this

#### Noise issue

Too much renders operation useless or unusably noisy

## Chapt. 8 Privacy Preserving Data Mining (Crypto)

*How to privately mine data?*

### Preword

Algorithm should be efficient

### Perturbation

- DP
- LDP
- etc.

### Cryptographic

- Lindell & Pinkas
- Completely accurate, completely secure

### Solutions

Secure multiparty computation
proofs of security

### Securely finding the closest cluster

adding r.v.s that add up to 0 to the encrypted values.

### SMC final points

It is still very slow and not practical, not good for large datasets.

## Chapt. 9-A Zero-Knowledge proof (ZKP)

Interactive proof - probabilistic, the verifier challenges the prover and only accepts after multiple challenges and responses

Without sharing any knowledge, prove that you have the *key*

Prover can reply with a part of knowledge that the verifier knows is protected / encrypted

Verifier can also send an encrypted value to be decrypted and then receive the decrypted value from the prover.

### Types of ZK Proofs

#### proof of statement

Convince verifier that statement is true without giving any other info

#### proof of knowledge

Convince verifier that prover has knowledge about something

If both parties are honest, protocol succeeds with overwhelming probability.

Anyone without the *key* should have a near zero chance of passing

This proof should not leak any information

### Fiat-Shamir protocol - quadratic residues

Proving a constant fits a quadratic residue $x^2 \cong q (mod n)$

### Observations on the protocol

multiple rounds where one commits, challenges, then responds

prediction of the challenge enables cheating

zero knowledge proof does not allow information to leak

Every *round* can run in parallel

