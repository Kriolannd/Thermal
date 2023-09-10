up:
	@echo "Запуск приложения"
	docker compose up
update:
	@echo "Обновление подмодулей"
	git submodule update --init --recursive