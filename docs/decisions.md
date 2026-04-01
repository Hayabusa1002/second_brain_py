# Functional decisions

## User status machine

| Status   | Allowed actions         |
|----------|-------------------------|
| pending  | Approve, Reject         |
| active   | Ban                     |
| inactive | Reopen request          |
| banned   | Unban                   |

## Role permissions matrix

| Action                                                                        | Admin | Owner | Partner |
|-------------------------------------------------------------------------------|-------|-------|---------|
| Log in                                                                        | Yes   | Yes   | Yes     |
| View own session (`/auth/me`)                                                 | Yes   | Yes   | Yes     |
| Public self-registration (`/auth/register`)                                   | Yes   | Yes   | Yes     |
| Create user from admin panel (`POST /users`)                                  | Yes   | No    | No      |
| List all users                                                                | Yes   | No    | No      |
| List pending users                                                            | Yes   | No    | No      |
| List active users                                                             | Yes   | No    | No      |
| Approve pending users                                                         | Yes   | No    | No      |
| Reject pending users                                                          | Yes   | No    | No      |
| Ban active users                                                              | Yes   | No    | No      |
| Unban banned users                                                            | Yes   | No    | No      |
| Reopen inactive users                                                         | Yes   | No    | No      |
| Delete users                                                                  | Yes   | No    | No      |
| Create individual account                                                     | Yes   | Yes   | Yes     |
| Create shared account                                                         | Yes   | Yes   | No      |
| Update account                                                                | Yes   | Yes   | No      |
| Delete account                                                                | Yes   | Yes   | No      |
| View active users for shared-account owner picker (`/accounts/users/active`)  | Yes   | Yes   | No      |
| Assign owner to shared account                                                | Yes   | Yes   | No      |
| Remove owner from shared account                                              | Yes   | Yes   | No      |
| List own accounts                                                             | Yes   | Yes   | Yes     |
| View account balance                                                          | Yes   | Yes   | Yes     |
| Create transactions                                                           | Yes   | Yes   | Yes     |
| Edit own transactions / allowed transactions                                  | Yes   | Yes   | Yes     |
| Delete own transactions / allowed transactions                                | Yes   | Yes   | Yes     |
| Change own password                                                           | Yes   | Yes   | Yes     |
| Log out                                                                       | Yes   | Yes   | Yes     |
