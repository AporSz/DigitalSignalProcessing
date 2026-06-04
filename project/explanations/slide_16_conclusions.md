# Slide 16 – Conclusions & Modeling Value

## What this slide shows

This is the **summary and forward-looking slide**. It synthesises all findings from the previous slides into a compact set of scientific conclusions and outlines directions for future work. There are no new plots — the slide presents two glass-card text panels side by side:

1. **Key Scientific Findings** — what the analysis proved.  
2. **Future Directions** — what comes next.

---

## Key scientific findings

### 1. Stratified CO₂ gas layering confirmed
The vertical heatmap (Slide 9) and the cross-stack correlation analysis (Slides 7–8) together prove that CO₂ accumulates in a **stable, stratified layer** at the bottom of the mofette chamber. This is not a measurement artefact — it is a physical consequence of CO₂ being denser than air, and it persists 24/7 throughout the 7-month campaign.

### 2. Barometric pressure is the primary immediate driver
The cross-correlation analysis (Slide 15) showed that CO₂ level responds to atmospheric pressure changes with **virtually zero time lag** (r = −0.42). This makes pressure the dominant short-term control mechanism — it acts like an atmospheric piston pumping the gas pool up and down.

### 3. A diurnal 24-hour rhythm driven by temperature with a 3-hour thermal lag
The bandpass filter (Slide 12), Welch PSD (Slide 13), and spectrogram (Slide 14) all independently confirm the existence of a rock-solid **24-hour breathing cycle**. Temperature drives this cycle with a 3-hour delay due to thermal conduction through the soil (Slide 15). The cycle is strongest in summer (July–August) when solar forcing is most intense.

---

## Future directions

| Direction | Description |
|---|---|
| **Predictive Models** | Train neural networks (e.g. LSTMs) or physical gas diffusion models using pressure and temperature as inputs to forecast CO₂ boundary height. |
| **Safety Monitoring** | Build real-time alert systems that trigger when forecast pressure drops are large enough to cause dangerous CO₂ surges above the normal safe zone. |
| **Volcanic Activity Indicators** | Monitor long-term changes in the mofette's breathing *rate* or *amplitude* as a proxy for deep crustal stress and tectonic activity. |

---

## Why this matters

This slide ties together the entire narrative arc of the presentation:

- **Slides 1–6** introduced the site, the sensors, and the raw data.  
- **Slides 7–8** validated the sensor network spatially.  
- **Slide 9** revealed the spatial structure of the gas column.  
- **Slides 10–12** decomposed the signal into seasonal and daily components.  
- **Slides 13–14** provided frequency-domain proof of the daily cycle.  
- **Slide 15** identified the environmental forces driving the cycle.  
- **Slide 16** (this slide) synthesises those findings and shows where the work leads next.

The study demonstrates that **digital signal processing is a powerful tool for geophysical monitoring**: by separating timescales and quantifying cross-correlations, it transforms a complex, noisy environmental dataset into actionable physical knowledge.
