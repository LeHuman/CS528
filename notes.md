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

## Chapt 3.

