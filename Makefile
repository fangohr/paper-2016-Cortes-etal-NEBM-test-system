.PHONY: relaxation nebm plot clean

relaxation:
	echo "Relaxing Ferromagnetic and Skyrmionic states"
	cd relaxation && python ferromagnetic.py
	cd relaxation && python skyrmion.py

nebm:
	echo "Starting NEBM relaxation"
	python neb_simulation_sk-fm.py

climbing:
	echo "Starting Climbing Image NEBM simulation"
	python climbing_image_neb_simulation_sk-fm.py

plot:
	echo "Generating Energy Bands plot"
	python plot_ebds.py

plot_climbing:
	echo "Generating snapshots for the Climbing Image NEBM simulation"
	python generate_snapshots_climbing_image.py

clean:
	rm -f *.ndt timings.dat energy_bands.pdf
	rm -f -r npys/
	rm -f -r vtks/
	rm -f -r relaxation/relax_fm_npys/
	rm -f -r relaxation/relax_fm_vtks/
	rm -f -r relaxation/relax_sk_npys/
	rm -f -r relaxation/relax_sk_vtks/
	rm -f relaxation/relax*.txt
