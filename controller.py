#Денис
import operations as o
import user_interface as ui


def button_click():
    while True:
       menu = ui.show_menu()
       choice = ui.get_choice(menu)
       if choice == 1:
              
            list = ui.get_contact   
            o.write_csv(list)
            o.write_json(list)
       elif choice == 2:
            lst = o.read_csv()
            result = o.search(lst)
            ui.view_data(result)
       elif choice == 3:
            result = o.read_csv()
            ui.view_data(result)
       elif choice == 4:
            o.write_json()
       else:
            break
