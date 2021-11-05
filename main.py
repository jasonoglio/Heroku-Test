

# https://www.youtube.com/watch?v=n6I58WJiKGU&t=368s
import argparse

from pywebio.input import input, FLOAT
from pywebio.output import put_text
from pywebio import start_server
import argparse

def main():
    put_text('This is my first interactive web app')
    username = input('Tell me your name', required=True)
    put_text('Hello', username)

# https://www.youtube.com/watch?v=sqR154NkwZk

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()

    start_server(main, port=args.port)

#if __name__ == '__main__':
#main()

#
# https://stackoverflow.com/questions/31684375/automatically-create-requirements-txt





# A simple script to calculate BMI
#def bmi():
#    height = input("Input your height(cm)：", type=FLOAT)
#    weight = input("Input your weight(kg)：", type=FLOAT)
#
#    BMI = weight / (height / 100) ** 2
#
#    top_status = [(16, 'Severely underweight'), (18.5, 'Underweight'),
#                  (25, 'Normal'), (30, 'Overweight'),
#                  (35, 'Moderately obese'), (float('inf'), 'Severely obese')]
#
#    for top, status in top_status:
#        if BMI <= top:
#            put_text('Your BMI: %.1f. Category: %s' % (BMI, status))
#            break
#
#if __name__ == '__main__':
#    bmi()