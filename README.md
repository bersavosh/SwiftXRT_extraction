# SwiftXRT Automated Spectral Extraction (XRT_ASE)
Quick spectral extraction of multiple Swift/XRT observations. 

This script uses resources and tasks provided by the Swift team (e.g., see [here](http://www.swift.ac.uk/analysis/xrt/spectra.php)) to quickly go through reduction and spectral extraction for multiple XRT observations with a few things done manually.

The code assumes all the event files for all observations are dumped in the same folder where the code runs. This can be done by running `xrtpipeline` on all observations and dumping products in the same folder.

The script [XRT_ASE](https://github.com/bersavosh/XRT_ASE/blob/master/XRT_ASE.py) is currently in preliminary form.

### Tasks:
- XRT spectral extraction (**Done**)
- XSPEC fitting 
- UVOT photometry
- plotting light curves

### Things to improve:
- Check observation/segment expsure and counts
- allow skipping extraction from a segment
- ask to launch DS9
- handling pile up
- file clean up
- create/open a logfile and check status of previous runs in the directory
- Tabulate observations better before analysis

### Things to watch out for:
- Automated lightcurve can look weird sometimes, if the source is faint and actual source coordinates are not exactly consistent with `OBJECT` coordinates in the observation.

More updates and detailed description to be added.
