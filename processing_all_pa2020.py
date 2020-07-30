import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer
import csv

from pa_mifflin_results_scrape import miff_scraping_one_page
from pa_beaver_results_scrape import beav_scraping_one_page
from pa_centre_results_scrape import centre_scraping_one_page
from pa_chester_results_scrape import ches_scraping_one_page

def big_scrape(viewer, doc, county_name):
    miff_type = False
    chester_type = False
    centre_type = False
    all_pages = [p for p in doc.pages()]
    viewer.navigate(1)
    viewer.render()
    first_page = viewer.canvas.strings
    #print(first_page)
    if "Absentee/M" in first_page:
        chester_type = True
    elif "Mail-In" in first_page and "Absentee" in first_page:
        miff_type = True
        #print("yo")
    elif "Voter Turnout - Total" in first_page and "Registered Voters - Total" in first_page:
        centre_type = True

    with open('20200602__pa__primary__mifflin__precinct.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if chester_type:
            writer.writerow(["county", "precint", "office", "district", "party", "candidate", "votes", "absentee_mail", "election_day"])
        else:
            writer.writerow(["county", "precint", "office", "district", "party", "candidate", "votes", "absentee_mail", "election_day", "mail", "absentee"])
        for i in range(len((all_pages))):
            viewer.navigate(i + 1)
            viewer.render()
            text_on_page = viewer.canvas.strings
            #print(text_on_page)

            if miff_type:
                print("TYPE 1")
                miff_scraping_one_page(text_on_page, writer, county_name)
                print("We are " + str((i / len(all_pages)) * 100) + "% done.")
            elif centre_type:
                print("TYPE 2")
                centre_scraping_one_page(text_on_page, writer, county_name)
                print("We are " + str((i / len(all_pages)) * 100) + "% done.")
            elif chester_type:
                print("TYPE 3")
                ches_scraping_one_page(text_on_page, writer, county_name)
                print("We are " + str((i / len(all_pages)) * 100) + "% done.")
            else:
                print("LAST TYPE")
                beav_scraping_one_page(text_on_page, writer, county_name)
                print("We are " + str((i / len(all_pages)) * 100) + "% done.")

#short function to grab the county name from the file name of the input pdf
def get_county(file_name):
    for i in range(len(file_name)):
        if file_name[i] == "_":
            stop = i
            break
    return file_name[:stop]

if __name__ == "__main__":
    file_name = "blair_results_2020.pdf"
    fd = open(file_name, "rb")
    doc = PDFDocument(fd)
    viewer = SimplePDFViewer(fd)
    county = get_county(file_name)
    big_scrape(viewer, doc, county)
