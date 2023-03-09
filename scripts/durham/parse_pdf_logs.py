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
        report_path = argv[0]
        try:
            if not report_path.endswith('/'):
                report_path += '/'
        except:
            print('A template file for page 1 must be defined')
            return
    else:
        # hardcode paths if known
        report_path = '../../data/durham/'
    path_list=[]
    for x in os.walk(report_path):
        print(x[0])
        pdfList=glob.glob(x[0]+"/*.pdf")
        if len(pdfList)==0:
            continue
        if str(x[0]) in path_list:
            continue
        else:
            path_list.append(str(x[0]))
        df_arrests, df_incidents = tools.parseArrestReports(str(x[0]), report_path + 'templates/')
        df_arrests.to_csv(x[0] + '/' + 'arrests_reports_data.csv')
        df_incidents.to_csv(x[0] + '/' + 'incident_reports_data.csv')
        print('Extracted data saved in ' + x[0])
        

if __name__ == "__main__":
	try:
	    main(sys.argv[1:])
	except:
	    main([])