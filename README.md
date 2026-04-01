# Schizophrenia GWAS Analysis

This is a production-style bioinformatics pipeline that processes a large data set of 7.5 million SNPs (genetic variants) from the Psychiatric Genomics Consortium Wave to identify significant loci associated with schizophrenia and characterizes the biological pathways they implicate. Results are served through an interactive web dashboard built on FastAPI that only requires two terminal commands that can be found in the next section. The analysis can be seen in analysis.ipynb and is described in this README.

The pipeline spans data ingestion, statistical 
filtering, genome-wide visualization, linkage disequilibrium pruning, 
REST API integration, and pathway enrichment analysis.

**Data**: Psychiatric Genomics Consortium Wave 3 (Nature, 2022) — 76,755 cases, 243,649 controls.

---

## Instructions for viewing the Interactive Web App of Findings
Run the following commands:

pip install -r requirements.txt
python main.py

Then copy and paste the url the terminal gives you into safari or firefox. The url will look something like 
http://localhost:5050 where localhost is replaced with your computer IP.


## Pipeline (View analysis.ipynb)

### 1. Loading & Quality Control
Raw summary statistics contain ~7.5M SNPs across all 22 autosomes. Variants are filtered to high-confidence imputed SNPs (IMPINFO > 0.8) and genome-wide significance (p < 5×10⁻⁸), reducing to 21,539 significant associations.

### 2. Manhattan Plot
Visualizes association strength across the genome. The dominant signal on chromosome 6 corresponds to the Major Histocompatibility Complex (MHC) — the most replicated schizophrenia locus, implicating immune and synaptic pruning pathways.

### 3. LD Pruning
21,539 significant SNPs collapse to **355 independent loci** using positional clumping: a 250kb sliding window retains only the most significant SNP per window, discarding redundant SNPs in linkage disequilibrium.

> **Note on method**: Formal LD pruning requires individual-level genotype data (not publicly available for PGC3) to compute pairwise r² between variants. Positional clumping is the standard approach for summary-statistic-only analyses and is used in published GWAS papers, but it is an approximation. This is especially seen in high-LD regions like the MHC on chromosome 6, where a single pruned SNP may represent hundreds of nearby genes.

### 4. Gene Annotation
Each independent locus is mapped to its nearest gene using the Ensembl VEP REST API, retrieving gene symbol, functional consequence (missense, intronic, 5' UTR, synonymous), and biotype (protein-coding, lncRNA). Results are cached in `results/mapped_snps.csv`.

**Note on method**: Additionally, I filter out so only the most relevant functional consequences are selected. If the SNP is in a non-coding region and its nearest gene is hundreds of kb away, then the relationship between SNP and nearest gene is extremeley weak, so it is important to filter these out.


### 5. Pathway Enrichment
The annotated gene list is submitted to Enrichr (GO Biological Process, Molecular Function, Cellular Component; KEGG) via gseapy. 15 pathways reach statistical significance after Benjamini-Hochberg correction (adjusted p < 0.05).

---

## Key Findings

- **MHC dominance**: 7 of the 15 top loci by effect size fall within the MHC on chromosome 6. The causal signal here most likely traces to HLA allele variation rather than the flanking genes assigned by positional annotation. The HLA-schizophrenia link is well-established in literature, so the fact this is showing up helps validate the quality of my analysis.
- **Calcium channel enrichment**: Voltage-gated calcium channel subunits (CACNA1C, CACNA1D, CACNA1I) appear across 7 enriched pathways — the dominant non-MHC biological theme. In the Calcium Ion Import pathway, 4 of 12 known pathway genes (33%) carry a variant associated with schizophrenia. 
- **Neurodevelopment**: TCF4, a bHLH transcription factor critical for GABAergic and glutamatergic neuron development, produces two independent association signals: the strongest convergent evidence for a single causal gene in the dataset. You can see in the top 15 list on the web app that there are two SNPs on this gene.
- **Only one missense variant in the top 15**: SLC39A8 (chr4), a zinc/manganese transporter, is the sole protein-altering variant among the top loci. All others are intronic, 5' UTR, or synonymous.

---
