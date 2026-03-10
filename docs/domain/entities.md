# Domain Entities

This document defines the core domain entities for the *Second Brain* project.  
It is the single source of truth for what exists in the system and how concepts relate to each other.

---

## Design principles

* Simplicity over sophistication
* Explicit relationships
* No implicit business rules
* Backend-driven, web first

---

## User

Represents a person who can access the system and operate according to their role.

**Fields:**

* `id`: Unique user identifier.
* `name`: Full name.
* `email`: Email address (unique).
* `password_hash`: Password hash.
* `status`: User status within the system. Possible values: `active`, `inactive`, `banned`, `suspended`, etc.
* `role`: Assigned role (admin, user, etc.).
* `created_at`: User creation date.
* `updated_at`: Last update date.

**Notes:**

* The `status` field controls user access and behavior within the system.
* A user with a status other than `active` should not be able to authenticate.
* A user can own one or more accounts.

---

## Account

Groups transactions and defines whether money is individual or shared.

**Fields:**

* `id`: Unique account identifier.
* `name`: Descriptive account name.
* `type`: Account type. Possible values: `individual`, `shared`.
* `owners`: List of users associated with the account.
* `created_at`: Account creation date.
* `updated_at`: Last update date.

**Notes:**

* Every transaction belongs to exactly one account.
* Shared accounts must have more than one owner.
* Individual accounts must have exactly one owner.
* A user can own multiple accounts.

---

## Category

Classifies a transaction by its nature.

**Fields:**

* `id`: Unique category identifier.
* `name`: Category name.
* `type`: Category type. Possible values: `income`, `expense`.
* `created_at`: Category creation date.
* `updated_at`: Last update date.

**Notes:**

* A transaction has exactly one category.
* In v0.2, categories are global (not user-specific).
* The category type must be consistent with the transaction type.

---

## Transaction

Represents a financial movement within an account.

**Fields:**

* `id`: Unique transaction identifier.
* `date`: Date when the transaction occurs.
* `amount`: Numeric value, always positive.
* `type`: Transaction type. Possible values: `income`, `expense`.
* `category`: Category associated with the transaction.
* `account`: Account to which the transaction belongs.
* `created_by`: User who registered the transaction.
* `description`: Optional text for additional details.
* `created_at`: Record creation date.
* `updated_at`: Last update date.

**Notes:**

* The sign of the amount is derived from the transaction type and is not stored.
* Transactions cannot exist without an account or category.
* `created_by` indicates who registered the transaction, not necessarily the account owner.

---

## Entity relationships

User → Account → Transaction → Category

* Users own accounts.
* Accounts group transactions.
* Transactions are classified by categories.

---

This document must be updated before modifying or adding domain concepts.
