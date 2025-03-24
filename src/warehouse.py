class Warehouse:
    def __init__(self, cds, cc_processor):
        self.cds = cds
        self.cc_processor = cc_processor
        
    def buy_cd(self, album, cc_info):
        if stock_info := self.check_stock(album):
            if self.authorise_payment(stock_info['price'], cc_info):
                self.remove_from_inventory(album)
                return True
            
        return False # no CD sold
            
    def authorise_payment(self, price, cc_info):
        # always succeeds for now...
        return self.cc_processor.authorise(price, cc_info)
    
    def check_stock(self, album):
        if album := self.cds.get(album):
            return album
        
    def remove_from_inventory(self, album):
        if item := self.cds.get(album):
            if item['stock'] > 1:
                item['stock'] = item['stock'] - 1
            else:
                del self.cds[album]