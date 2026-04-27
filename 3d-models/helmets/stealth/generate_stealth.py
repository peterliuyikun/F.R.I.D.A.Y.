#!/usr/bin/env python3
"""
Stealth Mode Helmet Generator
Matte black, angular, tactical design
Features stealth aesthetics with sharp angles
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class StealthHelmet(IronManHelmetBase):
    """
    Stealth Mode - Matte black tactical design
    Angular, aggressive styling
    Low visibility features
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.0)
        self.name = "Stealth Mode"
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Angular stealth cranium
        print("  Creating stealth cranium...")
        cranium = self._create_stealth_cranium()
        
        # Angular faceplate
        print("  Creating angular faceplate...")
        faceplate = self._create_angular_faceplate()
        
        # Sharp jaw
        print("  Creating sharp jaw...")
        jaw = self._create_sharp_jaw()
        
        # Stealth ear pieces
        print("  Creating stealth ear pieces...")
        left_ear = self._create_stealth_ear('left')
        right_ear = self._create_stealth_ear('right')
        
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
    
    def _create_stealth_cranium(self) -> trimesh.Trimesh:
        """Angular stealth cranium"""
        # Angular shape
        a = self.head_radius * 0.9
        b = self.head_radius * 0.93
        c = self.head_radius * 1.0
        
        # Low n for angular shape
        cranium = self.superellipsoid(a, b, c, n1=1.6, n2=1.7, resolution=56)
        
        # Add angular details
        details = [cranium]
        
        # Ridge spikes
        for i in range(3):
            spike = trimesh.creation.cone(radius=5, height=15, sections=6)
            spike.apply_translation([0, -15 + i*15, self.head_radius * 0.9])
            details.append(spike)
        
        # Side angular plates
        for side in [-1, 1]:
            plate = trimesh.creation.box([10, 40, 30])
            plate.apply_transform(trimesh.transformations.rotation_matrix(side * 0.2, [0, 0, 1]))
            plate.apply_translation([side * 48, -5, self.head_radius * 0.2])
            details.append(plate)
        
        cranium = trimesh.util.concatenate(details)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness)
        return cranium
    
    def _create_angular_faceplate(self) -> trimesh.Trimesh:
        """Very angular faceplate"""
        # Sharp angles
        a = self.head_radius * 0.86
        b = self.head_radius * 0.3
        c = self.head_radius * 0.68
        
        faceplate = self.superellipsoid(a, b, c, n1=1.5, n2=1.8, resolution=40)
        faceplate.apply_translation([0, self.head_radius * 0.8, -self.head_radius * 0.03])
        
        # Add angular details
        details = [faceplate]
        
        # Sharp brow
        brow = trimesh.creation.box([55, 6, 8])
        brow.apply_translation([0, self.head_radius * 0.82, self.head_radius * 0.25])
        details.append(brow)
        
        # Cheek angles
        for side in [-1, 1]:
            cheek = trimesh.creation.box([15, 25, 30])
            cheek.apply_transform(trimesh.transformations.rotation_matrix(side * 0.15, [0, 0, 1]))
            cheek.apply_translation([side * 38, self.head_radius * 0.75, -self.head_radius * 0.1])
            details.append(cheek)
        
        faceplate = trimesh.util.concatenate(details)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness)
        return faceplate
    
    def _create_sharp_jaw(self) -> trimesh.Trimesh:
        """Sharp angular jaw"""
        # Angular profile
        jaw_profile = [
            (24, -28), (30, -45), (34, -62), (36, -78),
            (34, -90), (26, -95), (14, -90), (8, -78),
            (10, -62), (16, -45), (20, -28)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        jaw.apply_translation([0, self.head_radius * 0.42, self.head_radius * 0.1])
        
        # Add sharp details
        details = [jaw]
        
        # Chin spike
        chin_spike = trimesh.creation.cone(radius=8, height=12, sections=6)
        chin_spike.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        chin_spike.apply_translation([0, self.head_radius * 0.55, -self.head_radius * 0.7])
        details.append(chin_spike)
        
        jaw = trimesh.util.concatenate(details)
        jaw = self.create_hollow_shell(jaw, self.wall_thickness)
        return jaw
    
    def _create_stealth_ear(self, side: str) -> trimesh.Trimesh:
        """Stealth angular ear pieces"""
        pieces = []
        x_offset = self.head_radius * 0.88 if side == 'left' else -self.head_radius * 0.88
        
        # Angular housing
        ear_main = trimesh.creation.cylinder(radius=18, height=14, sections=6)  # Hexagonal
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.08])
        pieces.append(ear_main)
        
        # Stealth vents (slits)
        for i in range(3):
            vent = trimesh.creation.box([20, 2, 1])
            vent.apply_translation([x_offset, -4 + i*4, self.head_radius * 0.15])
            pieces.append(vent)
        
        # Back detail
        back = trimesh.creation.cone(radius=12, height=10, sections=6)
        back.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        back.apply_translation([x_offset, -self.head_radius * 0.1, self.head_radius * 0.05])
        pieces.append(back)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Stealth visor shape"""
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.35, theta_end=np.pi/2 + 0.35,
            phi_start=-0.55, phi_end=0.55,
            resolution=24
        )
        visor_cutter.apply_translation([0, self.head_radius * 0.28, self.head_radius * 0.18])
        
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
    generator = StealthHelmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'stealth.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()
