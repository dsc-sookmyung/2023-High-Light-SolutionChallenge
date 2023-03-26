import fitz
import PIL.Image
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
import os
import json
import io
import re
import io
from io import BytesIO
import pandas as pd
from google.cloud import storage
from google.cloud import texttospeech

print("fitz version: ", fitz.__version__)
print("PIL.Image version: ", PIL.Image.__version__)
# print("pdfminer.high_level version: ", pdfminer.high_level.__version__)
# print("pdfminer.layout version: ", pdfminer.layout.__version__)
