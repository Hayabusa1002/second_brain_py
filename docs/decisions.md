# Functional decisions

## User status machine

| Status   | Allowed actions         |
|----------|-------------------------|
| pending  | Approve, Reject         |
| active   | Ban                     |
| inactive | Reopen request          |
| banned   | Unban                   |
