## Chapt 2.

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
#### implement privacy
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

## Chapt 3.

**Background knowledge!**
Anon methods so far do not protect against BG very well

TDC produce anon datasets, like HW1

### Differential Privacy
Promise for protection against arbitrary background knowledge

Protection relies on the fact that it is not certain if a particular user is part of the dataset

Causes a paradox
    learn nothing about the individual but learn about the population

Statistical outcome should be indistinguishable if a particular user is included or not
    Where there are spike, correlations

Cannot determine if a user is in a dataset or not -> plausible deniability

### Probability Div Priv
Two *users* that differ in one record / attribute should have a very similar probability in being an output
    an output being a specific user
    similar *user* entries should not have distinct outputs.

Noise is added to meet criteria? difficult to distinguish

### Parameter eps
control the degree at which two similar entries could be distinguished between eachother

D_2 neighboor of D_1

p(D_1) / p(D_2) <= e^eps

This is predefined

esp is privacy budget

### Indistinguishably
for every possible neighbor
p(D_1) / p(D_2) <= e^eps

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
#### dBitFlip

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

### Unary Encoding
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
- 