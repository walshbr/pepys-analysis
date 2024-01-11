import diary_analysis
import csv

diary = diary_analysis.Diary('sp_diary.json')
out_file = 'metadata.csv'

first = diary.entries[0]
with open(out_file,'w') as csvfile:
    fields = list(first.__dict__.keys())
    fields = ['filename'] + fields
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for entry in diary.entries[1:]:
        row = {}
        for column_name in fields:
            if column_name == 'filename':
                row['filename'] = entry.year + '-' + entry.month + '-' + entry.date + '.txt'
            elif column_name == 'entry_text':
                row[column_name] = getattr(entry, column_name).replace('\n', ' ')
            else:
                row[column_name] = getattr(entry, column_name)
        writer.writerow(row)