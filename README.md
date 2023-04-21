## Text-summarizer

This is a tool that can automatically generate summaries of long documents, allowing to grasp the main points without having to read through everything.

## Getting started

Before running text-summarizer. Make sure to run the following command to install all the needed packages :

`pip install -r requirements.txt`

To use text summarizer, simply run :

`pyhton3 main.py`

## Note

- First an output.pdf will be generated that contain the text without punctutations. Then the output will be printed in the terminal output. Otherwise, you can run `python3 main.py > file.txt` to save the summary in a text file.
- If you want to test an other pdf file, you can update the `inputFilePath` in the `main.py` file.

