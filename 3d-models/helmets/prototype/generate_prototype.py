#!/usr/bin/env python3
"""
Prototype Helmet Generator
Raw mechanical design with exposed hydraulics
Features industrial aesthetic with visible mechanics
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class PrototypeHelmet(IronManHelmetBase):
    """
    Prototype - Raw mechanical design
    Exposed hydraulics, industrial aesthetic
    Raw metal/unfinished look
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.02)
        self.name = "Prototype"
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Raw mechanical cranium
        print("  Creating mechanical cranium...")
        cranium = self._create_mechanical_cranium()
        
        # Exposed faceplate
        print("  Creating exposed faceplate...")
        faceplate = self._create_exposed_faceplate()
        
        # Hydraulic jaw
        print("  Creating hydraulic jaw...")
        jaw = self._create_hydraulic_jaw()
        
        # Mechanical ear pieces
        print("  Creating mechanical ear pieces...")
        left_ear = self._create_mechanical_ear('left')
        right_ear = self._create_mechanical_ear('right')
        
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
    
    def _create_mechanical_cranium(self) -> trimesh.Trimesh:
        """Raw mechanical cranium with exposed details"""
        # Angular industrial shape
        a = self.head_radius * 0.92
        b = self.head_radius * 0.95
        c = self.head_radius * 1.0
        
        cranium = self.superellipsoid(a, b, c, n1=1.9, n2=2.0, resolution=56)
        
        # Add mechanical details
        details = [cranium]
        
        # Exposed frame struts
        for angle in [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4]:
            strut = trimesh.creation.cylinder(radius=3, height=50, sections=8)
            strut.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, np.cos(angle), np.sin(angle)]))
            strut.apply_translation([
                np.cos(angle) * 35,
                np.sin(angle) * 35,
                self.head_radius * 0.5
            ])
            details.append(strut)
        
        # Top hydraulic cylinder
        hydraulic = trimesh.creation.cylinder(radius=8, height=35, sections=16)
        hydraulic.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        hydraulic.apply_translation([0, -10, self.head_radius * 0.85])
        details.append(hydraulic)
        
        # Bolt heads
        for i in range(8):
            angle = i * np.pi / 4
            bolt = trimesh.creation.cylinder(radius=4, height=6, sections=6)
            bolt.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            bolt.apply_translation([
                np.cos(angle) * 40,
                np.sin(angle) * 40,
                self.head_radius * 0.7
            ])
            details.append(bolt)
        
        cranium = trimesh.util.concatenate(details)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness * 1.3)
        return cranium
    
    def _create_exposed_faceplate(self) -> trimesh.Trimesh:
        """Faceplate with exposed mechanics"""
        # Main faceplate
        a = self.head_radius * 0.88
        b = self.head_radius * 0.28
        c = self.head_radius * 0.7
        
        faceplate = self.superellipsoid(a, b, c, n1=1.8, n2=2.0, resolution=40)
        faceplate.apply_translation([0, self.head_radius * 0.78, -self.head_radius * 0.05])
        
        # Add exposed details
        details = [faceplate]
        
        # Hydraulic pistons
        for side in [-1, 1]:
            piston = trimesh.creation.cylinder(radius=5, height=30, sections=12)
            piston.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
            piston.apply_translation([side * 25, self.head_radius * 0.8, self.head_radius * 0.15])
            details.append(piston)
            
            # Piston housing
            housing = trimesh.creation.cylinder(radius=8, height=15, sections=12)
            housing.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
            housing.apply_translation([side * 32, self.head_radius * 0.8, self.head_radius * 0.15])
            details.append(housing)
        
        # Center hydraulic
        center = trimesh.creation.cylinder(radius=6, height=25, sections=12)
        center.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        center.apply_translation([0, self.head_radius * 0.82, self.head_radius * 0.2])
        details.append(center)
        
        # Exposed wiring channels
        for z in [-15, 0, 15]:
            channel = trimesh.creation.box([40, 4, 6])
            channel.apply_translation([0, self.head_radius * 0.76, z])
            details.append(channel)
        
        faceplate = trimesh.util.concatenate(details)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness * 1.3)
        return faceplate
    
    def _create_hydraulic_jaw(self) -> trimesh.Trimesh:
        """Jaw with exposed hydraulics"""
        # Mechanical jaw profile
        jaw_profile = [
            (26, -30), (32, -46), (36, -64), (38, -80),
            (36, -92), (28, -98), (16, -92), (10, -80),
            (12, -64), (18, -46), (22, -30)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        jaw.apply_translation([0, self.head_radius * 0.42, self.head_radius * 0.1])
        
        # Add hydraulic details
        details = [jaw]
        
        # Side hydraulic cylinders
        for side in [-1, 1]:
            cylinder = trimesh.creation.cylinder(radius=6, height=25, sections=12)
            cylinder.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
            cylinder.apply_translation([side * 30, self.head_radius * 0.45, -self.head_radius * 0.3])
            details.append(cylinder)
            
            # Mount bracket
            bracket = trimesh.creation.box([12, 20, 8])
            bracket.apply_translation([side * 35, self.head_radius * 0.45, -self.head_radius * 0.3])
            details.append(bracket)
        
        # Chin hydraulic
        chin = trimesh.creation.cylinder(radius=10, height=20, sections=16)
        chin.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        chin.apply_translation([0, self.head_radius * 0.58, -self.head_radius * 0.7])
        details.append(chin)
        
        # Exposed bolts
        for side in [-1, 1]:
            for z in [-40, -20]:
                bolt = trimesh.creation.cylinder(radius=3, height=8, sections=6)
                bolt.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
                bolt.apply_translation([side * 28, self.head_radius * 0.48, z])
                details.append(bolt)
        
        jaw = trimesh.util.concatenate(details)
        jaw = self.create_hollow_shell(jaw, self.wall_thickness * 1.3)
        return jaw
    
    def _create_mechanical_ear(self, side: str) -> trimesh.Trimesh:
        """Ear pieces with exposed mechanics"""
        pieces = []
        x_offset = self.head_radius * 0.9 if side == 'left' else -self.head_radius * 0.9
        
        # Main housing - more industrial
        ear_main = trimesh.creation.cylinder(radius=22, height=20, sections=8)  # Octagonal
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.05])
        pieces.append(ear_main)
        
        # Exposed gears (simplified as cylinders)
        for i in range(3):
            gear = trimesh.creation.cylinder(radius=8 - i*2, height=4, sections=12)
            gear.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            gear.apply_translation([x_offset, -8 + i*8, self.head_radius * 0.15])
            pieces.append(gear)
        
        # Hydraulic line
        line = trimesh.creation.cylinder(radius=3, height=40, sections=8)
        line.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
        line.apply_translation([x_offset + (10 if side == 'left' else -10), 0, self.head_radius * 0.12])
        pieces.append(line)
        
        # Mount bolts
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            bolt = trimesh.creation.cylinder(radius=2.5, height=6, sections=6)
            bolt.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
            bolt.apply_translation([
                x_offset + np.cos(angle) * 18,
                np.sin(angle) * 18,
                self.head_radius * 0.15
            ])
            pieces.append(bolt)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness * 1.3)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Prototype visor shape"""
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.4, theta_end=np.pi/2 + 0.4,
            phi_start=-0.6, phi_end=0.6,
            resolution=24
        )
        visor_cutter.apply_translation([0, self.head_radius * 0.25, self.head_radius * 0.15])
        
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
    generator = PrototypeHelmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'prototype.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()
