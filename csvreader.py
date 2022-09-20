import csv

def read(infile):
    outfile = []
    with open(infile) as file:
        raw_file = csv.reader(file)
        teams_file = []
        for row in raw_file:
            outfile.append(row)

    return outfile