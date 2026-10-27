#!/bin/sh
# Primera vez que arranca la base en Docker: los dos usuarios de Vitalia y la base de desarrollo.
# El dueño de las tablas lo usan las migraciones y las pruebas; la aplicación usa vitalia_api,
# que no es dueño de nada y no puede saltarse los permisos por fila.
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<SQL
CREATE ROLE vitalia_migraciones LOGIN CREATEDB PASSWORD '$CLAVE_MIGRACIONES';
CREATE ROLE vitalia_api LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS PASSWORD '$CLAVE_API';
CREATE DATABASE vitalia_dev OWNER vitalia_migraciones;
SQL
