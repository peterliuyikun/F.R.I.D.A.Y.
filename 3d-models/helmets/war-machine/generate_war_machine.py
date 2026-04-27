#!/usr/bin/env python3
"""
War Machine Helmet Generator
Military heavy armor with weapon mounts and tactical design
Features angular, aggressive styling with heavy plating
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class WarMachineHelmet(IronManHelmetBase):
    """
    War Machine - Military heavy armor variant
    Angular design, weapon mounts, tactical aesthetic
    Dark grey/silver color scheme
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.05)  # Slightly larger
        self.name = "War Machine"
        self.base_color = (0.25, 0.25, 0.3)  # Dark grey
        self.accent_color = (0.5, 0.5, 0.55)  # Silver
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Heavy armored cranium
        print("  Creating armored cranium...")
        cranium = self._create_armored_cranium()
        
        # Tactical faceplate
        print("  Creating tactical faceplate...")
        faceplate = self._create_tactical_faceplate()
        
        # Heavy jaw
        print("  Creating heavy jaw...")
        jaw = self._create_heavy_jaw()
        
        # Weapon mount ear pieces
        print("  Creating weapon mount ears...")
        left_ear = self._create_weapon_ear('left')
        right_ear = self._create_weapon_ear('right')
        
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
    
    def _create_armored_cranium(self) -> trimesh.Trimesh:
        """Heavy armored cranium with plating details"""
        # More angular, heavy shape
        a = self.head_radius * 0.95
        b = self.head_radius * 0.98
        c = self.head_radius * 1.05
        
        # Lower n for more angular shape
        cranium = self.superellipsoid(a, b, c, n1=1.8, n2=1.9, resolution=56)
        
        # Add armor plating details
        details = [cranium]
        
        # Top plate ridge
        top_plate = trimesh.creation.box([40, 60, 8])
        top_plate.apply_translation([0, -10, self.head_radius * 0.95])
        details.append(top_plate)
        
        # Side armor plates
        for side in [-1, 1]:
            side_plate = trimesh.creation.box([8, 50, 35])
            side_plate.apply_translation([side * 45, -5, self.head_radius * 0.3])
            details.append(side_plate)
            
            # Bolt details
            for z in [-10, 0, 10]:
                for y in [-15, 15]:
                    bolt = trimesh.creation.cylinder(radius=2, height=6, sections=8)
                    bolt.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
                    bolt.apply_translation([side * 50, y, self.head_radius * 0.3 + z])
                    details.append(bolt)
        
        cranium = trimesh.util.concatenate(details)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness * 1.2)  # Thicker walls
        return cranium
    
    def _create_tactical_faceplate(self) -> trimesh.Trimesh:
        """Aggressive tactical faceplate"""
        # Angular faceplate
        a = self.head_radius * 0.9
        b = self.head_radius * 0.35
        c = self.head_radius * 0.7
        
        faceplate = self.superellipsoid(a, b, c, n1=1.7, n2=2.0, resolution=40)
        faceplate.apply_translation([0, self.head_radius * 0.8, -self.head_radius * 0.05])
        
        # Add tactical details
        details = [faceplate]
        
        # Brow ridge
        brow = trimesh.creation.box([60, 8, 6])
        brow.apply_translation([0, self.head_radius * 0.82, self.head_radius * 0.25])
        details.append(brow)
        
        # Cheek guards
        for side in [-1, 1]:
            cheek = trimesh.creation.box([12, 20, 25])
            cheek.apply_translation([side * 35, self.head_radius * 0.75, -self.head_radius * 0.15])
            details.append(cheek)
        
        faceplate = trimesh.util.concatenate(details)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness * 1.2)
        return faceplate
    
    def _create_heavy_jaw(self) -> trimesh.Trimesh:
        """Heavy reinforced jaw"""
        # More angular jaw profile
        jaw_profile = [
            (28, -32), (35, -48), (40, -65), (42, -80),
            (40, -92), (30, -98), (18, -92), (12, -80),
            (14, -65), (20, -48), (24, -32)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        jaw.apply_translation([0, self.head_radius * 0.42, self.head_radius * 0.08])
        
        # Add reinforcement details
        details = [jaw]
        
        # Chin guard
        chin = trimesh.creation.box([30, 15, 12])
        chin.apply_translation([0, self.head_radius * 0.55, -self.head_radius * 0.65])
        details.append(chin)
        
        # Side reinforcements
        for side in [-1, 1]:
            reinforce = trimesh.creation.box([8, 25, 30])
            reinforce.apply_translation([side * 32, self.head_radius * 0.45, -self.head_radius * 0.25])
            details.append(reinforce)
        
        jaw = trimesh.util.concatenate(details)
        jaw = self.create_hollow_shell(jaw, self.wall_thickness * 1.2)
        return jaw
    
    def _create_weapon_ear(self, side: str) -> trimesh.Trimesh:
        """Ear pieces with weapon mount capability"""
        pieces = []
        x_offset = self.head_radius * 0.92 if side == 'left' else -self.head_radius * 0.92
        
        # Main housing - larger and more industrial
        ear_main = trimesh.creation.cylinder(radius=24, height=22, sections=24)
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.05])
        pieces.append(ear_main)
        
        # Weapon mount rail
        rail = trimesh.creation.box([12, 35, 8])
        rail.apply_translation([x_offset, -10, self.head_radius * 0.18])
        pieces.append(rail)
        
        # Mount points
        for y in [-20, 0, 15]:
            mount = trimesh.creation.cylinder(radius=3, height=10, sections=8)
            mount.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            mount.apply_translation([x_offset, y, self.head_radius * 0.22])
            pieces.append(mount)
        
        # Back exhaust port
        exhaust = trimesh.creation.cylinder(radius=16, height=12, sections=20)
        exhaust.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        exhaust.apply_translation([x_offset, -self.head_radius * 0.15, self.head_radius * 0.05])
        pieces.append(exhaust)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness * 1.2)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Tactical visor shape"""
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
    generator = WarMachineHelmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'war-machine.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()