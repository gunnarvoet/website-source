---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "ADCP Sampling Schemes"
subtitle: ""
summary: "Continuous pinging or burst mode? The averaging statistics settle most of it, and the burst length compared against the decorrelation time of the flow settles the rest."
authors: []
tags: []
categories: []
date: 2026-09-03T15:45:20-07:00
lastmod: 2026-09-03T15:45:20-07:00
featured: false
draft: true
reading_time: false
math: true

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  placement: 3
  caption: "A 6000-m rated RDI Workhorse 300 on the bench during setup. Photo © Thomas Moore."
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
---

Have you ever wondered what sampling scheme to use when setting up your ADCP? The instrument can ping continuously at a set rate, or fire a rapid interval of pings in burst mode. But what is better? I have asked myself this question in the past, often at sea when getting instruments ready for deployment. Here are advantages for either mode for the next time I am out there. Maybe you find these helpful as well. Send me an [email](/#contact) if you disagree or have any advice!

The ocean signal is usually weak enough that you have to average over a handful of pings to push the noise amplitude of your measurement below what you would like to observe. And your battery fixes how many pings you get out of the whole deployment, with the memory card capping them too once you record every ping, so the same $N$ pings land in each ensemble interval either way, and you choose only where inside the interval they sit. Take the battery away and there is nothing to decide. You ping as fast as the instrument allows and average however you like afterwards.

## Noise floor

Start with the part that does not depend on the sampling scheme at all. Inherent measurement noise is uncorrelated from ping to ping, so averaging $N$ pings reduces it by $\sqrt{N}$ however the pings are distributed in time. Sixty rapid pings inside a minute and sixty pings spread over ten minutes have the same noise floor.

## Sampling error

The sampling scheme decides the gap between the pings you took and the average you wanted. Call $\hat{u}$ the ensemble the instrument writes down, the average of its $N$ pings, and call $\bar{u}_T$ the true average of the flow over the ensemble interval $T$, the number you were after. The $N$ pings sit inside a window $W$. Burst sampling has $W = \tau$, the burst length. Continuous pinging has $W = T$. The variance of the miss, $\mathrm{Var}(\hat{u} - \bar{u}_T)$, consists of two terms:

<div>
$$\mathrm{Var}\left(\hat{u} - \bar{u}_T\right) \approx \frac{\sigma_p^2}{N} + \sigma_s^2\,\frac{2 T_\mathrm{int}}{W}$$
</div>

with $\sigma_p$ the single-ping noise, and $\sigma_s$ and $T_\mathrm{int}$ the amplitude and integral timescale of the motions you are averaging over, which you never meant to resolve. Neither scheme biases the mean, so that variance is also the mean square error of one ensemble, and its square root is the error bar you would put on a single point of the record.

The first term counts pings. The second counts independent samples, $N_\mathrm{eff} = W/(2 T_\mathrm{int})$, and the length of the sampling window sets that number. The ping count does not enter. This is the standard effective-degrees-of-freedom result (see for example Thomson and Emery's *Data Analysis Methods in Physical Oceanography*).

A one-minute burst every ten minutes samples over $W = 1$ min where continuous pinging samples over $W = 10$ min, so the burst ensemble carries ten times the sampling-error variance, roughly three times the standard error, at more or less the same power consumption.

In the frequency domain it is the same statement. Burst ensembles alias everything between $1/T$ and $1/\tau$ into the spectrum you resolve, where continuous ensembles attenuate that band by the boxcar response of the average. If you are after tides or internal waves and there is energetic motion sitting above them, that alone settles the question.

## Burst length against decorrelation time

The ratio $\tau/T_\mathrm{int}$ carries the whole comparison, and the case for burst mode turns out to be the same equation read at the other end. At $\tau \gg T_\mathrm{int}$ the burst behaves like continuous pinging with fewer degrees of freedom, which is the cost above. At $\tau \ll T_\mathrm{int}$ every ping in the burst sees one realization of the flow, $N_\mathrm{eff}$ falls to one, and the burst average becomes the instantaneous velocity plus $\sigma_p/\sqrt{N}$.

So a burst-average is a very good quasi-instantaneous velocity measurement. The property that costs you accuracy on the mean is the same property you are paying for when you want the snapshot.

## Vertical velocity

The snapshot pays off most for vertical velocity. The noise geometry here is often read backwards: for a Janus pair at beam angle $\theta$ from vertical, $\sigma_u/\sigma_w = \cot\theta$, about 2.8 at the usual 20°, so $w$ is the quieter component per ping. $w$ itself is smaller by two or three orders of magnitude, though, and the events that produce it are short. Of everything the instrument measures, $w$ needs the most averaging and tolerates the least of it. Burst mode is the one configuration that offers both.

## Ping distribution and recording granularity

Picking the averaging scheme later only works if single pings reach the memory card. I usually record every ping, so that freedom is real for me. Let the instrument average a ten-minute ensemble onboard instead and continuous pinging quantizes your post-processing to ten-minute multiples, which is the complaint you would level at burst mode. Two separate choices hide in here: how the pings sit in time, and what granularity gets written. Only the second one buys flexibility.

## Reasons to pick burst

- **Turbulence methods need it.** The structure-function estimate of $\varepsilon$ ([Wiles et al. 2006](https://doi.org/10.1029/2006GL027050), and [Lucas et al. 2014](https://doi.org/10.1175/JTECH-D-13-00198.1) for the moored case) and the covariance method for Reynolds stress ([Lu and Lueck 1999](https://doi.org/10.1175/1520-0426(1999)016%3C1568:UABAIA%3E2.0.CO;2)) all want rapid pings resolving the turbulent band, with single pings written to memory. No duty cycle you can afford across a long deployment will give you that.
- **You can measure your own noise floor.** Rapid pings inside a burst let you estimate $\sigma_p$ from the high-frequency plateau of the within-burst spectrum, or from differences between adjacent pings, without taking the manufacturer's number on faith.
- **Power.** The instrument sleeps between bursts where continuous pinging keeps it awake, which can buy real deployment time at the same ping count. A wake-up cost works against very short and very frequent bursts, so put both configurations through the planning software before believing either.
- **Scheduling.** On a mooring carrying several acoustic instruments, bursts can be interleaved so the instruments stay out of each other's way.

## Reasons to pick continuous

- **Graceful degradation.** A fish, a knockdown or an interference hit costs you the whole ensemble in burst mode. Pinging continuously, you drop the bad pings on correlation and echo amplitude and keep the rest of the interval.
- **Extremes.** The mean stays unbiased either way, but a low duty cycle undersamples intermittent events. Event counts, maxima and variance then describe your sampling scheme as much as they describe the flow.
- **Recoverability.** Continuous pinging costs you the snapshot and some battery. Burst mode costs you a decision about $\tau$ against $T_\mathrm{int}$ that you had to make before you knew what $T_\mathrm{int}$ was, and that you cannot revisit at your desk.

## Two things worth checking

The $\sqrt{N}$ scaling assumes ping errors are independent. Fire faster than the scattering volume decorrelates and successive pings sample a partly correlated scatterer field, which should cost some of that $\sqrt{N}$. I do not know how large the effect is. It is checkable against records you already have, by comparing an observed burst-average noise floor with $\sigma_p/\sqrt{N}$.

Reverberation sets a floor under the burst ping interval. Fire again before the previous ping's echoes have faded and the new profile lands on top of them. The instrument already enforces a minimum interval covering its own profiling range, so the case to watch is a strong reflector outside that range, the surface for an upward-looker or the bottom for a downward one, returning after the profiling window has closed. How much margin that needs depends on geometry and frequency.

## A default

Continuous, and something specific has to push me off it. Turbulence estimates push. So does a regime where the vertical velocity snapshot is the measurement. So does a battery that forces a duty cycle on me. Absent one of those, spreading the pings costs nothing I can name and leaves the averaging decision for my desk, where I can still change my mind about it.

Whatever you end up picking, you'll probably end up with a dataset full of mysteries. At least that's what usually happens to me. Also: [velosearaptor](https://github.com/modscripps/velosearaptor) is ready to handle either sampling scheme.
