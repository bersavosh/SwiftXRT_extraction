# SwiftXRT_extraction
Quick spectral extraction of multiple Swift/XRT observations.

This script uses resources and tasks provided by the Swift team (e.g., see [here](http://www.swift.ac.uk/analysis/xrt/spectra.php)) to quickly go through reduction and spectral extraction for multiple XRT observations. 

** STILL IN DEVELOPEMENT AND NOT FUNCTIONAL **


Currently the code assumes all the event files for all observations are dumped in the same folder where the code runs. This can be done by running `xrtpipeline` on all observations and dumping products in the same folder.

Things to fix:

- handling GTI separated spectral extraction: currently it doesn't make exposure maps for each segment
- handling pile up for multi-segment observations: make image for each segment to run in Ximage
- for multiple-GTI observations even when you say no to extraction it asks for separation
- handling pile up within the code?
- better light curve plots with axis labels, etc.
