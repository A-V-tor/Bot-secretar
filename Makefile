start: # обновление кодовой базы
	poetry run alembic revision --autogenerate -m "Revision $$REVISION_NAME"
	poetry run alembic upgrade head
	systemctl restart redis.service
	systemctl restart bot.service
	systemctl restart adminpanel.service
	systemctl restart celeryd
	systemctl restart celerybeat
	systemctl restart nginx
