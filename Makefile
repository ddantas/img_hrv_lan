

dox:
	doxygen hrv_lan.dox

runop:
	python3 WinOp.py

runsub:
	python3 WinSub.py

# Synchronization of videos of both subjects.
# Force both videos to have the same length.
runsync:
	python3 01_sync/sync.py data/b046
	python3 01_sync/sync.py data/b048

runprep:
	#python3 02_preprocess/preprocess.py data/b*
	python3 02_preprocess/preprocess.py data/b001

# Profiling of WinOp.py
profop:
	yappi -b -f pstat -o data/yappi_profop WinOp.py
	snakeviz data/yappi_profop

# Profiling of WinSub.py
profsub:
	yappi -b -f pstat -o data/yappi_profsub WinSub.py
	snakeviz data/yappi_profsub



