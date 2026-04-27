#!/usr/bin/env python3
"""
Iron Man Mark 3 Helmet Generator
Parametric 3D modeling with advanced techniques:
- NURBS/Patch surfaces via superellipsoids
- Boolean operations for visor cutouts
- Subdivision surfaces for smoothness
- Symmetry mirroring
"""

import numpy as np
import trimesh
import sys
import os

# Add parent directory to path for helmet_lib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helmet_lib import IronManHelmetBase

class IronManMark3Helmet(IronManHelmetBase):
    """
    Iron Man Mark 3 Helmet - Classic design with proper faceplate, jaw mechanism, ear pieces
    Features:
    - Rounded superellipsoid cranium
    - Mechanical jaw with visible seams
    - Detailed ear pieces with vents
    - Classic visor shape
    """
    
    def __init__(self):
        super().__init__(scale_factor=1.0)
        self.name = "Iron Man Mark 3"
        
    def generate(self) -> trimesh.Trimesh:
        """Generate complete Mark 3 helmet"""
        print(f"Generating {self.name} helmet...")
        
        # 1. Base cranium using superellipsoid (NURBS-like smooth surface)
        print("  Creating cranium...")
        cranium = self._create_cranium()
        
        # 2. Faceplate with proper visor opening
        print("  Creating faceplate...")
        faceplate = self._create_faceplate()
        
        # 3. Jaw mechanism
        print("  Creating jaw mechanism...")
        jaw = self._create_jaw()
        
        # 4. Ear pieces with detail
        print("  Creating ear pieces...")
        left_ear = self._create_ear_piece('left')
        right_ear = self._create_ear_piece('right')
        
        # 5. Combine all parts using boolean union
        print("  Combining parts...")
        helmet = trimesh.util.concatenate([cranium, faceplate, jaw, left_ear, right_ear])
        
        # 6. Create visor cutout (boolean difference)
        print("  Creating visor cutout...")
        helmet = self._create_visor_cutout(helmet)
        
        # 7. Apply subdivision smoothing
        print("  Applying subdivision smoothing...")
        helmet = self.subdivide_smooth(helmet, iterations=1)
        
        # 8. Ensure watertight mesh
        print("  Finalizing mesh...")
        helmet = self._finalize_mesh(helmet)
        
        return helmet
    
    def _create_cranium(self) -> trimesh.Trimesh:
        """Create main cranium using superellipsoid"""
        # Superellipsoid for smooth rounded cranium
        a = self.head_radius * 0.92  # width (x)
        b = self.head_radius * 0.95  # depth (y)
        c = self.head_radius * 1.02  # height (z)
        
        # n=2.3 gives slightly squared but smooth shape
        cranium = self.superellipsoid(a, b, c, n1=2.3, n2=2.3, resolution=56)
        
        # Scale to create hollow shell
        shell = self.create_hollow_shell(cranium, self.wall_thickness)
        return shell
    
    def _create_faceplate(self) -> trimesh.Trimesh:
        """Create faceplate with mechanical details"""
        # Main faceplate - flattened superellipsoid front
        a = self.head_radius * 0.88
        b = self.head_radius * 0.3  # thin in depth
        c = self.head_radius * 0.75
        
        faceplate = self.superellipsoid(a, b, c, n1=2.0, n2=2.5, resolution=40)
        
        # Position at front
        faceplate.apply_translation([0, self.head_radius * 0.75, -self.head_radius * 0.1])
        
        # Create hollow version
        faceplate = self.create_hollow_shell(faceplate, self.wall_thickness)
        
        return faceplate
    
    def _create_jaw(self) -> trimesh.Trimesh:
        """Create mechanical jaw with proper articulation look"""
        # Jaw profile using revolve
        jaw_profile = [
            (25, -30), (30, -45), (35, -60), (38, -75),
            (35, -85), (25, -90), (15, -85), (10, -75),
            (12, -60), (18, -45), (20, -30)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        
        # Position jaw
        jaw.apply_translation([0, self.head_radius * 0.4, self.head_radius * 0.1])
        
        # Add jaw line details
        jaw_line_left = self._create_jaw_line('left')
        jaw_line_right = self._create_jaw_line('right')
        
        jaw = trimesh.util.concatenate([jaw, jaw_line_left, jaw_line_right])
        jaw = self.create_hollow_shell(jaw, self.wall_thickness)
        
        return jaw
    
    def _create_jaw_line(self, side: str) -> trimesh.Trimesh:
        """Create jaw separation line detail"""
        line = trimesh.creation.box([3, 2, 50])
        x_offset = 28 if side == 'left' else -28
        line.apply_translation([x_offset, self.head_radius * 0.45, -self.head_radius * 0.2])
        return line
    
    def _create_ear_piece(self, side: str) -> trimesh.Trimesh:
        """Create detailed ear piece with vents"""
        pieces = []
        
        # Main ear housing
        ear_main = trimesh.creation.cylinder(radius=22, height=20, sections=24)
        ear_main.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        x_offset = self.head_radius * 0.88 if side == 'left' else -self.head_radius * 0.88
        ear_main.apply_translation([x_offset, 0, self.head_radius * 0.05])
        pieces.append(ear_main)
        
        # Vent details
        for i in range(3):
            vent = trimesh.creation.box([8, 3, 2])
            vent.apply_translation([x_offset, -5 + i*5, self.head_radius * 0.15])
            pieces.append(vent)
        
        # Back detail
        back = trimesh.creation.cylinder(radius=18, height=8, sections=20)
        back.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
        back.apply_translation([x_offset, -self.head_radius * 0.1, self.head_radius * 0.05])
        pieces.append(back)
        
        ear = trimesh.util.concatenate(pieces)
        ear = self.create_hollow_shell(ear, self.wall_thickness)
        
        return ear
    
    def _create_visor_cutout(self, helmet: trimesh.Trimesh) -> trimesh.Trimesh:
        """Create visor opening using boolean difference"""
        # Visor shape - custom curved opening
        visor_points = []
        
        # Create visor profile
        width = 70
        height = 35
        depth = 60
        
        # Main visor cutter - use sphere segment for curved shape
        visor_cutter = self.create_sphere_segment(
            radius=self.head_radius * 1.1,
            theta_start=np.pi/2 - 0.4, theta_end=np.pi/2 + 0.4,
            phi_start=-0.6, phi_end=0.6,
            resolution=24
        )
        
        # Position at front
        visor_cutter.apply_translation([0, self.head_radius * 0.2, self.head_radius * 0.15])
        
        # Perform boolean difference
        try:
            result = trimesh.boolean.difference([helmet, visor_cutter])
            return result
        except:
            # Fallback - return helmet without cutout
            print("    Warning: Boolean difference failed, using helmet without visor cutout")
            return helmet
    
    def _finalize_mesh(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Ensure mesh is watertight and properly formed"""
        # Merge duplicate vertices
        mesh.merge_vertices()
        
        # Remove degenerate faces
        mesh.remove_degenerate_faces()
        
        # Remove unreferenced vertices
        mesh.remove_unreferenced_vertices()
        
        # Fill holes if any
        if not mesh.is_watertight:
            mesh.fill_holes()
        
        return mesh


def main():
    """Generate and save Mark 3 helmet"""
    generator = IronManMark3Helmet()
    helmet = generator.generate()
    
    # Save as binary STL
    output_path = os.path.join(os.path.dirname(__file__), 'ironman-mark3.stl')
    generator.save_stl(helmet, output_path)
    
    print(f"\nGeneration complete!")
    print(f"Output: {output_path}")
    print(f"Triangles: {len(helmet.faces)}")
    print(f"Vertices: {len(helmet.vertices)}")


if __name__ == "__main__":
    main()