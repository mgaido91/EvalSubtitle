#!/bin/bash

sys_file=$1
reference=$2
sys_name=$3
tl=$4

SCRIPTDIR=$(dirname $0)/../evalsub/util/MWER
outdir=$SCRIPTDIR/output

mkdir -p $outdir

# Tokenize and segment into subs
mkdir -p $outdir/tmp
python3 $SCRIPTDIR/split_subs.py $reference.tok $outdir/tmp ref $tl
python3 $SCRIPTDIR/split_subs.py $sys_file.tok $outdir/tmp sys $tl

for sysr in $outdir/tmp/*.sys
do
	# sgm
	perl $SCRIPTDIR/txt2sgm.pl < $sysr > $sysr.src.sgm   # FAKE SOURCE FILE
	perl $SCRIPTDIR/txt2sgm_ref.pl < $sysr > $sysr.subs.sgm  # REFERENCE FILE

	sys_file="${sysr/.sys/.ref}"
	$SCRIPTDIR/segmentBasedOnMWER.sh $sysr.src.sgm $sysr.subs.sgm $sys_file $sys_name $tl $sys_file.sgm -usecase 1
	sed -e "/<[^>]*>/d" $sys_file.sgm > $sys_file.hyp
	rm $sysr.src.sgm
	rm $sysr.subs.sgm

done

python3 $SCRIPTDIR/postprocess.py $outdir/tmp/ $outdir/$sys_name.sent.$tl $sys_file $tl
rm $outdir/tmp/
