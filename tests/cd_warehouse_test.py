import unittest

from src.warehouse import Warehouse, Cd

class CcMock():
    def __init__(self, result):
        self.result = result
    def authorise(self, price, cc_info):
        return self.result

class CdWarehouseTest(unittest.TestCase):
    def test_buy_single_cd(self):
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2)}, CcMock(True))
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))

    def test_buy_non_existing_cd(self):
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2)}, CcMock(True))
        self.assertEqual(False, warehouse.buy_cd('Oasis', "12345"))

    def test_buy_too_many_cds(self):
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2)}, CcMock(True))
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))
        self.assertEqual(False, warehouse.buy_cd('Foo Fighters', "12345"))

    def test_failed_auth(self):
        cc_processor = CcMock(False)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2)}, cc_processor)
        self.assertEqual(False, warehouse.buy_cd('Foo Fighters', "12345"))

    def test_find_album(self):
        cc_processor = CcMock(False)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, cc_processor)
        
        self.assertEqual([], warehouse.find_albums('Nirvana'))
        self.assertEqual(["Foo Fighters"], warehouse.find_albums('Foo Fighters'))
        self.assertEqual(["Oasis"], warehouse.find_albums('sis'))
        
    def test_get_warehouse_stock(self):
        cc_processor = CcMock(False)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, cc_processor)
        
        self.assertEqual({"Foo Fighters": 2, "Oasis": 10}, warehouse.inventory())
                
        
    def test_stock_update(self):
        cc_processor = CcMock(True)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, cc_processor)
        
        warehouse.buy_cd("Foo Fighters", "12345")
        
        self.assertEqual({"Foo Fighters": 1, "Oasis": 10}, warehouse.inventory())
       

    def test_sold_out(self):
        cc_processor = CcMock(True)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, cc_processor)
        
        warehouse.buy_cd("Foo Fighters", "12345")
        warehouse.buy_cd("Foo Fighters", "67890")
        
        self.assertEqual({"Foo Fighters": 0, "Oasis": 10}, warehouse.inventory())

       
    def test_sold_out_find(self):
        cc_processor = CcMock(True)

        # we have 2x Foo Fighters in the warehouse

        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, cc_processor)
        # we sell them both
        warehouse.buy_cd("Foo Fighters", "12345")
        warehouse.buy_cd("Foo Fighters", "67890")

        # if we list what's in stock foo fighters should not be in the list
        # of albums if we're searching for it.
        self.assertEqual(False, "Foo Fighters" in warehouse.find_albums("Foo"))