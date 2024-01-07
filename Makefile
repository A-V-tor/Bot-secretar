start: # обновление кодовой базы
	PATH=$$PATH:./alembic alembic revision --autogenerate -m "Revision $(REVISION_NAME)"
	PATH=$$PATH:./alembic alembic upgrade head
	systemctl restart redis.service
	systemctl restart bot.service
	systemctl restart adminpanel.service
	systemctl restart celeryd
	systemctl restart celerybeat
	systemctl restart nginx
