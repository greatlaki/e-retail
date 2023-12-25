from app.celery import app
from provider.services import increase_customers_debt, decrease_customers_debt, clear_customers_debt


@app.task
def increase_debt_task():
    increase_customers_debt()


@app.task
def decrease_debt_task():
    decrease_customers_debt()


@app.task
def clear_debt_task(customer_ids: list[int]):
    clear_customers_debt(customer_ids)
