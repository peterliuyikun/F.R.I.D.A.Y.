#!/usr/bin/env python3
"""
Iron Man Mark 85 Helmet Generator
Avengers Endgame design - Complex geometry with nanotech aesthetic
Features intricate surface details and advanced curves
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class IronManMark85Helmet(IronManHelmetBase):
    """
    Mark 85 - Nanotech suit from Avengers: Endgame
    Complex organic curves with tech details
    Red/gold/silver color scheme
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.0)
        self.name = "Iron Man Mark 85"
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Complex organic cranium
        print("  Creating nanotech cranium...")
        cranium = self._create_nanotech_cranium()
        
        # Advanced faceplate
        print("  Creating faceplate...")
        faceplate = self._create_advanced_faceplate()
        
        # Articulated jaw
        print("  Creating articulated jaw...")
        jaw = self._create_articulated_jaw()
        
        # Tech ear pieces
        print("  Creating ear pieces...")
        left_ear = self._create_tech_ear('left')
        right_ear = self._create_tech_ear('right')
        
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
    
    def _create_nanotech_cranium(self) -> trimesh.Trimesh:
        """Organic nanotech-style cranium"""
        # More organic shape with varied n values
        a = self.head_radius * 0.9
        b = self.head_radius * 0.94
        c = self.head_radius * 1.03
        
        # Varied exponents for organic feel
        cranium = self.superellipsoid(a, b, c, n1=2.4, n2=2.1, resolution=60)
        
        # Add surface tech details
        details = [cranium]
        
        # Ridge along top
        for i in range(5):
            ridge = trimesh.creation.cylinder(radius=3, height=30 - i*4, sections=12)
            ridge.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
            ridge.apply_translation([0, -15 + i*8, self.head_radius * 0.9 + i*2])
            details.append(ridge)
        
        cranium = trimesh.util.concatenate(details)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness)
        return cranium
    
    def _create_advanced_faceplate(self) -> trimesh.Trimesh:
        """Complex faceplate with nanotech details"""
        # Main faceplate
        a = self.head_radius * 0.87
        b = self.head_radius * 0.28
        c = self.head_radius * 0.72
        
        faceplate = self.superellipsoid(a, b, c, n1=2.2, n2=2.0, resolution=44)
        faceplate.apply_translation([0, self.head_radius * 0.76, -self.head_radius * 0.08])
        
        # Add nanotech surface pattern
        details = [faceplate]
        
        # Hex pattern simulation (simplified as small cylinders)
        for row in range(-2, 3):
            for col in range(-3, 4):
                if abs(row) + abs(col) <= 4:
                    hex_dot = trimesh.creation.cylinder(radius=2, height=1, sections=6)
                    hex_dot.apply_translation([
                        col * 8, 
                        self.head_radius * 0.78, 
                        row * 8 + self.head_radius * 0.1
                    ])
                    details.append(hex_dot)
        
        faceplate = trimesh.util.concatenate(details)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness)
        return faceplate
    
    def _create_articulated_jaw(self) -> trimesh.Trimesh:
        """Jaw with visible articulation points"""
        jaw_profile = [
            (24, -28), (30, -42), (34, -58), (36, -72),
            (34, -82), (26, -88), (16, -82), (10, -72),
            (12, -58), (16, -42), (20, -28)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=52)
        jaw.apply_translation([0, self.head_radius * 0.4, self.head_radius * 0.1])
        
        # Add articulation points
        details = [jaw]
        
        # Side hinges
        for side in [-1, 1]:
            hinge = trimesh.creation.cylinder(radius=4, height=8, sections=16)
            hinge.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            hinge.apply_translation([side * 32, self.head_radius * 0.35, -self.head_radius * 0.1])
            details.append(hinge)
        
        jaw = trimesh.util.concatenate(details)
        jaw = self.create_hollow_shell(jaw, self.wall_thickness)
        return jaw
    
    def _create_tech_ear(self, side: str) -> trimesh.Trimesh:
        """High-tech ear pieces with nanotech aesthetic"""
        pieces = []
        x_offset = self.head_radius * 0.9 if side == 'left' else -self.head_radius * 0.9
        
        # Main housing
        ear_main = trimesh.creation.cylinder(radius=20, height=18, sections=24)
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.06])
        pieces.append(ear_main)
        
        # Tech ring detail
        ring = trimesh.creation.cylinder(radius=22, height=4, sections=24)
        ring.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ring.apply_translation([x_offset, 0, self.head_radius * 0.12])
        pieces.append(ring)
        
        # LED-like dots
        for angle in [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]:
            dot = trimesh.creation.cylinder(radius=2, height=3, sections=8)
            dot.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            dot.apply_translation([
                x_offset + np.cos(angle) * 15,
                np.sin(angle) * 15,
                self.head_radius * 0.15
            ])
            pieces.append(dot)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Advanced visor shape"""
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.38, theta_end=np.pi/2 + 0.38,
            phi_start=-0.58, phi_end=0.58,
            resolution=28
        )
        visor_cutter.apply_translation([0, self.head_radius * 0.22, self.head_radius * 0.16])
        
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
    generator = IronManMark85Helmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'ironman-mark85.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()
