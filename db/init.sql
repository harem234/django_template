CREATE USER django_template_user_0 WITH ENCRYPTED PASSWORD 'h@unter2@';
CREATE DATABASE django_template_db_0;
GRANT ALL PRIVILEGES ON DATABASE django_template_db_0 TO django_template_user_0;

-- slight better performance with django
ALTER ROLE django_template_user_0 SET client_encoding TO 'utf8';
ALTER ROLE django_template_user_0 SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_template_user_0 SET timezone TO 'UTC';