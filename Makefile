install: #установка   зависимостей
	poetry install

bot-secretar:
	poetry run bot-secretar

build: #упаковка пакета
	poetry build

publish: #публикация проекта без добавления в индекс
	poetry publish --dry-run

package-install: #установка пакета
	python3 -m pip install --user dist/bot_secretar-0.7.0-py3-none-any.whl

lint: #запуск линтера
	poetry run flake8 bot

inst: # обновление пакета
	python3 -m pip install --upgrade --force-reinstall dist/bot_secretar-0.7.0-py3-none-any.whl