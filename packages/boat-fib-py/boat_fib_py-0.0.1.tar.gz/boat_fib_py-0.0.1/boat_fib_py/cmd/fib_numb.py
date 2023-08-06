import argparse

from boat_fib_py.fib_calcs.fib_number import recurring_fibonacci_number

def fib_numb() -> None:
    parser = argparse.ArgumentParser(description='Calculate Fib numbers')
    parser.add_argument('--number',action='store',type=int,required=True,help='Fib number to be calculated')
    args = parser.parse_args()
    print(f"Your fib number is:{recurring_fibonacci_number(number=args.number)}")