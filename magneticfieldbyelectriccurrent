import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.animation import FuncAnimation

# Streamlit 앱 제목 설정
st.title("전류에 의한 자기장 시뮬레이션")
st.markdown("전류의 흐름과 그에 의해 발생하는 자기장을 시각적으로 체험해보세요.")

# 시뮬레이션 선택
st.sidebar.header("시뮬레이션 선택")
simulation_type = st.sidebar.radio(
    "시뮬레이션 유형을 선택하세요.",
    ("직선 전류", "원형 전류", "솔레노이드")
)

# --------------------------------------------------------------------------------------------------
# 공통 스타일 설정
plt.style.use('dark_background')

def animate_arrows(ax, arrows, direction, speed, color):
    """화살표를 움직이는 애니메이션 함수"""
    for arrow in arrows:
        if direction == 'inward':
            arrow.set_xdata(arrow.get_xdata() - speed)
            if np.all(arrow.get_xdata() < -5):
                arrow.set_xdata(arrow.get_xdata() + 10)
        elif direction == 'outward':
            arrow.set_xdata(arrow.get_xdata() + speed)
            if np.all(arrow.get_xdata() > 5):
                arrow.set_xdata(arrow.get_xdata() - 10)
        elif direction == 'up':
            arrow.set_ydata(arrow.get_ydata() + speed)
            if np.all(arrow.get_ydata() > 5):
                arrow.set_ydata(arrow.get_ydata() - 10)
        elif direction == 'down':
            arrow.set_ydata(arrow.get_ydata() - speed)
            if np.all(arrow.get_ydata() < -5):
                arrow.set_ydata(arrow.get_ydata() + 10)
        elif direction == 'clockwise':
            theta = np.arctan2(arrow.get_ydata(), arrow.get_xdata()) - speed
            r = np.sqrt(arrow.get_xdata()**2 + arrow.get_ydata()**2)
            arrow.set_xdata(r * np.cos(theta))
            arrow.set_ydata(r * np.sin(theta))
        elif direction == 'counter-clockwise':
            theta = np.arctan2(arrow.get_ydata(), arrow.get_xdata()) + speed
            r = np.sqrt(arrow.get_xdata()**2 + arrow.get_ydata()**2)
            arrow.set_xdata(r * np.cos(theta))
            arrow.set_ydata(r * np.sin(theta))

# --------------------------------------------------------------------------------------------------
# 직선 전류 시뮬레이션
if simulation_type == "직선 전류":
    st.header("1. 직선 전류에 의한 자기장")
    st.markdown("수직 도선에 흐르는 전류와 그 주변에 형성되는 원형 자기장을 시뮬레이션합니다.")
    
    # 사용자 입력
    I = st.slider("전류의 세기 (I)", 0.1, 5.0, 2.0)
    r_val = st.slider("도선으로부터의 거리 (r)", 0.1, 5.0, 1.0)
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.set_xlim(-6, 6)
    ax.set_ylim(-6, 6)
    ax.axis('off')

    # 도선 (파란색)
    ax.plot([0, 0], [-5, 5], color='blue', linewidth=3)
    
    # 전류 화살표 (파란색, 위쪽 방향)
    current_arrow = FancyArrowPatch((0, -4), (0, -3), mutation_scale=20, color='blue', arrowstyle='->')
    ax.add_patch(current_arrow)
    
    # 자기장 선 (빨간색)
    theta = np.linspace(0, 2 * np.pi, 100)
    r = np.linspace(1, 5, 5)  # 여러 개의 자기장 선
    for rad in r:
        ax.plot(rad * np.cos(theta), rad * np.sin(theta), color='red', linestyle='--')
        
    # 자기장 화살표 (빨간색, 반시계 방향)
    arrow_positions = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    magnetic_field_arrows = []
    for rad in r:
        for angle in arrow_positions:
            x = rad * np.cos(angle)
            y = rad * np.sin(angle)
            dx = -y * 0.1
            dy = x * 0.1
            arrow = FancyArrowPatch((x, y), (x + dx, y + dy), mutation_scale=15, color='red', arrowstyle='->')
            ax.add_patch(arrow)
            magnetic_field_arrows.append(arrow)

    # 자기장의 세기 계산 및 표시
    k = 2e-7  # 비례상수 (SI 단위)
    B = k * I / r_val
    st.markdown(f"**자기장의 세기 (B)**: ${B:.2e}$ T")
    st.pyplot(fig)

