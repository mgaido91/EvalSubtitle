# coding: utf-8
from ttml import ttml_to_tagged_str
import re
import argparse

DESCRIPTION = """Script for computing precision/recall/F1 
 for the quality evaluation of subtitle segmentations
 based on Alvarez et al. 2016."""

LINE_TAG = '<eol>'
CAPTION_TAG = '<eob>'


def get_vectors(line, symbol):
    line = line + ' '
    line = line.replace(' ', ' <space> ')
    line = line.replace('<space> '+ symbol + ' <space>', symbol)
    vector = []
    [vector.append(1) if w == symbol else vector.append(0) if w == '<space>' else w for w in line.split(' ')]
    return vector


def evaluate_f1(reference_file, system_file, symbol, ttml=False, line_tag=LINE_TAG, caption_tag=CAPTION_TAG):
    # Evaluate Precision, Recall and F1
    breaks_ref = 0  # Number of total breaks in reference (used for precision)
    breaks_out = 0  # Number of total breaks in output (used for recall)
    correct_breaks = 0  # Total number of correct breaks (used for both pre-rec)
    # TODO: smoothing in case of no <eol> present in corpus?
    with open(reference_file) as r, open(system_file) as s:
        for lref, lseg in zip(r, s):
            if symbol == '<eox>':
                lref = ' '.join([br.replace(line_tag, symbol).replace(caption_tag, symbol) for br in lref.split(' ')])
                lseg = ' '.join([br.replace(line_tag, symbol).replace(caption_tag, symbol) for br in lseg.split(' ')])
            elif symbol == CAPTION_TAG:
                lref = lref.replace(' <eol>', '')
                lseg = lseg.replace(' <eol>', '')
            elif symbol == LINE_TAG:
                lref = lref.replace(' <eob>', '')
                lseg = lseg.replace(' <eob>', '')

            # Get sequence vectors
            splts_ref = get_vectors(lref.strip(), symbol)
            breaks_ref += splts_ref.count(1)
            splts_seg = get_vectors(lseg.strip(), symbol)
            breaks_out += splts_seg.count(1)

            # Compare vectors
            for ref_pos, seg_pos in zip(splts_ref, splts_seg):
                # TRUE negative if ref_pos == 0 and seg_pos == 0:
                if ref_pos == 1 and seg_pos == 1:
                    correct_breaks += 1

        # Calculate precision, recall, F1
        try:
            precision = correct_breaks / breaks_out
            recall = correct_breaks / breaks_ref
            f1 = 2 * ((precision * recall) / float(precision + recall))
        except ZeroDivisionError:
            precision, recall, f1 = 0, 0, 0
        print("Scores for " + symbol)
        print("Precision: " + str(round(precision, 3)))
        print("Recall: " + str(round(recall, 3)))
        print("F1 score: " + str(round(f1, 3)))
        return round(precision, 3), round(recall, 3), round(f1, 3)


def parse_args():
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('--reference_file', '-rf', type=str,
                        help="Reference file")
    parser.add_argument('--system_file', '-sf', type=str,
                        help="Segmented subtitle file to evaluate.")
    parser.add_argument('--ttml', '-ttml', action='store_true',
                        help="Whether the subtitle files are in ttml format")

    args = parser.parse_args()
    return args


def main(args):
    reference_file = args.reference_file
    system_file = args.system_file

    # TODO: add ttml processing
    #ttml = args.ttml
    evaluate_f1(reference_file, system_file, '<eox>', ttml=False, line_tag=LINE_TAG, caption_tag=CAPTION_TAG)
    evaluate_f1(reference_file, system_file, CAPTION_TAG, ttml=False, line_tag=LINE_TAG, caption_tag=CAPTION_TAG)
    evaluate_f1(reference_file, system_file, LINE_TAG, ttml=False, line_tag=LINE_TAG, caption_tag=CAPTION_TAG)


if __name__ == '__main__':
    main(parse_args())

"""Tests """
#reference_file = '/home/alin/Desktop/subtitling/02_data/Must-Cinema/en-fr/amara.en'
#system_file = '/home/alin/Desktop/subtitling/02_data/Must-Cinema/en-fr/amara.fr'
#evaluate_f1(reference_file, system_file, '<eox>', ttml=False, line_tag=LINE_TAG, caption_tag=CAPTION_TAG)
#get_vectors('Imagine waking up to a stranger -- <eob> sometimes multiple strangers -- <eob> questioning your right to existence <eob> for something that you wrote online, <eob> waking up to an angry message, <eob> scared and worried for your safety. <eob>', '<eob>')
#def get_break_positions(line, symbol):
#    # Get actual splits: word before <split> word after
#    re_eo = fr'(?:\S+\s)?\S*{symbol}\S*(?:\s\S+)?'
#    splits = re.findall(re_eo, line)
#    return splits
# Get splits
            #splts_ref = get_break_positions(lref.strip(), symbol)
            #splts_seg = get_break_positions(lseg.strip(), symbol)
            # Compare all splits ref-trans
            ##Problem in case splts have duplicate elements e.g. [2,2]
            #breaks_ref += len(splts_ref)
            #breaks_out += len(splts_seg)
            #correct_breaks += len(set(splts_ref) & set(splts_seg))