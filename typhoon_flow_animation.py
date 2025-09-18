import plotly.graph_objects as go
import numpy as np
import random

# Typhoon data from 2002 to 2023
typhoon_data = {
    2002: 6, 2003: 7, 2004: 5, 2005: 8, 2006: 7, 2007: 9, 2008: 6, 2009: 5,
    2010: 7, 2011: 8, 2012: 6, 2013: 7, 2014: 5, 2015: 8, 2016: 7, 2017: 9,
    2018: 8, 2019: 6, 2020: 5, 2021: 7, 2022: 6, 2023: 8
}

def generate_flow_curves(x_base, y_base, num_curves=15, curve_points=100):
    """生成烟雾状的流线"""
    curves_x = []
    curves_y = []
    opacities = []
    widths = []
    
    for _ in range(num_curves):
        # 为每条曲线创建扰动
        noise = np.random.normal(0, 0.5, curve_points)
        phase = random.uniform(0, 2*np.pi)
        amplitude = random.uniform(0.3, 1.0)
        
        # 生成基础曲线
        t = np.linspace(0, 2*np.pi, curve_points)
        x = x_base + amplitude * np.sin(t + phase) + noise * 0.3
        y = y_base + t/2 + noise
        
        curves_x.append(x)
        curves_y.append(y)
        opacities.append(random.uniform(0.3, 0.7))
        widths.append(random.uniform(1, 3))
    
    return curves_x, curves_y, opacities, widths

def create_visualization():
    years = list(typhoon_data.keys())
    counts = list(typhoon_data.values())
    max_count = max(counts)
    
    # 创建动画帧
    frames = []
    num_frames = 120
    
    for f in range(num_frames):
        data = []
        time_factor = f / num_frames
        
        # 添加背景星星
        star_x = np.random.uniform(-10, 10, 100)
        star_y = np.random.uniform(-10, 10, 100)
        data.append(go.Scatter(
            x=star_x,
            y=star_y,
            mode='markers',
            marker=dict(
                size=np.random.uniform(1, 2, 100),
                color=['rgba(255,255,255,0.3)'] * 100
            ),
            hoverinfo='skip',
            showlegend=False
        ))
        
        # 为每年数据创建流体效果
        for i, (year, count) in enumerate(zip(years, counts)):
            # 计算基准位置
            x_base = -8 + (16 * i / (len(years)-1))
            y_base = -5 + (10 * count / max_count)
            
            # 生成流线
            curves_x, curves_y, opacities, widths = generate_flow_curves(x_base, y_base)
            
            # 计算出现时间
            appear_progress = min(1.0, max(0.0, (f - i*3) / 20))
            
            # 添加流线
            for curve_x, curve_y, opacity, width in zip(curves_x, curves_y, opacities, widths):
                # 添加动态效果
                phase = f / 20 + i / 2
                curve_y_animated = curve_y + 0.3 * np.sin(curve_x + phase)
                
                data.append(go.Scatter(
                    x=curve_x,
                    y=curve_y_animated,
                    mode='lines',
                    line=dict(
                        width=width,
                        color=f'rgba(255,255,255,{opacity * appear_progress})',
                        shape='spline'
                    ),
                    hoverinfo='skip',
                    showlegend=False
                ))
            
            # 添加年份标签和数据点
            data.append(go.Scatter(
                x=[x_base],
                y=[y_base],
                mode='markers+text',
                marker=dict(
                    size=count*2,
                    color='rgba(255,215,0,0.8)',
                    line=dict(color='white', width=1)
                ),
                text=f'{year}: {count}台风',
                textposition='top center',
                textfont=dict(
                    size=12,
                    color='white',
                    family='Arial'
                ),
                hoverinfo='text',
                showlegend=False,
                opacity=appear_progress
            ))
        
        frames.append(go.Frame(data=data, name=str(f)))
    
    # 创建布局
    layout = go.Layout(
        title=dict(
            text='香港台风数据流体图 (2002-2023)',
            font=dict(size=24, color='white', family='Arial'),
            y=0.95
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
    
    # 创建图表
    fig = go.Figure(
        data=frames[0].data,
        layout=layout,
        frames=frames[1:]
    )
    
    return fig

if __name__ == '__main__':
    fig = create_visualization()
    fig.write_html('typhoon_flow_animation.html', auto_open=True)
