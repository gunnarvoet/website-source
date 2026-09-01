---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Moored Turbulence Sensors - MODchi"
summary: "Developing a moored temperature microstructure sensor, and measuring turbulent mixing across the equatorial Pacific cold tongue."
authors: []
tags: [modchi]
categories: []
date: "2026-07-01"

# Optional external URL for project (replaces project detail page).
external_link: ""

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  placement: 1
  caption: "Attaching an earlier version of the chipod to a [NISKINe](/project/niskine/) mooring in the Iceland Basin, 2019. MODchi builds on the same instrument."
  focal_point: ""
  preview_only: false

# Custom links (optional).
#   Uncomment and edit lines below to show custom links.
# links:
# - name: Follow
#   url: https://twitter.com
#   icon_pack: fab
#   icon: twitter

url_code: ""
url_pdf: ""
url_slides: ""
url_video: ""

# Slides (optional).
#   Associate this project with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides: ""
---

MODchi (pronounced *mochi*, /ˈmoʊtʃi/) is a moored turbulence sensor under development at [Multiscale Ocean Dynamics](https://www.mod.ucsd.edu). It is built to spend a year and a half on a mooring measuring ocean turbulence. A meridional array of these measurements goes on the TAO moorings at 140°W.

Sea surface temperature in the equatorial Pacific cold tongue exerts a controlling influence on ENSO dynamics and on climate variability far beyond the tropics. Its evolution is governed by horizontal advection, upwelling, net surface heat flux, and the vertical divergence of turbulent heat flux. The turbulent heat flux is a leading-order term and the least constrained by observations. At the equator, subsurface turbulent cooling can rival or exceed net surface heating during boreal summer, which makes it a primary control on the seasonal cycle of cold tongue SST. The flux has been measured continuously at a single location, 0°, 140°W, so its meridional structure is unresolved by observations.

The meridional structure matters because the net turbulent heating or cooling integrated across the cold tongue depends on how the flux converges between roughly 2°S and 2°N. High-resolution simulations place the peak within 2° of the equator with a pronounced north-south asymmetry, and the fluxes they produce run about a factor of two above the single observational estimate. On the equator, shear between the South Equatorial Current and the Equatorial Undercurrent holds the gradient Richardson number near its critical value of about 0.25, a state of marginal instability in which the diurnal cycle triggers mixing that penetrates 50 to 100 m into the stratified thermocline. Modeling work indicates this deep cycle turbulence also occurs away from the equator inside the cold cusps of tropical instability waves, where vortex tilting by the wave circulation converts equatorial zonal shear into intense meridional shear near 1 to 4°N. We are unaware of long microstructure time series off the equator that could confirm that modeled diurnal signal, quantify the heat fluxes that go with it, or resolve the north-south asymmetry.

Three chipods are mounted on each of five TAO moorings, at 2°S, 1°S, the equator, 1°N and 2°N, giving continuous records that resolve the cross-equatorial structure of turbulent mixing, with a few MODchi prototypes alongside them for ground-truthing. The National Data Buoy Center deploys the moorings in fall 2027 and recovers them in spring 2029. The array is part of the Tropical Eastern Pacific Experiment (TEPEX-E).

The moored chipod, developed by Jim Moum's group at Oregon State University, is the instrument behind these records. It clamps to the mooring wire and carries two fast thermistors, a pressure sensor, three linear accelerometers and a compass. Temperature-gradient spectra fit to the Kraichnan universal form and integrated give χ, the rate at which molecular diffusion removes temperature variance, and from χ follow dissipation rate of turbulent kinetic energy, turbulent heat flux and eddy diffusivity. Accelerometer records are integrated in time to recover cable motion, which together with the ambient current from a co-located ADCP gives flow speed past the sensors, a critical input to the spectral fit. A new version carries a deflector that keeps fishing gear off the instrument, is approved by NDBC, and is designed to measure for up to 18 months.

Fifteen chipods for the array are being built at Oregon State. The MODchi prototypes keep the OSU mechanical design and analog front end and pair them with the electronics of the MOD Epsilometer. The development effort goes into adapting the MOD system-on-module controller and its firmware to acquire and store year-long thermistor, pressure and inertial records, and into characterizing power draw well enough that the instrument survives an 18-month deployment. A single controller architecture is essential for keeping moored turbulence sensor production sustainable inside our group. MOD engineers will train at Oregon State during the build phase, and the prototypes will be validated in a test deployment offshore San Diego in spring 2027, on a subsurface mooring carrying a MODchi and an OSU chipod within about 2 m of each other, with shipboard microstructure shear profiling as a reference for both instruments.

The project is carried out at Scripps together with Arnaud Le Boyer and Matthew Alford, in collaboration with Jim Moum at Oregon State University, and is funded by the Climate Variability and Predictability program of the National Oceanic and Atmospheric Administration.
