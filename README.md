## Финансовый бот
  
Финансовый ассистент — это чат-бот, предназначенный для помощи пользователям в управлении личными финансами. Его основная задача — повышение финансовой грамотности и формирование осознанного финансового поведения. Программа позволяет легко отслеживать доходы и расходы, анализировать финансовые привычки, ставить цели и получать напоминания о регулярных платежах. Особенностью бота является его интеграция в мессенджер, что делает процесс управления бюджетом простым, быстрым и доступным для всех пользователей, включая тех, кто не имеет экономического образования.
  
Разрабатываемый финансовый ассистент решает проблему отсутствия систематического подхода к управлению финансами, которая может привести к неэффективному расходованию средств, накоплению долгов и снижению финансовой стабильности. Осложняют задачу такие факторы, как разнообразие финансовых привычек пользователей, необходимость простого и интуитивного интерфейса, а также конкуренция с платными аналогами.
  
  
## Запуск

Для запуска приложения добавьте следующие переменные окружения:
1. BOT_TOKEN - токен вашего бота
2. DB_HOST - hostname базы данных
3. DB_PORT - port - базы данных
4. DB_NAME - имя базы данных
5. DB_USERNAME - имя пользователя базы данных
6. DB_PASSWORD - пароль пользователя базы данных
  
После, запустите `docker-compose` с помощью команды:
```bash
docker-compose up --build -d
```
  
Если вы планируете запускать бота без использования `Docker`, создайте базу данных `Postgres` с указанными вами ранее параметрами.

Теперь подключитесь к базе данных и запустите команды:
```sql
CREATE TABLE users(
	id SERIAL PRIMARY KEY,
	telegram_id VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE expenses(
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	value FLOAT NOT NULL DEFAULT 0,
	category VARCHAR(20) NOT NULL,
	date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE incomes(
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	value FLOAT NOT NULL DEFAULT 0,
	category VARCHAR(20),
	date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE notifies(
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL,
	last_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	description VARCHAR(100) NOT NULL,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE goals(
	id SERIAL PRIMARY KEY,
	user_id INT NOT NULL UNIQUE,
	max_value FLOAT NOT NULL DEFAULT 0,
	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```
  
Бот готов к использованию!