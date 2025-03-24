import unittest

from src.warehouse import Warehouse



class CdWarehouseTest(unittest.TestCase):
    def test_buy_single_cd(self):
        warehouse = Warehouse({"Foo Fighters":{"price":9.95, "stock":2}})
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))

    def test_buy_non_existing_cd(self):
        warehouse = Warehouse({"Foo Fighters":{"price":9.95, "stock":2}})
        self.assertEqual(False, warehouse.buy_cd('Oasis', "12345"))

    def test_buy_too_many_cds(self):
        warehouse = Warehouse({"Foo Fighters":{"price":9.95, "stock":2}})
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))
        self.assertEqual(False, warehouse.buy_cd('Foo Fighters', "12345"))
