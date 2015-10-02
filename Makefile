.PHONY: relaxation nebm plot clean

relaxation:
	echo "Relaxing Ferromagnetic and Skyrmionic states"
	cd relaxation && python ferromagnetic.py
	cd relaxation && python skyrmion.py

nebm:
	echo "Starting NEBM relaxation with k=1e10 and 1e11"
	python neb_simulation_sk-fm.py

plot:
	echo "Generating Energy Bands plot"
	python plot_ebds.py

clean:
	rm -f *.ndt timings.dat energy_bands.pdf
	rm -f -r npys/
	rm -f -r vtks/
	rm -f -r relaxation/relax_fm_npys/
	rm -f -r relaxation/relax_fm_vtks/
	rm -f -r relaxation/relax_sk_npys/
	rm -f -r relaxation/relax_sk_vtks/
	rm -f relaxation/relax*.txt