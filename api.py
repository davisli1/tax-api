from flask import Flask, request, jsonify

app = Flask(__name__)

# Define tax brackets and rates for British Columbia (BC)
tax_brackets = [10, 20]  # Example tax brackets
tax_rates = [0.05, 0.07]  # Example tax rates

def calculate_tax(income):
    tax = 0
    remaining_income = income

    for i in range(len(tax_brackets)):
        bracket_limit = tax_brackets[i]
        rate = tax_rates[i]

        if remaining_income > bracket_limit:
            tax += bracket_limit * rate
            remaining_income -= bracket_limit
        else:
            tax += remaining_income * rate
            remaining_income = 0
            break

    if remaining_income > 0:
        tax += remaining_income * tax_rates[-1]

    return tax

@app.route('/calculate-tax', methods=['GET'])
def calculate_tax_break():
    net_income_before_expense = float(request.args.get('netIncomeBeforeExpense'))
    net_income_after_expense = float(request.args.get('netIncomeAfterExpense'))

    tax_before = calculate_tax(net_income_before_expense)
    tax_after = calculate_tax(net_income_after_expense)
    tax_break = tax_before - tax_after

    return jsonify({
        'taxBreak': round(tax_break, 2),
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)