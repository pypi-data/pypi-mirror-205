import random

def generate_offer():
    offers = [
        'June 1st 50% Off on all dairy products',
        'June 2nd Donut day buy one get one free',
        'January 19 weight loss day get offers on our healthy range',
        'June 21st Biryani Day pay only half',
        'Diwali Offers on all items ',
        'November 1st Fast Food day all offers',
    ]
    return random.choice(offers)
