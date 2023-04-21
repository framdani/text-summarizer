from transformers import PegasusTokenizer, PegasusForConditionalGeneration
import re

import PyPDF2

try:
    # set input and output files
    inputFilePath = "mercedes.pdf"
    outputFilePath = "output.pdf"

    # Open the input file for reading
    pdfFileObj = open(inputFilePath, "rb")
    pdfReader = PyPDF2.PdfReader(pdfFileObj)
    # set the max-length for each chunk of text
    max_length = 400

    chunk_size = 1024 * 1024
    ############################################################
    # Open the file and remove punctuation => streaming approach because text is very large
    #############################################################

    # Create a pdf writer
    pdf_writer = PyPDF2.PdfWriter()


    for page_number in range(len(pdfReader.pages)):
         # extract the text from the page
        pageObj=pdfReader.pages[page_number]
        text = pageObj.extract_text()
         # Split the text into chunks instead of loading the entire
         # text once in the memory due to memory contraints
        for j in range(0, len(text), chunk_size):
            # remove punctuation from the chunk using regex
            cleaned_chunk = re.sub(r'[^\w\s]', '',text[j:j+chunk_size])
            pdf_writer.add_page(pageObj)
            pdf_writer.add_outline_item(title=f"Page {page_number+1}", page_number=page_number)
            # write the PDF writer to the output file
            pdf_writer.write(outputFilePath)
    pdfFileObj.close()

    ################################################
    # Text - Summarization
    ################################################
    model_name = "human-centered-summarization/financial-summarization-pegasus"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    max_length = 512
    pdfFileObj2 = open(outputFilePath, "rb")
    pdfReader = PyPDF2.PdfReader(pdfFileObj2)
    for i in range(len(pdfReader.pages)):
        pageObj=pdfReader.pages[i]

        text = pageObj.extract_text()

        # split the text into smaller chunks to avoid self index out of range
        chunks = []
        for j in range(0, len(text), max_length):
            chunks.append(text[j:j+max_length])

        for input in chunks:
            input_ids = tokenizer(input, return_tensors="pt").input_ids
            output = model.generate(
            input_ids, 
            max_length=32, 
            num_beams=5, 
            early_stopping=True
        )  
            print(tokenizer.decode(output[0], skip_special_tokens=True))



    pdfFileObj2.close()
except Exception as E:
    print(f"An exception occurred {E}")
