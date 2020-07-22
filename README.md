# Overview

Kc-Align is a fast and accurate tool for performing codon-aware multiple sequence alignments (MSA). It makes use of the very fast multiple alignment program Kalign3 to ensure maximum speed. Kc-Align is a extremely extremely versatile tool, capable of taking a variety of inputs and achieving the same result. Every other aligner requires the sequence inputs to be the coding sequences of the gene/open reading frame (ORF) to be aligned, requiring curation from the whole-genome sequences and also preventing use of assemblies that may not be properly annotated. Kc-Align solves this problem by using pairwise alignments to extract the sequence from each whole genome that is homologous to the sequence of a high quality and well annotated reference sequence. This feautre may also be bypassed for those who already have curated data and simply desire a quick and accurate codon-aware multiple aligner (see Modes below).

## What Is a Codon-Alignment?

In a codon-aware alignment, coding sequences of nucleotides are converted to their amino acid sequences before being aligned and then following the alignment, the original nucleotide sequence of each sequence in the alignment is restored, converting any gap character that was inserted into three consecutive gaps to represent to inserted or deleted codon. This method of alignment prevents synonymous mutations from affecting the alignment while also preserving them for downstream analyses such as dN/dS calculations.

## What Can Kc-Align be Used For?

Kc-Align can be used to produce accurate and high quality MSA that can be used for various bioinformatic analyses such as homology modeling, phylogenetic reconstruction, and evolutionary selection analysis. These downstream analyses are heavily affected by the quality of the alignment that they are given and by aligning sequences on a codon-level, alignments from Kc-Align are able to produce more accurate downstream results. 

## Obtaining Kc-Align

