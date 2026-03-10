# Domain Models

This document defines the **core domain models** of the *Second Brain* system.
Models represent the main business concepts and their relationships, independent of
any specific database or framework implementation.

---

## Principles

- Models reflect **business concepts**, not tables
- Free of technical or persistence concerns
- Enforce domain rules and invariants
- Serve as the foundation for use cases and business rules

---

## User

Represents a person who can access and interact with the system.

### Attributes

- `id` (UUID)
- `name` (string)
- `email` (string, unique)
- `password_hash` (string)
- `status` (enum: `active`, `inactive`, `banned`)
- `created_at` (datetime)
- `updated_at` (datetime)

### Notes

- Authentication is allowed only when `status = active`
- Status changes must be auditable in the future

---

## Account

Represents a financial account where transactions are recorded.

### Account Attributes

- `id` (UUID)
- `name` (string)
- `type` (enum: `individual`, `shared`)
- `owners` (list of Users)
- `created_at` (datetime)

### Account Notes

- Must have at least one owner
- Ownership rules depend on account type

---

## Category

Represents a classification for transactions.

### Category Attributes

- `id` (UUID)
- `name` (string)
- `type` (enum: `income`, `expense`)
- `created_at` (datetime)

### Category Notes

- Category type must match transaction type
- Cannot be deleted if linked to transactions

---

## Transaction

Represents a financial movement within an account.

### Transaction Attributes

- `id` (UUID)
- `account_id` (UUID)
- `category_id` (UUID)
- `amount` (decimal, positive)
- `type` (enum: `income`, `expense`)
- `date` (date)
- `created_by` (User)
- `created_at` (datetime)

### Transaction Notes

- Amount is always positive
- The logical sign is derived from the transaction type
- Transaction type cannot be changed once created

---

## Relationships Overview

- A **User** can own one or more **Accounts**
- An **Account** can have one or more **Users** as owners
- An **Account** contains many **Transactions**
- A **Transaction** belongs to one **Account** and one **Category**

---

This document must remain consistent with:

- `entities.md`
- `business_rules.md`
- `use_cases.md`
