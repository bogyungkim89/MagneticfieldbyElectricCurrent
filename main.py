# --------------------------------------------------------------------------------------------------
# 3. 솔레노이드에 의한 자기장 (3D)
elif simulation_type == "솔레노이드":
    st.header("3. 솔레노이드에 의한 자기장")
    st.markdown("원통형 코일에 흐르는 전류와 내부의 균일한 자기장을 3차원으로 보여줍니다.")

    # 사용자 입력 (슬라이더)
    I = st.slider("전류의 세기 (I)", 0.1, 5.0, 2.0, help="자기장의 세기와 전류 선의 굵기에 영향을 줍니다.")
    n = st.slider("단위 길이당 코일 감은 수 (n)", 10, 100, 50, help="자기장의 세기와 솔레노이드의 빽빽한 정도에 영향을 줍니다.")
    
    # 3D 그래프 생성
    fig = go.Figure()

    # 솔레노이드 코일 (파란색)
    num_points = 200
    coil_length = 6 # 코일 길이 고정
    
    # n 값에 따라 theta의 범위를 변경하여 빽빽한 정도 조절
    theta = np.linspace(0, n / 5 * 2 * np.pi, num_points)  
    
    # 코일을 y축에 나란하게 그리기 위해 x와 z를 코사인/사인으로 설정
    y_coil = np.linspace(-coil_length/2, coil_length/2, num_points)
    x_coil = np.cos(theta)
    z_coil = np.sin(theta)
    
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
        
        x_end = np.cos(angle)
        z_end = np.sin(angle)
        x_start = np.cos(angle + 0.1)
        z_start = np.sin(angle + 0.1)
        
        fig.add_trace(go.Cone(
            x=[x_end], y=[y_pos], z=[z_end],
            u=[x_end - x_start], v=[0], w=[z_end - z_start],
            sizemode="absolute", sizeref=0.3,
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

    # 솔레노이드의 반지름은 1.0이므로, 내부에서만 궤적을 그리도록 범위를 줄입니다.
    x_positions = np.linspace(-0.5, 0.5, 3)  
    z_positions = np.linspace(-0.5, 0.5, 3)  
    
    # 자기장 궤적의 길이를 코일 길이(6)보다 길게 설정합니다.
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
                showlegend=False
            ))
            
            # 자기장 화살표 (각 궤적 위에 3개)
            # 궤적의 새로운 범위에 맞춰 화살표 위치를 조정합니다.
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
            xaxis=dict(showticklabels=False, range=[-2, 2]),  
            yaxis=dict(showticklabels=False, range=[-4, 4]),  
            zaxis=dict(showticklabels=False, range=[-2, 2]),
            aspectmode='cube'
        ),
        margin=dict(l=0, r=0, b=0, t=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig, use_container_width=True, config=config)
