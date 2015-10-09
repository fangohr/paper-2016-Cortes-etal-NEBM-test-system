all:
	python generate_povray_inc.py
	povray generate[fm] generate_spins.pov
	povray generate[sk] generate_spins.pov
	povray generate[ds] generate_spins.pov
	convert ferromagnetic.jpg -crop 2500x1100+300+400 ferromagnetic.jpg
	convert skyrmion.jpg -crop 2500x1100+300+400 skyrmion.jpg
	convert destruction.jpg -crop 2500x1100+300+400 destruction.jpg

clean:
	rm *.inc
	rm *.jpg
