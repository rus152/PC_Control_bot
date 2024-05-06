# Бот для дистанционного управления ПК

## Готово на данный момент или в процессе доработки

- [x] Система выключения ПК с отменой его отключения
- [x] Логин система 
- [X] Устойчивость к вылетам
- [X] Система скриншота
- [ ] Управление приложением из трея
- [ ] Интерфейс

## Что дальше?
- [ ] Блокировка компа
- [ ] Перевод системы в гибернацию/сон
- [ ] Автозапуск
- [ ] Приоритет запуск от админа(По желанию, например для просмотра температуры пк)
- [ ] Переезд на ctk

## Код для компиляции
```
pyinstaller --onefile --windowed --add-data "C:\Users\Ruslan\Documents\GitHub\PC_Control_bot\icon.png;." --add-data "C:\Users\Ruslan\Documents\GitHub\PC_Control_bot\logo_screenshot.png;." --add-data "C:\Users\Ruslan\Documents\GitHub\PC_Control_bot\logo_error.png;." --add-data "C:\Users\Ruslan\Documents\GitHub\PC_Control_bot\logo_init.png;." --add-data "C:\Users\Ruslan\Documents\GitHub\PC_Control_bot\logo_ping.png;." --add-data "C:\Users\Ruslan\Documents\GitHub\PC_Control_bot\logo_work.png;." "C:\Users\Ruslan\Documents\GitHub\PC_Control_bot\main.py" --icon="C:\Users\Ruslan\Documents\GitHub\PC_Control_bot\icon.ico"
```