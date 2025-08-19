import numpy as np

t_range_mark = False   # whether to mark pub in the following range (yr+mon)
tpub_max = 202306
tpub_min = 202207

tmax_cut = False       # whether to cut off at tpub_max
chronological = False   # False for inverse chronological order

fdir = './'
fname = 'export-bibtex.bib'
list_savename = ['py_list_submitted.tex', 'py_list_123_published.tex',
                 'py_list_N_published.tex', 'py_list_pub_all.tex']

my_last = 'Lu'
my_first = 'Wenbin'
Nauthor_crit = 4   # critical number of authors for folding

journal_dict = {'mnras': 'MNRAS', 'apj': 'ApJ', 'apjl': 'ApJL',
                'apjs': 'ApJS', 'apss': 'Ap\\&SS', 'aa': 'A\\&A',
                'aap': 'A\\&A', 'aj': 'AJ', 'aara': 'ARA\\&A',
                'nat': 'Nature', 'pasj': 'PASJ',
                'ssr': 'Space Sci. Rev.', 'GCN': 'GCN Circ',
                'PRD': 'Phys. Rev. D', 'prd': 'Phys. Rev. D',
                'PRL': 'Phys. Rev. L', 'prl': 'Phys. Rev. L',
                'procspie': 'Proc. SPIE', 'nar': 'New Astronomy Reviews',
                'arXiv e-prints': 'submitted'}
month_dict = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5,
              'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10,
              'nov': 11, 'dec': 12}


# obtain the info within the bracket for 'target = {...}'
def find_in_brackets(lines, target):
    k = 0
    while target not in lines[k]:
        k += 1
        if k == len(lines):  # not found
            return ''
    line = lines[k]
    jstart = line.find('{') + 1
    jend = len(line) - line[::-1].find('}') - 1
    return line[jstart:jend]


def find_simple(lines, target):
    k = 0
    while target not in lines[k]:
        k += 1
        if k == len(lines):
            return ''
    line = lines[k]
    jstart = line.find('=') + 1
    jend = line.find(',')
    return line[jstart:jend].replace(' ', '')


with open(fdir+fname, 'r') as f:
    data = f.readlines()


def write_head(fsave):
    fsave.write('\\begin{itemize}[leftmargin=0.65cm]')


def write_tail(fsave):
    fsave.write('\\end{itemize}')


def write_item(fsave, my_last, my_first, i_paper, author_last,
               author_first, title, journal,
               year, month, volume, number, eprint, adsurl,
               mark, refereed):
    fsave.write('\n')
    fsave.write('\\vspace{-0.1cm}\n')
    authors = ''
    me_included = False
    for i in range(len(author_last)):
        if author_last[i] == my_last and author_first[i][0] == my_first[0]:
            authors += '{\\bf ' + author_last[i] + ', ' \
                       + author_first[i][0] + '.}, '
            me_included = True
        else:
            authors += author_last[i] + ', ' + author_first[i][0] + '., '
        if i >= Nauthor_crit:
            if not me_included:
                authors += 'et al. {\\bf (' \
                           + my_last + ', ' + my_first[0] + '.)}, '
            else:
                authors += 'et al., '
            break
    it_title = '{\\it ' + title + '}, '
    title = '{' + title + '}, '
    if journal == 'submitted':
        volume = ''
        number = ''
        eprint = 'arXiv: ' + eprint + ', '
    else:
        eprint = ''
        if volume != '':
            volume += ', '
        if number != '':
            number += ', '
    it_journal = '{\\it ' + journal + '}, '
    journal = journal + ', '
    # print(i_paper, authors, year, it_title, journal,
    #       volume, number, eprint, adsurl)
    c_number = '%d' % i_paper
    if not refereed:  # not a refereed publication
        c_number = '*' + c_number
    if t_range_mark and mark:
        fsave.write('\\item[\\textbf{' + c_number + '.}]{')
    else:
        fsave.write('\\item[' + c_number + '.]{')
    fsave.write(authors + title + it_journal
                + volume + number + eprint
                + '(' + year + ')'
                + '(' + month + ')'
                + ' \\href{' + adsurl + '}{\\underline{PDF}}'
                + '}\n')
    #fsave.write(authors
    #            + year + ', '
    #            + it_title
    #            + journal + volume + number
    #            + eprint
    #            + '\\href{' + adsurl + '}{\\underline{PDF}}'
    #            + '}\n')


# go through each line to find the number of papers
Nlines = len(data)
Npapers = 0
for i in range(Nlines):
    if data[i][0] == '@':
        Npapers += 1

