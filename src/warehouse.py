class Cd:
    def __init__(self, album, artist, title, price, stock):
        self.album = album
        self.artist= artist
        self.title = title
        self.price = price
        self.stock = stock

    def remove_from_inventory(self):
        if self.stock > 1:
            self.stock = self.stock - 1
        else:
            self.stock = 0


class Warehouse:
    def __init__(self, cd_store, cc_processor, chars_notfiier = None):
        self.cd_store = cd_store
        self.cc_processor = cc_processor
        self.charts_notifier = chars_notfiier
        
    def buy_cd(self, album_name, cc_info):
        if cd := self.check_stock(album_name):
            if self.authorise_payment(cd.price, cc_info):
                cd.remove_from_inventory()
                if self.charts_notifier:
                    self.charts_notifier.notify(cd.artist, cd.title)
                return True
            
        return False
            
    def authorise_payment(self, price, cc_info):
        # always succeeds for now...
        return self.cc_processor.authorise(price, cc_info)
    
    def check_stock(self, album_name):
        if cd := self.cd_store.get(album_name):
            if cd.stock > 0:
                return cd
         
    def inventory(self):
        return {album: item.stock for album, item in self.cd_store.items()}

    def find_albums(self, search_string):
        albums = []
        for album_name, cd in self.cd_store.items():
            if ((search_string in cd.artist) or (search_string in cd.title)) and (cd.stock > 0):
                albums.append(album_name)
        return albums