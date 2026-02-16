from django import template
import datetime

register = template.Library()

days = {
    1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth",
    6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth", 10: "Tenth",
    11: "Eleventh", 12: "Twelfth", 13: "Thirteenth", 14: "Fourteenth",
    15: "Fifteenth", 16: "Sixteenth", 17: "Seventeenth", 18: "Eighteenth",
    19: "Nineteenth", 20: "Twentieth", 21: "Twenty First",
    22: "Twenty Second", 23: "Twenty Third", 24: "Twenty Fourth",
    25: "Twenty Fifth", 26: "Twenty Sixth", 27: "Twenty Seventh",
    28: "Twenty Eighth", 29: "Twenty Ninth", 30: "Thirtieth",
    31: "Thirty First"
}

months = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December"
}


def year_to_words(year):
    nums = {
        0:"Zero",1:"One",2:"Two",3:"Three",4:"Four",5:"Five",
        6:"Six",7:"Seven",8:"Eight",9:"Nine",10:"Ten",
        11:"Eleven",12:"Twelve",13:"Thirteen",14:"Fourteen",
        15:"Fifteen",16:"Sixteen",17:"Seventeen",18:"Eighteen",19:"Nineteen"
    }

    tens = {
        2:"Twenty",3:"Thirty",4:"Forty",5:"Fifty",
        6:"Sixty",7:"Seventy",8:"Eighty",9:"Ninety"
    }

    if year < 20:
        return nums[year]

    if year < 100:
        return tens[year//10] + (" " + nums[year%10] if year%10 else "")

    if year < 1000:
        return nums[year//100] + " Hundred " + year_to_words(year%100)

    if year < 10000:
        return year_to_words(year//1000) + " Thousand " + year_to_words(year%1000)

    return str(year)


@register.filter
def date_in_words(value):
    if not value:
        return ""

    if isinstance(value, datetime.date):
        day = days[value.day]
        month = months[value.month]
        year = year_to_words(value.year)

        return f"{day} {month} {year}"

    return value
