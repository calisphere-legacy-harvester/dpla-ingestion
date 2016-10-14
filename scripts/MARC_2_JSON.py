import os
from pymarc import MARCReader

# Quick and dirty script to create JSON from MARC data
# Use MARCEdit->MARCSplit to split into multiple files,
# Then choose one file/record to best represent scope of MARC metadata

# Change output path/filename as needed
out = open(
    os.path.expanduser('~/dpla-ingestion/test/test_data/csl-marc.json'), 'w+')

# Change input MARC path/filename as needed
with open(
        os.path.expanduser(
            '~/dpla-ingestion/test/test_data/msplit00000022.mrc'), 'rb') as fh:
    reader = MARCReader(fh, to_unicode=True)
    for record in reader:
        out.write(record.as_json())
out.close()
