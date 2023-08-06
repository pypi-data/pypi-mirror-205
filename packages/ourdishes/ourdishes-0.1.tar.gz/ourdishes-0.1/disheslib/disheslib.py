import time

class FoodDishDisplay:
    def __init__(self, dish_list):
        self.dish_list = dish_list
        self.last_displayed_index = None

    def display_dishes(self):
        def display_helper():
            nonlocal self
            current_time = time.localtime()
            current_day = current_time.tm_mday
            current_index = current_day % len(self.dish_list)
            if current_index != self.last_displayed_index:
                print(self.dish_list[current_index])
                self.last_displayed_index = current_index
            time.sleep(10)
            display_helper()

        display_helper()
