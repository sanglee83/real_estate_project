import numpy as np
import matplotlib.pyplot as plt

# 파라미터 설정
tau_k = 0.5     # 시간상수
v = 3.0
k_u = 0.3
dt = 0.1
T_end = 5.0
N = int(T_end / dt)

# 초기값
k_exact = 0.0
theta_exact = 0.0

k_euler = 0.0
theta_euler = 0.0

t_list = []
theta_continuous_list = []
theta_exact_list = []
theta_euler_list = []

# 시뮬레이션 루프
for i in range(N+1):
    t = i*dt
    
    # -- (1) 연속시간 해(폐형해) 직접 계산
    # k(t)
    k_continuous = k_u + (0.0 - k_u)*np.exp(-t/tau_k)
    # theta(t)
    theta_continuous = v * (
        k_u*t
        + ( (0.0 - k_u)*tau_k )*(1 - np.exp(-t/tau_k))
    )
    
    t_list.append(t)
    theta_continuous_list.append(theta_continuous)
    theta_exact_list.append(theta_exact)
    theta_euler_list.append(theta_euler)
    
    if i < N:
        # -- (2) 정적분(Analytical Integration) 기반 이산화
        next_k_exact = k_u + (k_exact - k_u)*np.exp(-dt/tau_k)
        delta_theta_exact = v * (
            k_u*dt
            + ( (k_exact - k_u)*tau_k )*(1 - np.exp(-dt/tau_k))
        )
        next_theta_exact = theta_exact + delta_theta_exact
        
        k_exact = next_k_exact
        theta_exact = next_theta_exact
        
        # -- (3) 단순화(Euler) 기반 이산화
        next_k_euler = k_euler + (dt/tau_k)*(k_u - k_euler)
        next_theta_euler = theta_euler + v*k_euler*dt
        
        k_euler = next_k_euler
        theta_euler = next_theta_euler

# 그래프 그리기
plt.figure(figsize=(8,5))
plt.plot(t_list, theta_continuous_list, 'k-*', label='연속시간 해(정확해)')
plt.plot(t_list, theta_exact_list, 'r-',  label='정적분(이산화)')
plt.plot(t_list, theta_euler_list, 'b-.', label='단순화(Euler) 이산화')
plt.xlabel('time [s]')
plt.ylabel(r'$\delta \theta$')
plt.title('2초간 시뮬레이션 결과 비교')
plt.legend()
plt.grid(True)
plt.show()

# 정적분 vs 연속해, 오차의 크기
error_exact = theta_exact_list[-1] - theta_continuous_list[-1]
error_euler = theta_euler_list[-1] - theta_continuous_list[-1]
print(f"시뮬레이션 종료 시점(2초)에서:")
print(f"  - 정적분(이산화) 오차  : {error_exact: .6f}")
print(f"  - 단순화(Euler) 오차    : {error_euler: .6f}")
