import unittest

from src.warehouse import Warehouse

class CcMock():
    def __init__(self, result):
        self.result = result
    def authorise(self, price, cc_info):
        return self.result


class CdWarehouseTest(unittest.TestCase):
    def test_buy_single_cd(self):
        warehouse = Warehouse({"Foo Fighters":{"price":9.95, "stock":2}}, CcMock(True))
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))

    def test_buy_non_existing_cd(self):
        warehouse = Warehouse({"Foo Fighters":{"price":9.95, "stock":2}}, CcMock(True))
        self.assertEqual(False, warehouse.buy_cd('Oasis', "12345"))

    def test_buy_too_many_cds(self):
        warehouse = Warehouse({"Foo Fighters":{"price":9.95, "stock":2}}, CcMock(True))
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))
        self.assertEqual(False, warehouse.buy_cd('Foo Fighters', "12345"))

    def test_failed_auth(self):
        cc_processor = CcMock(False)
        warehouse = Warehouse({"Foo Fighters":{"price":9.95, "stock":2}}, cc_processor)
        self.assertEqual(False, warehouse.buy_cd('Foo Fighters', "12345"))

    def test_find_album(self):
        cc_processor = CcMock(False)
        warehouse = Warehouse({"Foo Fighters":{"price":9.95, "stock":2},
                               "Oasis":{"price":3.95, "stock": 10}}, cc_processor)
        
        self.assertEqual([], warehouse.find_albums('Nirvana'))
        self.assertEqual(["Foo Fighters"], warehouse.find_albums('Foo Fighters'))
        self.assertEqual(["Oasis"], warehouse.find_albums('sis'))
        
    
        

