import pandas # openpyxl and xlrd must be installed
import numpy as np

def read():
    df = pandas.read_excel('talklists/talklist.xlsx', engine='openpyxl')
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

def make_tex_talk_list(df, sep_by_year=True, only_selected=True, inverse=False, language='en'):
    # sort by year and month 
    df.sort_values(by=['year','month'], inplace=True, ascending = [False, False])

    if only_selected:
        N_talk_all = len(df)
        df = df.query('selected == 1')
        N_talk_selected = len(df)

    if language == 'en':
        title_col_name = 'title (EN)'
        conference_col_name = 'conference name (EN)'
    elif language == 'ja':
        title_col_name = 'title'
        conference_col_name = 'conference name'
    else:
        raise ValueError('language must be either "en" or "ja".')

    lines = []
    years = []
    for index, row in df.iterrows():
        line = '\\item '
        # basic information
        title    = row[title_col_name] if row[title_col_name] is not np.nan else row['title']
        confname = row[conference_col_name] if row[conference_col_name] is not np.nan else  row['conference name']
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
        if inverse:
            lines = np.insert(lines, 0, '\\begin{etaremune}')
            lines = np.append(lines, '\\end{etaremune}')
        else:
            lines = np.insert(lines, 0, '\\begin{enumerate}')
            lines = np.append(lines, '\\end{enumerate}')
        lines = '\n'.join(lines)

    if only_selected:
        if language == 'en':
            lines = 'Listing %d selected talks out of %d talks.\n'%(N_talk_selected, N_talk_all) +\
                    'See \href{https://github.com/git-sunao/cv/blob/main/en/sunao_type_list.pdf}{here} for the full list of talks.' +\
                    lines
        elif language == 'ja':
            lines = '全%d件のうち%d件のトークを選出しました。\n'%(N_talk_all, N_talk_selected) +\
                    '全リストは\href{https://github.com/git-sunao/cv/blob/main/ja/sunao_type_list.pdf}{こちら}をご覧ください。' +\
                    lines
        else:
            raise ValueError('language must be either "en" or "ja".')

    return lines

def wrap_cv_style(tex_in, language='en'):
    if language == 'en':
        tex = '\\begin{rSection}{Talks}\n'
    elif language == 'ja':
        tex = '\\begin{rSection}{講演}\n'
    tex+= tex_in
    tex+= '\\end{rSection}\n'
    return tex

if __name__ == '__main__':
    df = read()
    df = discard_row_with_NaN_title(df)
    for language in ['en', 'ja']:
        # 
        tex = make_tex_talk_list(df, sep_by_year=False, only_selected=True, language=language)
        tex = wrap_cv_style(tex, language=language)
        fnameout='%s/talklist.tex'%language
        with open(fnameout, 'w') as f:
            f.write(tex)
        # 
        tex = make_tex_talk_list(df, sep_by_year=False, only_selected=False, language=language)
        tex = wrap_cv_style(tex, language=language)
        fnameout='%s/talklist_full.tex'%language
        with open(fnameout, 'w') as f:
            f.write(tex)
        #
        tex = make_tex_talk_list(df, sep_by_year=True, only_selected=False, language=language)
        tex = wrap_cv_style(tex, language=language)
        fnameout='%s/talklist_full_sepbyyear.tex'%language
        with open(fnameout, 'w') as f:
            f.write(tex)
