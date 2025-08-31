import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Streamlit 앱 제목 설정
st.title("전류에 의한 자기장 3D 시뮬레이션")
st.markdown("전류와 자기장의 세기에 따라 굵기가 달라지는 3차원 시뮬레이션입니다.")

# 시뮬레이션 선택
st.sidebar.header("시뮬레이션 선택")
simulation_type = st.sidebar.radio(
    "시뮬레이션 유형을 선택하세요.",
    ("직선 전류", "원형 전류", "솔레노이드")
)

# 그래프 설정 (다운로드, 초기화, 전체화면 버튼만 남김)
config = {
    'displaylogo': False,
    'modeBarButtonsToRemove': [
        'zoom', 'pan', 'select2d', 'lasso2d', 'zoomIn2d', 'zoomOut2d',
        'autoScale2d', 'resetScale2d', 'hoverClosestCartesian',
        'hoverCompareCartesian', 'zoom3d', 'pan3d', 'orbitRotation',
        'tableRotation', 'handleDrag3d'
    ]
}

# --------------------------------------------------------------------------------------------------
# 1. 직선 전류에 의한 자기장 (3D)
if simulation_type == "직선 전류":
    # 제목 변경
    st.header("1. 직선 전류에 의한 자기장")
    st.markdown("<span style='font-size: 150%;'> $$B=k\\frac{I}{r}$$", unsafe_allow_html=True)
    st.markdown("수직 도선에 흐르는 전류와 주변에 형성되는 자기장을 3차원으로 보여줍니다.")

    # 사용자 입력 (슬라이더)
    I = st.slider("전류의 세기 (I)", 0.1, 5.0, 2.0, help="자기장의 세기와 전류 선의 굵기에 영향을 줍니다.")
    r_val = st.slider("도선으로부터의 거리 (r)", 0.5, 3.0, 1.5, help="자기장 궤적의 반지름을 조절합니다.")

    # 3D 그래프 생성
    fig = go.Figure()

    # 전류가 흐르는 직선 도선 (파란색)
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-5, 5],
        mode='lines',
        line=dict(color='blue', width=I * 2),
        name='전류 (I)'
    ))
    
    # 전류 방향 화살표 (파란색)
    fig.add_trace(go.Cone(
        x=[0], y=[0], z=[4],
        u=[0], v=[0], w=[1],
        sizemode="absolute", sizeref=0.5,
        showscale=False,
        colorscale=[[0, 'blue'], [1, 'blue']],
        name='전류 방향'
    ))

    # 자기장 궤적 (빨간색)
    theta = np.linspace(0, 2 * np.pi, 100)
    x = r_val * np.cos(theta)
    y = r_val * np.sin(theta)
    z = np.zeros_like(theta)
    
    B_r = 2e-7 * I / r_val
    line_width = B_r / (2e-7 * 5.0 / 0.5) * 10 * 3
    
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color='red', width=line_width),
        name='자기장 (B)'
    ))

    # 자기장 방향 화살표 (빨간색, 시계 방향)
    arrow_angles = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    for i, angle in enumerate(arrow_angles):
        x_end = r_val * np.cos(angle)
        y_end = r_val * np.sin(angle)
        x_start = r_val * np.cos(angle + 0.1)
        y_start = r_val * np.sin(angle + 0.1)
        
        B_r = 2e-7 * I / r_val
        arrow_size = B_r / (2e-7 * 5.0 / 0.5) * 3.0
        
        fig.add_trace(go.Cone(
            x=[x_end], y=[y_end], z=[0],
            u=[x_start - x_end], v=[y_start - y_end], w=[0],
            sizemode="absolute", sizeref=arrow_size,
            showscale=False,
            colorscale=[[0, 'red'], [1, 'red']],
            name='자기장 방향' if i == 0 else ''
        ))

    # 레이아웃 및 카메라 설정
    fig.update_layout(
        scene=dict(
            xaxis_title='X축', yaxis_title='Y축', zaxis_title='Z축',
            xaxis=dict(showticklabels=False, range=[-4, 4]), 
            yaxis=dict(showticklabels=False, range=[-4, 4]), 
            zaxis=dict(showticklabels=False, range=[-4, 4]),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig, use_container_width=True, config=config)

# --------------------------------------------------------------------------------------------------
# 2. 원형 전류에 의한 자기장 (3D)
elif simulation_type == "원형 전류":
    # 제목 변경
    st.header("2. 원형 전류에 의한 자기장 ($B=k'(I/r)$, $k'=\pi k$)")
    st.markdown("원형 도선에 흐르는 전류와 중심을 뚫고 나오는 자기장을 3차원으로 보여줍니다.")

    # 사용자 입력 (슬라이더)
    I = st.slider("전류의 세기 (I)", 0.1, 5.0, 2.0, help="자기장의 세기와 전류 선의 굵기에 영향을 줍니다.")
    r_val = st.slider("원형 전류의 반지름 (r)", 0.5, 3.0, 1.5, help="원형 도선의 크기를 조절합니다.")
    
    # 3D 그래프 생성
    fig = go.Figure()

    # 원형 도선 (파란색)
    theta = np.linspace(0, 2 * np.pi, 100)
    x = r_val * np.cos(theta) 
    y = r_val * np.sin(theta) 
    z = np.zeros_like(theta)
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color='blue', width=I * 2),
        name='전류 (I)'
    ))
    
    # 전류 방향 화살표 (파란색, 반시계 방향)
    arrow_angles = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    for i, angle in enumerate(arrow_angles):
        x_end = r_val * np.cos(angle)
        y_end = r_val * np.sin(angle)
        x_start = r_val * np.cos(angle + 0.1)
        y_start = r_val * np.sin(angle + 0.1)
        fig.add_trace(go.Cone(
            x=[x_end], y=[y_end], z=[0],
            u=[x_start - x_end], v=[y_start - y_end], w=[0],
            sizemode="absolute", sizeref=I * 0.3, 
            showscale=False,
            colorscale=[[0, 'blue'], [1, 'blue']],
            name='전류 방향' if i == 0 else ''
        ))

    # 자기장 (빨간색)
    k_prime = 2e-7 * np.pi
    B = k_prime * I / r_val
    line_width = B / (k_prime * 5.0 / 0.5) * 10
    
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[-5, 5],
        mode='lines',
        line=dict(color='red', width=line_width),
        name='자기장 (B)'
    ))

    # 자기장 화살표
    arrow_size = B / (k_prime * 5.0 / 0.5) * 3.0 
    fig.add_trace(go.Cone(
        x=[0], y=[0], z=[4],
        u=[0], v=[0], w=[1],
        sizemode="absolute", sizeref=arrow_size,
        showscale=False,
        colorscale=[[0, 'red'], [1, 'red']],
        name='자기장 방향'
    ))

    # 레이아웃 및 카메라 설정
    fig.update_layout(
        scene=dict(
            xaxis_title='X축', yaxis_title='Y축', zaxis_title='Z축',
            xaxis=dict(showticklabels=False, range=[-4, 4]), 
            yaxis=dict(showticklabels=False, range=[-4, 4]), 
            zaxis=dict(showticklabels=False, range=[-4, 4]),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig, use_container_width=True, config=config)

# --------------------------------------------------------------------------------------------------
# 3. 솔레노이드에 의한 자기장 (3D)
elif simulation_type == "솔레노이드":
    # 제목 변경
    st.header("3. 솔레노이드에 의한 자기장 ($B=k''(I/r)$, $k''=2k'=2\pi k$)")
    st.markdown("원통형 코일에 흐르는 전류와 내부의 균일한 자기장을 3차원으로 보여줍니다.")

    # 사용자 입력 (슬라이더)
    I = st.slider("전류의 세기 (I)", 0.1, 5.0, 2.0, help="자기장의 세기와 전류 선의 굵기에 영향을 줍니다.")
    n = st.slider("단위 길이당 코일 감은 수 (n)", 10, 100, 50, help="자기장의 세기와 솔레노이드의 빽빽한 정도에 영향을 줍니다.")
    
    # 솔레노이드 반지름을 1.7로 고정
    r_val = 1.7

    # 3D 그래프 생성
    fig = go.Figure()

    # 솔레노이드 코일 (파란색)
    num_points = 200
    coil_length = 6 # 코일 길이 고정
    
    # n 값에 따라 theta의 범위를 변경하여 빽빽한 정도 조절
    theta = np.linspace(0, n / 5 * 2 * np.pi, num_points) 
    
    # 코일을 y축에 나란하게 그리기 위해 x와 z를 코사인/사인으로 설정 (크기 일정하게 유지)
    y_coil = np.linspace(-coil_length/2, coil_length/2, num_points)
    x_coil = r_val * np.cos(theta) # r_val 고정
    z_coil = r_val * np.sin(theta) # r_val 고정
    
    fig.add_trace(go.Scatter3d(
        x=x_coil, y=y_coil, z=z_coil,
        mode='lines',
        line=dict(color='blue', width=I * 2),
        name='전류 (I)'
    ))

    # 코일 방향 화살표 (파란색)
    num_arrows = 10
    for i in range(num_arrows):
        y_pos = np.linspace(-2.5, 2.5, num_arrows)[i]
        angle = np.interp(y_pos, y_coil, theta)
        
        # 수정: np.cos(angle + 0.1)의 닫는 괄호 추가
        x_end = r_val * np.cos(angle)
        z_end = r_val * np.sin(angle)
        x_start = r_val * np.cos(angle + 0.1)
        z_start = r_val * np.sin(angle + 0.1)
        
        fig.add_trace(go.Cone(
            x=[x_end], y=[y_pos], z=[z_end],
            u=[x_end - x_start], v=[0], w=[z_end - z_start],
            sizemode="absolute", sizeref=0.5,
            showscale=False,
            colorscale=[[0, 'blue'], [1, 'blue']],
            name='코일 전류 방향' if i == 0 else ''
        ))
    
    # 솔레노이드 내부 자기장 (빨간색)
    # 자기장 방향을 y축에 나란하게 설정
    mu_0 = 4 * np.pi * 1e-7
    B = mu_0 * n * I
    arrow_size = B / (mu_0 * 100 * 5.0) * 1.5
    line_width = B / (mu_0 * 100 * 5.0) * 10

    # 솔레노이드의 반지름에 맞춰 자기장 궤적 범위를 조정
    x_positions = np.linspace(-r_val * 0.5, r_val * 0.5, 3)  
    z_positions = np.linspace(-r_val * 0.5, r_val * 0.5, 3)  
    
    # 자기장 궤적의 길이를 코일 길이(6)보다 길게 설정
    y_range = np.linspace(-4, 4, 50)  

    for col_idx, x_pos in enumerate(x_positions):
        for row_idx, z_pos in enumerate(z_positions):
            # 자기장 궤적 (직선)
            fig.add_trace(go.Scatter3d(
                x=np.full_like(y_range, x_pos),
                y=y_range,
                z=np.full_like(y_range, z_pos),
                mode='lines',
                line=dict(color='red', width=line_width),
                # 첫 번째 선분만 legend에 표시
                showlegend=True if (col_idx == 0 and row_idx == 0) else False,
                name='자기장 (B)'
            ))
            
            # 자기장 화살표 (각 궤적 위에 3개)
            # 궤적의 새로운 범위에 맞춰 화살표 위치를 조정
            y_arrow_positions = np.linspace(-3.5, 3.5, 3)  
            for y_arrow_pos in y_arrow_positions:
                fig.add_trace(go.Cone(
                    x=[x_pos], y=[y_arrow_pos], z=[z_pos],
                    u=[0], v=[1], w=[0],
                    sizemode="absolute", sizeref=arrow_size,
                    showscale=False,
                    colorscale=[[0, 'red'], [1, 'red']],
                    name='자기장 화살표' if (col_idx == 0 and row_idx == 0 and y_arrow_pos == y_arrow_positions[0]) else ''
                ))

    # 레이아웃 및 카메라 설정
    fig.update_layout(
        scene=dict(
            xaxis_title='X축', yaxis_title='Y축', zaxis_title='Z축',
            # 축 범위도 자기장 범위에 맞게 조정
            xaxis=dict(showticklabels=False, range=[-4, 4]),  
            yaxis=dict(showticklabels=False, range=[-4, 4]),  
            zaxis=dict(showticklabels=False, range=[-4, 4]),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig, use_container_width=True, config=config)
