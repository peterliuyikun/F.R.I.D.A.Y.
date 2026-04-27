#!/usr/bin/env python3
"""
Iron Patriot Helmet Generator
Red/white/blue patriotic theme with star details
Features bold patriotic styling
"""

import numpy as np
import trimesh
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class IronPatriotHelmet(IronManHelmetBase):
    """
    Iron Patriot - Patriotic variant
    Red/white/blue color scheme
    Star and stripe details
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.0)
        self.name = "Iron Patriot"
        
    def generate(self) -> trimesh.Trimesh:
        print(f"Generating {self.name} helmet...")
        
        # Patriotic cranium
        print("  Creating patriotic cranium...")
        cranium = self._create_patriotic_cranium()
        
        # Patriotic faceplate
        print("  Creating patriotic faceplate...")
        faceplate = self._create_patriotic_faceplate()
        
        # Bold jaw
        print("  Creating bold jaw...")
        jaw = self._create_bold_jaw()
        
        # Patriotic ear pieces
        print("  Creating ear pieces...")
        left_ear = self._create_patriotic_ear('left')
        right_ear = self._create_patriotic_ear('right')
        
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
    
    def _create_patriotic_cranium(self) -> trimesh.Trimesh:
        """Cranium with patriotic styling"""
        a = self.head_radius * 0.93
        b = self.head_radius * 0.96
        c = self.head_radius * 1.02
        
        cranium = self.superellipsoid(a, b, c, n1=2.2, n2=2.2, resolution=56)
        
        # Add patriotic details
        details = [cranium]
        
        # Star detail on top
        star = self._create_star(12, 5)
        star.apply_translation([0, -8, self.head_radius * 0.92])
        details.append(star)
        
        # Stripe details on sides
        for i, side in enumerate([-1, 1]):
            for z in [-20, 0, 20]:
                stripe = trimesh.creation.box([6, 30, 8])
                stripe.apply_translation([side * 45, -5, z])
                details.append(stripe)
        
        cranium = trimesh.util.concatenate(details)
        cranium = self.create_hollow_shell(cranium, self.wall_thickness)
        return cranium
    
    def _create_star(self, outer_radius: float, inner_radius: float) -> trimesh.Trimesh:
        """Create a 3D star shape"""
        vertices = []
        faces = []
        
        # Create star points
        num_points = 5
        height = 4
        
        for i in range(num_points * 2):
            angle = np.pi * i / num_points
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            
            # Top and bottom vertices
            vertices.append([x, y, height/2])
            vertices.append([x, y, -height/2])
        
        # Center vertices
        vertices.append([0, 0, height/2])
        vertices.append([0, 0, -height/2])
        
        top_center = len(vertices) - 2
        bottom_center = len(vertices) - 1
        
        # Create faces
        for i in range(num_points * 2):
            next_i = (i + 1) % (num_points * 2)
            
            # Top faces
            faces.append([i * 2, next_i * 2, top_center])
            # Bottom faces
            faces.append([i * 2 + 1, bottom_center, next_i * 2 + 1])
            # Side faces
            faces.append([i * 2, i * 2 + 1, next_i * 2 + 1])
            faces.append([i * 2, next_i * 2 + 1, next_i * 2])
        
        return trimesh.Trimesh(vertices=np.array(vertices), faces=np.array(faces))
    
    def _create_patriotic_faceplate(self) -> trimesh.Trimesh:
        """Faceplate with patriotic elements"""
        a = self.head_radius * 0.88
        b = self.head_radius * 0.28
        c = self.head_radius * 0.72
        
        faceplate = self.superellipsoid(a, b, c, n1=2.0, n2=2.3, resolution=40)
        faceplate.apply_translation([0, self.head_radius * 0.77, -self.head_radius * 0.05])
        
        # Add patriotic details
        details = [faceplate]
        
        # Center stripe
        center_stripe = trimesh.creation.box([12, 5, 55])
        center_stripe.apply_translation([0, self.head_radius * 0.78, -self.head_radius * 0.1])
        details.append(center_stripe)
        
        # Side accents
        for side in [-1, 1]:
            accent = trimesh.creation.box([8, 4, 40])
            accent.apply_translation([side * 30, self.head_radius * 0.76, -self.head_radius * 0.05])
            details.append(accent)
        
        faceplate = trimesh.util.concatenate(details)
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness)
        return faceplate
    
    def _create_bold_jaw(self) -> trimesh.Trimesh:
        """Bold, strong jaw"""
        jaw_profile = [
            (26, -28), (32, -44), (36, -60), (38, -75),
            (36, -88), (28, -95), (16, -88), (10, -75),
            (12, -60), (18, -44), (22, -28)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        jaw.apply_translation([0, self.head_radius * 0.4, self.head_radius * 0.1])
        
        # Add bold chin detail
        details = [jaw]
        
        chin = trimesh.creation.cylinder(radius=18, height=8, sections=20)
        chin.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        chin.apply_translation([0, self.head_radius * 0.52, -self.head_radius * 0.6])
        details.append(chin)
        
        jaw = trimesh.util.concatenate(details)
        jaw = self.create_hollow_shell(jaw, self.wall_thickness)
        return jaw
    
    def _create_patriotic_ear(self, side: str) -> trimesh.Trimesh:
        """Ear pieces with patriotic details"""
        pieces = []
        x_offset = self.head_radius * 0.9 if side == 'left' else -self.head_radius * 0.9
        
        # Main housing
        ear_main = trimesh.creation.cylinder(radius=20, height=18, sections=24)
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.06])
        pieces.append(ear_main)
        
        # Star detail
        star = self._create_star(8, 3)
        star.apply_translation([x_offset, 0, self.head_radius * 0.15])
        pieces.append(star)
        
        # Ring detail
        ring = trimesh.creation.cylinder(radius=22, height=4, sections=24)
        ring.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        ring.apply_translation([x_offset, 0, self.head_radius * 0.1])
        pieces.append(ring)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness)
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Patriotic visor shape"""
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.38, theta_end=np.pi/2 + 0.38,
            phi_start=-0.58, phi_end=0.58,
            resolution=24
        )
        visor_cutter.apply_translation([0, self.head_radius * 0.23, self.head_radius * 0.15])
        
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
    generator = IronPatriotHelmet()
    helmet = generator.generate()
    output_path = os.path.join(os.path.dirname(__file__), 'iron-patriot.stl')
    generator.save_stl(helmet, output_path)
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")

if __name__ == "__main__":
    main()
