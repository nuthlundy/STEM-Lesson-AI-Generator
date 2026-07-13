import unittest
from services.presentation.navigation.controller import NavigationController

class TestPresentationNavigation(unittest.TestCase):
    def test_navigation_basic_flow(self):
        ctrl = NavigationController(total_slides=5)
        self.assertEqual(ctrl.navigator.current_slide(), 0)
        
        # Test next slide
        self.assertEqual(ctrl.next(), 1)
        self.assertEqual(ctrl.next(), 2)
        
        # Test previous slide
        self.assertEqual(ctrl.previous(), 1)
        
        # Test jump
        self.assertEqual(ctrl.jump_to(4), 4)
        with self.assertRaises(ValueError):
            ctrl.jump_to(5)
            
        # Test history
        self.assertEqual(ctrl.get_history(), [0, 1, 2, 1, 4])
        
        # Test bookmarks
        ctrl.add_bookmark(2)
        ctrl.add_bookmark(4)
        self.assertEqual(ctrl.get_bookmarks(), [2, 4])
        
        ctrl.remove_bookmark(2)
        self.assertEqual(ctrl.get_bookmarks(), [4])

if __name__ == "__main__":
    unittest.main()
