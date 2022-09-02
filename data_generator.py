from csv import reader as csv_reader
from collections import defaultdict

categories = {}
category_price_range = {}

with open('purchase_categories.csv') as f:
    categories_reader = csv_reader(f)
    next(categories_reader)
    probabilities_sum = 0
    for category, price_range_min, price_range_max, probability in categories_reader:
        probability = float(probability)
        probabilities_sum += probability
        categories[category] = probability

        category_price_range[category] = float(price_range_min), float(price_range_max)

    for category, probability in categories.items():
        categories[category] = probability / probabilities_sum

purchase_names = defaultdict(dict)

with open('purchase_names.csv') as f:
    purchase_names_reader = csv_reader(f)
    next(purchase_names_reader)
    probabilities_sums = defaultdict(int)
    for purchase_name, category, probability, regularity_probability in purchase_names_reader:
        purchase_names[category][purchase_name] = float(probability), float(regularity_probability)
        probabilities_sums[category] += float(probability)

    for category, purchase_names_list in purchase_names.items():
        purchase_names[category] = {name: (probability / probabilities_sums[category], regularity_probability) for name, (probability, regularity_probability) in purchase_names_list.items()}

desired_num_of_rows = 100

from random import choices, random


def rand_with_range(min, max):
    r = max - min
    return random() * r + min


with open('result.csv', 'w') as f:
    print('purchase_name,price,category,month,is_regular', file=f)
    generated_categories = choices(population=list(categories.keys()), weights=list(categories.values()), k=desired_num_of_rows)
    generated_months = choices(population=[month + 1 for month in range(11)], k=desired_num_of_rows)
    for category, month in zip(generated_categories, generated_months):
        min_price, max_price = category_price_range[category]
        price = round(rand_with_range(min_price, max_price), 1)
        category_purchase_names = purchase_names[category]
        purchase_name = choices(population=list(category_purchase_names.keys()), weights=list(map(lambda x: x[0], category_purchase_names.values())))[0]
        regularity_probability = purchase_names[category][purchase_name][1]
        is_regular = choices(population=[True, False], weights=[regularity_probability, 1 - regularity_probability])[0]
        print(purchase_name, price, category, month, is_regular, sep=',', file=f)
