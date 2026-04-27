#!/usr/bin/env python3
"""
Generate Iron Man Mark 2 Helmet STL - Pure Python
Classic smooth helmet design with faceplate details
"""

import struct
import math

def vec_add(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def vec_sub(a, b):
    return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]

def vec_scale(v, s):
    return [v[0] * s, v[1] * s, v[2] * s]

def vec_dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def vec_length(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])

def vec_normalize(v):
    length = vec_length(v)
    if length < 0.0001:
        return [0, 0, 1]
    return [v[0]/length, v[1]/length, v[2]/length]

def vec_cross(a, b):
    return [
        a[1]*b[2] - a[2]*b[1],
        a[2]*b[0] - a[0]*b[2],
        a[0]*b[1] - a[1]*b[0]
    ]

def vec_round(v, decimals=6):
    return (round(v[0], decimals), round(v[1], decimals), round(v[2], decimals))

def sphere_point(theta, phi, radius, center=[0, 0, 0]):
    """Generate point on sphere surface"""
    x = center[0] + radius * math.sin(phi) * math.cos(theta)
    y = center[1] + radius * math.sin(phi) * math.sin(theta)
    z = center[2] + radius * math.cos(phi)
    return [x, y, z]

def create_ironman_helmet():
    """
    Create Iron Man Mark 2 helmet mesh
    """
    vertices = []
    faces = []
    vertex_dict = {}
    
    def add_vertex(v):
        key = vec_round(v)
        if key not in vertex_dict:
            vertex_dict[key] = len(vertices)
            vertices.append(v)
        return vertex_dict[key]
    
    def add_triangle(v1, v2, v3):
        i1 = add_vertex(v1)
        i2 = add_vertex(v2)
        i3 = add_vertex(v3)
        faces.append([i1, i2, i3])
    
    # Helmet parameters
    head_radius = 35.0
    head_height = 45.0
    
    # Create helmet shell using parametric surface
    # We'll create a modified sphere for the helmet shape
    
    theta_steps = 48  # Around (azimuthal)
    phi_steps = 32    # Up-down (polar)
    
    # Generate helmet surface points
    surface_points = {}
    
    for i in range(theta_steps + 1):
        theta = 2 * math.pi * i / theta_steps
        for j in range(phi_steps + 1):
            phi = math.pi * j / phi_steps
            
            # Base sphere point
            base_r = head_radius
            
            # Modify radius based on position for helmet shape
            # Front (face area) - slightly flattened
            # Top - rounded
            # Back - rounded
            
            # Calculate normalized direction
            dx = math.sin(phi) * math.cos(theta)
            dy = math.sin(phi) * math.sin(theta)
            dz = math.cos(phi)
            
            # Modify shape
            # Flatten front (where face would be)
            if dy > 0.3:  # Front area
                r_mod = base_r * (0.85 + 0.15 * (1 - dy))
            # Elongate top
            elif dz > 0.5:
                r_mod = base_r * (1.0 + 0.1 * dz)
            # Widen sides slightly
            elif abs(dx) > 0.7:
                r_mod = base_r * 1.05
            else:
                r_mod = base_r
            
            # Elongate vertically
            z_scale = 1.15 if dz > 0 else 1.0
            
            x = r_mod * dx
            y = r_mod * dy
            z = head_height/2 * dz * z_scale
            
            surface_points[(i, j)] = [x, y, z]
    
    # Create faces from grid
    for i in range(theta_steps):
        for j in range(phi_steps):
            p00 = surface_points[(i, j)]
            p10 = surface_points[(i + 1, j)]
            p01 = surface_points[(i, j + 1)]
            p11 = surface_points[(i + 1, j + 1)]
            
            # Two triangles per quad
            add_triangle(p00, p10, p11)
            add_triangle(p00, p11, p01)
    
    # Add faceplate details (eyes and mouth area)
    # Eye slits
    add_eye_details(vertices, faces, vertex_dict, head_radius, head_height)
    
    # Add ear pieces / side details
    add_ear_details(vertices, faces, vertex_dict, head_radius, head_height)
    
    return vertices, faces

