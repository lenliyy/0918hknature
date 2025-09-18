import plotly.graph_objects as go
import numpy as np
import random

# Typhoon data from 2002 to 2023
typhoon_data = {
    2002: 6, 2003: 7, 2004: 5, 2005: 8, 2006: 7, 2007: 9, 2008: 6, 2009: 5,
    2010: 7, 2011: 8, 2012: 6, 2013: 7, 2014: 5, 2015: 8, 2016: 7, 2017: 9,
    2018: 8, 2019: 6, 2020: 5, 2021: 7, 2022: 6, 2023: 8
}

def generate_cluster(center_x, center_y, num_points, radius, year, count):
    """Generate a star cluster with fluid-like distribution"""
    points_x = []
    points_y = []
    sizes = []
    colors = []
    
    # Generate main cluster points
    for _ in range(num_points):
        # Use gaussian distribution for more natural clustering
        dx = np.random.normal(0, radius/2)
        dy = np.random.normal(0, radius/2)
        points_x.append(center_x + dx)
        points_y.append(center_y + dy)
        sizes.append(np.random.uniform(3, 8))
        
        # Create a slight color variation for depth effect
        brightness = np.random.uniform(0.7, 1.0)
        colors.append(f'rgba(255,255,255,{brightness})')
    
    # Add some "dust" particles
    for _ in range(num_points // 2):
        angle = np.random.uniform(0, 2*np.pi)
        r = np.random.uniform(radius/2, radius*1.5)
        points_x.append(center_x + r*np.cos(angle))
        points_y.append(center_y + r*np.sin(angle))
        sizes.append(np.random.uniform(1, 3))
        colors.append(f'rgba(255,215,0,{np.random.uniform(0.3, 0.6)})')
    
    return points_x, points_y, sizes, colors

def create_visualization():
    # Calculate positions for each year's cluster
    years = list(typhoon_data.keys())
    counts = list(typhoon_data.values())
    num_years = len(years)
    
    # Arrange clusters in a wave pattern along the axes
    x_positions = np.linspace(-5, 5, num_years)  # Spread along x-axis
    y_amplitudes = np.array(counts) / max(counts) * 3  # Scale y positions based on typhoon counts
    
    # Create animation frames
    frames = []
    num_frames = 120
    
    for f in range(num_frames):
        data = []
        
        # Add background stars
        bg_stars_x = np.random.uniform(-6, 6, 200)
        bg_stars_y = np.random.uniform(-6, 6, 200)
        data.append(go.Scatter(
            x=bg_stars_x,
            y=bg_stars_y,
            mode='markers',
            marker=dict(
                size=np.random.uniform(1, 3, 200),
                color=[f'rgba(255,255,255,{np.random.uniform(0.3, 0.6)})' for _ in range(200)]
            ),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # Add clusters sequentially
        for i, (year, count, x_pos) in enumerate(zip(years, counts, x_positions)):
            # Calculate cluster position with wave motion
            wave_phase = f / 20 + i / 2  # Controls wave motion
            y_amplitude = y_amplitudes[i]
            center_x = x_pos
            center_y = y_amplitude * np.sin(wave_phase)
            
            # Calculate appearance timing
            delay = i * 5  # Delay between clusters
            duration = 30  # Duration of appearance animation
            progress = min(1.0, max(0.0, (f - delay) / duration))
            
            if progress > 0:
                # Generate cluster points
                points_x, points_y, sizes, colors = generate_cluster(
                    center_x * progress,
                    center_y * progress,
                    count * 10,  # More points for bigger clusters
                    0.3 + count * 0.05,  # Cluster size based on typhoon count
                    year,
                    count
                )
                
                # Add cluster
                data.append(go.Scatter(
                    x=points_x,
                    y=points_y,
                    mode='markers+text',
                    marker=dict(
                        size=sizes,
                        color=colors
                    ),
                    text=[f'{year}: {count}台风' if i == 0 else '' for i in range(len(points_x))],
                    textposition='top center',
                    textfont=dict(
                        size=14,
                        color='white',
                        family='Arial'
                    ),
                    hoverinfo='text',
                    hovertext=[f'{year}年: {count}个台风' for _ in range(len(points_x))],
                    showlegend=False,
                    opacity=progress
                ))
        
        frames.append(go.Frame(data=data, name=str(f)))
    
    # Create layout
    layout = go.Layout(
        title=dict(
            text='香港台风数据星空图 (2002-2023)',
            font=dict(size=24, color='white', family='Arial'),
            y=0.95
        ),
        xaxis=dict(
            visible=True,
            range=[-6, 6],
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            gridwidth=1,
            zerolinecolor='rgba(255,255,255,0.4)',
            zerolinewidth=2,
            linecolor='rgba(255,255,255,0.4)',
            linewidth=2,
            tickfont=dict(color='white'),
            title=dict(
                text='X轴',
                font=dict(color='white', size=14),
                standoff=10
            )
        ),
        yaxis=dict(
            visible=True,
            range=[-6, 6],
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)',
            gridwidth=1,
            zerolinecolor='rgba(255,255,255,0.4)',
            zerolinewidth=2,
            linecolor='rgba(255,255,255,0.4)',
            linewidth=2,
            tickfont=dict(color='white'),
            title=dict(
                text='Y轴',
                font=dict(color='white', size=14),
                standoff=10
            )
        ),
        plot_bgcolor='rgb(0,0,0)',
        paper_bgcolor='rgb(0,0,0)',
        margin=dict(l=20, r=20, t=80, b=20),
        updatemenus=[dict(
            type='buttons',
            showactive=False,
            y=0.1,
            x=0.5,
            xanchor='center',
            yanchor='bottom',
            pad=dict(t=0, r=10),
            buttons=[dict(
                label='播放动画',
                method='animate',
                args=[None, {
                    'frame': {'duration': 50, 'redraw': True},
                    'fromcurrent': True,
                    'transition': {'duration': 30, 'easing': 'cubic-in-out'}
                }]
            )]
        )]
    )
    
    # Create figure
    fig = go.Figure(
        data=frames[0].data,
        layout=layout,
        frames=frames[1:]  # Skip first frame to avoid initial flash
    )
    
    return fig

if __name__ == '__main__':
    fig = create_visualization()
    fig.write_html('typhoon_star_animation.html', auto_open=True)
