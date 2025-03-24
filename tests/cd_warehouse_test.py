import unittest

from src.warehouse import Warehouse



class CdWarehouseTest(unittest.TestCase):
    def test_by_cd(self):
        warehouse = Warehouse([])
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', "12345"))