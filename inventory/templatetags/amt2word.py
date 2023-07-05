from django.template import Library
# from num2words import num2words

import decimal    

def num2words(num):
    
    num = int(num)

    under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

    if num < 20:
        return under_20[num]

    if num < 100:
        return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])

    return num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot==0 else ' ' + num2words(num % pivot))



register = Library()

@register.filter
def amt2word(num):
    tmp = ""
    ls = str(num).split(".")
    if ls[0]:
        tmp = str(num2words(int(ls[0]))) + " rupee "
    if len(ls)>1:
        if ls[0] == '0':
            tmp += str(num2words(int(ls[1])) + " paise ")
        else:
            tmp += "and " + str(num2words(int(ls[1])) + " paise ")

    tmp += "only "
    return tmp