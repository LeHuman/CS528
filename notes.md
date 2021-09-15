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

### Probability Div Priv
Two *users* that differ in one record / attribute should have a very similar probability in being an output
    an output being a specific user
    similar *user* entries should not have distinct outputs.

Noise is added to meet criteria? difficult to distinguish

### Parameter eps
control the degree at which two similar entries could be distinguished between eachother

D_2 neighboor of D_1

p(D_1) / p(D_2) <= e^eps

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
- Global sensitivity
  - How sensitive a func is
- More noise is added if a function is sensitive