import os
import time 
import csv

cols = ['t','dmv_confirmed','dmv_deaths','dmv_recovered','us_confirmed','us_deaths','us_recovered']

rootdir = 'csse_covid_19_data/csse_covid_19_daily_reports'
outfilename = f'report_{int(time.time())}.csv'

with open(outfilename, 'a') as outfile:
    outfile.write(','.join(str(x) for x in cols) + '\n')
    writer = csv.writer(outfile)
    for subdir, dirs, filenames in os.walk(rootdir):
        for filename in sorted(filenames):
            if filename.endswith('csv'):
                    with open(f'{rootdir}/{filename}') as file:
                        stats = dict(zip(cols, [0] * len(cols)))
                        stats['t'] = filename.split('.')[0];
                        file.readline(); # chomp first line
                        source = csv.reader(file)
                        for source_row in source:
                            country = source_row[1];
                            if country != 'US':
                                continue
                            state = source_row[0];
                            dmv = (state == 'Virginia' or state == 'Maryland' or state == 'District of Columbia')
                            confirmed = 0
                            deaths = 0
                            recovered = 0

                            try:
                                confirmed = int(source_row[3]);
                                deaths = int(source_row[4]);
                                recovered = int(source_row[5]);
                            except: 
                                pass
                            
                            if dmv:
                                stats['dmv_confirmed'] += confirmed
                                stats['dmv_deaths'] += deaths
                                stats['dmv_recovered'] += recovered

                            stats['us_confirmed'] += confirmed
                            stats['us_deaths'] += deaths
                            stats['us_recovered'] += recovered

                        writer.writerow(str(stats[col]) for col in cols);
