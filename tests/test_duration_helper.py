import unittest
from duration_helper import parse_duration
from datetime import timedelta

class TestDurationHelper(unittest.TestCase):    
    def test_hours_min_seconds_being_present(self):
        api_duration = '2H22M33S'
        expected = timedelta(hours=2, minutes=22, seconds=33)
        result = parse_duration(api_duration)
        self.assertEqual(result, expected)
        
    def test_hours_missing(self):
        api_duration = '22M33S'
        expected = timedelta(minutes=22, seconds=33)
        result = parse_duration(api_duration)
        self.assertEqual(result, expected)
        
    def test_minutes_missing(self):
        api_duration = '2H33S'
        expected = timedelta(hours=2, seconds=33)
        result = parse_duration(api_duration)
        self.assertEqual(result, expected)
        
    def test_seconds_missing(self):
        api_duration = '2H22M'
        expected = timedelta(hours=2, minutes=22)
        result = parse_duration(api_duration)
        self.assertEqual(result, expected)
        
    def test_only_seconds_present(self):
        api_duration = '33S'
        expected = timedelta(seconds=33)
        result = parse_duration(api_duration)
        self.assertEqual(result, expected)
        
    def test_empty_string(self):
        api_duration = ''
        expected = timedelta(0)
        result = parse_duration(api_duration)
        self.assertEqual(result, expected)
        
    def test_invalid_format(self):
        api_duration = 'NOTVALID'
        expected = timedelta(0)
        result = parse_duration(api_duration)
        self.assertEqual(result, expected)
        
    def test_values_larger_than_60_should_carry_over(self):
        api_duration = '66M66S'
        expected = timedelta(hours=1, minutes=7, seconds=6)
        result = parse_duration(api_duration)
        self.assertEqual(result, expected)
               
if __name__ == "__main__":
    unittest.main()