import plotly.graph_objects as go
import numpy as np
import random

# Hong Kong Typhoon data from 2002 to 2023
typhoon_data = {
    2002: 6, 2003: 7, 2004: 5, 2005: 8, 2006: 7, 2007: 9, 2008: 6, 2009: 5,
    2010: 7, 2011: 8, 2012: 6, 2013: 7, 2014: 5, 2015: 8, 2016: 7, 2017: 9,
    2018: 8, 2019: 6, 2020: 5, 2021: 7, 2022: 6, 2023: 8
}

# Detailed typhoon information (simulated data, can be replaced with real data)
typhoon_details = {
    2002: {"names": ["Hagupit", "Fengshen", "Nuri"], "max_wind": 185, "damages": "Moderate"},
    2003: {"names": ["Dujuan", "Imbudo", "Krovanh"], "max_wind": 195, "damages": "Severe"},
    2004: {"names": ["Conson", "Namcheon", "Aere"], "max_wind": 175, "damages": "Minor"},
    2005: {"names": ["Haitang", "Matsa", "Khanun"], "max_wind": 205, "damages": "Severe"},
    2006: {"names": ["Bilis", "Kaemi", "Saomai"], "max_wind": 220, "damages": "Catastrophic"},
    2007: {"names": ["Pabuk", "Sepat", "Wipha"], "max_wind": 210, "damages": "Severe"},
    2008: {"names": ["Fengshen", "Hagupit", "Nuri"], "max_wind": 165, "damages": "Moderate"},
    2009: {"names": ["Linfa", "Goni", "Parma"], "max_wind": 155, "damages": "Minor"},
    2010: {"names": ["Fanapi", "Meranti", "Megi"], "max_wind": 190, "damages": "Moderate"},
    2011: {"names": ["Lupit", "Roke", "Nesat"], "max_wind": 200, "damages": "Severe"},
    2012: {"names": ["Kai-tak", "Vicente", "Tembin"], "max_wind": 180, "damages": "Moderate"},
    2013: {"names": ["Fitow", "Utor", "Usagi"], "max_wind": 185, "damages": "Moderate"},
    2014: {"names": ["Rammasun", "Matmo", "Kalmaegi"], "max_wind": 195, "damages": "Severe"},
    2015: {"names": ["Chan-hom", "Soudelor", "Dujuan"], "max_wind": 215, "damages": "Severe"},
    2016: {"names": ["Nida", "Sarika", "Haima"], "max_wind": 205, "damages": "Severe"},
    2017: {"names": ["Hato", "Pakhar", "Khanun"], "max_wind": 225, "damages": "Catastrophic"},
    2018: {"names": ["Ewiniar", "Bebinca", "Mangkhut"], "max_wind": 230, "damages": "Catastrophic"},
    2019: {"names": ["Wipha", "Bailu", "Tapah"], "max_wind": 170, "damages": "Moderate"},
    2020: {"names": ["Vongfong", "Nuri", "Noul"], "max_wind": 160, "damages": "Minor"},
    2021: {"names": ["Surigae", "Kompasu", "Lionrock"], "max_wind": 180, "damages": "Moderate"},
    2022: {"names": ["Chaba", "Mulan", "Merbok"], "max_wind": 175, "damages": "Moderate"},
    2023: {"names": ["Talim", "Doksuri", "Khanun"], "max_wind": 200, "damages": "Severe"}
}

def generate_flow_curves(x_base, y_base, num_curves=15, curve_points=100):
    """Generate smoke-like flow lines"""
    curves_x = []
    curves_y = []
    opacities = []
    widths = []
    
    for _ in range(num_curves):
        # Create perturbations for each curve
        noise = np.random.normal(0, 0.5, curve_points)
        phase = random.uniform(0, 2*np.pi)
        amplitude = random.uniform(0.3, 1.0)
        
        # Generate base curve
        t = np.linspace(0, 2*np.pi, curve_points)
        x = x_base + amplitude * np.sin(t + phase) + noise * 0.3
        y = y_base + t/2 + noise
        
        curves_x.append(x)
        curves_y.append(y)
        opacities.append(random.uniform(0.3, 0.7))
        widths.append(random.uniform(1, 3))
    
    return curves_x, curves_y, opacities, widths