Kc-Align is availbe through PyPI (`pip install kcalign`) and through Bioconda (`conda install kcalign`). Alternatively, a GUI interface for Kc-Align is installed and available for use on Galaxy (http://usegalaxy.org).

## Using Kc-Align

### USAGE:

`kc-align --mode genome --reference [reference sequence] --sequences [other seqs to align] --start [start coordinate] --end [end coordinate]`

#### (or)

`kc-align --mode [gene | mixed] --reference [reference sequence] --sequences [other seqs to align]`

### Arguments:

```
--mode/-m         Alignment mode (genome, gene, or mixed) (required)

--reference/-r    Reference sequences to align against (required)

--sequences/-S    Other sequences to align (required)

--start/-s        1-based start position (required in genome mode)

--end/-e          1-based end position (required in genome mode)

--compress/-c     Compress identical sequences

--parallel/-p     Enable parallelization of homology search

--table/-t        Choose an alternative translation table (See https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi for values)
```

### Modes

Kc-Align can be run in three different modes, depending on your input data. These modes are: genome, gene, and mixed.

#### Genome

If the reference sequences and all other sequences to be aligned are full genomes, this mode should be used. This mode requires the start and end coordinates of the gene/ORF to be aligned with regard to the reference sequence. Kc-Align will excise the appropriate subsequence from the referencce and then use pairwise alignments to find the corresponding homologous sequences from each of the other input genomes. It will then perform the MSA using the extracted sequences.

If the gene/ORF you wish to align exists in multiple distinct segments in the genome (ribosomal frameshift during transcription), Kc-Align can find each homologous segment separately for each input sequence and then concatenate them before performing the final MSA. This requires the user to enter the start and end coordinates of each segment as a comma-separated list following their respective arguments.

##### Example

`kc-align -m genome -r reference.fasta -S sequences.fasta -s 3532,3892 -e 3894,5326`

In the above example, the two segments being aligned have the coordinates 3532-3894 and 3892-5326.

#### Gene

If the input sequences have already been trimmed to the coding sequences of the gene/ORF of interest, then this mode can be used and Kc-Align will not perform the homology search as it does in genome mode. It instead simply immediately performs the MSA, making this mode much faster than the others.

#### Mixed

For the case when your reference is a coding sequence while all other sequences are whole genomes. Like gene mode, this mode does not require the start and end point position parameters but like genome mode it will perform homology searching in order to extract the sequences homologous to the reference from the other input sequences.

### Outputs

Kc-Align will output two files: a FASTA format alignment and a CLUSTAL format alignment.

### Compress Identical Sequences

If the `--compress/-c` parameter is specified, Kc-Align will compress identical sequences into a single sequence. In the FASTA output, compressed sequences will have an ID of the form MultiSeq[incremental index]_[number of sequences that were compressed] (ex: MultiSeq3_321, third compression with 321 sequences having that same sequence) while the description field is a comma-separated list of every ID that was compressed into that single sequence. The reference sequence will not be compressed.

### Parallelization

If the `--parallel/-p` parameter is used in genome or mixed mode, the calculations for the homology search will be split between 3 cores (if possible), decreasing runtimes by up to 35%.

## Kc-Align In Action

To demonstrate the utility of Kc-Align we analyzed 4,224 SARS-CoV2 genome assemblies available at NCBI at the time of writing. For this analysis we used Kc-align genome mode to generate codon-aware alignment for each of the SARS-CoV2 open reading frames (ORFs). We then analyzed codon alignments of each ORF using HyPhy, a software package for detection of selection and recombination. In particular we used the FEL (Fixed Effects Likelihood), MEME (Mixed Effects Model of Evolution), and FUBAR (Fast, Unconstrained Bayesian AppRoximation) methods. FEL uses a maximum-likelihood (ML) approach to infer nonsynoymous (dN) and synonymous (dS) substitution rates on a per-site basis for a given coding alignment and corresponding phylogeny. MEME employs a mixed-effects ML approach to test the hypothesis that individual sites have been subject to episodic positive or diversifying selection. FUBAR uses a Bayesian approach to infer dN and dS substitution rates on a per-site basis for a given coding alignment and corresponding phylogeny. The HyPhy tools identified 40 potential sites under positive selection. Three of these sites have been identified by all methods (these sites are marked with a star in the below table). Two have also been identified in more comprehensive analysis (see https://covid19.datamonkey.org). A UCSC genome browser visualization of the results can be found at http://genome.ucsc.edu/cgi-bin/hgTracks?db=wuhCor1&lastVirtModeType=default&lastVirtModeExtraState=&virtModeType=default&virtMode=0&nonVirtPosition=&position=NC_045512v2%3A1%2D29903&hgsid=863069951_GPeqUMFmcBlaA4afiGWTI9K936Wv


| Gene/ORF  | Codon Coordinates | FEL | MEME | FUBAR | Known Site | Nextstrain Variant |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| ORF1ab (leader)  | 626-628  |   |   | X  |   |   |
| ORF1ab (nsp2)*  | 1058-1060  | X  | X  | X  | X  | X  |
| ORF1ab (nsp2)  | 1514-1516  |   |   | X  |   | X  |
| ORF1ab (nsp3)  | 2945-2947  | X  |   |   |   |   |
| ORF1ab (nsp3)  | 3371-3373  | X  |   |   |   | X  |
| ORF1ab (nsp3)  | 6725-6727  | X  |   |   |   |   |
| ORF1ab (nsp4)  | 8885-8887  |   |   | X  |   |   |
| ORF1ab (3CL)  | 10097-10099  | X  |   |   |   | X  |
| ORF1ab (3CL)  | 10187-10189  | X  | X  |   |   |   |
| ORF1ab (3CL)  | 10265-10267  | X  |   |   |   | X  |
| ORF1ab (3CL)  | 10277-10279  | X  | X  |   |   |   |
| ORF1ab (nsp6)  | 11381-11383  | X  | X  |   |   |   |
| ORF1ab (nsp6)  | 11837-11839  | X  |   |   |   | X  |
| ORF1ab (RdRp/nsp11)  | 13445-13447  |   | X  |   |   |   |
| ORF1ab (RdRp/nsp11)  | 13451-13453  |   | X  |   |   |   |
| ORF1ab (RdRp/nsp11)  | 13457-13459  | X  | X  |   | X  | X  |
| ORF1ab (RdRp/nsp11)  | 13463-13465  | X  | X  |   | X  |   |
| ORF1ab (RdRp)*  | 14407-14409  | X  | X  | X  | X  | X  |
| ORF1ab (RdRp)  | 14425-14427  | X  |   |   |   | X  |
| ORF1ab (RdRp)  | 15922-15924  | X  | X  |   |   |   |
| ORF1ab (helicase)  | 17410-17412  | X  | X  |   |   | X  |
| ORF1ab (methyltransferase)  | 21145-21148  | X  |   |   |   |   |
| ORF1ab (methyltransferase)  | 21151-21153  | X  |   |   |   |   |
| Spike  | 21575-21577  | X  |   |   |   |   |
| Spike  | 21722-21724  | X  |   | X  |   |   |
| Spike  | 23402-23404  | X  |   | X  | X  | X  |
| ORF3a  | 25561-25563  |   |   | X  | X  | X  |
| ORF7b  | 27876-27878  | X  | X  |   |   |   |
| ORF8  | 27963-27965  | X  | X  |   |   | X  |
| ORF8  | 28077-28079  | X  | X  |   |   |   |
| ORF8  | 28086-28088  | X  | X  |   |   |   |
| ORF8  | 28092-28094  | X  | X  |   |   |   |
| ORF8  | 28143-28145  | X  | X  |   |   |   |
| N*  | 28310-28312  | X  | X  | X  |   | X  |
| N  | 28826-28828  | X  |   | X  |   |   |
| N  | 28850-28852  | X  |   |   |   |   |
| N  | 28886-28888  | X  |   | X  | X  |   |
| N  | 28985-28987  |   |   | X  |   | X  |
| N  | 29291-29293  | X  |   |   |   | X  |
| N  | 29450-29452  | X  |   |   |   | X  |

## Speed

The speed of Kc-Align is largely dependent on the analysis mode. In gene mode, it is comparable to Kalign3 on its own as there is little additional calculation needed to make the alignment codon aware. The genome and mixed modes, however, are several times slower than gene mode in order to facilitate the homology search, but an option to enable parallelization increases this speed by ~35%. This is accomplished by testing the three reading frames of each input sequence in parallel. We tested the speed of Kc-Align in Gene and Genome mode, as well as Genome mode with parallelization enabled, by aligning five SARS-CoV-2 CDSs of varying lengths using 1,000 total genomes. 

| Gene  | Length (nucleotides) | Gene Mode Run Time | Genome Mode (1 core) Run Time | Genome Parallel Run Time |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| ORF3a  | 827  | 00:00:28  | 00:08:23  | 00:05:19  |
| N  | 1259  | 00:00:28  | 00:12:54  | 00:08:14  |
| Spike  | 3821  | 00:00:50  | 01:20:51  | 00:52:47  |
| ORF1b  | 8084  | 00:01:54  | 5:04:43  | 03:20:00  |
| ORF1a  | 13202  | 00:04:31  | 13:55:10  | 9:09:25  |
