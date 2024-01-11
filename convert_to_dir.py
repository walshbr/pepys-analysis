import diary_analysis

diary = diary_analysis.Diary('sp_diary.json')
out_dir = 'as_txt/'

for entry in diary.entries:
    with open(out_dir + entry.year + '-' + entry.month + '-' + entry.date + '.txt','w') as fout:
        fout.write(entry.entry_text)