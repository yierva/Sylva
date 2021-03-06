#!/bin/bash
echo "Before loading, check that tables 'auth_permission', 'django_content_type', 'accounts_account' and 'accounts_userprofile' are empty"
echo "
TRUNCATE CASCADE FROM accounts_userprofile WHERE 1=1;
TRUNCATE CASCADE FROM accounts_account WHERE 1=1;
TRUNCATE CASCADE FROM auth_permission WHERE 1=1;
TRUNCATE CASCADE FROM django_content_type WHERE 1=1;
" > python manage.py dbshell
echo "Remember the ALTER SEQUENCE command in PostgreSQL (try select 'pg_stat_reset();')"
echo "
ALTER SEQUENCE accounts_userprofile_id_seq RESTART WITH 1;
ALTER SEQUENCE accounts_account_id_seq RESTART WITH 1;
" > python manage.py dbshell
python ./manage.py loaddata backups/contenttypes.json
python ./manage.py loaddata backups/sessions.json
python ./manage.py loaddata backups/sites.json
python ./manage.py loaddata backups/messages.json
python ./manage.py loaddata backups/umessages.json
python ./manage.py loaddata backups/south.json
python ./manage.py loaddata backups/auth.json
python ./manage.py loaddata backups/guardian.json
python ./manage.py loaddata backups/accounts.json
python ./manage.py loaddata backups/easy_thumbnails.json
python ./manage.py loaddata backups/base.json
python ./manage.py loaddata backups/engines.json
python ./manage.py loaddata backups/data.json
python ./manage.py loaddata backups/schemas.json
python ./manage.py loaddata backups/graphs.json
python ./manage.py loaddata backups/tools.json
python ./manage.py loaddata backups/search.json
python ./manage.py loaddata backups/operators.json

