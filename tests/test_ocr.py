"""Tests for the doc2sentences.my_module module."""
import pytest
import doc2sentences.lib as d2s


def test_pdf_with_ocr():
    file_path = 'tests/test_data/bad.pdf'
    text = d2s.get_pdf_txt_ocr(file_path)
    assert d2s.isLanguage(text)



