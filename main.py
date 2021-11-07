

# https://www.youtube.com/watch?v=n6I58WJiKGU&t=368s
import argparse

from pywebio import *
from pywebio.input import *
from pywebio.output import *
import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
from pywebio import start_server
import argparse

def main():
    put_text('This is my first interactive web app')
    username = input('Tell me your name', required=True,
                     help_text='write anything here, your data is not saved',
                     placeholder='Your Name'
                     )
    put_markdown('# Hello %s' %username)



    data = [1000, 1000, 5000, 3000, 4000, 16000, 2000]

    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True

    plt.figure()
    plt.plot([1, 2])

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')

    im = Image.open(img_buf)
    #im.show(title="My Image")

    put_image(src=im)

    img_buf.close()




# https://www.youtube.com/watch?v=sqR154NkwZk

# this section is for Heroku
#if __name__ == '__main__':
#    parser = argparse.ArgumentParser()
#    parser.add_argument("-p", "--port", type=int, default=8080)
#    args = parser.parse_args()
#
#    start_server(main, port=args.port)

if __name__ == '__main__':
    main()

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