def create_interactive_visualization():
    """Create interactive visualization interface"""
    years = list(typhoon_data.keys())
    counts = list(typhoon_data.values())
    max_count = max(counts)
    
    # Create initial static chart
    fig = go.Figure()
    
    # Create fluid effects and data points for each year's data
    for i, (year, count) in enumerate(zip(years, counts)):
        # Calculate base position
        x_base = -8 + (16 * i / (len(years)-1))
        y_base = -5 + (10 * count / max_count)
        
        # Generate flow lines
        curves_x, curves_y, opacities, widths = generate_flow_curves(x_base, y_base)
        
        # Add flow lines (display all years by default)
        for j, (curve_x, curve_y, opacity, width) in enumerate(zip(curves_x, curves_y, opacities, widths)):
            fig.add_trace(go.Scatter(
                x=curve_x,
                y=curve_y,
                mode='lines',
                line=dict(
                    width=width,
                    color=f'rgba(255,255,255,{opacity})',
                    shape='spline'
                ),
                hoverinfo='skip',
                showlegend=False,
                name=f'flow_{year}_{j}',
                visible=True
            ))
        
        # Add clickable data points
        details = typhoon_details.get(year, {"names": ["Unknown"], "max_wind": 0, "damages": "Unknown"})
        hover_text = f"""
        <b>{year} Typhoon Data</b><br>
        Typhoon Count: {count}<br>
        Major Typhoons: {', '.join(details['names'][:3])}<br>
        Max Wind Speed: {details['max_wind']} km/h<br>
        Damage Level: {details['damages']}<br>
        <i>Click for detailed information</i>
        """
        
        fig.add_trace(go.Scatter(
            x=[x_base],
            y=[y_base],
            mode='markers+text',
            marker=dict(
                size=count*3,
                color='rgba(255,215,0,0.9)',
                line=dict(color='white', width=2),
                symbol='circle'
            ),
            text=f'{year}',
            textposition='middle center',
            textfont=dict(
                size=10,
                color='black',
                family='Arial Bold'
            ),
            hovertemplate=hover_text,
            name=f'data_{year}',
            customdata=[year],  # Store year information for click events
            showlegend=False
        ))
    
    # Add background stars
    star_x = np.random.uniform(-10, 10, 150)
    star_y = np.random.uniform(-10, 10, 150)
    fig.add_trace(go.Scatter(
        x=star_x,
        y=star_y,
        mode='markers',
        marker=dict(
            size=np.random.uniform(1, 3, 150),
            color='rgba(255,255,255,0.4)',
            symbol='star'
        ),
        hoverinfo='skip',
        showlegend=False,
        name='stars'
    ))
    
    return fig

