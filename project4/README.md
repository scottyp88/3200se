# US Military Rifles

## Resource

Rifle

Attributes:

- name (text)
- cartridge (text)
- action_type (text)
- barrel_length_in (text)
- adoption_year (text)
- weight_lb (text)
- standard_capacity (text)
- adoption_branch (text)

## Schema

```sql
CREATE TABLE IF NOT EXISTS rifles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cartridge TEXT NOT NULL DEFAULT 'unknown',
    action_type TEXT NOT NULL DEFAULT 'unknown',
    barrel_length_in TEXT NOT NULL DEFAULT 'unknown',
    adoption_year TEXT NOT NULL DEFAULT 'unknown',
    weight_lb TEXT NOT NULL DEFAULT 'unknown',
    standard_capacity TEXT NOT NULL DEFAULT 'unknown',
    adoption_branch TEXT NOT NULL DEFAULT 'unknown'
);
```

## REST Endpoints

| Name | Method | Path |
| --- | --- | --- |
| Retrieve rifle collection | GET | `/rifles` |
| Retrieve rifle member | GET | `/rifles/<id>` |
| Create rifle member | POST | `/rifles` |
| Update rifle member | PUT | `/rifles/<id>` |
| Delete rifle member | DELETE | `/rifles/<id>` |
