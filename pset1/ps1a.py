#import something

#initial num
current_savings = 0
portion_down_payment = 0.25 
#invest retrun  current_savings*r/12
r = 0.04

annual_salary = int(input("Enter your annual salary:  "))
#dedicate a certain amount of your salary each month to saving forthe down payment.
portion_saved =  float(input("Enter the percent of your salary to save, as a decimal:  "))
total_cost = int(input("Enter the cost of your dream home:  "))

def main():
    month = 0
    while current_savings <= total_cost * portion_down_payment:
        current_savings = annual_salary/12*portion_down_payment + current_savings/12 *r
        month += 1
       print(f"Number of months: {month}")
    
main()
