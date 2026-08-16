# DipjoSearch Examples

## search_demo.dipjo

A complete example demonstrating DipjoSearch features:

- Creating a search index
- Adding documents with fields (title, content, tags)
- Committing the index
- Searching with ranked results
- Autocomplete suggestions
- Index statistics

### Run the example

```bash
dipjo run examples/dipjo_search/search_demo.dipjo
```

### Run from CLI

```bash
# Create an index
dipjo search create articles

# Add documents
dipjo search add articles id 1 title "Dipjo Language" content "Human-readable programming."
dipjo search add articles id 2 title "Python Guide" content "Learn Python."

# Search
dipjo search query articles "dipjo"

# View stats
dipjo search stats articles

# List all indexes
dipjo search list
```

### HTTP API

If your Dipjo app has an HTTP server running, you can search via HTTP:

```
GET /search/articles?q=dipjo
GET /search/articles?q=dipjo&limit=10
GET /search/articles?q=dipjo&limit=10&offset=20
```
