def sampletext():
    print('Hello, welcome to QuickSample package.')

def sort_on_key(key, list):
    return sorted(list, key=lambda i: i[key])

def return_only_values(dict):
    return dict.keys()