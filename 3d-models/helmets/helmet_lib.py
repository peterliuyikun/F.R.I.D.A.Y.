"""
F.R.I.D.A.Y. Helmet Generator Library
Advanced parametric 3D modeling techniques for Iron Man style helmets
"""

import numpy as np
import trimesh
from trimesh import creation, transformations, boolean
import struct
from typing import List, Tuple, Optional, Callable
import math

class HelmetGenerator:
    """Base class for parametric helmet generation using advanced 3D modeling techniques"""
    
    def __init__(self, scale_factor: float = 1.0):
        self.scale_factor = scale_factor
        self.wall_thickness = 2.5  # mm for 3D printing
        self.head_circumference = 580  # mm (life-size)
        self.head_radius = self.head_circumference / (2 * np.pi)
        
    def superellipsoid(self, a: float, b: float, c: float, 
                       n1: float, n2: float, 
                       resolution: int = 64) -> trimesh.Trimesh:
        """
        Create a superellipsoid for smooth rounded shapes
        n1, n2 control the squareness (2 = ellipsoid, <2 = more square, >2 = more pointy)
        """
        theta = np.linspace(-np.pi/2, np.pi/2, resolution)
        phi = np.linspace(-np.pi, np.pi, resolution * 2)
        theta, phi = np.meshgrid(theta, phi)
        
        # Superellipsoid equation
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        cos_phi = np.cos(phi)
        sin_phi = np.sin(phi)
        
        # Avoid division by zero
        cos_theta = np.sign(cos_theta) * np.abs(cos_theta + 1e-10)**(2/n1)
        sin_theta = np.sign(sin_theta) * np.abs(sin_theta + 1e-10)**(2/n1)
        cos_phi = np.sign(cos_phi) * np.abs(cos_phi + 1e-10)**(2/n2)
        sin_phi = np.sign(sin_phi) * np.abs(sin_phi + 1e-10)**(2/n2)
        
        x = a * cos_theta * cos_phi
        y = b * cos_theta * sin_phi
        z = c * sin_theta
        
        # Create mesh from parametric surface
        vertices = np.stack([x.flatten(), y.flatten(), z.flatten()], axis=1)
        
        # Generate faces
        faces = []
        res_phi = resolution * 2
        res_theta = resolution
        
        for i in range(res_phi - 1):
            for j in range(res_theta - 1):
                v0 = i * res_theta + j
                v1 = (i + 1) * res_theta + j
                v2 = (i + 1) * res_theta + (j + 1)
                v3 = i * res_theta + (j + 1)
                
                faces.append([v0, v1, v2])
                faces.append([v0, v2, v3])
        
        mesh = trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
        return mesh
    
    def create_sphere_segment(self, radius: float, theta_start: float, theta_end: float,
                              phi_start: float, phi_end: float, 
                              resolution: int = 32) -> trimesh.Trimesh:
        """Create a spherical segment using parametric surface"""
        theta = np.linspace(theta_start, theta_end, resolution)
        phi = np.linspace(phi_start, phi_end, resolution)
        theta, phi = np.meshgrid(theta, phi)
        
        x = radius * np.sin(theta) * np.cos(phi)
        y = radius * np.sin(theta) * np.sin(phi)
        z = radius * np.cos(theta)
        
        vertices = np.stack([x.flatten(), y.flatten(), z.flatten()], axis=1)
        
        faces = []
        for i in range(resolution - 1):
            for j in range(resolution - 1):
                v0 = i * resolution + j
                v1 = (i + 1) * resolution + j
                v2 = (i + 1) * resolution + (j + 1)
                v3 = i * resolution + (j + 1)
                faces.append([v0, v1, v2])
                faces.append([v0, v2, v3])
        
        return trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
    
    def revolve_profile(self, profile_points: List[Tuple[float, float]], 
                        segments: int = 64) -> trimesh.Trimesh:
        """
        Revolve a 2D profile around the Z-axis to create 3D solid
        profile_points: list of (r, z) coordinates
        """
        vertices = []
        faces = []
        
        # Create vertices by revolving each profile point
        for i, (r, z) in enumerate(profile_points):
            for j in range(segments):
                angle = 2 * np.pi * j / segments
                x = r * np.cos(angle)
                y = r * np.sin(angle)
                vertices.append([x, y, z])
        
        vertices = np.array(vertices)
        num_rings = len(profile_points)
        
        # Create faces
        for i in range(num_rings - 1):
            for j in range(segments):
                v0 = i * segments + j
                v1 = i * segments + ((j + 1) % segments)
                v2 = (i + 1) * segments + ((j + 1) % segments)
                v3 = (i + 1) * segments + j
                
                faces.append([v0, v1, v2])
                faces.append([v0, v2, v3])
        
        mesh = trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
        return mesh
    
    def loft_profiles(self, profiles: List[np.ndarray], 
                      resolution: int = 32) -> trimesh.Trimesh:
        """
        Create surface by lofting between multiple profiles
        profiles: list of Nx3 arrays representing cross-sections
        """
        vertices = []
        faces = []
        
        num_profiles = len(profiles)
        points_per_profile = len(profiles[0])
        
        # Add all vertices
        for profile in profiles:
            vertices.extend(profile.tolist())
        
        vertices = np.array(vertices)
        
        # Create faces between profiles
        for i in range(num_profiles - 1):
            for j in range(points_per_profile):
                v0 = i * points_per_profile + j
                v1 = i * points_per_profile + ((j + 1) % points_per_profile)
                v2 = (i + 1) * points_per_profile + ((j + 1) % points_per_profile)
                v3 = (i + 1) * points_per_profile + j
                
                faces.append([v0, v1, v2])
                faces.append([v0, v2, v3])
        
        return trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
    
    def apply_mirror_symmetry(self, mesh: trimesh.Trimesh, 
                              axis: str = 'x') -> trimesh.Trimesh:
        """Mirror mesh for perfect symmetry"""
        if axis == 'x':
            mirror_matrix = np.array([[-1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 0, 1]])
        elif axis == 'y':
            mirror_matrix = np.array([[1, 0, 0, 0],
                                      [0, -1, 0, 0],
                                      [0, 0, 1, 0],
                                      [0, 0, 0, 1]])
        else:  # z
            mirror_matrix = np.array([[1, 0, 0, 0],
                                      [0, 1, 0, 0],
                                      [0, 0, -1, 0],
                                      [0, 0, 0, 1]])
        
        mirrored = mesh.copy()
        mirrored.apply_transform(mirror_matrix)
        
        # Combine original and mirrored
        combined = trimesh.util.concatenate([mesh, mirrored])
        return combined
    
    def create_hollow_shell(self, outer_mesh: trimesh.Trimesh, 
                           thickness: float) -> trimesh.Trimesh:
        """Create hollow shell by offsetting surface inward"""
        # Scale mesh down by thickness to create inner surface
        centroid = outer_mesh.centroid
        scale_factor = (self.head_radius - thickness) / self.head_radius
        
        inner_mesh = outer_mesh.copy()
        inner_mesh.apply_scale(scale_factor)
        
        # Combine outer and inner (with flipped normals for inner)
        inner_mesh.invert()
        shell = trimesh.util.concatenate([outer_mesh, inner_mesh])
        return shell
    
    def apply_fillet(self, mesh: trimesh.Trimesh, radius: float) -> trimesh.Trimesh:
        """Apply fillet (rounded edges) to mesh - simplified version"""
        # For now, return mesh as-is (trimesh doesn't have native fillet)
        # In production, would use CGAL or similar
        return mesh
    
    def boolean_union(self, mesh1: trimesh.Trimesh, mesh2: trimesh.Trimesh) -> trimesh.Trimesh:
        """CSG union operation"""
        try:
            result = trimesh.boolean.union([mesh1, mesh2])
            return result
        except:
            # Fallback to simple concatenation
            return trimesh.util.concatenate([mesh1, mesh2])
    
    def boolean_difference(self, mesh1: trimesh.Trimesh, mesh2: trimesh.Trimesh) -> trimesh.Trimesh:
        """CSG difference operation"""
        try:
            result = trimesh.boolean.difference([mesh1, mesh2])
            return result
        except:
            # Fallback
            return mesh1
    
    def boolean_intersection(self, mesh1: trimesh.Trimesh, mesh2: trimesh.Trimesh) -> trimesh.Trimesh:
        """CSG intersection operation"""
        try:
            result = trimesh.boolean.intersection([mesh1, mesh2])
            return result
        except:
            return mesh1
    
    def create_visor_cutout(self, helmet: trimesh.Trimesh, 
                           width: float, height: float, 
                           depth: float) -> trimesh.Trimesh:
        """Create a visor opening using boolean difference"""
        # Create cutting box for visor
        visor_cutter = trimesh.creation.box([width, depth, height])
        # Position at front of helmet
        visor_cutter.apply_translation([0, self.head_radius * 0.7, self.head_radius * 0.1])
        
        result = self.boolean_difference(helmet, visor_cutter)
        return result
    
    def subdivide_smooth(self, mesh: trimesh.Trimesh, iterations: int = 1) -> trimesh.Trimesh:
        """Apply subdivision surface smoothing"""
        for _ in range(iterations):
            mesh = mesh.subdivide()
        return mesh
    
    def save_stl(self, mesh: trimesh.Trimesh, filepath: str):
        """Save mesh as binary STL"""
        # Ensure mesh is watertight
        if not mesh.is_watertight:
            mesh.fill_holes()
        
        # Export as binary STL
        mesh.export(filepath, file_type='stl')
        print(f"Saved: {filepath}")
        print(f"  Vertices: {len(mesh.vertices)}")
        print(f"  Faces: {len(mesh.faces)}")
        print(f"  Watertight: {mesh.is_watertight}")
        print(f"  Volume: {mesh.volume:.2f} mm³")


