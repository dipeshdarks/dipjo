import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from search import SearchIndex


def cmd_create(args):
    if len(args) < 1:
        print("Error: search create requires a name", file=sys.stderr)
        sys.exit(1)
    name = args[0]
    index = SearchIndex(name)
    index.close()
    print(f"Created search index: {name}")


def cmd_add(args):
    if len(args) < 2:
        print("Error: search add requires a name and document", file=sys.stderr)
        sys.exit(1)
    name = args[0]
    index = SearchIndex(name)

    if len(args) == 2 and os.path.isfile(args[1]):
        with open(args[1], "r", encoding="utf-8") as f:
            doc = json.load(f)
        if isinstance(doc, list):
            for d in doc:
                index.add(d)
        else:
            index.add(doc)
    else:
        key_val_args = args[1:]
        if len(key_val_args) < 2 or len(key_val_args) % 2 != 0:
            print("Error: Usage: dipjo search add <name> <key1> <val1> [key2 val2 ...]", file=sys.stderr)
            sys.exit(1)
        doc = {}
        doc_id = None
        for i in range(0, len(key_val_args), 2):
            key = key_val_args[i]
            val = key_val_args[i + 1]
            if key == "id":
                doc_id = val
            else:
                try:
                    doc[key] = json.loads(val)
                except (json.JSONDecodeError, ValueError):
                    doc[key] = val
        if doc_id is None:
            doc_id = str(index.count() + 1)
        doc["id"] = doc_id
        index.add(doc)

    index.commit()
    index.close()
    print(f"Added document to index '{name}'")


def cmd_query(args):
    if len(args) < 2:
        print("Error: search query requires a name and query string", file=sys.stderr)
        sys.exit(1)
    name = args[0]
    query = args[1]
    index = SearchIndex(name)
    results = index.search(query)
    index.close()

    print(json.dumps(results, indent=2, default=str))


def cmd_stats(args):
    if len(args) < 1:
        print("Error: search stats requires a name", file=sys.stderr)
        sys.exit(1)
    name = args[0]
    index = SearchIndex(name)
    stats = index.stats()
    index.close()

    print(json.dumps(stats, indent=2, default=str))


def cmd_rebuild(args):
    if len(args) < 1:
        print("Error: search rebuild requires a name", file=sys.stderr)
        sys.exit(1)
    name = args[0]
    index = SearchIndex(name)
    count = index.rebuild()
    index.close()
    print(f"Rebuilt index '{name}': {count} documents")


def cmd_delete(args):
    if len(args) < 1:
        print("Error: search delete requires a name", file=sys.stderr)
        sys.exit(1)
    name = args[0]
    if SearchIndex.delete_index(name):
        print(f"Deleted search index: {name}")
    else:
        print(f"Index '{name}' not found")


def cmd_list(args):
    indexes = SearchIndex.list_indexes()
    if not indexes:
        print("No search indexes found.")
    else:
        print(f"Search indexes ({len(indexes)}):")
        for name in indexes:
            try:
                index = SearchIndex(name)
                count = index.count()
                index.close()
                print(f"  {name} ({count} documents)")
            except Exception:
                print(f"  {name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: search_cli.py <command> [args...]", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "create": cmd_create,
        "add": cmd_add,
        "query": cmd_query,
        "stats": cmd_stats,
        "rebuild": cmd_rebuild,
        "delete": cmd_delete,
        "list": cmd_list,
    }

    if command in commands:
        commands[command](args)
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
