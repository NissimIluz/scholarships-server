def scan(file_path, document_type):
    return True

# load scanner to the sys.path server
# import os
# import sys
# sys.path.append('..\\Scan_Documents_Test')  # make sure the project is in the same folder as the Server folder
# from analyzing import *
# from ocr import ocr
#
#
# # static method
# def scan(file_path, document_type):
#     """
#     check, by using scanner, if the document is valid
#     :param file_path: the file location
#     :param document_type: the name of desired requirement
#     :return: True iff the document meets the requirement
#     """
#     txt = ocr(file_path)
#     result:bool = False
#     try:
#         result = bool(is_doc_recognized(txt, DOCUMENT_DICT[document_type]))
#     except Exception as e:
#         print(e)
#     return result
#
