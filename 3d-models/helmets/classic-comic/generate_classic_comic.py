#!/usr/bin/env python3
"""
Classic Comic Iron Man Helmet Generator
Retro rounded design inspired by classic comics
Features smooth curves and vintage styling
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class ClassicComicHelmet(IronManHelmetBase):
    """
    Classic Comic - Retro rounded design
    Smooth curves, vintage aesthetic
    Classic red/yellow color scheme
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.0)
        self.name = "Classic Comic Iron Man"
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Retro rounded cranium
        print("  Creating retro cranium...")
        cranium = self._create_retro_cranium()
        
        # Classic faceplate
        print("  Creating classic faceplate...")
        faceplate = self._create_classic_faceplate()
        
        # Rounded jaw
        print("  Creating rounded jaw...")
        jaw = self._create_rounded_jaw()
        
        # Simple ear pieces
        print("  Creating ear pieces...")
        left_ear = self._create_simple_ear('left')
        right_ear = self._create_simple_ear('right')
        
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
    
    def _create_retro_cranium(self) -> trimesh.Trimesh:
        """Very rounded retro cranium"""
        # Very round shape
        a = self.head_radius * 0.94
        b = self.head_radius * 0.96
        c = self.head_radius * 1.0
        
        # High n values for very round shape
        cranium = self.superellipsoid(a, b, c, n1=3.0, n2=3.0, resolution=56)
        
        # Add retro fin detail
        details = [cranium]
        
        # Classic fin on top
        fin = trimesh.creation.cylinder(radius=6, height=40, sections=12)
        fin.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        fin.apply_translation([0, -5, self.head_radius * 0.88])
        details.append(fin)
        
        cranium = trimesh.util.concatenate(details)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness)
        return cranium
    
    def _create_classic_faceplate(self) -> trimesh.Trimesh:
        """Classic rounded faceplate"""
        # Very rounded
        a = self.head_radius * 0.9
        b = self.head_radius * 0.32
        c = self.head_radius * 0.7
        
        faceplate = self.superellipsoid(a, b, c, n1=2.8, n2=3.0, resolution=40)
        faceplate.apply_translation([0, self.head_radius * 0.76, -self.head_radius * 0.05])
        
        # Add classic details
        details = [faceplate]
        
        # Simple brow ridge
        brow = trimesh.creation.cylinder(radius=4, height=50, sections=12)
        brow.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        brow.apply_translation([0, self.head_radius * 0.78, self.head_radius * 0.2])
        details.append(brow)
        
        faceplate = trimesh.util.concatenate(details)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness)
        return faceplate
    
    def _create_rounded_jaw(self) -> trimesh.Trimesh:
        """Very rounded jaw"""
        # Smooth rounded profile
        jaw_profile = [
            (28, -32), (32, -45), (36, -58), (38, -72),
            (36, -82), (28, -88), (18, -82), (12, -72),
            (14, -58), (18, -45), (22, -32)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        jaw.apply_translation([0, self.head_radius * 0.4, self.head_radius * 0.1])
        
        # Add rounded chin
        details = [jaw]
        
        chin = trimesh.creation.cylinder(radius=20, height=10, sections=20)
        chin.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        chin.apply_translation([0, self.head_radius * 0.5, -self.head_radius * 0.6])
        details.append(chin)
        
        jaw = trimesh.util.concatenate(details)
        jaw = self.create_hollow_shell(jaw, self.wall_thickness)
        return jaw
    
    def _create_simple_ear(self, side: str) -> trimesh.Trimesh:
        """Simple rounded ear pieces"""
        pieces = []
        x_offset = self.head_radius * 0.9 if side == 'left' else -self.head_radius * 0.9
        
        # Simple rounded housing
        ear_main = trimesh.creation.cylinder(radius=20, height=16, sections=24)
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.05])
        pieces.append(ear_main)
        
        # Simple ring
        ring = trimesh.creation.cylinder(radius=22, height=4, sections=24)
        ring.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ring.apply_translation([x_offset, 0, self.head_radius * 0.1])
        pieces.append(ring)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Classic rounded visor"""
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.4, theta_end=np.pi/2 + 0.4,
            phi_start=-0.6, phi_end=0.6,
            resolution=24
        )
        visor_cutter.apply_translation([0, self.head_radius * 0.25, self.head_radius * 0.12])
        
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
    generator = ClassicComicHelmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'classic-comic.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()
