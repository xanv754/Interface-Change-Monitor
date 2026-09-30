# REFACTOR.md — Refactor por capas

> Documento vivo. Índice general del refactor del backend, capa por capa, siguiendo el orden `data/` → `access/` → `business/` → `presentation/`. El detalle de cada capa (funcionamiento general, bugs encontrados, refactorizaciones urgentes/menores, análisis de seguridad, análisis de pruebas unitarias y comentarios extra) vive en su propio documento — ver "Índice de capas" abajo. Este archivo solo mantiene el resumen ejecutivo de "Estado general" y se actualiza a medida que se resuelven hallazgos o aparecen nuevos en cualquiera de las capas.

## Índice de capas

- [REFACTOR-DATA.md](REFACTOR-DATA.md) — capa `data/`.
- [REFACTOR-ACCESS.md](REFACTOR-ACCESS.md) — capa `access/`.
- [REFACTOR-BUSINESS.md](REFACTOR-BUSINESS.md) — capa `business/`.
- [REFACTOR-PRESENTATION.md](REFACTOR-PRESENTATION.md) — capa `presentation/`.

## Estado general

- ✅ **`data/`** — migrada a SQLAlchemy ORM. 14/14 bugs y 16/17 refactorizaciones resueltos (queda pendiente, a propósito, un sistema de migraciones versionado con Alembic). 32 pruebas en `tests/data/`. Detalle en REFACTOR-DATA.md.
- ✅ **`access/`** — migrada a SQLAlchemy ORM sobre el `data/` ya migrado. 7/7 bugs y 11/12 refactorizaciones resueltos (queda pendiente, a propósito, sacar la normalización de negocio de `UserQuery` hacia `business/`). 44 pruebas nuevas en `tests/access/`. Detalle en REFACTOR-ACCESS.md.
- ⏳ **`business/`** — `api/`, `controllers/`, `cli/` y `models/` refactorizados (`ResponseCode` reemplazado por `BusinessError` + exception handler global), verificados (`/verify`) y con **123 pruebas nuevas** en `tests/business/`. 8/13 bugs (los 5 críticos: los 3 originales + 2 encontrados al escribir las pruebas, ambos ya resueltos) y 2/7 refactors urgentes resueltos; `updater/libs/{ping,snmp,ssh,host}.py` queda pendiente a propósito para una sub-sesión dedicada (concentra el resto de los hallazgos urgentes/seguridad, y sus pruebas). Detalle en REFACTOR-BUSINESS.md.
- ⏳ **`presentation/`** — 8/8 bugs y 13/13 refactors menores resueltos, y 6/8 hallazgos de seguridad resueltos (cookie `secure`/`expires`, guard de rutas vía `middleware.ts`, validación runtime con Zod, headers de seguridad básicos, y el bug real de contraseña-en-query-string; `business/` ganó de paso una cookie httpOnly aditiva en el login, sin romper el header `Authorization` existente — 123 pruebas de `tests/business/` en verde). Además, se rediseñó visualmente toda la capa (nueva identidad "profesional/seria/moderna": tokens de color/tipografía, `@layer components` de Tailwind, `StatusBadge`, fila de diff old→new compacta en las listas de cambios) preservando el 100% de las funciones/controles existentes — verificado con `tsc`, `bun run build`, `next lint` limpio, y un recorrido end-to-end real contra backend + Postgres (login, asignación, cambio de estatus, cambio de contraseña, todos con datos reales). Quedan pendientes 5 refactors urgentes, 2 hallazgos de seguridad (migrar el cliente a la cookie httpOnly, CSP completo) y las pruebas de `presentation/` (`PRUEBAS POR IMPLEMENTAR`, ningún framework configurado). Detalle en REFACTOR-PRESENTATION.md.

**Próximo paso concreto:** dos sub-sesiones pendientes de implementación en paralelo, sin orden estricto entre ellas: la de `updater/libs/{ping,snmp,ssh,host}.py` (dentro de `business/`) y el resto de `presentation/` — empezando por el `ApiClient` centralizado (ver el orden recomendado dentro de REFACTOR-PRESENTATION.md, sección "Comentarios extras").
