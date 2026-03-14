# Bulk Import – File Format Specification

> This document defines the expected file format, validation rules, and error handling
> for the bulk transaction import feature (v0.5).

---

## Supported formats

| Format | Extension | Notes                          |
|--------|-----------|--------------------------------|
| CSV    | `.csv`    | UTF-8 encoded, comma-separated |
| Excel  | `.xlsx`   | First sheet is used            |

---

## Columns

| Column        | Required | Type    | Description                                             |
|---------------|----------|---------|---------------------------------------------------------|
| `date`        | Y        | date    | Transaction date. Format: `YYYY-MM-DD`                  |
| `amount`      | Y        | decimal | Positive number. No currency symbols                    |
| `type`        | Y        | string  | Exactly `income` or `expense` (lowercase)               |
| `category`    | Y        | string  | Must match an existing category name (case-insensitive) |
| `account`     | Y        | string  | Must match an existing account name (case-insensitive)  |
| `description` | N        | string  | Optional. Free text for additional context              |

---

## Example — valid file

```csv
date,amount,type,category,account,description
2026-01-15,50000,expense,Food,Personal,Lunch at restaurant
2026-01-16,2000000,income,Salary,Personal,Monthly salary
2026-01-17,30000,expense,Transport,Shared,Bus tickets
2026-01-18,15000,expense,Entertainment,Shared,Movie night
2026-01-19,500000,income,Freelance,Personal,
```

> A downloadable template is available at `GET /transactions/import/template`

---

## Validation rules

### date

- Must be a valid calendar date
- Recommended format: `YYYY-MM-DD`
- Other formats accepted by pandas (e.g. `DD/MM/YYYY`) may work but are not guaranteed

### amount

- Must be a positive number (`> 0`)
- Decimals allowed (e.g. `15000.50`)
- No currency symbols, commas as thousands separators, or spaces

### type

- Accepted values: `income`, `expense`
- Case-insensitive (`Income`, `EXPENSE` also accepted)

### category

- Must match the name of an existing category (case-insensitive)
- The category type must be consistent with the transaction type:
  - `expense` transactions → must use an `expense` category
  - `income` transactions → must use an `income` category

**Available categories at v0.5:**

| Name          | Type    |
|---------------|---------|
| Salary        | income  |
| Freelance     | income  |
| Other income  | income  |
| Food          | expense |
| Transport     | expense |
| Housing       | expense |
| Entertainment | expense |
| Health        | expense |
| Other expense | expense |

### account

- Must match the name of an existing account (case-insensitive)

**Available accounts at v0.5:**

| Name     | Type       |
|----------|------------|
| Personal | individual |
| Shared   | shared     |

### description

- Optional — can be empty or omitted entirely
- Free text, no restrictions

---

## Import response

The endpoint `POST /transactions/import` returns a JSON object:

```json
{
  "total": 10,
  "imported": 8,
  "errors": [
    { "row": 3, "error": "Category 'Groceries' not found" },
    { "row": 7, "error": "Amount must be a positive number: '-500'" }
  ]
}
```

| Field      | Description                                         |
|------------|-----------------------------------------------------|
| `total`    | Total number of rows in the file (excluding header) |
| `imported` | Number of rows successfully imported                |
| `errors`   | List of rows that failed, with reason               |

> Rows are processed independently — a failed row does not stop the rest of the import.

---

## Common errors

| Error message                              | Cause                              | Fix                                       |
|--------------------------------------------|------------------------------------|-------------------------------------------|
| `Missing columns: category, account`       | Required columns not found in file | Check column names match exactly          |
| `Invalid date: '15-01-2026'`               | Wrong date format                  | Use `YYYY-MM-DD`                          |
| `Amount must be a positive number: '-500'` | Negative or zero amount            | Use only positive values                  |
| `Type must be 'income' or 'expense'`       | Typo or unexpected value           | Check the type column values              |
| `Category not found: 'Groceries'`          | Category name doesn't match        | Use exact names from the categories table |
| `Category 'Salary' is income, not expense` | Type mismatch with category        | Align transaction type with category type |
| `Account not found: 'Mine'`                | Account name doesn't match         | Use `Personal` or `Shared`                |
| `Unsupported format. Use .csv or .xlsx`    | Wrong file type uploaded           | Convert file to CSV or Excel              |

---

## Related

- `docs/domain/business_rules.md` — transaction invariants enforced during import
- `docs/domain/entities.md` — Category and Account entity definitions
- `backend/app/services/import_service.py` — implementation
- `backend/app/routers/imports.py` — API endpoint