# --------------------------------------------------------------------------------------------------
# 원형 전류 시뮬레이션
elif simulation_type == "원형 전류":
    st.header("2. 원형 전류에 의한 자기장")
    st.markdown("원형 도선에 흐르는 전류와 그 중심에서 발생하는 자기장을 시뮬레이션합니다.")
    
    # 사용자 입력
    I = st.slider("전류의 세기 (I)", 0.1, 5.0, 2.0)
    r_val = st.slider("원형 전류의 반지름 (r)", 0.5, 3.0, 1.5)
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axis('off')

    # 원형 도선 (파란색)
    circle = plt.Circle((0, 0), r_val, color='blue', fill=False, linewidth=3)
    ax.add_artist(circle)
    
    # 전류 화살표 (파란색, 반시계 방향)
    num_arrows = 10
    angles = np.linspace(0, 2 * np.pi, num_arrows, endpoint=False)
    for angle in angles:
        x_start = r_val * np.cos(angle)
        y_start = r_val * np.sin(angle)
        dx = -r_val * np.sin(angle) * 0.1
        dy = r_val * np.cos(angle) * 0.1
        arrow = FancyArrowPatch((x_start, y_start), (x_start + dx, y_start + dy), mutation_scale=15, color='blue', arrowstyle='->')
        ax.add_patch(arrow)
    
    # 자기장 화살표 (빨간색, 위로)
    B_arrow = FancyArrowPatch((0, -2), (0, 2), mutation_scale=20, color='red', arrowstyle='<->', linestyle='--')
    ax.add_patch(B_arrow)

    # 자기장의 세기 계산 및 표시
    k_prime = 2e-7 * np.pi  # 비례상수 (SI 단위)
    B = k_prime * I / r_val
    st.markdown(f"**자기장의 세기 (B)**: ${B:.2e}$ T")
    st.pyplot(fig)

# --------------------------------------------------------------------------------------------------
# 솔레노이드 시뮬레이션
elif simulation_type == "솔레노이드":
    st.header("3. 솔레노이드에 의한 자기장")
    st.markdown("솔레노이드 내부에 형성되는 균일한 자기장을 시뮬레이션합니다.")

    # 사용자 입력
    I = st.slider("전류의 세기 (I)", 0.1, 5.0, 2.0)
    n = st.slider("단위 길이당 코일 감은 수 (n)", 10, 100, 50)
    
    # 그래프 생성
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_xlim(-5, 5)
    ax.set_ylim(-2, 2)
    ax.axis('off')

    # 솔레노이드 코일 (파란색)
    x = np.linspace(-4, 4, 100)
    y = np.sin(x * n / 10) * 0.5
    ax.plot(x, y, color='blue', linewidth=2)
    
    # 전류 화살표 (파란색, 위쪽)
    ax.arrow(-4, 0.5, 0, 0.5, head_width=0.2, head_length=0.2, fc='blue', ec='blue')
    ax.text(-4, 1.2, "I", color='blue', fontsize=16)

    # 솔레노이드 내부 자기장 (빨간색, 왼쪽 방향)
    num_arrows = 5
    for i in range(num_arrows):
        start_x = 4
        end_x = -4
        y_pos = np.linspace(-0.5, 0.5, num_arrows)[i]
        
        arrow = FancyArrowPatch((start_x, y_pos), (end_x, y_pos), mutation_scale=15, color='red', arrowstyle='<->', linestyle='--')
        ax.add_patch(arrow)
        
    # 자기장의 세기 계산 및 표시
    k_double_prime = 4 * np.pi * 1e-7  # 비례상수 (투자율)
    B = k_double_prime * n * I
    st.markdown(f"**자기장의 세기 (B)**: ${B:.2e}$ T")
    st.pyplot(fig)
