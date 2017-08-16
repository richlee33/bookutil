import bookendpoint
import pandas
import ast


def build_library(search):
#creates a list of books, ie a library of the required size.
#duplicate ids are not saved to the library

    min_books = 100
    max_books = 200
    library = []

    book_request = bookendpoint.Book_Request()

    start_index=0

    if len(search)== 0:
        return None


    while len(library) < min_books: 
        response = book_request.get_books(search=search, startIndex=start_index)
        list_books = response.json()['items']

        for item in list_books:
            if duplicate_id(library, item['id']):
                pass
            else:
                library.append(item)
             

        start_index = len(library) - 1

    return library


def duplicate_id(library, book_id):
#checks list of books for specified book_id

    for item in library:
        if book_id == item['id']:
            return True

    #no existing id found
    return False


def group_by_publisher(library):
#takes a list of books and creates a dictionary of publishers that contains a list of books

    publisher = {}
    item_publisher = ''

    for item in library:
        try:
            item_publisher = item['volumeInfo']['publisher'] 
        except KeyError:
            item_publisher = "No Publisher"

        if item_publisher not in publisher:
            publisher[item_publisher] = []
            
        publisher[item_publisher].append(item)

    return publisher


def group_by_format(library):
#takes a list of books and creates a dictionary of formats that contains a list of books

    formats = {'epub':[],
               'pdf':[]}

    for item in library:
        try:
            epub_avail = item['accessInfo']['epub']['isAvailable']
        except KeyError:
            epub_avail = None

        try:
            pdf_avail = item['accessInfo']['pdf']['isAvailable']
        except KeyError:
            pdf_avail = None

        if epub_avail == True:
            formats['epub'].append(item)

        if pdf_avail == True:
            formats['pdf'].append(item)

    return formats


def print_grouped_dict(dictionary):
#helper function that takes a dictionary of lists and prints the key a unique set of book attributes

    keys = dictionary.keys()

    for item in keys:
        print ("==============================================")
        print (item)
        print_list_books(dictionary[item])


def print_list_books(l, volume_attribute=None, price_attribute=None):
#helper function that takes a list of books and prints a unique set of book attributes

    if volume_attribute == None:
        volume_attribute = 'ratingsCount'

    if price_attribute == None:
        price_attribute = 'listPrice'

    for item in l:
        print ("    " + "--------------------------------------")
        print ("    id: " + item['id'])
        print ("    title: " + item['volumeInfo']['title'])
        try:
            print ("    subtitle: " + item['volumeInfo']['subtitle'])
        except KeyError: pass
        try:
            author_string = ", ".join(item['volumeInfo']['authors'])
            print ("    author: " + author_string)
        except KeyError: pass
        try:
            print ("    publisher: " + item['volumeInfo']['publisher'])
        except KeyError: pass
        try:
            print ("    " + volume_attribute + ": " + str(item['volumeInfo'][volume_attribute]))
        except KeyError: pass
        try:
            print ("    " + price_attribute + ": " + str(item['saleInfo'][price_attribute]['amount']))
        except KeyError: pass


def sort_by_volumeInfo(library, attribute=None, reverse=None):
#takes a list of books and string attribute under volumeInfo and performs sort
#NOTE books that are missing the attribute are not included

    sorted_list = []
    sort_list = []
    missing_attribute_list = []

    if attribute == None:
        attribute = 'ratingsCount'

    if reverse == None:
        reverse = False

    #separate books without the attribute to sort against otherwise sorted breaks
    for item in library:
        try:
            value = item['volumeInfo'][attribute]
        except KeyError:
            missing_attribute_list.append(item)
        else:
            sort_list.append(item)

    sorted_list = sorted(sort_list, key=lambda k: k['volumeInfo'][attribute], reverse=reverse)

    return sorted_list


def sort_by_price(library, attribute=None, reverse=None):
#takes a list of books and a string attribute under saleInfo and performs sort
#allowed attributes are listPrice or retailPrice
#NOTE books that are missing the attribute are not included

    sorted_list = []
    sort_list = []
    missing_attribute_list = []

    if attribute == None:
        attribute = 'listPrice'

    if reverse == None:
        reverse = False

    #separate books without the attribute to sort against otherwise sorted breaks
    for item in library:
        try:
            value = item['saleInfo'][attribute]['amount']
        except KeyError:
            missing_attribute_list.append(item)
        else:
            sort_list.append(item)

    sorted_list = sorted(sort_list, key=lambda k: k['saleInfo'][attribute]['amount'], reverse=reverse)

    return sorted_list


def flatten_json(dictionary, delim):
#takes dictionary formatted in json and formats to remove the nesting
#https://stackoverflow.com/questions/1871524/how-can-i-convert-json-to-csv

    flattened_dict = {}

    for i in dictionary.keys():
        if isinstance(dictionary[i], dict):
            get = flatten_json(dictionary[i], delim)
            for j in get.keys():
                flattened_dict[i + delim + j] = get[j]
        else:
            flattened_dict[i] = dictionary[i]

    return flattened_dict


def unflatten_json(dictionary, delim):
#takes dictionary without any nesting and puts back the nesting
#https://github.com/amirziai/flatten/blob/master/flatten_json.py#L72
    
    unflattened_dict = {}

    def _unflatten(dic, keys, value):
        for key in keys[:-1]:
            dic = dic.setdefault(key, {})

        dic[keys[-1]] = value

    for item in dictionary:
        _unflatten(unflattened_dict, item.split(delim), dictionary[item])

    return unflattened_dict


def save_to_csv(library, file_name):
#saved a list of books with the specified file name
    import pandas

    flattened_list = []

    #convert list if dictionaries into list of flattened dictionaries
    for item in library:
        flat_dict = flatten_json(item, "___")
        flattened_list.append(flat_dict)

    df = pandas.DataFrame(flattened_list)
    df.to_csv(file_name, encoding='utf-8', index=False)


def load_csv(file_name):
#load a list of books from the specified file name

    loaded_list = []
    unflattened_list = []

    def _remove_nan_keys(d):

        key = []
        key = d.keys()
        for item in key:
            if pandas.isnull(d[item]):
                del d[item]


    def _convert_unicode_to_list(d):
    #fix values that are unicode objects that contain lists to be list objects

        key = []
        key = d.keys()

        for item in key:
            list_value = []    #store fixed list value
            if isinstance(d[item], unicode):
                if '[' in d[item] and ']' in d[item]:
                    try:
                        list_value = ast.literal_eval(d[item])
	            #except SyntaxError:
	            except:
                        if ' ' in d[item]:
                            #handles author first and last name and multiple authors
                            list_value = d[item][1:-1].split(', ')
                        else:
                            #handles single item and one word in list
                            list_value.append(d[item][1:-1])
             
            if len(list_value) > 0:
                d[item] = list_value

    df = pandas.read_csv(file_name, encoding='utf-8')
    loaded_list = df.to_dict('records')

    for item in loaded_list:
        _remove_nan_keys(item)
        _convert_unicode_to_list(item)
        if duplicate_id(unflattened_list, item['id']):
            pass
        else:
            unflattened_list.append(unflatten_json(item, "___"))

    return unflattened_list



