"""Tests for the doc2sentences.my_module module."""
import pytest
import doc2sentences.lib as d2s


def test_good_pdf():
    file_path = 'tests/test_data/test.pdf'
    text = d2s.get_pdf_text(file_path)
    assert d2s.isLanguage(text)

def test_bad_pdf():
    file_path = 'tests/test_data/bad.pdf'
    text = d2s.get_pdf_text(file_path)
    assert not d2s.isLanguage(text)

def test_good_rtf():
    file_path = 'tests/test_data/test.rtf'
    text = d2s.get_rtf_text(file_path)
    assert d2s.isLanguage(text)

def test_good_txt():
    file_path = 'tests/test_data/test.txt'
    text = d2s.get_txt_text(file_path)
    assert d2s.isLanguage(text)

def text_bad_txt():
    file_path = 'tests/test_data/bad.txt'
    text = d2s.get_txt_text(file_path)
    assert not isLanguage(text)


