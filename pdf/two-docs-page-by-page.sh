#!/bin/sh

ps2pdf index_left.ps left.pdf
ps2pdf index_right.ps right.pdf
pdftk left.pdf burst
rm -f left.pdf
rename pg_ left_pg_ pg_*.pdf
left_count=`ls -1 left_pg_*.pdf|wc -l`
echo "processed index_left.ps, $left_count pages"
pdftk right.pdf burst
rm -f right.pdf
rename pg_ right_pg_ pg_*.pdf
right_count=`ls -1 right_pg_*.pdf|wc -l`
echo "processed index_right.ps, $right_count pages"
page_count=$(($left_count>$right_count?$left_count:$right_count))
echo total pages: $page_count
pairs=$(for i in `seq 1 $page_count` ; do echo -n {left,right}_pg_00`printf %02d $i`.pdf" " ; done)
valid_pairs=`for f in $pairs ; do if [ -e $f ] ; then echo $f ; else echo empty-a4.pdf ; fi; done`
pdftk $valid_pairs cat output output.pdf
rm left_pg_*.pdf right_pg_*.pdf
pdfnup output.pdf
rm output.pdf
