import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib as mpl


def colorFader(c1,c2,mix=0):
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


def main():
    fig, ax = plt.subplots()
    ax.grid(True)
    c1='red'
    c2='green'

    cond = input('Введите условие остановки (по малости приращения чего? 0 - значения функции, 1 - аргумента): ')
    while cond not in ('0', '1'):
        print('Неверный ввод!')
        cond = input('Введите условие остановки (по малости приращения чего?): 0 - значения функции, 1 - аргумента: ')

    start_time = time.time()
    x0, y0 = 5, 5
    X = np.array([x0])
    Y = np.array([y0])
    D = np.array([((x0 - 4/3)**2 + (y0 - 4/3)**2)**(1/2)])

    xk, yk = x0, y0
    fk = float('infinity')
    fn = xk**2 + yk**2 - xk**3 - yk**3 + 2*xk*yk

    k = 1
    e = 0.001
    d = 0.001

    while True:
        xn = xk + 1/15*0.9**k * (2*xk - 3*xk**2 + 2*yk) # вычисление точек
        yn = yk + 1/15*0.9**k * (2*yk - 3*yk**2 + 2*xk)
        print(k)
        if (cond == '1' and abs(fk - fn) < e) or (cond == '0' and ((xn - xk)**2 + (yn - yk)**2)**(1/2) < d):
            break
        
        fk, fn = fn, xn**2 + yn**2 - xn**3 - yn**3 + 2*xn*yn # значения функции
        xk, yk = xn, yn
        X = np.append(X, xn)
        Y = np.append(Y, yn)
        D = np.append(D, [((4/3 - xk)**2 + (4/3 - yk)**2)**(1/2)]) # считаем, далеко ли от нужной точки (4/3, 4/3)
        k += 1

    var = X[-1]**2 + Y[-1]**2 - X[-1]**3 - Y[-1]**3 + 2*X[-1]*Y[-1]
    end_time = time.time()
    execution_time = end_time - start_time


    print("\n\nКритерий остановки: малость приращения " + 
            (f"значения функции (epsilon = {e})" if cond == '0' else f"аргумента (delta = {d})") + '\n')
    print(f'Количество итерация: {k}' + '\n')        
    print('Полученная точка:', f'{X[-1]}, {Y[-1]}\n')
    print(f"Значение функции: {var}\n")
    print(f"Время выполнения программы: {execution_time:5.5f} секунд\n")
    print(f"Отличие от требуемого результата: {D[-1]:5.4f}")

    ax.plot(X, D, label='График ошибки от координаты x')
    ax.legend()
    for i in range(1, k+1):
        label = f"Полученная точка: ({X[-1]:3.2f}, {Y[-1]:3.2f})\nЗначение функции: {var:3.2f}"
        ax.scatter(X[i-1], Y[i-1], color = colorFader(c1,c2,i/k), linewidth=1, 
                label = label if i == k else "")
        if i == k:
            ax.legend()
    plt.title(f"Остановка: " + ("функция" if cond == '0' else "аргумент") +
                f", итераций: {k}, ошибка: {D[-1]:3.3f}")
    plt.show()


if __name__ == "__main__":
    main()