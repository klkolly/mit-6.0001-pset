

def main():
    current_savings = 0
    portion_down_payment = 0.25
    #invest retrun  current_savings*r/12
    r = 0.04

    annual_salary = int(input("Enter your annual salary:  "))
    #dedicate a certain amount of your salary each month to saving forthe down payment.
    portion_saved =  float(input("Enter the percent of your salary to save, as a decimal:  "))
    total_cost = int(input("Enter the cost of your dream home:  "))
    semi_annual_raise= float(input("Enter the semi_annual raise, as a decimal:  "))

    month = 0
    month_salary_portion=annual_salary*portion_saved/12
    while current_savings <= total_cost * portion_down_payment:
        current_savings += month_salary_portion + (current_savings*r/12 )

        month += 1
        if month%6 == 0:
            month_salary_portion = month_salary_portion * (1 + semi_annual_raise)
    print(f"Number of months: {month}")

main()
