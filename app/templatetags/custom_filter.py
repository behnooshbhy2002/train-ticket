from django import template
from datetime import datetime, date


register = template.Library()

# this filter is for getting total passenger by addding number of adult and child
@register.filter(name="passengers")
def passengers(adult, child):
    adult = int(adult)
    child = int(child)
    return adult + child

# this filter is for multiplying total passenger with class price
@register.filter(name="multiply")
def multiply(price, passenger):
    if passenger is None or price is None:
        return 0
    return passenger * price

# this filter is for getting duration between departure time to arrival time
@register.filter(name="duration")
def duration(departure, arrival):
    if not departure or not arrival:
        return "N/A"  # Return a default value if either time is None
    sub = datetime.combine(datetime.min, departure) - datetime.combine(datetime.min, arrival)
    return str(abs(sub))
    
                                                                      