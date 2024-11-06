# 🌟 Twinkle

**Twinkle** — это многофункциональное приложение для отслеживания калорий и управления питанием, помогающее вам достичь ваших целей в питании и фитнесе. Приложение позволяет вести дневник питания, строить планы питания, создавать расписание тренировок и получать напоминания о питье воды.

## 📋 Основные функции

- **Дневник питания**: Легко добавляйте и отслеживайте свой рацион.
- **План питания**: Составляйте персонализированные программы питания.
- **План тренировок**: Строьте программу тренировок и отслеживайте прогресс.
- **Напоминания о воде**: Регулярные уведомления о питье воды через Telegram-бот.
- **Импорт данных**: Автоматический сбор информации о питательных продуктах и упражнениях из каталога **DailyFit**.

## 🚀  Стек технологий

- **Backend**: FastAPI + PostgreSQL
- **Frontend**: HTML + JavaScript для создания удобного интерфейса
- **Авторизация**: Безопасность с использованием JWT-токенов 🔒
- **Парсер данных**: Beautiful Soup для извлечения информации из каталога DailyFit 
- **Telegram-бот**: aiogram для напоминаний о питье воды 

## 🔒 JWT tokens
- Безопасная авторизация по сессионным токенам, которая обеспечивает надежность и конфидециальность

## 🤖 Telegram-бот
- Telegram-бот отправляет напоминания о питье воды. Чтобы начать использовать, выполните команду /start в Telegram, и бот будет отправлять уведомления в течение дня.

## 📊 Парсер данных
- Парсер, созданный на основе Beautiful Soup, автоматически собирает информацию из каталога DailyFit и сохраняет её в базе данных для удобного доступа и использования в приложении.

## 🐋 Запуск через Docker Compose
- Для удобного развертывания можно использовать Docker Compose. Создайте файл docker-compose.yml

## 💡 Планы на будущее
- Добавить тестирование API с pytest
- Усовершенствовать вронтенд приложения
- Добавить асинхронность