class IronManHelmetBase(HelmetGenerator):
    """Base class for Iron Man style helmets"""
    
    def __init__(self, scale_factor: float = 1.0):
        super().__init__(scale_factor)
        self.base_color = (0.8, 0.1, 0.1)  # Red
        self.secondary_color = (0.9, 0.7, 0.1)  # Gold
        
    def create_base_helmet(self) -> trimesh.Trimesh:
        """Create base helmet shape using superellipsoid"""
        # Main cranium - slightly elongated superellipsoid
        a = self.head_radius * 0.95  # width
        b = self.head_radius * 0.95  # depth  
        c = self.head_radius * 1.05  # height
        
        helmet = self.superellipsoid(a, b, c, n1=2.2, n2=2.2, resolution=48)
        
        # Scale to create hollow shell
        shell = self.create_hollow_shell(helmet, self.wall_thickness)
        
        return shell
    
    def create_faceplate(self) -> trimesh.Trimesh:
        """Create faceplate with eye slots"""
        # Base faceplate - flattened sphere segment
        faceplate = self.create_sphere_segment(
            self.head_radius * 0.96,
            theta_start=0.3, theta_end=np.pi/2,
            phi_start=-0.8, phi_end=0.8,
            resolution=32
        )
        return faceplate
    
    def create_eye_slot(self, side: str = 'left') -> trimesh.Trimesh:
        """Create eye slot geometry"""
        # Eye shape - elongated box
        eye = trimesh.creation.box([25, 10, 8])
        
        x_offset = 35 if side == 'left' else -35
        eye.apply_translation([x_offset, self.head_radius * 0.85, self.head_radius * 0.25])
        
        return eye
    
    def create_ear_piece(self, side: str = 'left') -> trimesh.Trimesh:
        """Create ear piece with mechanical details"""
        # Main ear cylinder
        ear = trimesh.creation.cylinder(radius=20, height=15, sections=24)
        # Rotate to be horizontal
        rotation = trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0])
        ear.apply_transform(rotation)
        
        x_offset = self.head_radius * 0.9 if side == 'left' else -self.head_radius * 0.9
        ear.apply_translation([x_offset, 0, 0])
        
        return ear
    
    def create_jaw_mechanism(self) -> trimesh.Trimesh:
        """Create jaw mechanism with hinge"""
        # Jaw shape - revolved profile
        jaw_profile = [
            (30, -40), (35, -50), (40, -60), (38, -70),
            (30, -75), (20, -70), (15, -60), (20, -50)
        ]
        jaw = self.revolve_profile(jaw_profile, segments=48)
        jaw.apply_translation([0, self.head_radius * 0.3, 0])
        
        return jaw