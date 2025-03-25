import unittest
from unittest.mock import MagicMock

from src.warehouse import Warehouse, Cd

class CcStub():
    def __init__(self, result):
        self.result = result
    def authorise(self, price):
        return self.result
    
class ChartsUpdater:
    def __init__(self, position=101, best_price=0):
        self.position = position
        self.best_price = best_price
        
    def notify(self, artist, title, count):
        pass

    def get_chart_data(self, artist, title):
        return self.position, self.best_price
        
class CdWarehouseTest(unittest.TestCase):
    def test_buy_single_cd(self):
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2)})
        cc_processor = CcStub(True)
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', cc_processor))

    def test_buy_non_existing_cd(self):
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2)})
        cc_processor = CcStub(True)
        self.assertEqual(False, warehouse.buy_cd('Oasis', cc_processor))

    def test_buy_too_many_cds(self):
        cc_processor = CcStub(True)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2)})
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', cc_processor))
        self.assertEqual(True, warehouse.buy_cd('Foo Fighters', cc_processor))
        self.assertEqual(False, warehouse.buy_cd('Foo Fighters', cc_processor))

    def test_failed_auth(self):
        cc_processor = CcStub(False)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2)})
        self.assertEqual(False, warehouse.buy_cd('Foo Fighters', cc_processor))

    def test_find_album(self):
        cc_processor = CcStub(False)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)})
        
        self.assertEqual([], warehouse.find_albums('Nirvana'))
        self.assertEqual(["Foo Fighters"], warehouse.find_albums('Foo Fighters'))
        self.assertEqual(["Oasis"], warehouse.find_albums('sis'))
        
    def test_get_warehouse_stock(self):
        cc_processor = CcStub(False)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, cc_processor)
        
        self.assertEqual({"Foo Fighters": 2, "Oasis": 10}, warehouse.inventory())
                
        
    def test_stock_update(self):
        cc_processor = CcStub(True)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)})
        
        warehouse.buy_cd("Foo Fighters", cc_processor)
        
        self.assertEqual({"Foo Fighters": 1, "Oasis": 10}, warehouse.inventory())
       

    def test_sold_out(self):
        cc_processor = CcStub(True)
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)})
        
        warehouse.buy_cd("Foo Fighters", cc_processor)
        warehouse.buy_cd("Foo Fighters", cc_processor)
        
        self.assertEqual({"Foo Fighters": 0, "Oasis": 10}, warehouse.inventory())

       
    def test_sold_out_find(self):
        cc_processor = CcStub(True)

        # we have 2x Foo Fighters in the warehouse

        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)})
        # we sell them both
        warehouse.buy_cd("Foo Fighters", cc_processor)
        warehouse.buy_cd("Foo Fighters", cc_processor)

        # if we list what's in stock foo fighters should not be in the list
        # of albums if we're searching for it.
        self.assertEqual(False, "Foo Fighters" in warehouse.find_albums("Foo"))

    def test_notify_record_label(self):
        cc_processor = CcStub(True)
        charts_interface = ChartsUpdater()
        charts_interface.notify = MagicMock()
        cc_processor.authorise = MagicMock()
        # we have 2x Foo Fighters in the warehouse

        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, charts_interface)
        
        warehouse.buy_cd("Foo Fighters", cc_processor, 2)
        
        charts_interface.notify.assert_called_with("Foo Fighters", "1998", 2)
        cc_processor.authorise.assert_called_once_with(19.90)

    def test_competitor_price_match(self):
        cc_processor = CcStub(True)
        cc_processor.authorise = MagicMock()

        # our competitor has Foo Fighter 1998 for 9.00 and it is at place 56 in the chart
        charts_interface = ChartsUpdater(56, 9.00)

        
        # we have 2x Foo Fighters in the warehouse
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, charts_interface)
        
        warehouse.buy_cd("Foo Fighters", cc_processor, 2)
        cc_processor.authorise.assert_called_once_with(16)
        

    def test_competitor_price_match_no_top_100(self):
        cc_processor = CcStub(True)
        cc_processor.authorise = MagicMock()

        # our competitor has Foo Fighter 1998 for 9.00 and it is at place 56 in the chart
        charts_interface = ChartsUpdater(101, 9.00)

        
        # we have 2x Foo Fighters in the warehouse
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, charts_interface)
        
        warehouse.buy_cd("Foo Fighters", cc_processor, 2)
        cc_processor.authorise.assert_called_once_with(19.90)

    
    def test_competitor_price_match_100_higher_price(self):
        cc_processor = CcStub(True)
        cc_processor.authorise = MagicMock()

        # our competitor has Foo Fighter 1998 for 10.00 and it is at place 56 in the chart
        charts_interface = ChartsUpdater(56, 10.00)

        
        # we have 2x Foo Fighters in the warehouse
        warehouse = Warehouse({"Foo Fighters":Cd("Foo Fighters", "Foo Fighters", "1998", 9.95, 2),
                               "Oasis":Cd("Oasis", "Oasis", "1995", 3.95, 10)}, charts_interface)
        
        warehouse.buy_cd("Foo Fighters", cc_processor, 2)
        cc_processor.authorise.assert_called_once_with(18.00)

    
                

if __name__ == '__main__':
    unittest.main()