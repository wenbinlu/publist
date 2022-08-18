fdir = '/Users/wenbinlu/Documents/non_research/CV_pub_list/'
fname = 'export-bibtex.bib'
list_savename = ['py_list_submitted.tex', 'py_list_123_published.tex',
                 'py_list_N_published.tex', 'py_list_pub_all.tex']

my_last = 'Lu'
my_first = 'Wenbin'
Nauthor_crit = 4   # critical number of authors for folding

journal_dict = {'mnras': 'MNRAS', 'apj': 'ApJ', 'apjl': 'ApJL',
                'apjs': 'ApJS', 'apss': 'Ap\\&SS', 'aa': 'A\\&A',
                'aap': 'A\\&A', 'aj': 'AJ', 'aara': 'ARA\\&A',
                '\\nat': 'Nature', 'pasj': 'PASJ',
                'ssr': 'Space Sci. Rev.', 'GCN': 'GCN Circ',
                'PRD': 'Phys. Rev. D', 'prd': 'Phys. Rev. D',
                'PRL': 'Phys. Rev. L', 'prl': 'Phys. Rev. L',
                'procspie': 'Proc. SPIE', 'nar': 'New Astronomy Reviews',
                'arXiv e-prints': 'submitted'}


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
              year, volume, number, eprint, adsurl):
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
    journal = journal + ', '
    # print(i_paper, authors, year, it_title, journal,
    #       volume, number, eprint, adsurl)
    fsave.write('\\item[%d.]{' % i_paper
                + authors
                + year + ', '
                + it_title
                + journal + volume + number
                + eprint
                + '\\href{' + adsurl + '}{\\underline{PDF}}'
                + '}\n')


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
list_journal, list_year, list_volume = [], [], []
list_number, list_eprint, list_adsurl = [], [], []
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
        title = find_in_brackets(lines, 'title')
        journal = find_in_brackets(lines, 'journal').replace('\\', '')
        if journal in list(journal_dict.keys()):
            journal = journal_dict[journal]
        year = find_simple(lines, 'year')
        volume = find_in_brackets(lines, 'volume')
        number = find_in_brackets(lines, 'number')
        adsurl = find_in_brackets(lines, 'adsurl')
        eprint = find_in_brackets(lines, 'eprint')
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
        list_volume += [volume]
        list_number += [number]
        list_eprint += [eprint]
        list_adsurl += [adsurl]

print('number of first- and second-author papers: %d and %d'
      % (list_i_author.count(1), list_i_author.count(2)))

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
for i in range(Npapers):
    if list_journal[i] == 'submitted':
        fsave = list_fsave[0]
        c = Nsub - c1
        c1 += 1
    elif int(list_i_author[i]) <= 3:
        fsave = list_fsave[1]
        c = N123 - c2
        c2 += 1
    else:
        fsave = list_fsave[2]
        c = Nn - c3
        c3 += 1
    args = list_author_last[i], list_author_first[i], list_title[i],\
           list_journal[i], list_year[i], list_volume[i],\
           list_number[i], list_eprint[i], list_adsurl[i]
    write_item(fsave, my_last, my_first, c, *args)
    if list_journal[i] != 'submitted':
        c = Npapers-Nsub-c4
        c4 += 1
        write_item(list_fsave[3], my_last, my_first, c, *args)

[(write_tail(fsave), fsave.close()) for fsave in list_fsave]