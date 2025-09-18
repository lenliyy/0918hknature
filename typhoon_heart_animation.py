import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import to_hex
import random

# Typhoon data from 2002 to 2023
typhoon_data = {
    2002: 6, 2003: 7, 2004: 5, 2005: 8, 2006: 7, 2007: 9, 2008: 6, 2009: 5,
    2010: 7, 2011: 8, 2012: 6, 2013: 7, 2014: 5, 2015: 8, 2016: 7, 2017: 9,
    2018: 8, 2019: 6, 2020: 5, 2021: 7, 2022: 6, 2023: 8
}

def heart_shape(t, scale=1.0):
    """Heart shape formula"""
    r = scale * (2 - 2 * np.sin(t) + np.sin(t) * np.sqrt(np.abs(np.cos(t))) / (np.sin(t) + 1.4))
    return r

def generate_stars(num_stars, min_x=-2.2, max_x=2.2, min_y=-2.2, max_y=2.2):
    """Generate background stars data"""
    x = [random.uniform(min_x, max_x) for _ in range(num_stars)]
    y = [random.uniform(min_y, max_y) for _ in range(num_stars)]
    sizes = [random.uniform(2, 7) for _ in range(num_stars)]
    colors = [f'rgba({random.randint(120,180)},{random.randint(80,120)},{random.randint(180,255)},{random.uniform(0.3,0.8)})'
             for _ in range(num_stars)]
    return x, y, sizes, colors

def generate_heart_stars(num_stars):
    """Generate stars inside the heart shape"""
    x, y, sizes, colors = [], [], [], []
    for _ in range(num_stars):
        t = random.uniform(0, 2*np.pi)
        r = random.uniform(0.3, 1.0)
        base_r = heart_shape(t)
        x.append(r * base_r * np.sin(t))
        y.append(r * base_r * np.cos(t))
        sizes.append(random.uniform(3, 10))
        colors.append(f'rgba({random.randint(180,255)},{random.randint(120,180)},{random.randint(200,255)},{random.uniform(0.5,1.0)})')
    return x, y, sizes, colors

def create_visualization():
    # Basic parameter settings
    num_points = 200
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    years = list(typhoon_data.keys())
    counts = np.array(list(typhoon_data.values()))
    
    # Generate gradient colors
    purples = cm.get_cmap('Purples')
    num_layers = len(typhoon_data)
    layer_colors = [to_hex(purples(0.4 + 0.6*i/max(num_layers-1,1))) for i in range(num_layers)]
    
    # Calculate scaling ratios
    min_scale, max_scale = 0.7, 1.3
    scales = min_scale + (counts - min(counts)) / (max(counts) - min(counts) + 1e-6) * (max_scale - min_scale)
    
    # Generate background stars and heart-shaped stars
    bg_x, bg_y, bg_sizes, bg_colors = generate_stars(120)
    heart_x, heart_y, heart_sizes, heart_colors = generate_heart_stars(60)
    
    # Create animation frames
    frames = []
    num_frames = 60
    
    for f in range(num_frames):
        angle = 2 * np.pi * f / num_frames
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        data = []
        
        # Add background stars
        data.append(go.Scatter(
            x=bg_x, y=bg_y,
            mode='markers',
            marker=dict(size=bg_sizes, color=bg_colors),
            hoverinfo='skip',
            opacity=0.7,
            showlegend=False
        ))
        
        # Add heart-shaped internal stars
        data.append(go.Scatter(
            x=heart_x, y=heart_y,
            mode='markers',
            marker=dict(size=heart_sizes, color=heart_colors),
            hoverinfo='skip',
            opacity=0.85,
            showlegend=False
        ))
        
        # Add multi-layer heart shapes
        for i, (scale, color, year, count) in enumerate(zip(scales, layer_colors, years, counts)):
            r = heart_shape(theta, scale)
            x = r * np.sin(theta)
            y = r * np.cos(theta)
            x_rot = x * cos_a - y * sin_a
            y_rot = x * sin_a + y * cos_a
            
            data.append(go.Scatter(
                x=x_rot, y=y_rot,
                mode='lines',
                line=dict(width=6, color=color),
                name=f'{year}',
                hoverinfo='skip',
                opacity=0.45 + 0.5 * (i / max(num_layers-1,1)),
                showlegend=False
            ))
        
        # Add year markers
        r = heart_shape(theta, scales[-1])
        x = r * np.sin(theta)
        y = r * np.cos(theta)
        x_rot = x * cos_a - y * sin_a
        y_rot = x * sin_a + y * cos_a
        idxs = np.linspace(0, num_points, num_layers, endpoint=False, dtype=int)
        
        data.append(go.Scatter(
            x=x_rot[idxs],
            y=y_rot[idxs],
            mode='markers+text',
            marker=dict(
                size=18,
                color=layer_colors,
                line=dict(width=2, color='white'),
                opacity=0.95
            ),
            text=[f'Year {y}<br>Typhoons: {c}' for y, c in zip(years, counts)],
            textposition='top center',
            hoverinfo='text',
            showlegend=False
        ))
        
        frames.append(go.Frame(data=data, name=str(f)))
    
    # Create initial layout
    layout = go.Layout(
        title='Hong Kong Typhoon Data Visualization (2002-2023) - Animated Heart Shape',
        xaxis=dict(visible=False, range=[-2.5, 2.5]),
        yaxis=dict(visible=False, range=[-2.5, 2.5]),
        showlegend=False,
        plot_bgcolor='rgb(20,10,40)',
        paper_bgcolor='rgb(20,10,40)',
        title_font_color='white',
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            buttons=[dict(
                label='Play',
                method='animate',
                args=[None, {'frame': {'duration': 80, 'redraw': True},
                            'fromcurrent': True}]
            )]
        )]
    )
    
    # Create figure
    fig = go.Figure(
        data=frames[0].data,
        layout=layout,
        frames=frames
    )
    
    return fig

if __name__ == '__main__':
    # 创建并保存可视化
    fig = create_visualization()
    fig.write_html('typhoon_heart_animation.html', auto_open=True)
