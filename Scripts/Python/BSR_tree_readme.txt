Logic for calculating bitscore ratios:
I mostly used datafram manipulation for this. My original blast output looks like this:
unbinned.contig56955_bioreactor|33545	unbinned.contig56955_bioreactor|33545	100.000	216	0	0	1	216	1	216	1.91e-159	436	100
unbinned.contig56955_bioreactor|33546	unbinned.contig56955_bioreactor|33546	100.000	151	0	0	1	151	1	151	4.83e-110	305	100

1. import the blast output as a csv file, only use columns "qseqid" "sseqid" "pident" and "bitscore"

2. filter for pident >= 40 and delete this column

3. create two more columns based on the contig names from qseqid and sseqid. Now my dataframe looks like:

qcontig | qseqid | scontig | sseqid | bitscore

4. group and sum by qcontig and scontig. All proteins belonging to the same contig that are matched to another contig, the bitscore is summed --> goes into new dataframe. 
Now my dataframe looks like:

qcontig | scontig | bitscore_SUM

5. Change dataframe from long format to wide format. Now it looks like:
			j=0			j=1
		scontig		unbinned.contig56955	bin12.contig0010
	qcontig
i=0	unbinned.contig56955	Bitscore_sum		Bitscore_sum
i=1	bin12.contig0010	Bitscore_sum		Bitscore_sum

6. Create a nested list (2D array) from above dataframe

7. Create a dictionary (hash table) of all the contigs based the contigs in the above dataframe. The dictionary looks like this:

{unbinned.contig56955: 0, bin12.contig0010: 1}

8. Iterate through the 2D array to calculate bit score ratios using i,j counters and add to new dictionary

for i (0 -> 60):
	for j (0 -> 60):
		BSR= BSR=max(arr[i][j],arr[j][i])/min(arr[i][i],arr[j][j])
		new_dict[i,j]=BSR

Now my new_dict looks like:
{(0,0):1, (0,1):0.06, etc}

9. Inverse map my previous contigs dictionary:
{0:unbinned.contig56955, 1: bin12.contig0010}

10: Loop through my new_dict, where contigs and BSRs are stored to pull out contigs from my inverse map dictionary

for k1,k2 in new_dict.keys():
    print({'contig1':inv_map[k1],'contig2':inv_map[k2],'BSR':new_dict[k1,k2]})

my printed output is:
bin12.contig0010	bin12.contig0010	1.0
bin12.contig0010	bin23.contig0003	0.01729577076732332
bin12.contig0010	bin34.contig0002	0.0
bin12.contig0010	bin34.contig0019	0.0
bin12.contig0010	bin35.contig0006	0.0
bin12.contig0010	bin35.contig0174	0.0
bin12.contig0010	bin50.contig0037	0.0
bin12.contig0010	bin52.contig0160	0.5052948557089084
bin12.contig0010	bin52.contig0161	0.4906071613907628

11. Wrote my pairwise BSRs into a csv file

