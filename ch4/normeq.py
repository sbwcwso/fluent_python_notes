"""Utility functions for normalized Unicode string comparison."""
from unicodedata import normalize

def nfc_equal(str1, str2):
  """Using Normal Form C, case sensitive"""
  return normalize('NFC', str1) == normalize('NFC', str2)

def fold_equal(str1, str2):
  """Using Normal Form C with case folding"""
  return normalize('NFC', str1).casefold() == normalize('NFC', str2).casefold()