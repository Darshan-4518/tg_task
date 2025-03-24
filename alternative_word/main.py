import json

def is_digits_available(value):
    characters = "0123456789"
    for ch in characters:
        if ch in value:
            return True
    return False

def find_alternative_for_id_or_name_or_data(locator_val):
    if is_digits_available(locator_val):
        return None
    return locator_val

def find_alternative_for_css_selector(locator_val):
    split_by = ""

    if "#" in locator_val:
        split_by = "#"
    elif "."  in locator_val:
        split_by = "."

    after_split_by_hash = locator_val.split(split_by)

    if is_digits_available(after_split_by_hash[1]):
        return None

    return after_split_by_hash[1]


def get_locator_from_xpath(locator_val):
    sub1 = locator_val[locator_val.find('@') + 1:-1]
    split = sub1.split("=")
    identifier = split[0]
    value = split[1]
    return [identifier,value]


def find_alternative_for_class_locator(locator_val):
    class_names = locator_val.split(" ")
    words = []
    for name in class_names:
        if not is_digits_available(name):
            words.append(name)
    if len(words) == 0:
        return None
    return words

def find_alternative_words(locator,locator_val):
    locator = locator.lower()
    if locator == "id":
        return find_alternative_for_id_or_name_or_data(locator_val)
    elif locator == "css selector":
        return find_alternative_for_css_selector(locator_val)
    elif locator == "name":
        return find_alternative_for_id_or_name_or_data(locator_val)
    elif locator == "class":
        return find_alternative_for_class_locator(locator_val)
    elif "data" in locator:
        return find_alternative_for_id_or_name_or_data(locator_val)
    elif locator == "xpath" and  not locator_val.startswith("//html"):
        locator,locator_val = get_locator_from_xpath(locator_val)
        return find_alternative_words(locator,locator_val)




with open("data.json","r") as file:
    data = json.load(file)
    for dictionary in data:
        return_vals = find_alternative_words(dictionary['locators'],dictionary['locators_val'])
        if return_vals:
            print(return_vals)

