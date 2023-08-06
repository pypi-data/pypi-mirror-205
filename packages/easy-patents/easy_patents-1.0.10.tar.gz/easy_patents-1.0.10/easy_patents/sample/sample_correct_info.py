from easy_patents.get_info import app_progress, app_doc_cont_refusal_reason_decision
from easy_patents.errors import *

laws = ['trademark', 'design', 'patent']
year = 2017
num = 0

for j in range(3, 4):
    law = laws[j-1]
    for i in range(1, 101):
        num += 1
        app_number = "%s%06d" % (year, num)
        print(law, app_number)
        try:
            app_progress(app_number, law=law)
            print("Got process_info")
        except NoDocumentError:
            pass
        try:
            refusal_path = app_doc_cont_refusal_reason_decision(app_number, law=law)
            print(refusal_path)
        except NoDocumentError:
            pass
