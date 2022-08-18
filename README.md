# publist
Generate publication lists from an ADS library:

1. Download a "BibTex" file from ADS which contains all the papers you are interested in

2. Put the downloaded file (e.g., "export-bibtex.bib") into a folder and change "fdir" in the Python code "latex_items.py" to point to that folder. Also, change "fname" in the Python code to the actual name of the "*.bib" file.

3. Change 3 variables in "latex_items.py" to reflect your name, and "Nauthor_crit" means the number of authors above which you would like to fold the author list of a given publication.

4. Run the Python code by "python latex_items.py". This will generate four "*.tex" files whose names are given by the variable "list_savename". They include (1) submitted papers, (2) papers with you as the 1st/2nd/3rd author, (3) papers with you as the N-th (N>=4) author, and (4) all your published papers.

5. Include one or more of above files (e.g. "py_list_pub_all.tex") by adding the following line in your overall ".tex" file

   \input{py_list_pub_all}

   and the publication list will appear in the final pdf where you added this line.
   
---- an example is provided by my own publication list as in "export-bibtex.bib".
