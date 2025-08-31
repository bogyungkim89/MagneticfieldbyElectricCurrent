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

# --------------------------------------------------------------------------------------------------
# 1. 직선 전류에 의한 자기장 (3D)
if simulation_type == "직선 전류":
    st.header("1. 직선 전류에 의한 자기장")
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
        line=dict(color='blue', width=I * 2),  # 전류 세기에 따라 굵기 조절
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
    line_width = B_r / (2e-7 * 5.0 / 0.5) * 10
    
    fig.add_trace(go.Scatter3d(
        x=x, y=y, z=z,
        mode='lines',
        line=dict(color='red', width=line_width),
        name='자기장 궤적'
    ))

    # 자기장 방향 화살표 (빨간색, 반시계 방향)
    arrow_angles = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    for i, angle in enumerate(arrow_angles):
        x_end = r_val * np.cos(angle)
        y_end = r_val * np.sin(angle)
        x_start = r_val * np.cos(angle + 0.1)
        y_start = r_val * np.sin(angle + 0.1)
        
        B_r = 2e-7 * I / r_val
        arrow_size = B_r / (2e-7 * 5.0 / 0.5) * 0.8
        
        fig.add_trace(go.Cone(
            x=[x_end], y=[y_end], z=[0],
            u=[x_end - x_start], v=[y_end - y_start], w=[0],
            sizemode="absolute", sizeref=arrow_size,
            showscale=False,
            colorscale=[[0, 'red'], [1, 'red']],
            name='자기장 방향' if i == 0 else ''
        ))

    # 자기장의 세기 계산 및 표시
    k = 2e-7
    B = k * I / r_val
    st.markdown(f"**자기장의 세기 (B)**: ${B:.2e}$ T")

    # 레이아웃 및 카메라 설정
    fig.update_layout(
        scene=dict(
            xaxis_title='X축', yaxis_title='Y축', zaxis_title='Z축',
            xaxis=dict(range=[-4, 4]), yaxis=dict(range=[-4, 4]), zaxis=dict(range=[-4, 4]),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------------------------------------------------------
# 2. 원형 전류에 의한 자기장 (3D)
elif simulation_type == "원형 전류":
    st.header("2. 원형 전류에 의한 자기장")
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
        name='원형 전류 (I)'
    ))
    
    # 전류 방향 화살표 (파란색)
    arrow_angles = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    for i, angle in enumerate(arrow_angles):
        x_end = r_val * np.cos(angle)
        y_end = r_val * np.sin(angle)
        x_start = r_val * np.cos(angle + 0.1)
        y_start = r_val * np.sin(angle + 0.1)
        fig.add_trace(go.Cone(
            x=[x_end], y=[y_end], z=[0],
            u=[x_end - x_start], v=[y_end - y_start], w=[0],
            sizemode="absolute", sizeref=I * 0.1,  # 전류 세기에 따라 화살표 크기 조절
            showscale=False,
            colorscale=[[0, 'blue'], [1, 'blue']],
            name='전류 방향' if i ==
