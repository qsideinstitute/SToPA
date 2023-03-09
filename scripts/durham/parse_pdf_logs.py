""" Script to parse downloaded Durham PD records
"""
import glob
import os
import sys
sys.path.append('../..')
import src as tools

def main(argv):
    # Pass in command line arguments for report and templates if any
    if argv != []:
        reportPath = argv[0]
        try:
            if not reportPath.endswith('/'):
                reportPath += '/'
        except:
            print('A template file for page 1 must be defined')
            return
    else:
        # hardcode paths if known
        reportPath = '../../data/durham/'
    pathList=[]
    for x in os.walk(reportPath):
        print(x[0])
        pdfList=glob.glob(x[0]+"/*.pdf")
        if len(pdfList)==0:
            continue
        if str(x[0]) in pathList:
            continue
        else:
            pathList.append(str(x[0]))
        dfArrests, dfIncidents = tools.parseArrestReports(str(x[0]), reportPath + 'templates/')
        dfArrests.to_csv(x[0] + '/' + 'arrests_reports_data.csv')
        dfIncidents.to_csv(x[0] + '/' + 'incident_reports_data.csv')
        print('Extracted data saved in ' + x[0])
        

if __name__ == "__main__":
	try:
	    main(sys.argv[1:])
	except:
	    main([])