def add_eye_details(vertices, faces, vertex_dict, radius, height):
    """Add eye slit details to the helmet"""
    # Left and right eye positions
    eye_y = radius * 0.35  # Front
    eye_z = height * 0.15  # Slightly above center
    eye_x_offset = radius * 0.35
    
    # Eye dimensions
    eye_width = 12.0
    eye_height = 4.0
    eye_depth = 3.0
    
    for side in [-1, 1]:  # Left and right
        center_x = side * eye_x_offset
        
        # Create eye slit as a recessed rectangle
        # We'll add triangles around the eye area
        
        # Eye corners
        eye_corners = [
            [center_x - eye_width/2, eye_y, eye_z - eye_height/2],
            [center_x + eye_width/2, eye_y, eye_z - eye_height/2],
            [center_x + eye_width/2, eye_y, eye_z + eye_height/2],
            [center_x - eye_width/2, eye_y, eye_z + eye_height/2],
        ]
        
        # Recessed eye points (pushed back)
        recessed = [[c[0], c[1] - eye_depth, c[2]] for c in eye_corners]
        
        # Add faces for eye recess
        for i in range(4):
            next_i = (i + 1) % 4
            
            # Add triangles to vertex list and faces
            def add_v(v):
                key = vec_round(v)
                if key not in vertex_dict:
                    vertex_dict[key] = len(vertices)
                    vertices.append(v)
                return vertex_dict[key]
            
            # Side walls of eye recess
            i1 = add_v(eye_corners[i])
            i2 = add_v(eye_corners[next_i])
            i3 = add_v(recessed[next_i])
            i4 = add_v(recessed[i])
            
            faces.append([i1, i2, i3])
            faces.append([i1, i3, i4])

def add_ear_details(vertices, faces, vertex_dict, radius, height):
    """Add ear piece details"""
    # Ear positions (sides of helmet)
    ear_x = radius * 1.0
    ear_z = height * 0.1
    
    # Create simple ear piece protrusions
    ear_points = [
        [ear_x, -5, ear_z - 8],
        [ear_x + 3, -5, ear_z - 8],
        [ear_x + 3, -5, ear_z + 8],
        [ear_x, -5, ear_z + 8],
        [ear_x, 5, ear_z - 8],
        [ear_x + 3, 5, ear_z - 8],
        [ear_x + 3, 5, ear_z + 8],
        [ear_x, 5, ear_z + 8],
    ]
    
    def add_v(v):
        key = vec_round(v)
        if key not in vertex_dict:
            vertex_dict[key] = len(vertices)
            vertices.append(v)
        return vertex_dict[key]
    
    # Add ear piece faces (simplified box)
    indices = [add_v(p) for p in ear_points]
    
    # Front face
    faces.append([indices[0], indices[1], indices[2]])
    faces.append([indices[0], indices[2], indices[3]])
    # Back face  
    faces.append([indices[4], indices[6], indices[5]])
    faces.append([indices[4], indices[7], indices[6]])
    # etc... (simplified)

def write_stl_binary(vertices, faces, filename):
    """Write mesh to binary STL file"""
    
    with open(filename, 'wb') as f:
        # 80 byte header
        header = b'Iron Man Mark 2 Helmet' + b'\x00' * (80 - 22)
        f.write(header)
        
        # Number of triangles
        f.write(struct.pack('<I', len(faces)))
        
        for face in faces:
            v0 = vertices[face[0]]
            v1 = vertices[face[1]]
            v2 = vertices[face[2]]
            
            # Calculate normal
            edge1 = vec_sub(v1, v0)
            edge2 = vec_sub(v2, v0)
            normal = vec_cross(edge1, edge2)
            normal = vec_normalize(normal)
            
            # Write normal (float32)
            f.write(struct.pack('<fff', *normal))
            
            # Write vertices (float32)
            f.write(struct.pack('<fff', *v0))
            f.write(struct.pack('<fff', *v1))
            f.write(struct.pack('<fff', *v2))
            
            # Attribute byte count (uint16)
            f.write(struct.pack('<H', 0))
    
    print(f"Binary STL file written: {filename}")
    print(f"Vertices: {len(vertices)}, Faces: {len(faces)}")

def main():
    print("Generating Iron Man Mark 2 Helmet STL...")
    
    # Generate the helmet
    vertices, faces = create_ironman_helmet()
    
    # Write binary STL
    write_stl_binary(vertices, faces, 'ironman-helmet.stl')
    
    print("Done! File: ironman-helmet.stl")

if __name__ == '__main__':
    main()