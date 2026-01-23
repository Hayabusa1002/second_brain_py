# Domain Use Cases

This document describes the main use cases of the *Second Brain* system.  
It defines **what the user can do** and **how they interact with the entities**, without going into technical implementation details.

---

## Principles

* User-centered
* UI-independent
* Domain-driven, not database-driven
* Evolutive

---

## UC-01: User registration

**Actor:** User

**Description:**  
Allows a person to create an account to access the system.

**Main flow:**

1. The user enters name, email, and password.
2. The system validates that the email does not already exist.
3. The user is created with `active` status.

**Rules:**

* The email must be unique.
* The password is stored as a hash.

---

## UC-02: Create account

**Actor:** Authenticated user

**Description:**  
Allows creating an individual or shared financial account.

**Main flow:**

1. The user defines the account name and type.
2. Assigns one or more owners.
3. The system creates the account.

**Rules:**

* Individual accounts must have a single owner.
* Shared accounts must have at least two owners.

---

## UC-03: Register transaction

**Actor:** Authenticated user

**Description:**  
Allows registering an income or expense in an account.

**Main flow:**

1. The user selects an account and category.
2. Defines date, amount, and type.
3. The system registers the transaction.

**Rules:**

* The amount must be positive.
* The type determines the logical sign of the movement.

---

## UC-04: View transactions

**Actor:** Authenticated user

**Description:**  
Allows viewing personal or shared transactions.

**Main flow:**

1. The user selects an account.
2. Applies filters by date, type, or category.
3. The system displays the list.

**Rules:**

* The user can only view accounts where they are an owner.

---

This document must remain aligned with `entities.md`.