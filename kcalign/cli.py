#!/usr/bin/env python
import argparse
from kcalign import genome_mode, gene_mode, mixed_mode


def main():
    long_description = 'Performs a codon-aware (aka translation) multiple sequence alignment. Can be run in 3 different modes depending on the input. See the documentation for more information: https://github.com/galaxyproject/kc-align'
    parser = argparse.ArgumentParser(description='Align a sequence against multiple others in a codon-aware fashion.', epilog=long_description)
    parser.add_argument('--reference', '-r', dest='reference', action='store', required=True, help='Reference sequence')
    parser.add_argument('--sequences', '-S', dest='seqs', action='store', required=True, help='Other sequences to align')
    parser.add_argument('--start', '-s', dest='start', type=str, action='store', help='1-based start position (required in genome mode)')
    parser.add_argument('--end', '-e', dest='end', type=str, action='store', help='1-based end position (required in genome mode)')
    parser.add_argument('--mode', '-m', dest='mode', action='store', choices=['genome', 'gene', 'mixed'], required=True, help='Alignment mode (genome, gene, or mixed) (required)')
    parser.add_argument('--compress', '-c', dest='compress', action='store_true', help='Compress identical sequences')
    parser.add_argument('--table', '-t', dest='table', action='store', help='Choose alternative translation table (See https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi for values)')
    parser.add_argument('--keep', '-k', dest='keep', action='store_true', help='Keep translated pre-alignment sequences file named pre_align.fasta, otherwise will delete')
    parser.add_argument('--dist', '-d', dest='distance', action='store', choices=['very-close', 'close', 'semi-close', 'less-close', 'none'], default='none', help='For genome/mixed mode, determines the max distance a homologous sequence can be before it is discarded from the alignment (default = none). Distance limits: none < very-close < close < semi-close < less-close')
    parser.add_argument('--threads', '-th', dest='threads', action='store', default=1, help='Number of simultaneous threads to use (must be a multiple of 3)')

    args = parser.parse_args()

    if args.mode == 'genome':
        return genome_mode(args.reference, args.seqs, args.start, args.end, args.compress, args.table, args.keep, args.distance, args.threads)
    elif args.mode == 'gene':
        return gene_mode(args.reference, args.seqs, args.compress, args.table, args.keep)
    else:
        return mixed_mode(args.reference, args.seqs, args.compress, args.table, args.keep, args.distance)

if __name__ == '__main__':
    exit(main())
