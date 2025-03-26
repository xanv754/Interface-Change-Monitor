# Interface Change Monitor Server
---
# Environment Variables
This is a list of environment variables that be required to run the system:
```bash
URI=postgresql://postgres:postgres@localhost:5432/postgres
URI_TEST=postgresql://postgres:postgres@localhost:5432/postgres
SECRET_KEY=secret
```

You can generate a secret key with the following command:
```bash
openssl rand -hex 32
```