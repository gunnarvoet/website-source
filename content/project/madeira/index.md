---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Sensing the Ocean with Seafloor Fiber-Optic Cables"
summary: "Ground-truthing distributed fiber-optic sensing on a telecommunication cable off Madeira against conventional ocean measurements."
authors: []
tags: [madeira]
categories: []
date: "2025-01-01"

# Optional external URL for project (replaces project detail page).
external_link: ""

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  placement: 1
  caption: "The southern coast of Madeira seen from the ship during one of our surveys, with the cliffs of Cabo Girão in the center left."
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

Optical fibers make good strain sensors. Light scattered back along a fiber responds to tiny changes in its length, so a cable on the seafloor, interrogated with a laser from shore, works as a line of receivers about ten meters apart running tens of kilometers offshore. Telecommunication cables already cross the ocean basins, and that array is already in the water.

Read directly, the fiber reports on itself. Raman backscatter responds to temperature alone and Brillouin backscatter to both temperature and strain, the basis of distributed temperature-strain sensing, and either one gives a record along the cable, on the seafloor where it lies. We are after the water column above it, and the signal that carries information about that water is sound. Acoustic travel times depend on the temperature and the current along the path, and combining travel times over many paths is ocean acoustic tomography. Tomography has stayed rare because it needs a network of powerful sound sources, costly to maintain and a concern for marine life.

Noise interferometry does away with the sources. Cross-correlating the ambient noise recorded at two points recovers the wave that would travel between them, which turns any pair of sensors into virtual acoustic transceivers. The travel time between them gives sound speed and with it temperature, and the difference between travel times in the two directions gives the current. Oleg Godin has developed and tested the approach in the ocean using hydrophones.

A constraint on noise interferometry has been the sensors. Hydrophone pairs need sub-millisecond clocks kept on moorings for months, more sensors than is practical for oceanographically useful resolution, and hours to days of averaging to pull a clean arrival out of the noise. A cable removes all three. Every channel sits on the same fiber and the same clock, the record comes ashore in real time, and the number of sensor pairs grows as the square of the number of channels, which brings the averaging time down toward minutes.

Reading a cable this way is the new step. It should reach past the seafloor into the water column above, giving temperature and velocity at ten meters in the vertical and a few minutes in time, continuously and over the full length of the cable. Whether the inference holds, and how well it holds where the mechanical coupling between cable and seabed varies along the route, have to be settled by measurement. We instrument the water directly above the cable with conventional oceanographic sensors and compare the two records side by side.

The site is Madeira, where a telecommunication cable runs southward from Funchal, down the steep flank of the island and out into deep water. The internal tide over the slope is energetic, so there is a large signal for the method to find.

The observational part of the experiment has a pilot phase and a main phase. During the pilot phase we deployed instruments from RRS *Discovery* in October 2025 and recovered them in January 2026: a full water column mooring carrying ADCPs and McLane Moored Profilers, a shallow coastal mooring for our colleagues at the Oceanic Observatory of Madeira, and eight ocean bottom seismometers. We also occupied CTD/LADCP time series stations with MOD Epsilometers attached for turbulence, and transmitted from a towed sound source. The main phase runs from November 2026 through April 2027 with another mooring deployment and more shipboard profiling.

{{< figure src="station_map.png" narrow="true" caption="Instruments deployed on the southern slope of Madeira during the pilot phase: a full water column profiling mooring, a shallow coastal mooring, eight ocean bottom seismometers, and the stations where we occupied CTD/LADCP time series and transmitted from a towed sound source." >}}

The project is jointly funded by NSF in the US and NERC in the UK and is a collaboration between Matthew Alford and myself at Scripps, Oleg Godin at the Naval Postgraduate School, and colleagues at the National Oceanography Centre in the UK.
