#!/usr/bin/env python3
"""
Iron Man Mark 42 Helmet Generator
Sleek, segmented design with gold/silver contrast
Features smooth curves with panel-like segmentation
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class IronManMark42Helmet(IronManHelmetBase):
    """
    Mark 42 - The "Prehensile" suit helmet
    Sleeker, more angular design with visible panel lines
    Gold/silver color scheme with segmented appearance
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.0)
        self.name = "Iron Man Mark 42"
        self.base_color = (0.9, 0.7, 0.1)  # Gold
        self.secondary_color = (0.85, 0.85, 0.9)  # Silver-white
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Sleeker cranium with sharper edges
        print("  Creating sleek cranium...")
        cranium = self._create_sleek_cranium()
        
        # Segmented faceplate
        print("  Creating segmented faceplate...")
        faceplate = self._create_segmented_faceplate()
        
        # Sleek jaw
        print("  Creating jaw...")
        jaw = self._create_sleek_jaw()
        
        # Compact ear pieces
        print("  Creating ear pieces...")
        left_ear = self._create_compact_ear('left')
        right_ear = self._create_compact_ear('right')
        
        # Combine
        print("  Combining parts...")
        helmet = trimesh.util.concatenate([cranium, faceplate, jaw, left_ear, right_ear])
        
        # Visor cutout
        print("  Creating visor...")
        helmet = self._create_visor_cutout(helmet)
        
        # Smooth
        helmet = self.subdivide_smooth(helmet, iterations=1)
        helmet = self._finalize_mesh(helmet)
        
        return helmet
    
    def _create_sleek_cranium(self) -> trimesh.Trimesh:
        """Sleeker cranium with sharper edges (lower n values)"""
        a = self.head_radius * 0.88  # narrower
        b = self.head_radius * 0.92
        c = self.head_radius * 1.0   # less tall
        
        # Lower n = sharper edges
        cranium = self.superellipsoid(a, b, c, n1=2.0, n2=2.0, resolution=56)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness)
        return cranium
    
    def _create_segmented_faceplate(self) -> trimesh.Trimesh:
        """Faceplate with panel-like segmentation"""
        # Main faceplate
        a = self.head_radius * 0.85
        b = self.head_radius * 0.25
        c = self.head_radius * 0.7
        
        faceplate = self.superellipsoid(a, b, c, n1=1.8, n2=2.2, resolution=40)
        faceplate.apply_translation([0, self.head_radius * 0.78, -self.head_radius * 0.05])
        
        # Add panel lines using thin boxes
        panels = [faceplate]
        
        # Vertical center line
        center_line = trimesh.creation.box([2, 4, 60])
        center_line.apply_translation([0, self.head_radius * 0.75, -self.head_radius * 0.05])
        panels.append(center_line)
        
        # Horizontal brow line
        brow_line = trimesh.creation.box([50, 4, 2])
        brow_line.apply_translation([0, self.head_radius * 0.75, self.head_radius * 0.2])
        panels.append(brow_line)
        
        faceplate = trimesh.util.concatenate(panels)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness)
        
        return faceplate
    
    def _create_sleek_jaw(self) -> trimesh.Trimesh:
        """More angular, sleek jaw"""
        jaw_profile = [
            (22, -25), (28, -40), (32, -55), (35, -70),
            (32, -80), (22, -85), (12, -80), (8, -70),
            (10, -55), (15, -40), (18, -25)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        jaw.apply_translation([0, self.head_radius * 0.38, self.head_radius * 0.12])
        jaw = self.create_hollow_shell(jaw, self.wall_thickness)
        return jaw
    
    def _create_compact_ear(self, side: str) -> trimesh.Trimesh:
        """Smaller, more integrated ear pieces"""
        pieces = []
        
        # Sleek ear housing
        ear_main = trimesh.creation.cylinder(radius=18, height=15, sections=20)
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        x_offset = self.head_radius * 0.86 if side == 'left' else -self.head_radius * 0.86
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.08])
        pieces.append(ear_main)
        
        # Subtle vent lines
        for i in range(2):
            vent = trimesh.creation.box([6, 2, 1])
            vent.apply_translation([x_offset, -3 + i*6, self.head_radius * 0.15])
            pieces.append(vent)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Sleek visor opening"""
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.35, theta_end=np.pi/2 + 0.35,
            phi_start=-0.55, phi_end=0.55,
            resolution=24
        )
        visor_cutter.apply_translation([0, self.head_radius * 0.25, self.head_radius * 0.18])
        
        try:
            result = trimesh.boolean.difference([helmet, visor_cutter])
            return result
        except:
            return helmet
    
    def _finalize_mesh(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        mesh.merge_vertices()
        mesh.remove_degenerate_faces()
        mesh.remove_unreferenced_vertices()
        if not mesh.is_watertight:
            mesh.fill_holes()
        return mesh


def main():
    generator = IronManMark42Helmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'ironman-mark42.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()
