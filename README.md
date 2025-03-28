## Running the App

```bash
docker compose up
```

## Testing

```bash
make test
```

## Resetting the Database

```bash
rm database.sqlite3
make upgrade
```