

dox:
	doxygen hrv_lan.dox

runop:
	python3 WinOp.py

runsub:
	python3 WinSub.py

# Synchronization of videos of both subjects.
# Force both videos to have the same length.
runsync:
	python3 01_sync/sync.py data/a003

runprep:
	python3 preprocessing/rr_interpolation.py data/a003/subj1_rr.tsv
	python3 preprocessing/rr_interpolation.py data/a003/subj2_rr.tsv
	python3 preprocessing/Preprocess.py data/a003 subj1_ecg.tsv subj2_ecg.tsv processed/subj1_rr_linear.tsv processed/subj2_rr_linear.tsv annotation.eaf output.tsv

# Profiling of WinOp.py
profop:
	yappi -b -f pstat -o data/yappi_profop WinOp.py
	snakeviz data/yappi_profop

# Profiling of WinSub.py
profsub:
	yappi -b -f pstat -o data/yappi_profsub WinSub.py
	snakeviz data/yappi_profsub



