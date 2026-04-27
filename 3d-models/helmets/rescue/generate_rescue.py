#!/usr/bin/env python3
"""
Rescue (Pepper Potts) Helmet Generator
Sleek feminine design with blue/silver color scheme
Features elegant curves and refined proportions
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class RescueHelmet(IronManHelmetBase):
    """
    Rescue - Pepper Potts' suit helmet
    Sleek feminine design, elegant curves
    Blue/silver color scheme
    """
    
    def __init__(self):
        super().__init__(scale_factor=0.92)  # Slightly smaller
        self.name = "Rescue"
        self.base_color = (0.1, 0.4, 0.8)  # Blue
        self.accent_color = (0.85, 0.9, 0.95)  # Silver-white
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Elegant cranium
        print("  Creating elegant cranium...")
        cranium = self._create_elegant_cranium()
        
        # Refined faceplate
        print("  Creating refined faceplate...")
        faceplate = self._create_refined_faceplate()
        
        # Sleek jaw
        print("  Creating sleek jaw...")
        jaw = self._create_sleek_jaw()
        
        # Elegant ear pieces
        print("  Creating ear pieces...")
        left_ear = self._create_elegant_ear('left')
        right_ear = self._create_elegant_ear('right')
        
        # Combine
        print("  Combining parts...")
        helmet = trimesh.util.concatenate([cranium, faceplate, jaw, left_ear, right_ear])
        
        # Visor
        print("  Creating visor...")
        helmet = self._create_visor_cutout(helmet)
        
        # Smooth and finalize
        helmet = self.subdivide_smooth(helmet, iterations=1)
        helmet = self._finalize_mesh(helmet)
        
        return helmet
    
    def _create_elegant_cranium(self) -> trimesh.Trimesh:
        """Elegant, sleek cranium with refined curves"""
        # More elongated, graceful shape
        a = self.head_radius * 0.85  # narrower
        b = self.head_radius * 0.88
        c = self.head_radius * 1.0   # proportional height
        
        # Higher n for smoother curves
        cranium = self.superellipsoid(a, b, c, n1=2.6, n2=2.5, resolution=56)
        
        # Add elegant details
        details = [cranium]
        
        # Subtle crown detail
        crown = trimesh.creation.cylinder(radius=8, height=25, sections=16)
        crown.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        crown.apply_translation([0, -8, self.head_radius * 0.85])
        details.append(crown)
        
        cranium = trimesh.util.concatenate(details)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness)
        return cranium
    
    def _create_refined_faceplate(self) -> trimesh.Trimesh:
        """Refined, elegant faceplate"""
        # Sleeker faceplate
        a = self.head_radius * 0.82
        b = self.head_radius * 0.22
        c = self.head_radius * 0.68
        
        faceplate = self.superellipsoid(a, b, c, n1=2.4, n2=2.6, resolution=40)
        faceplate.apply_translation([0, self.head_radius * 0.75, -self.head_radius * 0.05])
        
        # Add elegant details
        details = [faceplate]
        
        # Delicate brow line
        brow = trimesh.creation.box([45, 3, 3])
        brow.apply_translation([0, self.head_radius * 0.76, self.head_radius * 0.22])
        details.append(brow)
        
        # Subtle cheek accents
        for side in [-1, 1]:
            accent = trimesh.creation.cylinder(radius=6, height=4, sections=16)
            accent.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            accent.apply_translation([side * 25, self.head_radius * 0.72, -self.head_radius * 0.15])
            details.append(accent)
        
        faceplate = trimesh.util.concatenate(details)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness)
        return faceplate
    
    def _create_sleek_jaw(self) -> trimesh.Trimesh:
        """Sleek, refined jaw"""
        # More tapered jaw profile
        jaw_profile = [
            (20, -22), (25, -35), (30, -50), (32, -65),
            (30, -75), (22, -80), (14, -75), (10, -65),
            (10, -50), (14, -35), (16, -22)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        jaw.apply_translation([0, self.head_radius * 0.38, self.head_radius * 0.12])
        
        # Add subtle details
        details = [jaw]
        
        # Refined chin
        chin = trimesh.creation.cylinder(radius=12, height=6, sections=16)
        chin.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        chin.apply_translation([0, self.head_radius * 0.45, -self.head_radius * 0.55])
        details.append(chin)
        
        jaw = trimesh.util.concatenate(details)
        jaw = self.create_hollow_shell(jaw, self.wall_thickness)
        return jaw
    
    def _create_elegant_ear(self, side: str) -> trimesh.Trimesh:
        """Elegant, compact ear pieces"""
        pieces = []
        x_offset = self.head_radius * 0.85 if side == 'left' else -self.head_radius * 0.85
        
        # Sleek housing
        ear_main = trimesh.creation.cylinder(radius=16, height=12, sections=20)
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.08])
        pieces.append(ear_main)
        
        # Elegant ring
        ring = trimesh.creation.cylinder(radius=18, height=3, sections=20)
        ring.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ring.apply_translation([x_offset, 0, self.head_radius * 0.12])
        pieces.append(ring)
        
        # Subtle detail dots
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            dot = trimesh.creation.cylinder(radius=1.5, height=2, sections=8)
            dot.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            dot.apply_translation([
                x_offset + np.cos(angle) * 12,
                np.sin(angle) * 12,
                self.head_radius * 0.14
            ])
            pieces.append(dot)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Elegant visor shape"""
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.32, theta_end=np.pi/2 + 0.32,
            phi_start=-0.5, phi_end=0.5,
            resolution=24
        )
        visor_cutter.apply_translation([0, self.head_radius * 0.28, self.head_radius * 0.2])
        
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
    generator = RescueHelmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'rescue.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()
