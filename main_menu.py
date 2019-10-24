from utils import *


def book_menu():

    main_menu = {}
    main_menu['1']="Create New Library" 
    main_menu['2']="Load Library from a CSV"
    main_menu['3']="Save Library to a CSV"
    main_menu['4']="Group Books"
    main_menu['5']="Sort Books"
    main_menu['6']="Print Library"
    main_menu['9']="Exit"

    group_menu = {}
    group_menu['1']="Group by Publishers and Print"
    group_menu['2']="Group by Publishers and Save as CSV"
    group_menu['3']="Group by Available Formats and Print"
    group_menu['4']="Group by Available Formats and Save as CSV"
    group_menu['9']="Back to Main Menu"

    sort_menu = {}
    sort_menu['1']="Sort by Price"
    sort_menu['2']="Sort by Average Rating"
    sort_menu['3']="Sort by Rating Count"
    sort_menu['4']="Sort by Published Date"
    sort_menu['5']="Sort by Page Count"
    sort_menu['9']="Back to Main Menu"

    library = []
    search_string = ''

    while True: 
        main_options=list(main_menu.keys())
        main_options.sort()
        print("====Main Menu====")
        if (len(library) == 0):
            #empty libray so only allow menu items for build new library or load library from csv
            entry = [0, 1, 6]
            for item in entry:
                print(main_options[item], main_menu[main_options[item]])
        else:
            #full menu allowed
            for entry in main_options: 
                print(entry, main_menu[entry])

        selection=input(">>>Please Select:") 

        if selection == '1': 
            #build library
            search_string = str(input(">>>Search String:"))
            if len(search_string) > 0:
                library = build_library(search_string)
                print((str(len(library)) + " books in library."))
            else:
                print("Blank search string.  Please enter a search string")

        elif selection == '2':
            #load library
            file_name = str(input(">>>File Name to load from:"))
            if len(file_name) > 0:
                try:
                    library = load_csv(file_name)
                    print((str(len(library)) + " books in library."))
                except IOError:
                    print("File not found.  Please enter valid file name")
            else:
                print("Blank file name.  Please enter file name.")

        elif selection == '3': 
            #save library
            if len(library) > 0:
                file_name = str(input(">>>File name to save to:"))
                if len(file_name) == 0:
                    print("Blank file name.  Please enter a file name.")
                else:
                    save_to_csv(library, file_name)
            else:
                print("No books in library.  Please Create or Load a library first.")

        elif selection == '4':
            #group library
            stay_submenu = True
            
            if len(library) == 0:
                #nothing to do get out of submenu
                stay_submenu = False

            while stay_submenu:
                group_options=list(group_menu.keys())
                group_options.sort()
                print("====Group By Menu====")
                for subentry in group_options:
                    print(subentry, group_menu[subentry])

                subselection=input(">>>Please Select:")

                if subselection == '1':
                    #publisher to screen
                    dict_pub = group_by_publisher(library)
                    print_grouped_dict(dict_pub)

                elif subselection == '2':
                    #publisher to csv
                    file_name = ''
                    list_dict_pub = []
                    publishers = []
                    publisher_books = []

                    dict_pub = group_by_publisher(library)
                    
                    #build list of grouped books
                    pub_keys = list(dict_pub.keys())
                    for item in pub_keys:
                        publisher_books = dict_pub[item]
                        list_dict_pub.extend(publisher_books)
                    file_name =input(">>>Enter file name to save:") 
                    if len(file_name) == 0:
                        print("Blank file name.  Please enter a file name.")
                    else:
                        save_to_csv(list_dict_pub, file_name) 

                elif subselection == '3':
                    #formats to screen
                    dict_formats = group_by_format(library)
                    print_grouped_dict(dict_formats)

                elif subselection == '4':
                    #formats to csv"
                    dict_formats = []
                    file_name = ''
                    list_dict_formats = []
                
                    dict_formats = group_by_format(library)
                    
                    #build list of grouped books
                    format_keys = list(dict_formats.keys())
                    for item in format_keys:
                        list_dict_formats.extend(dict_formats[item])
                    file_name =input(">>>Enter file name to save:")    
          
                    if len(file_name) == 0:
                        print("Blank file name.  Please enter a file name.")
                    else:
                        save_to_csv(list_dict_formats, file_name)

                elif subselection == '9':
                    print("exit group")
                    stay_submenu = False
                else:
                    print("Invalid menu item chosen.")

        elif selection == '5':
            #sort library
            stay_submenu = True

            if len(library) == 0:
                #nothing to do get out of submenu
                stay_submenu = False

            while stay_submenu:
                sort_options=list(sort_menu.keys())
                sort_options.sort()
                print("====Sort Menu====")
                for subentry in sort_options:
                    print(subentry, sort_menu[subentry])
                subselection=input(">>>Please Select:")

                if subselection == '1':
                    print("price")
                    #set the attribute below to sort on retail or list price
                    #price_attribute="retailPrice"
                    price_attribute="listPrice"

                    lib_sorted = sort_by_price(library, price_attribute)
                    print_list_books(lib_sorted, price_attribute = price_attribute)

                elif subselection == '2':
                    print("average rating")
                    volume_attribute = "averageRating"
                    lib_sorted = sort_by_volumeInfo(library, volume_attribute)
                    print_list_books(lib_sorted, volume_attribute = volume_attribute)

                elif subselection == '3':
                    print("ratings count")
                    volume_attribute = "ratingsCount"
                    lib_sorted = sort_by_volumeInfo(library, volume_attribute)
                    print_list_books(lib_sorted, volume_attribute = volume_attribute)

                elif subselection == '4':
                    print("publish date")
                    volume_attribute = "publishedDate"
                    lib_sorted = sort_by_volumeInfo(library, volume_attribute)
                    print_list_books(lib_sorted, volume_attribute = volume_attribute)

                elif subselection == '5':
                    print("page count")
                    volume_attribute = "pageCount"
                    lib_sorted = sort_by_volumeInfo(library, volume_attribute)
                    print_list_books(lib_sorted, volume_attribute = volume_attribute)

                elif subselection == '9':
                    print("exit group")
                    stay_submenu = False

                else:
                    print("Invalid menu item chosen.")

        elif selection == '6':
            #print library
            if len(library) == 0:
                #nothing to do
                pass
            else:
                print_list_books(library)

        elif selection == '9':
            #exit program
            break

        else: 
            print("Invalid menu item chosen.") 


book_menu()
