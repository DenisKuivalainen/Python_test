"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from currency_checker import CurrencyChecker

if __name__ == "__main__":
    ceo_name = "АКуйвалайнен Денис"
    ceo_email = "kuyvalaynen@gmail.com"

    checker = CurrencyChecker(ceo_name, ceo_email)
    checker.run(timeout=30, currencies=["USD", "EUR", "AAA"])
