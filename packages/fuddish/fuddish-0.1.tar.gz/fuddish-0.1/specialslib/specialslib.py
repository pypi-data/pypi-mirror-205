import datetime

class FoodDishDisplay:
    def __init__(self, dish_list):
        self.dish_list = dish_list
        self.last_displayed_index = None

    def get_current_dish(self):
        current_time = datetime.datetime.now()
        current_day = current_time.day
        current_index = current_day % len(self.dish_list)
        if current_index == self.last_displayed_index:
            return None
        self.last_displayed_index = current_index
        return self.dish_list[current_index]