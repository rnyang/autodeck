import glob
import sys
import subprocess

## Usage:
## autodeck.py directory filename

## Get command line input

directory = sys.argv[1]
outfile = sys.argv[2]

## Load image files

images = glob.glob(directory + "*png")
print(images)

## Load figure titles (if available)
titles = None
try:
    f = open(directory + "config.txt")
    lines = f.readlines()


    # Check correct number of figure titles
    if len(lines) == len(images):
        titles = list(map(lambda x:x.strip(), lines))
    else:
        titles = None

    f.close()

except FileNotFoundError:
    titles = None
    
# Create Latex Header

texOut = ""

header = """\\documentclass{beamer}
\\usepackage{graphicx}
\graphicspath{{""" + directory + """}}
\\title{Auto Deck Title}
\\author{Author}
\\date{\\today}
\\begin{document}
\\frame{\\titlepage}
"""

texOut = texOut + header

# Create slides

for (i,imageFile) in enumerate(images):
    texOut = texOut + "\\frame{\n"
    if titles != None:
        texOut = texOut + "\\frametitle{" + titles[i] +  "}\n"

    texOut = texOut + "\\begin{center}\n"
    texOut = texOut + "\\includegraphics[height=6cm]{" + images[i].split('/')[-1].replace('.png','') +  "}\n"
    texOut = texOut + "\\end{center}\n"
    texOut = texOut + "}\n"

# Create Latex Footer

footer = "\end{document}\n"
texOut = texOut + footer

# Compile and output to PDF

f = open(outfile, 'w')
f.write(texOut)
f.close()

subprocess.call("pdflatex " + outfile, shell=True)
