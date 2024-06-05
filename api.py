from flask import Flask, request, jsonify

app = Flask(__name__)

# Define federal tax brackets and rates
federal_tax_brackets = [55867, 111733, 173205, 246752]
federal_tax_rates = [0.15, 0.205, 0.26, 0.29, 0.33]

# Define provincial tax brackets and rates for Ontario and British Columbia
provincial_tax_data = {
    'ON': {
        'brackets': [51446, 102894, 150000, 220000],
        'rates': [0.0505, 0.0915, 0.1116, 0.1216, 0.1316]
    },
    'BC': {
        'brackets': [47937, 95875, 110076, 133664, 181232, 252752],
        'rates': [0.0506, 0.077, 0.105, 0.1229, 0.147, 0.168, 0.205]
    }
}

def calculate_tax(income, brackets, rates):
    tax = 0
    remaining_income = income
    
    for i in range(len(brackets)):
        if i == 0:
            # First bracket calculation
            if remaining_income > brackets[i]:
                tax += brackets[i] * rates[i]
                remaining_income -= brackets[i]
            else:
                tax += remaining_income * rates[i]
                remaining_income = 0
                break
        else:
            # Subsequent bracket calculations
            if remaining_income > (brackets[i] - brackets[i-1]):
                tax += (brackets[i] - brackets[i-1]) * rates[i]
                remaining_income -= (brackets[i] - brackets[i-1])
            else:
                tax += remaining_income * rates[i]
                remaining_income = 0
                break

    # If income exceeds the highest bracket
    if remaining_income > 0:
        tax += remaining_income * rates[-1]
        
    return tax

@app.route('/calculate-tax', methods=['GET'])
def calculate_tax_break():
    net_income_before_expense = float(request.args.get('netIncomeBeforeExpense'))
    net_income_after_expense = float(request.args.get('netIncomeAfterExpense'))
    province = request.args.get('province')

    if province not in provincial_tax_data:
        return jsonify({'error': 'Invalid province provided'}), 400

    federal_tax_before = calculate_tax(net_income_before_expense, federal_tax_brackets, federal_tax_rates)
    provincial_brackets = provincial_tax_data[province]['brackets']
    provincial_rates = provincial_tax_data[province]['rates']
    provincial_tax_before = calculate_tax(net_income_before_expense, provincial_brackets, provincial_rates)
    total_tax_before = federal_tax_before + provincial_tax_before

    federal_tax_after = calculate_tax(net_income_after_expense, federal_tax_brackets, federal_tax_rates)
    provincial_tax_after = calculate_tax(net_income_after_expense, provincial_brackets, provincial_rates)
    total_tax_after = federal_tax_after + provincial_tax_after

    tax_break = total_tax_before - total_tax_after

    return jsonify({
        'taxBreak': round(tax_break, 2),
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)