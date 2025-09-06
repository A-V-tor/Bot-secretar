fill_db:
	poetry shell
	python scripts/add_records_in_db.py
deploy:
	python scripts/dokku/deploy.py
