import os
import csv
import fitz as PyMuPDF
import nltk
import datetime
import re
import spacy
from spacy.lang.en import English
import langid
from striprtf.striprtf import rtf_to_text
import chardet
nlp = spacy.load("en_core_web_sm")

nltk.download('punkt')
nltk.download('words')


def file_exists(file_path):
    return os.path.exists(file_path)


def get_file_extension(file_path):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()


def extract_pdf_metadata(file_path):
    # Open the PDF file
    pdf_document = PyMuPDF.open(file_path)

    # Get document metadata
    metadata = pdf_document.metadata

    # Close the PDF document
    pdf_document.close()
    return metadata


def extract_text_with_page_numbers(file_path):
    # Open the PDF file
    pdf_document = PyMuPDF.open(file_path)
    text_with_page_numbers = []

    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        text = page.get_text("text")
        text_with_page_numbers.append((page_number + 1, text))  # Add 1 to start page numbering from 1

    # Close the PDF document
    pdf_document.close()

    return text_with_page_numbers


def test_pdf_for_text(file_path, lang="en"):
    with PyMuPDF.open(file_path) as doc:
        for page in doc:
            text = page.get_text()
            if isLanguage(text, lang):
                return True
    return False


def isLanguage(text, lang="en"):
    detected_lang, _ = langid.classify(text)
    if detected_lang == lang:
        return True
    return False


def get_pdf_text(file_path) -> str:
    text = ''
    with PyMuPDF.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def get_rtf_text(file_path, encoding='utf-8'):
    text = ''
    with open(file_path) as infile:
        content = infile.read()
        text = rtf_to_text(content, encoding=encoding, errors="ignore")
    return text


def get_binary_text(file_path):
    binary_data = None
    with open(file_path, 'rb') as bf:
        binary_data = bf.read()
    return binary_data


def get_txt_text(file_path, encoding='utf-8'):
    text = ''
    with open(file_path, 'r', encoding=encoding, errors='ignore') as file:
        text = file.read()
    return text


def create_folder_if_not_exists(folder_path):
    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the folder if it does not exist
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")


def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

def get_sentences_spacy(text, min_len=5, lang='en'):
    nlp = English()
    nlp.add_pipe('sentencizer')
    text = text.replace('e.g.', 'eeggee')
    text = text.replace('e. g.', 'eeggee')
    text = text.replace('i. e.', 'iieeii')
    text = text.replace('i.e.', 'iieeii')
    text = text.replace('\n', ' ').replace('\r', '')
    doc = nlp(text)
    def filter(s, min_len, lang):
        if len(s.split(' ')) < min_len:
            return False
        if not isLanguage(s, lang):
            return False
        return True

    def transform(s):
        s = re.sub(r'[^\w\s\-.!:;,?()]', ' ', s)
        s = s.replace('eeggee', 'e.g.')
        s = s.replace('iieeii', 'i.e.')
        return re.sub(r'\s+', ' ', s).strip().lower()

    sentences = [transform(s.text) for s in doc.sents if filter(s.text.strip(), min_len, lang)]
    return sentences

def get_sentences(text, min_len=5, lang='en', backend='spacy'):
    if not lang == 'en':
        raise Exception('Only english supported at the moment.')
    if backend == 'spacy':
        return get_sentences_spacy(text, min_len, lang)
    if backend == 'nltk':
        return get_sentences_nltk(text, min_len, lang)
    raise Exception(f'Backend {backend} not supported.')

def get_sentences_nltk(text, min_len=5, lang='en', split_lists=False):
    text = text.replace('e.g.', 'eeggee')
    text = text.replace('e. g.', 'eeggee')
    text = text.replace('i. e.', 'iieeii')
    text = text.replace('i.e.', 'iieeii')
    text = text.replace('\n', ' ').replace('\r', '')

    def filter(s, min_len, lang):
        if len(s.split(' ')) < min_len:
            return False
        if not isLanguage(s, lang):
            return False
        return True

    def transform(s):
        s = re.sub(r'[^\w\s\-.!:;,?()]', ' ', s)
        s = s.replace('eeggee', 'e.g.')
        s = s.replace('iieeii', 'i.e.')
        return re.sub(r'\s+', ' ', s).strip().lower()

    sentences = []
    for line in text.splitlines():
        ss = nltk.sent_tokenize(line)
        if split_lists:
            # Attempt to split itemized lists into sentences.
            # N.B. might be quite error prone.
            for s in ss:
                sub_sentences = split_itemized_sentence(s)
                sentences += sub_sentences
        else:
            sentences += ss
    sentences = [transform(s) for s in sentences if filter(s.strip(), min_len, lang)]
    return sentences

def isItemized(text):
    list_pattern = re.compile(r'(?:\d+\.|[IVX]+[.)]|[ivx]+[.)]|\([a-z]\)|\s*[a-z]\))')
    return bool(list_pattern.match(text))

def split_itemized_sentence(text):
    def filter(s):
        if len(s.split(' ')) < 3:
            return False
        if '.....' in s:
            return False
        return True

    text = text.replace('i.e.', 'iieeii')
    pattern = r'(\d+)\.(\d+)'
    replacement = r'\1DOT\2'
    text = re.sub(pattern, replacement, text)
    items = re.split(r'(?:\d+\.|[IVX]+[.)]|[ivx]+[.)]|\([a-z]\)|\s*[a-z]\))', text)
    items = [item.strip() for item in items if item]
    items = [item.replace('iieeii', 'i.e.') for item in items]
    items = [item.replace('DOT', '.') for item in items]
    items = [re.sub(r'^\d+', '', item) for item in items if filter(item)]
    return items


def replace_file_extension(filename, new_extension):
    # Split the filename into root and extension
    root, old_extension = os.path.splitext(filename)

    # Create the new filename with the replaced extension
    new_filename = root + new_extension

    return new_filename


def create_data_structure(sentences, columns=[]):
    rows = []
    for sentence in sentences:
        length = len(sentence.split(' '))
        row = (sentence, length) + tuple(columns)
        rows.append(row)
    return rows


def save_to_csv(rows, output_file=None, overwrite=False, append=False):
    current_datetime_utc = datetime.datetime.utcnow()
    # convert the datetime object to ISO format with 'Z' indicating UTC timezone
    current_datetime_utc_iso = current_datetime_utc.replace(microsecond=0).isoformat() + 'Z'
    if len(rows) == 0:
        return (False, None, current_datetime_utc_iso)

    if os.path.exists(output_file) and overwrite is False:
        return False
    else:
        mode = "a" if append else "w"
        with open(output_file, mode=mode, newline="", encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            if not append:
                writer.writerow([f"# Generated on {current_datetime_utc_iso}"])
                # header = ("sentence")
                # writer.writerow(header)
            else:
                print(f"appending to {output_file}")
            for row in rows:
                writer.writerow(row)
        return True
