#!/usr/bin/env python3
"""
Hulkbuster Helmet Generator
Massive, heavy industrial design
Features extreme proportions and heavy armor plating
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class HulkbusterHelmet(IronManHelmetBase):
    """
    Hulkbuster - Massive heavy industrial design
    Extreme proportions, heavy armor
    Industrial yellow/red color scheme
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.25)  # Much larger
        self.name = "Hulkbuster"
        self.wall_thickness = 4.0  # Much thicker walls
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Massive armored cranium
        print("  Creating massive cranium...")
        cranium = self._create_massive_cranium()
        
        # Heavy faceplate
        print("  Creating heavy faceplate...")
        faceplate = self._create_heavy_faceplate()
        
        # Industrial jaw
        print("  Creating industrial jaw...")
        jaw = self._create_industrial_jaw()
        
        # Massive ear pieces
        print("  Creating massive ear pieces...")
        left_ear = self._create_massive_ear('left')
        right_ear = self._create_massive_ear('right')
        
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
    
    def _create_massive_cranium(self) -> trimesh.Trimesh:
        """Massive heavy armored cranium"""
        # Much larger proportions
        a = self.head_radius * 0.98
        b = self.head_radius * 1.0
        c = self.head_radius * 1.08
        
        # Angular heavy shape
        cranium = self.superellipsoid(a, b, c, n1=1.7, n2=1.8, resolution=64)
        
        # Add massive armor details
        details = [cranium]
        
        # Heavy top plate
        top_plate = trimesh.creation.box([60, 80, 15])
        top_plate.apply_translation([0, -10, self.head_radius * 0.95])
        details.append(top_plate)
        
        # Armor ridges
        for i in range(3):
            ridge = trimesh.creation.box([50 - i*10, 70 - i*15, 10])
            ridge.apply_translation([0, -8, self.head_radius * 0.85 - i*8])
            details.append(ridge)
        
        # Side armor plates
        for side in [-1, 1]:
            # Main side plate
            side_plate = trimesh.creation.box([15, 60, 50])
            side_plate.apply_translation([side * 55, -5, self.head_radius * 0.2])
            details.append(side_plate)
            
            # Secondary plate
            sec_plate = trimesh.creation.box([10, 45, 40])
            sec_plate.apply_translation([side * 68, -5, self.head_radius * 0.15])
            details.append(sec_plate)
            
            # Large bolts
            for z in [-15, 0, 15]:
                for y in [-20, 20]:
                    bolt = trimesh.creation.cylinder(radius=5, height=12, sections=8)
                    bolt.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
                    bolt.apply_translation([side * 62, y, self.head_radius * 0.2 + z])
                    details.append(bolt)
        
        # Rear exhaust ports
        for side in [-1, 1]:
            exhaust = trimesh.creation.cylinder(radius=15, height=20, sections=16)
            exhaust.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
            exhaust.apply_translation([side * 50, -self.head_radius * 0.4, self.head_radius * 0.3])
            details.append(exhaust)
        
        cranium = trimesh.util.concatenate(details)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness)
        return cranium
    
    def _create_heavy_faceplate(self) -> trimesh.Trimesh:
        """Heavy industrial faceplate"""
        # Massive faceplate
        a = self.head_radius * 0.94
        b = self.head_radius * 0.4
        c = self.head_radius * 0.75
        
        faceplate = self.superellipsoid(a, b, c, n1=1.6, n2=1.9, resolution=48)
        faceplate.apply_translation([0, self.head_radius * 0.85, -self.head_radius * 0.05])
        
        # Add heavy details
        details = [faceplate]
        
        # Massive brow ridge
        brow = trimesh.creation.box([80, 12, 12])
        brow.apply_translation([0, self.head_radius * 0.88, self.head_radius * 0.28])
        details.append(brow)
        
        # Heavy cheek guards
        for side in [-1, 1]:
            cheek = trimesh.creation.box([20, 30, 40])
            cheek.apply_translation([side * 45, self.head_radius * 0.8, -self.head_radius * 0.1])
            details.append(cheek)
            
            # Secondary cheek
            sec_cheek = trimesh.creation.box([15, 25, 35])
            sec_cheek.apply_translation([side * 58, self.head_radius * 0.78, -self.head_radius * 0.08])
            details.append(sec_cheek)
        
        # Center reinforcement
        center = trimesh.creation.box([20, 35, 50])
        center.apply_translation([0, self.head_radius * 0.82, -self.head_radius * 0.05])
        details.append(center)
        
        faceplate = trimesh.util.concatenate(details)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness)
        return faceplate
    
    def _create_industrial_jaw(self) -> trimesh.Trimesh:
        """Massive industrial jaw"""
        # Heavy jaw profile
        jaw_profile = [
            (32, -35), (40, -52), (46, -72), (48, -92),
            (46, -105), (36, -112), (22, -105), (14, -92),
            (16, -72), (22, -52), (28, -35)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=56)
        jaw.apply_translation([0, self.head_radius * 0.48, self.head_radius * 0.1])
        
        # Add industrial details
        details = [jaw]
        
        # Massive chin guard
        chin = trimesh.creation.box([45, 25, 18])
        chin.apply_translation([0, self.head_radius * 0.65, -self.head_radius * 0.75])
        details.append(chin)
        
        # Side reinforcements
        for side in [-1, 1]:
            reinforce = trimesh.creation.box([15, 35, 45])
            reinforce.apply_translation([side * 40, self.head_radius * 0.55, -self.head_radius * 0.3])
            details.append(reinforce)
            
            # Hydraulic cylinders
            cylinder = trimesh.creation.cylinder(radius=10, height=35, sections=16)
            cylinder.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
            cylinder.apply_translation([side * 48, self.head_radius * 0.5, -self.head_radius * 0.35])
            details.append(cylinder)
        
        # Bottom vent
        vent = trimesh.creation.box([30, 20, 8])
        vent.apply_translation([0, self.head_radius * 0.72, -self.head_radius * 0.9])
        details.append(vent)
        
        jaw = trimesh.util.concatenate(details)
        jaw = self.create_hollow_shell(jaw, self.wall_thickness)
        return jaw
    
    def _create_massive_ear(self, side: str) -> trimesh.Trimesh:
        """Massive industrial ear pieces"""
        pieces = []
        x_offset = self.head_radius * 0.95 if side == 'left' else -self.head_radius * 0.95
        
        # Massive housing
        ear_main = trimesh.creation.cylinder(radius=30, height=28, sections=24)
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.05])
        pieces.append(ear_main)
        
        # Outer ring
        ring = trimesh.creation.cylinder(radius=35, height=8, sections=24)
        ring.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ring.apply_translation([x_offset, 0, self.head_radius * 0.15])
        pieces.append(ring)
        
        # Heavy mount plate
        mount = trimesh.creation.box([20, 50, 40])
        mount.apply_translation([x_offset + (15 if side == 'left' else -15), 0, self.head_radius * 0.1])
        pieces.append(mount)
        
        # Large bolts
        for angle in [0, np.pi/3, 2*np.pi/3, np.pi, 4*np.pi/3, 5*np.pi/3]:
            bolt = trimesh.creation.cylinder(radius=5, height=15, sections=8)
            bolt.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            bolt.apply_translation([
                x_offset + (np.cos(angle) * 25),
                np.sin(angle) * 25,
                self.head_radius * 0.2
            ])
            pieces.append(bolt)
        
        # Rear exhaust
        exhaust = trimesh.creation.cylinder(radius=20, height=18, sections=20)
        exhaust.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        exhaust.apply_translation([x_offset, -self.head_radius * 0.2, self.head_radius * 0.05])
        pieces.append(exhaust)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Heavy visor shape"""
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.45, theta_end=np.pi/2 + 0.45,
            phi_start=-0.65, phi_end=0.65,
            resolution=28
        )
        visor_cutter.apply_translation([0, self.head_radius * 0.3, self.head_radius * 0.1])
        
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
    generator = HulkbusterHelmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'hulkbuster.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()
