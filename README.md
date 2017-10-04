
#Creating barcode labels for  printing out

This script takes as input a list of IDs and then produces barcodes for the inputs and formats it in a form suitable for printing on labels.

This tool uses LaTeX and assumes you have a standard distribution of LaTeX including the psbarcode package. You also need to have dvips and epstopdf installed.  These are easy to install on most systsems

One restriction is that it currently it only supports A4  though it would be trivial to change to support letter paper.


`producetemplate.py -h` shows all options


Simple way to run: takes two arguments -- the list of barcode and an output file

producetemplate.py witsset.dat wits

By default  6 x 2 barcodes produced, but you you can change this using options. The program tries to guess the correct height and width but you can change.

You can also change the type of barcodes produced.

For printing onto labels you may need to adjust the top spacing and
interlabel spacing -- there are options for that.

*Unfortunately, every printer is different. If any computing device is the work of the devil, it is the printer. Undoubtedly you will need to fiddle with the spacing to align the barcodes to your labels. Sorry.*

See the complete list of options below

Here is a more complex example:

`python producetemplate.py -r 21 -c 4 -n 10 -s -u -w 1.3 -H 0.21  set0.dat wits`

* Print labels with 21 rows and 4 columns. 
*  For each person print 10 copies.
* After each person's 10 copies, skip (print a blank label)
* Order the labels up-down then left-right (column-wise) -- default is 
   L-R then top down
* Adjust the height and width spacing of the barcodes by factors of 1.3 and 0.21.

```
Usage: producetemplate.py [options] list_of_codes output_file

Options:
  -h, --help            show this help message and exit
  -r INT, --rows=INT     number of rows [default: 6]
  -c INT, --cols=INT     number of columns [default: 2]
  -H FLOAT, --height=FLOAT
                         height of barcode [default autoadjust]
  -w FLOAT, --width=FLOAT
                         width of barcode  [default autoadjust]
  -b STRING, --barcode=STRING
                         type of barcode  [default code39]
  -t INT (mm), --topagemargin=INT (mm)
                         top page margin  [default 6]
  -l INT (mm), --leftborder=INT (mm)
                         leftborder  [default 12]
  -n INT (mm), --num_copies=INT (mm)
                         leftborder  [default 1]
  -i INT (mm), --interlabel=INT (mm)
                         interlabel width  [default -24]
  -u, --updown           order of labels  [default L-R then down]
  -s, --skip             blanklabel after each person  [default false]
  -d, --dummy            dummy run -- don't latex etc  [default false]
```






