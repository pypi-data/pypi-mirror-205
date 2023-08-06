import unittest

from katlas.motif import SequenceMotif


class TestSequenceMotif(unittest.TestCase):

    def test_init(self):
        sm = SequenceMotif('____spxLs*QExyDL', phospho_priming=False)
        self.assertEqual(sm.motif,'_SPXLSQEXYDL')
        self.assertEqual(len(sm), 9)
    
    def test_init_invalid(self):
        with self.assertRaises(ValueError):
            SequenceMotif("ACGTU")

    def test_no_asterisk(self):
        with self.assertRaises(ValueError):
            SequenceMotif('____spxLsQExyDL') # missing asterisk
    def test_invalid_phosphoacceptor(self):
        with self.assertRaises(ValueError):
            SequenceMotif('____spxLsQ*ExyDL') # invalid phosphoacceptor `Q`
        
    def test_multiple_asterisk(self):
        with self.assertRaises(ValueError):
            SequenceMotif('____spxLs*QExyDs*') # multiple asterisks
            

    def test_phospho_priming(self):
        sm = SequenceMotif('____spxLs*QExyDL', phospho_priming=True)
        self.assertEqual(sm.motif, '_sPXLsQEXyDL')
    



unittest.main()