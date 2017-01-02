# SwiftXRT Automated Spectral Extraction (XRT_ASE)
Quick spectral extraction of multiple Swift/XRT observations. 

This script uses resources and tasks provided by the Swift team (e.g., see [here](http://www.swift.ac.uk/analysis/xrt/spectra.php)) to quickly go through reduction and spectral extraction for multiple XRT observations with a few things done manually.

Currently the code assumes all the event files for all observations are dumped in the same folder where the code runs. This can be done by running `xrtpipeline` on all observations and dumping products in the same folder.

Things to fix:

- automated lightcurve can look weird sometimes, maybe due to `xrtpipeline` coords being set to `OBJECT`.
- handling GTI separated spectral extraction: currently it doesn't make exposure maps for each segment
- handling pile up for multi-segment observations: make image for each segment to run in Ximage
- for multiple-GTI observations even when you say no to extraction it asks for separation
- handling pile up within the code?
- better light curve plots with axis labels, etc.
- file clean up
