#!/bin/bash
python ./manage.py dumpdata --format=json --indent=4 auth > backups/auth.json
python ./manage.py dumpdata --format=json --indent=4 contenttypes > backups/contenttypes.json
python ./manage.py dumpdata --format=json --indent=4 sessions > backups/sessions.json
python ./manage.py dumpdata --format=json --indent=4 sites > backups/sites.json
python ./manage.py dumpdata --format=json --indent=4 messages > backups/messages.json
python ./manage.py dumpdata --format=json --indent=4 umessages > backups/umessages.json
python ./manage.py dumpdata --format=json --indent=4 guardian > backups/guardian.json
python ./manage.py dumpdata --format=json --indent=4 easy_thumbnails > backups/easy_thumbnails.json
python ./manage.py dumpdata --format=json --indent=4 base > backups/base.json
python ./manage.py dumpdata --format=json --indent=4 data > backups/data.json
python ./manage.py dumpdata --format=json --indent=4 graphs > backups/graphs.json
python ./manage.py dumpdata --format=json --indent=4 schemas > backups/schemas.json
python ./manage.py dumpdata --format=json --indent=4 engines > backups/engines.json
python ./manage.py dumpdata --format=json --indent=4 accounts > backups/accounts.json
python ./manage.py dumpdata --format=json --indent=4 tools > backups/tools.json
python ./manage.py dumpdata --format=json --indent=4 search > backups/search.json
python ./manage.py dumpdata --format=json --indent=4 operators > backups/operators.json
python ./manage.py dumpdata --format=json --indent=4 south > backups/south.json
