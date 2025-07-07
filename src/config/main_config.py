import os

from dotenv import load_dotenv

load_dotenv()


class BotConfig:
    token: str = os.getenv("BOT_TOKEN")


class DatabaseConfig:
    host: str = os.getenv("DB_HOST")
    port: str = os.getenv("DB_PORT")
    name: str = os.getenv("DB_NAME")
    username: str = os.getenv("DB_USERNAME")
    password: str = os.getenv("DB_PASSWORD")


class MainMenuMarkupsConfig:
    add_expense: str = "➕ Добавить расход"
    add_income: str = "💰 Добавить доход"
    statistics: str = "📊 Баланс & Статистика"
    goals: str = "🎯 Цели"
    help: str = "ℹ Помощь"
    placeholder: str = "Выберите раздел в меню"


class StatisticsMarkupsConfig:
    monthly_analytics: str = "📈 Аналитика за месяц"


class ExpenseCategoryMarkupConfig:
    products: str = "Продукты"
    transport: str = "Транспорт"
    housing: str = "Жильё"
    shops: str = "Покупки"
    credit: str = "Кредит (ипотека)"


class IncomesCategoryMarkupConfig:
    payment: str = "Зарплата"
    remittance: str = "Перевод"
    business: str = "Бизнес"
    passive: str = "Пассивный доход"


class TransactionsMarkupsConfig:
    cancel: str = "❌ Отмена"
    expenses: ExpenseCategoryMarkupConfig = ExpenseCategoryMarkupConfig()
    incomes: IncomesCategoryMarkupConfig = IncomesCategoryMarkupConfig()


class MarkupsConfig:
    main_menu: MainMenuMarkupsConfig = MainMenuMarkupsConfig()
    statistics: StatisticsMarkupsConfig = StatisticsMarkupsConfig()
    transactions: TransactionsMarkupsConfig = TransactionsMarkupsConfig()


class CallbacksConfig:
    monthly_analytics = "monthly_analytics"


class MainConfig:
    bot: BotConfig = BotConfig()
    database: DatabaseConfig = DatabaseConfig()
    markups: MarkupsConfig = MarkupsConfig()
    callbacks: CallbacksConfig = CallbacksConfig()


config = MainConfig()
