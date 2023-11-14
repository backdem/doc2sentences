# doc2sentences
The script can convert PDF, RTF and TXT files to CSV by splitting the files into sentences.

## Install cli
To install and use from cli

```console
git clone git@github.com:backdem/doc2sentences.git
cd doc2sentences
pip install -r requirments.txt
```

## To use the script

The following command will split a pdf file into sentences and output a csv file. By default the csv file has 2 columns; 
the sentence and the length of the sentence.
```console
python doc2sentences/d2s.py --inputfile /tmp/test.pdf --outputfile /tmp/test.csv
```

Adding more columns e.g. labels can be done by adding the command line argument columns. 
In the following command the resulting csv file will have two extra columns with values label1 and label2.
The command overwrite will overwrite the output file if it already exists.
```console
python doc2sentences/d2s.py --inputfile /tmp/test.pdf --outputfile /tmp/test.csv --columns label1,label2 --overwrite
```

## Installation as package

To install doc2sentences from GitHub repository, do:

```console
git clone git@github.com:backdem/doc2sentences.git
cd doc2sentences
python -m pip install .
```
Then from python
```console
import doc2sentences.lib as d2s 
text = d2s.get_pdf_text(PATH_TO_PDF)
senteces = d2s.get_sentences(text)
print(text)
```

## Documentation

Include a link to your project's full documentation here.

## Contributing

If you want to contribute to the development of doc2sentences,
have a look at the [contribution guidelines](CONTRIBUTING.md).

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
