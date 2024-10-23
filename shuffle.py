import csv
import random
import sys

def shuffle_csv(input_file, output_file):
    # Read the contents of the input CSV file
    with open(input_file, newline='', mode='r') as csvfile:
        reader = list(csv.reader(csvfile))
        
        # Separate the header from the rest of the data (if there's a header)
        header = reader[0]
        rows = reader[1:]
        
        # Shuffle the rows
        random.shuffle(rows)
        
        # Write the shuffled data to a new CSV file
        with open(output_file, newline='', mode='w') as shuffled_csv:
            writer = csv.writer(shuffled_csv)
            # Write the header and the shuffled rows
            writer.writerow(header)
            writer.writerows(rows)
        

print(sys.argv[1])
shuffle_csv(sys.argv[1], sys.argv[2])