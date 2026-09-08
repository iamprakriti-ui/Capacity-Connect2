# CAPACITY CONNECT Authentication Testing

1. POST `/api/auth/login` with `employee@capacityconnect.demo` / `Demo123!`, store cookies, then GET `/api/auth/me`.
2. Verify employee can GET `/api/dashboard` and cannot GET `/api/trainer/learners`.
3. Login as `trainer@capacityconnect.demo` / `Demo123!`; verify trainer learner and analytics endpoints.
4. Login as `admin@capacityconnect.demo` / `Admin123!`; verify `/api/admin/summary`.
5. POST `/api/auth/logout`; verify `/api/auth/me` returns 401.
6. Register a new employee, verify login, then exercise forgot-password response and reset validation.
