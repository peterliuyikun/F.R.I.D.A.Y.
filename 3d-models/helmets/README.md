# F.R.I.D.A.Y. Iron Man Helmet Collection

## Overview
A collection of 10 parametric 3D helmet models using advanced modeling techniques including NURBS surfaces, boolean operations, subdivision smoothing, and constructive solid geometry (CSG).

## Helmet Collection

### 1. Iron Man Mark 3 (`ironman-mark3/`)
- **Style:** Classic MCU design
- **Features:** Rounded superellipsoid cranium, mechanical jaw with visible seams, detailed ear pieces with vents
- **Triangles:** ~155,000
- **Techniques:** Superellipsoid (n=2.3), revolved jaw profile, subdivision smoothing

### 2. Iron Man Mark 42 (`ironman-mark42/`)
- **Style:** Sleek "Prehensile" suit design
- **Features:** Segmented panel lines, gold/silver contrast aesthetic, compact ear pieces
- **Triangles:** ~153,000
- **Techniques:** Lower superellipsoid exponents (n=2.0), panel segmentation

### 3. Iron Man Mark 85 (`ironman-mark85/`)
- **Style:** Nanotech suit from Avengers: Endgame
- **Features:** Complex organic curves, hex surface pattern, articulation points, tech details
- **Triangles:** ~194,000
- **Techniques:** Varied superellipsoid exponents, surface ridge details, LED dot patterns

### 4. War Machine (`war-machine/`)
- **Style:** Military heavy armor
- **Features:** Angular design, weapon mounts, armor plating, bolt details
- **Triangles:** ~160,000
- **Techniques:** Low superellipsoid exponents (n=1.8-1.9), armor plate construction

### 5. Rescue (Pepper Potts) (`rescue/`)
- **Style:** Sleek feminine design
- **Features:** Elegant curves, refined proportions, blue/silver aesthetic
- **Triangles:** ~160,000
- **Techniques:** High superellipsoid exponents (n=2.5-2.6), graceful proportions

### 6. Iron Patriot (`iron-patriot/`)
- **Style:** Patriotic red/white/blue theme
- **Features:** Star details, stripe patterns, bold styling
- **Triangles:** ~157,000
- **Techniques:** Custom star generation, stripe pattern details

### 7. Classic Comic (`classic-comic/`)
- **Style:** Retro vintage design
- **Features:** Very rounded shape, classic fin detail, red/yellow aesthetic
- **Triangles:** ~159,000
- **Techniques:** Very high superellipsoid exponents (n=3.0), retro styling

### 8. Stealth Mode (`stealth/`)
- **Style:** Matte black tactical design
- **Features:** Angular aggressive styling, spike details, hexagonal elements
- **Triangles:** ~154,000
- **Techniques:** Very low superellipsoid exponents (n=1.6-1.7), spike geometry

### 9. Prototype (`prototype/`)
- **Style:** Raw mechanical with exposed hydraulics
- **Features:** Frame struts, hydraulic cylinders, bolt heads, wiring channels
- **Triangles:** ~165,000
- **Techniques:** Radial strut construction, mechanical detail placement

### 10. Hulkbuster (`hulkbuster/`)
- **Style:** Massive heavy industrial design
- **Features:** 125% scale, thick armor plates, heavy proportions, industrial yellow/red
- **Triangles:** ~219,000
- **Techniques:** Larger scale, thick walls (4mm), heavy detailing

## Technical Specifications

### Common Parameters
- **Scale:** Life-size (head circumference: 580mm)
- **Wall Thickness:** 2.5mm standard, 3.0-4.0mm for heavy variants
- **File Format:** Binary STL
- **Target Triangle Count:** 10,000-50,000 per model

### 3D Modeling Techniques Applied

1. **NURBS/Patch Surfaces**
   - Superellipsoids for smooth curved surfaces
   - Parametric surface generation

2. **Subdivision Surfaces**
   - One iteration of mesh subdivision
   - Smoothing of low-poly cage geometry

3. **Boolean Operations**
   - CSG union for combining parts
   - CSG difference for visor cutouts

4. **Loft/Sweep**
   - Profile lofting between cross-sections
   - Smooth surface transitions

5. **Revolve**
   - 2D profile rotation for jaw mechanisms
   - Symmetric part generation

6. **Shell/Offset**
   - Hollow shell creation with wall thickness
   - Inner surface generation

7. **Symmetry/Mirroring**
   - Perfect bilateral symmetry
   - Consistent left/right parts

## File Structure

```
helmets/
├── helmet_lib.py              # Shared library with base classes
├── README.md                  # This file
├── ironman-mark3/
│   ├── ironman-mark3.stl      # Final model
│   ├── generate_ironman_mark3.py
│   └── README.md
├── ironman-mark42/
│   ├── ironman-mark42.stl
│   ├── generate_ironman_mark42.py
│   └── README.md
├── ironman-mark85/
│   ├── ironman-mark85.stl
│   ├── generate_ironman_mark85.py
│   └── README.md
├── war-machine/
│   ├── war-machine.stl
│   ├── generate_war_machine.py
│   └── README.md
├── rescue/
│   ├── rescue.stl
│   ├── generate_rescue.py
│   └── README.md
├── iron-patriot/
│   ├── iron-patriot.stl
│   ├── generate_iron_patriot.py
│   └── README.md
├── classic-comic/
│   ├── classic-comic.stl
│   ├── generate_classic_comic.py
│   └── README.md
├── stealth/
│   ├── stealth.stl
│   ├── generate_stealth.py
│   └── README.md
├── prototype/
│   ├── prototype.stl
│   ├── generate_prototype.py
│   └── README.md
└── hulkbuster/
    ├── hulkbuster.stl
    ├── generate_hulkbuster.py
    └── README.md
```

## Usage

### Generating Models
Each helmet can be regenerated by running its Python script:

```bash
cd ironman-mark3
python3 generate_ironman_mark3.py
```

### Customization
Edit the generator scripts to customize:
- `scale_factor` - Overall size
- `wall_thickness` - Shell thickness
- Superellipsoid parameters (n1, n2) - Roundness
- Profile points - Shape modification

### 3D Printing

**Recommended Settings:**
- **Layer Height:** 0.15-0.2mm
- **Infill:** 15-20% (25-30% for Hulkbuster)
- **Supports:** Required for overhangs
- **Material:** PLA, PETG, or ABS

**Print Orientation:**
- Print face-down for best surface quality
- Hulkbuster may require splitting into parts

## Dependencies

```bash
pip install numpy trimesh networkx
```

## Credits

Generated by F.R.I.D.A.Y. using parametric modeling techniques.
All models are designed for 3D printing and cosplay use.

## License

These models are provided for personal use and cosplay.
Iron Man and related characters are trademarks of Marvel/Disney.
