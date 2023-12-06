import argparse
import lib as d2s


def main():
    parser = argparse.ArgumentParser(description='Split documents to sentences and save as CSV.')
    parser.add_argument('--overwrite', action='store_true',
                        help='overwrite output file.')
    parser.add_argument('--ocr', action='store_true',
                        help='try ocr extraction if text extraction fails.')
    parser.add_argument('--chunk', action='store_true',
                        help='try semantically chuinks sentences togather using gpt LLM.')
    parser.add_argument('--maxtokens', nargs='?', default=300,
                        help='set max_tokens for chunking algorithm.')
    parser.add_argument('--language', nargs='?', default='en',
                        help='test text for language e.g. "en" for english.')
    parser.add_argument('--inputfile', nargs='?', default=None,
                        help='input file to convert to csv.')
    parser.add_argument('--outputfile', nargs='?', default=None,
                        help='name of output csv file.')
    parser.add_argument('--columns', nargs='?', default=None,
                        help='Additional coma seperated values to add as columns to the CSV file.')

    args = parser.parse_args()
    if not args.inputfile:
        print("[error] must provide --inputfile")
        return
    file_path = args.inputfile

    if not d2s.file_exists(file_path):
        print(f'[error] {file_path} does not exist')
        return

    file_type = d2s.get_file_extension(file_path)

    text = ""
    if file_type == '.pdf':
        text = d2s.get_pdf_text(file_path)
        # Some PDFs need OCR to extract text. It is costly so we only do when normal routine fails
        if not d2s.isLanguage(text) and args.ocr:
            text = d2s.get_pdf_txt_ocr(file_path)
    if file_type == '.txt':
        encoding = d2s.detect_encoding(file_path)
        text = d2s.get_txt_text(file_path, encoding)
    if file_type == '.rtf':
        text = d2s.get_rtf_text(file_path, 'utf-16')
    if not text:
        print(f'[error] no text extracted from {file_path}.')
        return

    if not text:
        print(f'[error] can not seem to extract any text from {file_path}.')
        return

    if args.language and not d2s.isLanguage(text, args.language):
        print(f'[error] text from {file_path} does not seem to be language {args.language}.')
        return

    sentences = d2s.get_sentences(text, min_len=5, lang='en', backend='spacy')

    if args.chunk:
        sentences = d2s.chunk_sentences(sentences, int(args.maxtokens))

    columns = []
    if args.columns:
        columns = args.columns.split(',')
        columns = [c.lower().strip() for c in columns]
    rows = d2s.create_data_structure(sentences, columns)
    output_file = args.outputfile
    if not args.outputfile:
        output_file = d2s.replace_file_extension(file_path, '.csv')

    done = d2s.save_to_csv(rows, output_file, args.overwrite)
    if done:
        print(f'output csv file: {output_file}')
    else:
        print('[error] producing file.')


main()