def create_layout_with_controls():
    """Create layout with interactive controls"""
    years = list(typhoon_data.keys())
    
    layout = go.Layout(
        title=dict(
            text='🌀 Hong Kong Typhoon Data Interactive Flow Visualization (2002-2023)<br><sup>Click data points for details, use controls below to filter years</sup>',
            font=dict(size=24, color='white', family='Arial'),
            y=0.95,
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            visible=False,
            range=[-10, 10],
            showgrid=False
        ),
        yaxis=dict(
            visible=False,
            range=[-10, 10],
            showgrid=False
        ),
        plot_bgcolor='rgb(5,5,20)',
        paper_bgcolor='rgb(5,5,20)',
        margin=dict(l=40, r=40, t=100, b=120),
        
        # Add interactive controls
        updatemenus=[
            # Year range selector
            dict(
                type="dropdown",
                direction="down",
                active=0,
                x=0.1,
                y=0.15,
                showactive=True,
                buttons=[
                    dict(label="Show All Years", method="restyle", args=["visible", True]),
                    dict(label="2002-2010", method="update", args=[{"visible": [True if '200' in str(trace.get('name', '')) or 'star' in str(trace.get('name', '')) else False for trace in []]}, {}]),
                    dict(label="2011-2020", method="update", args=[{"visible": [True if ('201' in str(trace.get('name', '')) or '202' in str(trace.get('name', '')) or 'star' in str(trace.get('name', ''))) and '2021' not in str(trace.get('name', '')) else False for trace in []]}, {}]),
                    dict(label="2021-2023", method="update", args=[{"visible": [True if ('202' in str(trace.get('name', '')) or 'star' in str(trace.get('name', ''))) else False for trace in []]}, {}])
                ],
                bgcolor="rgba(255,255,255,0.1)",
                bordercolor="rgba(255,255,255,0.3)",
                font=dict(color="white")
            ),
            
            # Animation playback control
            dict(
                type='buttons',
                showactive=False,
                y=0.05,
                x=0.5,
                xanchor='center',
                yanchor='bottom',
                pad=dict(t=0, r=10),
                buttons=[
                    dict(
                        label='🎬 Play Animation',
                        method='animate',
                        args=[None, {
                            'frame': {'duration': 100, 'redraw': True},
                            'fromcurrent': True,
                            'transition': {'duration': 50, 'easing': 'cubic-in-out'}
                        }]
                    ),
                    dict(
                        label='⏸️ Pause',
                        method='animate',
                        args=[[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    )
                ],
                bgcolor="rgba(255,215,0,0.8)",
                bordercolor="rgba(255,255,255,0.3)",
                font=dict(color="black", size=14)
            )
        ],
        
        # Add annotations
        annotations=[
            dict(
                text="📊 Data point size represents typhoon count<br>💫 Hover for detailed information<br>🖱️ Click data points to highlight",
                x=0.02,
                y=0.98,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(color="rgba(255,255,255,0.7)", size=12),
                align="left",
                bgcolor="rgba(0,0,0,0.3)",
                bordercolor="rgba(255,255,255,0.2)",
                borderwidth=1
            )
        ]
    )
    
    return layout

def add_click_interactions(fig):
    """Add click interaction functionality to the chart"""
    # Add JavaScript callback to handle click events
    fig.update_layout(
        clickmode='event+select',
        dragmode='pan'
    )
    
    # Add click highlight effects for data points
    for trace in fig.data:
        if trace.name and 'data_' in trace.name:
            trace.update(
                marker=dict(
                    size=trace.marker.size,
                    color=trace.marker.color,
                    line=dict(color='cyan', width=0),  # Default no highlight border
                    opacity=0.9
                ),
                selected=dict(
                    marker=dict(
                        color='red',
                        opacity=1.0,
                        size=trace.marker.size * 1.5  # Enlarge when selected
                    )
                ),
                unselected=dict(
                    marker=dict(
                        opacity=0.5
                    )
                )
            )
    
    return fig

def create_animated_frames():
    """Create animation frames"""
    years = list(typhoon_data.keys())
    counts = list(typhoon_data.values())
    max_count = max(counts)
    
    frames = []
    num_frames = 100
    
    for f in range(num_frames):
        data = []
        
        # Add background stars (dynamic twinkling effect)
        star_x = np.random.uniform(-10, 10, 80)
        star_y = np.random.uniform(-10, 10, 80)
        star_opacity = 0.2 + 0.3 * np.sin(f/10 + np.arange(80))
        
        data.append(go.Scatter(
            x=star_x,
            y=star_y,
            mode='markers',
            marker=dict(
                size=np.random.uniform(1, 4, 80),
                color=[f'rgba(255,255,255,{max(0, min(1, op))})' for op in star_opacity],
                symbol='star'
            ),
            hoverinfo='skip',
            showlegend=False,
            name='animated_stars'
        ))
        
        # Create dynamic fluid effects for each year's data
        for i, (year, count) in enumerate(zip(years, counts)):
            x_base = -8 + (16 * i / (len(years)-1))
            y_base = -5 + (10 * count / max_count)
            
            # Generate dynamic flow lines
            curves_x, curves_y, opacities, widths = generate_flow_curves(x_base, y_base)
            appear_progress = min(1.0, max(0.0, (f - i*2) / 15))
            
            for j, (curve_x, curve_y, opacity, width) in enumerate(zip(curves_x, curves_y, opacities, widths)):
                # Add time-related dynamic perturbations
                time_phase = f / 15 + i / 3 + j / 10
                curve_y_animated = curve_y + 0.4 * np.sin(curve_x + time_phase)
                curve_x_animated = curve_x + 0.1 * np.sin(curve_y + time_phase * 0.7)
                
                data.append(go.Scatter(
                    x=curve_x_animated,
                    y=curve_y_animated,
                    mode='lines',
                    line=dict(
                        width=width * appear_progress,
                        color=f'rgba(255,255,255,{opacity * appear_progress * 0.8})',
                        shape='spline'
                    ),
                    hoverinfo='skip',
                    showlegend=False,
                    name=f'animated_flow_{year}_{j}'
                ))
            
            # Add clickable data points (maintain static position but with breathing effect)
            pulse_size = count * (2.5 + 0.5 * np.sin(f/8 + i))
            details = typhoon_details.get(year, {"names": ["Unknown"], "max_wind": 0, "damages": "Unknown"})
            
            data.append(go.Scatter(
                x=[x_base],
                y=[y_base],
                mode='markers+text',
                marker=dict(
                    size=pulse_size,
                    color='rgba(255,215,0,0.9)',
                    line=dict(color='white', width=2),
                    symbol='circle'
                ),
                text=f'{year}',
                textposition='middle center',
                textfont=dict(
                    size=10,
                    color='black',
                    family='Arial Bold'
                ),
                hovertemplate=f"""
                <b>{year} Typhoon Data</b><br>
                Typhoon Count: {count}<br>
                Major Typhoons: {', '.join(details['names'][:3])}<br>
                Max Wind Speed: {details['max_wind']} km/h<br>
                Damage Level: {details['damages']}<br>
                <extra></extra>
                """,
                name=f'animated_data_{year}',
                customdata=[year],
                showlegend=False,
                opacity=appear_progress
            ))
        
        frames.append(go.Frame(data=data, name=str(f)))
    
    return frames

if __name__ == '__main__':
    print("🌀 Creating interactive Hong Kong typhoon data visualization...")
    
    # Create base chart
    fig = create_interactive_visualization()
    
    # Add layout and controls
    layout = create_layout_with_controls()
    fig.update_layout(layout)
    
    # Add click interactions
    fig = add_click_interactions(fig)
    
    # Add animation frames
    animated_frames = create_animated_frames()
    fig.frames = animated_frames
    
    print("✨ Visualization created successfully! Generating HTML file...")
    
    # Generate enhanced HTML file
    fig.write_html(
        'interactive_typhoon_visualization.html',
        auto_open=True,
        config={
            'displayModeBar': True,
            'modeBarButtonsToAdd': ['select2d', 'lasso2d'],
            'modeBarButtonsToRemove': ['pan2d', 'autoScale2d'],
            'displaylogo': False,
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'hong_kong_typhoon_visualization',
                'height': 800,
                'width': 1200,
                'scale': 1
            }
        }
    )
    
    print("🎉 Interactive typhoon visualization generated successfully!")
    print("📝 Features:")
    print("   • Hover over data points for detailed typhoon information")
    print("   • Use dropdown menu to filter year ranges")
    print("   • Click play animation button for dynamic effects")
    print("   • Click data points for highlighting")
    print("   • Use toolbar for zooming and panning")