



def main():

    portion_down_payment = 0.25
    #invest retrun  current_savings*r/12
    r = 0.04

    total_cost = 1000000
    semi_annual_raise= 0.07

    annual_salary = int(input("Enter your annual salary:  "))
    #dedicate a certain amount of your salary each month to saving forthe down payment.

    #cant pay
    if annual_salary < 62523 :
        print("it is not possible to pay down payment in three years")
        return


    rate_max = 10000
    rate_min = 0
    step = 0

    current_savings = 0
    while abs(total_cost * portion_down_payment-current_savings ) > 100 :
        step += 1
        portion_saved = (rate_max + rate_min)/2
        month_salary_portion=annual_salary*(portion_saved/10000)/12

        current_savings = 0
        for i in range(1,37):
            current_savings += month_salary_portion + (current_savings*r/12 )
            if i%6 == 0:
                month_salary_portion = month_salary_portion * (1 + semi_annual_raise)

        if current_savings < total_cost * portion_down_payment: #存少了
            rate_min = portion_saved
        else:
            rate_max = portion_saved

    print(f"best saving rate:{ int(portion_saved + 0.5)/10000}")
    print("steps in bisecton search:", step)


main()