# then go through each paper
i_paper = 0
list_i_author = []
list_author_last, list_author_first, list_title = [], [], []
list_journal, list_year, list_month, list_volume = [], [], [], []
list_number, list_eprint, list_adsurl = [], [], []
list_refereed = []
i = 0
while i < Nlines:
    new_line = data[i]
    i += 1
    if new_line[0] == '@':
        istart = i - 1
        iend = i
        while data[iend][0] != '@':
            iend += 1
            if iend == len(data):
                break
        i_paper += 1
        i = iend
        # all information in this paper is contained here
        lines = data[istart:iend]
        # next line contains author information
        k = 0
        while 'author' not in lines[k]:
            k += 1
            if k == len(lines):  # no author information
                print('no authors!')
                exit()
        line = lines[k]
        jstart = line.find('{') + 1
        jend = len(line) - line[::-1].find('}') - 1
        # print(line[jstart:jend])
        author_last = []
        author_first = []
        j = jstart
        while j < jend:
            if line[j] == '{':
                j1 = j+1
                if line[j1:].find('{') != -1 and line[j1:].find('{') < line[j1:].find('}'):
                    # special character(s)
                    j1_tilde = line[j1:].find('}') + j1 + 1
                    while line[j1_tilde:].find('{') != -1 and line[j1_tilde:].find('{') < line[j1_tilde:].find('}'):
                        j1_tilde = line[j1_tilde:].find('}') + j1_tilde + 1
                    j2 = line[j1_tilde:].find('}') + j1_tilde
                else:
                    j2 = line[j1:].find('}') + j1
                author_last += [line[j1:j2]]
                j3 = j2 + 3
                if line[j3:].find(' ') == -1:  # the last author
                    j4 = line[j3:].find('}') + j3
                else:
                    j4 = line[j3:].find(' ') + j3
                author_first += [line[j3:j4]]
                j = j4
            else:
                j += 1
        # print(author_last)
        # print(author_first)
        title = find_in_brackets(lines, 'title = ')
        booktitle = find_in_brackets(lines, 'booktitle = ')
        journal = find_in_brackets(lines, 'journal = ').replace('\\', '')
        if journal in list(journal_dict.keys()):
            journal = journal_dict[journal]
        if journal == '' and booktitle != '':  # this is a book
            list_refereed += [False]  # not refereed
            journal = booktitle
        else:
            list_refereed += [True]
        year = find_simple(lines, 'year = ')
        month = find_simple(lines, 'month = ')
        volume = find_in_brackets(lines, 'volume = ')
        number = find_in_brackets(lines, 'number = ')
        adsurl = find_in_brackets(lines, 'adsurl = ')
        eprint = find_in_brackets(lines, 'eprint = ')
        i_author = 0
        while i_author < len(author_last):
            if author_last[i_author] == my_last and author_first[i_author][0] == my_first[0]:
                break
            i_author += 1
        list_i_author += [i_author+1]
        list_author_last += [author_last]
        list_author_first += [author_first]
        list_title += [title]
        list_journal += [journal]
        list_year += [year]
        list_month += [month]
        list_volume += [volume]
        list_number += [number]
        list_eprint += [eprint]
        list_adsurl += [adsurl]

print('number of first- and second-author papers: %d and %d'
      % (list_i_author.count(1), list_i_author.count(2)))

# sort the lists according to publication time (or submission time if not published)
list_pub_time = []
list_mark_or_not = []
for i in range(Npapers):
    t_year = '%4d' % int(list_year[i])
    if list_month[i] == '':  # month information is not available
        t_month = '12'
    else:
        t_month = '%02d' % int(month_dict[list_month[i]])
    t_combined = int(t_year + t_month)
    if tpub_min<= t_combined <= tpub_max:
        list_mark_or_not += [True]
    else:
        list_mark_or_not += [False]
    list_pub_time += [t_combined]
    
if chronological:
    index_list = np.argsort(list_pub_time)   # chronological order
else:
    index_list = np.argsort(list_pub_time)[::-1]   # inverse chronological order
    
# count the number of papers in each category
Nsub, N123, Nn = 0, 0, 0
for i in range(Npapers):
    if list_journal[i] == 'submitted':
        Nsub += 1
    elif int(list_i_author[i]) <= 3:
        N123 += 1
    else:
        Nn += 1

list_fsave = [open(fdir+savename, 'w') for savename in list_savename]
[write_head(fsave) for fsave in list_fsave]

c1, c2, c3, c4 = 0, 0, 0, 0
#for i in range(Npapers):
for i in index_list:
    if tmax_cut:  # do not include publications later than tpub_max
        if list_pub_time[i] > tpub_max:
            continue
    
    if list_journal[i] == 'submitted':
        fsave = list_fsave[0]
        if chronological:
            c = c1 + 1
        else:
            c = Nsub - c1
        c1 += 1
    elif int(list_i_author[i]) <= 3:
        fsave = list_fsave[1]
        if chronological:
            c = c2 + 1
        else:
            c = N123 - c2
        c2 += 1
    else:
        fsave = list_fsave[2]
        if chronological:
            c = c3 + 1
        else:
            c = Nn - c3
        c3 += 1
    args = list_author_last[i], list_author_first[i], list_title[i],\
           list_journal[i], list_year[i], list_month[i], list_volume[i],\
           list_number[i], list_eprint[i], list_adsurl[i], \
           list_mark_or_not[i], list_refereed[i]
    write_item(fsave, my_last, my_first, c, *args)
    if list_journal[i] != 'submitted':
        if chronological:
            c = c4 + 1
        else:
            c = Npapers-Nsub-c4
        c4 += 1
        write_item(list_fsave[3], my_last, my_first, c, *args)

[(write_tail(fsave), fsave.close()) for fsave in list_fsave]
