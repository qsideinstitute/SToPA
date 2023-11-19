# Taking a stab at this Rochester data...
# Looks like it's pdf files again! 
# Only a handful, oddly enough. 
# 
# Manuchehr Aminian
# November 5, 2022
#

import glob
import os
import pandas

pdf_types = ['ACC', 'DWI_REPORT', 'DWI_REFUSAL', 'DWI_REPORT_FELCOMP', 'Genl101A', 'Utt']

# TODO: DWI_REPORT and DWI_REPORT_FELCOMP have overlapping 
# report names and result in a duplicate in a single case.
# 
# Redesign code so that pdf files are unique identified and then 
# removed from further searches. Currently glob.glob just matches 
# based on a pattern on the entire static list, leading to the overlap.
# 
# TODO: apparent overlap with ACC forms as well.
# Probably just need to list-split on "-" and take the big boy form name

pdf_dir = os.path.join('..', '..', 'data', 'rochester') # operating system agnostic file path.

files = {
    pt: glob.glob(os.path.join(pdf_dir, pt) + '*') for pt in pdf_types
}

tabular = []
for i,(k,v) in enumerate( files.items() ):
    prefix = k
    for j,pdfname in enumerate(v):
        basename = os.path.basename(pdfname)
        chunks = ''.join(basename.split('.')[:-1]) # throw out .pdf suffix.
        chunks = chunks.split('-')
        if chunks[-1]=='Redacted':
            identifier = chunks[-2]
        else:
            identifier = chunks[-1]

        #print(i,j,k,identifier)
        tabular.append([identifier, k, pdfname])

# this dataframe only has case id and filename information.
df = pandas.DataFrame(data=tabular, columns=['case_id', 'form_type', 'filename'])

if __name__=="__main__":
    # proof of concept -- often multiple forms per case_id
    for k,(case_id,dfs) in enumerate( df.groupby('case_id') ):
        print('%3i'%k, ', Case: ', '%15s'%case_id, ', Forms: ', list(dfs['form_type']))

    df.to_csv('rochester_pdf_inventory.csv', index=None)

