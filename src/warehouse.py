class Cd:
    def __init__(self, album, artist, title, price, stock):
        self.album = album
        self.artist= artist
        self.title = title
        self.price = price
        self.stock = stock

    def remove_from_inventory(self, count = 1):
        if self.stock > count:
            self.stock = self.stock - count
        else:
            self.stock = 0

    def check_stock(self, count = 1):
        return self.stock >= count

    def buy_cd(self, count, cc_info, chart_interface = None):
        if self.check_stock(count):
            price = self.calculate_price(chart_interface)

            if cc_info.authorise(price * count):
                self.remove_from_inventory(count)
                if chart_interface:
                    chart_interface.notify(self.artist, self.title, count)
                return True
            
        return False

    def calculate_price(self, chart_interface):
        price = self.price

        if chart_interface:
            position, best_price = chart_interface.get_chart_data(self.artist, self.title)
            if (position <= 100 ):
                price = min(price, best_price - 1)
        return price
    
    def is_related(self, search_string, min_stock=1):
        return ((search_string in self.artist) or (search_string in self.title)) and (self.stock >= min_stock)
            


class Warehouse:
    def __init__(self, cd_store, charts_notfier = None):
        self.cd_store = cd_store
        self.charts_notifier = charts_notfier

    def buy_cd(self, album_name, cc_info, count=1):
        if cd := self.cd_store.get(album_name):
            return cd.buy_cd(count, cc_info, self.charts_notifier)
        
        return False
         
    def inventory(self):
        return {album: item.stock for album, item in self.cd_store.items()}

    def find_albums(self, search_string):
        albums = []
        for album_name, cd in self.cd_store.items():
            if cd.is_related(search_string):
                albums.append(album_name)
        return albums