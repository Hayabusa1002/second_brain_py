# Domain Business Rules

This document defines the **business rules and invariants of the domain** for the *Second Brain* project.  
These rules must always be enforced, regardless of the interface, API, or technology used.

---

## Principles

* Rules live in the domain, not in the UI
* They must be explicit and verifiable
* They are independent of the database
* Any violation is a system error

---

## User Rules

1. A user with a `status` other than `active` cannot authenticate.
2. A `banned` user cannot perform any action within the system.
3. An `inactive` user cannot create or modify information.
4. Any change to a user’s status must be recorded (auditable in the future).

---

## Account Rules

1. Every account must have at least one owner.
2. Accounts of type `individual` must have exactly one owner.
3. Accounts of type `shared` must have two or more owners.
4. Only account owners can view an account.
5. Only account owners can register transactions in an account.

---

## Category Rules

1. Every category must have a type (`income` or `expense`).
2. The category type must be consistent with the transaction type.
3. Categories cannot be deleted if there are associated transactions.

---

## Transaction Rules

1. Every transaction must belong to a valid account.
2. Every transaction must have a valid category.
3. The transaction amount must always be positive.
4. The sign of the movement is derived from the transaction type and is not stored.
5. The user who creates a transaction must be an owner of the account.
6. The transaction type cannot be modified once the transaction is created.

---

## Access and Visibility Rules

1. A user can only access information from accounts they own.
2. In shared accounts, all owners have the same level of access.
3. Actions must be validated both by user status and account ownership.

---

## Domain Evolution

1. Any new functionality must respect these rules or explicitly extend them.
2. If a rule changes, this document must be updated before implementing the change.

---

This document complements `entities.md` and `use_cases.md` and defines the mandatory behavior of the domain.
