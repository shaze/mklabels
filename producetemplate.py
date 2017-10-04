
import os
import sys
import sys
from optparse import OptionParser





def InitStuff():
    usage = "usage: %prog [options] list_of_codes output_file"
    parser = OptionParser(usage=usage)


    parser.add_option("-r","--rows",dest="num_rows",
                  default = "6",
                  metavar = "INT",
                  help = " number of rows [default: %default]")

    parser.add_option("-c","--cols",dest="num_cols",
                  default = "2",
                  metavar = "INT",
		                    help = " number of columns [default: %default]")

    parser.add_option("-H","--height",dest="height",
                  metavar = "FLOAT",
                  default = "0",
                      help = " height of barcode [default autoadjust]")

    parser.add_option("-w","--width",dest="width",default="0",
                  metavar = "FLOAT",
                      help = " width of barcode  [default autoadjust]")

    parser.add_option("-b","--barcode",dest="barcodetype",default="code39",
                  metavar = "STRING",
                      help = " type of barcode  [default %default]")

    parser.add_option("-t","--topagemargin",dest="topmargin",default="6",
                  metavar = "INT (mm)",
                      help = " top page margin  [default %default]")

    parser.add_option("-l","--leftborder",dest="leftborder",default="0",
                  metavar = "INT (mm)",
                      help = " leftborder  [default %default]")

    parser.add_option("-n","--num_copies",dest="num_copies",default="1",
                  metavar = "INT (mm)",
                      help = " leftborder  [default %default]")

    parser.add_option("-i","--interlabel",dest="interlabel",default="-24",
                  metavar = "INT (mm)",
                      help = " interlabel width  [default %default]")


    parser.add_option("-u","--updown",dest="updown",default=False,
                  action="store_true",
                      help = " order of labels  [default L-R then down]")

    parser.add_option("-s","--skip",dest="skip",default=False,
                  action="store_true",
                      help = " blanklabel after each person  [default false]")

    parser.add_option("-d","--dummy",dest="dummy",default=False,
                  action="store_true",
                      help = " dummy run -- don't latex etc  [default false]")



    return  parser.parse_args()

(options,args) = InitStuff()


barcode_fn  = args[0]
output_fn   = args[1]
num_rows    = int(options.num_rows)
num_columns = int(options.num_cols)




header_s=r"""
\documentclass[12pt]{article}
\usepackage[a4paper]{geometry}
\usepackage[newdimens]{labels}
\usepackage{pstricks}
\usepackage{pst-barcode}
\LabelCols=%d
\LabelRows=%d
\TopPageMargin=%smm
\setlength{\LeftLabelBorder}{%smm}
\InterLabelColumn=-1mm
\InterLabelRow=%spt
\newcommand{\FRAMEWIDTH}{%smm}
\newcommand{\PICHEIGHT}{%smm}
\newcommand{\HEIGHT}{%s}
\newcommand{\WIDTH}{%f}
\usepackage{xcolor}
\usepackage{fancybox}

\newcommand{\cfbox}[2]{\colorlet{currentcolor}{.}{\color{#1}\ovalbox{\color{currentcolor}#2}}}



\newcommand{\barcodetype}{%s}




\begin{document}
"""

entry=r"""

\cfbox{white}{
\begin{pspicture}(0,-2mm)(\FRAMEWIDTH,\PICHEIGHT)
\psbarcode{%s}{includetext height=\HEIGHT\   width=\WIDTH}{\barcodetype}
\end{pspicture}}
"""

template = r"""


\begin{labels}

\cfbox{white}{\begin{pspicture}(0,-2mm)(\FRAMEWIDTH,\PICHEIGHT)
\psbarcode{%s}{includetext height=\HEIGHT\   width=\WIDTH}{\barcodetype}
\end{pspicture}}
"""

options.width=float(options.width)

if (options.width<0.001):
    width = 6.0/num_columns
else:
    width = options.width


framewidth = 27*width



options.height=float(options.height)
num_copies = int(options.num_copies)

if (options.height<0.001):
    height = 3.6/num_rows
else:
    height = options.height




def pos_row_wise(i):
    return i

def pos_col_wise(i):
    r=i % num_rows
    c=i / num_rows
    return r*num_columns+c





if options.updown:
    pos=pos_col_wise
    break_major=num_rows
    break_minor= num_columns
else:
    pos = pos_row_wise
    break_major = num_columns
    break_minor = num_rows

print "Break_major %d break_minor %d\n"%(break_major,break_minor)
num_segs  = (break_major+1)/(num_copies+1)
print "Num_segs=%d; num_copies=%d\n"%(num_segs,num_copies)
num_skips = (num_segs-1)*break_minor if options.skip else 0
codes_per_page = num_columns*num_rows

if num_segs<0:
    sys.exit("Combination of row, column, num_copies and skip won't work")

print "Number of skips ",num_skips

header = header_s%(num_columns,num_rows,options.topmargin,options.leftborder,options.interlabel,framewidth,height*27,height,width,options.barcodetype)



for i in range(1,codes_per_page):
    template=template+entry
template=template+"\n"+r"\end{labels}"







bf = open(barcode_fn)


of = open("%s.tex"%output_fn,"w")

of.write(header)

toprocess = True


while toprocess:
    codes=[""]*codes_per_page
    n=0
    for i in range(codes_per_page-num_skips):
        if i % num_copies == 0:
            line=bf.readline()
            print "New person i=%d; n=%d; i MOD num_segs=%d"%(i,n,i%num_segs)
            if options.skip and ( (i/num_copies % num_segs) !=0) :
                codes[pos(n%codes_per_page)]=line[0:3]
                n=n+1
        print line
        if not line:
            toprocess =False
            break
        #print "pos(%d)=%d\n"%(n%codes_per_page,pos(n%codes_per_page))
        codes[pos(n%codes_per_page)]=line.rstrip("\n")
        n=n+1
    if not toprocess: break
    print tuple(codes)
    of.write(template%(tuple(codes)))

bf.close()

of.write(r"\end{document}")
of.close()

if options.dummy: sys.exit(0)

os.system("latex %s.tex"%output_fn)
os.system("dvips -o %s.eps %s.dvi"%(output_fn,output_fn))
os.system("epstopdf %s.eps"%output_fn)



