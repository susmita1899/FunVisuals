import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Hyperbola parameters for x^2/a^2 - y^2/b^2 = 1
a, b = 1, 0.5

# Parameter for hyperbola generation
t = np.linspace(-2, 2, 400)
# Two branches: using cosh/sinh for branch with x ≥ a and its mirror for x ≤ -a.
x_pos = a * np.cosh(t)
y_pos = b * np.sinh(t)
x_neg = -a * np.cosh(t)
y_neg = b * np.sinh(t)

# Asymptotes for the standard hyperbola: y = ± (b/a) x
x_asym = np.linspace(-5, 5, 200)
y_asym1 = (b/a) * x_asym
y_asym2 = -(b/a) * x_asym

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-5, 5)
ax.set_ylim(-5, 5)
ax.set_aspect('equal', 'box')
ax.grid(True, linestyle='--', alpha=0.5)
ax.set_title("Enhanced Visualization: Rotating Hyperbola with Four Moving Markers")

# Static hyperbola (unrotated) and asymptotes
line_static1, = ax.plot(x_pos, y_pos, color='gray', linestyle='--', alpha=0.5, label='Static Hyperbola')
line_static2, = ax.plot(x_neg, y_neg, color='gray', linestyle='--', alpha=0.5)
asymptote1, = ax.plot(x_asym, y_asym1, color='green', linestyle=':', alpha=0.7, label='Asymptotes')
asymptote2, = ax.plot(x_asym, y_asym2, color='green', linestyle=':', alpha=0.7)

# Fixed rotation point
origin, = ax.plot([0], [0], 'ro', markersize=8, label='Rotation Point')

# Rotating hyperbola (both branches)
line_rot1, = ax.plot([], [], color='blue', linewidth=2, label='Rotating Hyperbola')
line_rot2, = ax.plot([], [], color='blue', linewidth=2)

# Markers for rotated hyperbola branches
marker_rot1, = ax.plot([], [], 'o', color='magenta', markersize=10, label='Rotated Marker Branch 1')
marker_rot2, = ax.plot([], [], 'o', color='orange', markersize=10, label='Rotated Marker Branch 2')

# Markers for static hyperbola branches
marker_static1, = ax.plot([], [], 's', color='purple', markersize=8, label='Static Marker Branch 1')
marker_static2, = ax.plot([], [], 's', color='brown', markersize=8, label='Static Marker Branch 2')

# Trails for the rotated markers
trail_rot1, = ax.plot([], [], color='magenta', linestyle='-', linewidth=1, alpha=0.5)
trail_rot2, = ax.plot([], [], color='orange', linestyle='-', linewidth=1, alpha=0.5)
trail_rot1_x, trail_rot1_y = [], []
trail_rot2_x, trail_rot2_y = [], []

# Annotation for current rotation angle
angle_text = ax.text(0.05, 0.95, '', transform=ax.transAxes, fontsize=12, verticalalignment='top')

ax.legend(loc='upper right')

def init():
    line_rot1.set_data([], [])
    line_rot2.set_data([], [])
    marker_rot1.set_data([], [])
    marker_rot2.set_data([], [])
    marker_static1.set_data([], [])
    marker_static2.set_data([], [])
    trail_rot1.set_data([], [])
    trail_rot2.set_data([], [])
    angle_text.set_text('')
    return (line_rot1, line_rot2, marker_rot1, marker_rot2, marker_static1, marker_static2,
            trail_rot1, trail_rot2, angle_text)

def update(frame):
    # Convert the current frame (degrees) to radians.
    angle = np.radians(frame)
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    
    # Rotate the hyperbola points for both branches.
    x_rot1 = cos_a * x_pos - sin_a * y_pos
    y_rot1 = sin_a * x_pos + cos_a * y_pos
    x_rot2 = cos_a * x_neg - sin_a * y_neg
    y_rot2 = sin_a * x_neg + cos_a * y_neg
    
    line_rot1.set_data(x_rot1, y_rot1)
    line_rot2.set_data(x_rot2, y_rot2)
    
    # Choose a parameter index that cycles over t.
    idx = int(frame) % len(t)
    
    # Update markers on the rotated hyperbola.
    x_marker_rot1 = x_rot1[idx]
    y_marker_rot1 = y_rot1[idx]
    x_marker_rot2 = x_rot2[idx]
    y_marker_rot2 = y_rot2[idx]
    marker_rot1.set_data(x_marker_rot1, y_marker_rot1)
    marker_rot2.set_data(x_marker_rot2, y_marker_rot2)
    
    # Update markers on the static hyperbola (unrotated).
    x_marker_static1 = x_pos[idx]
    y_marker_static1 = y_pos[idx]
    x_marker_static2 = x_neg[idx]
    y_marker_static2 = y_neg[idx]
    marker_static1.set_data(x_marker_static1, y_marker_static1)
    marker_static2.set_data(x_marker_static2, y_marker_static2)
    
    # Update trails for the rotated markers.
    trail_rot1_x.append(x_marker_rot1)
    trail_rot1_y.append(y_marker_rot1)
    trail_rot2_x.append(x_marker_rot2)
    trail_rot2_y.append(y_marker_rot2)
    
    # Limit the length of each trail for visual clarity.
    max_trail_length = 100
    if len(trail_rot1_x) > max_trail_length:
        del trail_rot1_x[0]
        del trail_rot1_y[0]
    if len(trail_rot2_x) > max_trail_length:
        del trail_rot2_x[0]
        del trail_rot2_y[0]
    
    trail_rot1.set_data(trail_rot1_x, trail_rot1_y)
    trail_rot2.set_data(trail_rot2_x, trail_rot2_y)
    
    # Update the annotation with the current rotation angle.
    angle_text.set_text(f'Rotation Angle: {frame:.1f}°')
    
    return (line_rot1, line_rot2, marker_rot1, marker_rot2, marker_static1, marker_static2,
            trail_rot1, trail_rot2, angle_text)

ani = FuncAnimation(fig, update, frames=np.linspace(0, 360, 360),
                    init_func=init, blit=True, interval=50)

plt.show()
