import pandas # openpyxl and xlrd must be installed
import numpy as np

def read():
    df = pandas.read_excel('talklist.xlsx', engine='openpyxl')
    return df

def discard_row_with_NaN_title(df):
    titles = df['title'].values
    sel = []
    for t in titles:
        if isinstance(t, str):
            sel.append(True)
        else:
            sel.append(False)
    sel = np.array(sel)
    return df[sel]

def replace_double_quatation(string):
    ss = string.split('"')
    string_new = ss[0]
    for i, s in enumerate(ss[1:]):
        d = ['``', "''"][i%2]
        string_new += d+s
    return string_new

def write(df, sep_by_year=True):
    # sort by year and month 
    df.sort_values(by=['year','month'], inplace=True, ascending = [False, False])

    lines = []
    years = []
    for index, row in df.iterrows():
        line = '\\item '
        # basic information
        title    = row['title (EN)'] if row['title (EN)'] is not np.nan else row['title']
        confname = row['conference name (EN)'] if row['conference name (EN)'] is not np.nan else  row['conference name']
        year     = row['year']
        month    = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.'][int(row['month'])-1]
        if row['conference url'] is not np.nan:
            url = row['conference url']
            line+= "\\textbf{%s}, \\href{%s}{%s}, %d, %s"%( title, url, confname, year, month )
        else:
            line+= "\\textbf{%s}, %s, %d, %s"%( title, confname, year, month )
        # append additional infomation
        if not np.isnan(row['oral']):
            line += ', \\textit{Oral}'
        if not np.isnan(row['poster']):
            line += ', \\textit{Poster}'
        if not np.isnan(row['invited']):
            line += ' (\\textbf{Invited Talk})'
        # escape '&'
        line = line.replace('&', '\&')
        # replace double quatation "*" pair with ``*''.
        line = replace_double_quatation(line)


        lines.append(line)
        years.append(year)

    if sep_by_year:
        lines2 = []
        yuniq = np.unique(years)
        inc = 1
        for y in yuniq:
            sel = y == np.array(years)
            n = np.sum(sel)
            inc+= n
            l = np.array(lines, dtype=str)[sel]
            #l = np.insert(l, 0, ['\\begin{enumerate}', '\\setcounter{enumi}{%d}'%inc])
            #l = np.append(l, '\\end{enumerate}')
            l = np.insert(l, 0, ['\\begin{etaremune}', '\\setcounter{enumi}{%d}'%inc])
            l = np.append(l, '\\end{etaremune}')
            l = '\n'.join(l)
            l = '\\underline{%d}\n'%y + l
            lines2.append(l)
        lines = '\n\n'.join(lines2[::-1])
    else:
        lines = np.insert(lines, 0, '\\begin{etaremune}')
        lines = np.append(lines, '\\end{etaremune}')
        lines = '\n'.join(lines)

    with open('talklist.tex', 'w') as f:
        f.write(lines)


if __name__ == '__main__':
    df = read()
    df = discard_row_with_NaN_title(df)
    #write(df, sep_by_year=False)
    write(df, sep_by_year=True)