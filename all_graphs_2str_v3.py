import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
from random import randint
import math

from file_writing import append_to_file
from file_parsing_v2 import parse_file, get_values_for_time

fig, axs = plt.subplots(2, 3, figsize=(12, 8))
graph_titles = [['График кажущейся температуры от времени', 'Кажущийся цвет каления стали во времени', 'Запланированная работа нагревателя во времени'], ['График реальной температуры от времени', 'Реальный цвет каления стали во времени', 'Реализованная работа нагревателя во времени']]
x_limit = 5
file_check_period = 1

def get_color(temp):
    if temp < 630:
       return '#800000'
    elif 630 <= temp < 680:
        return '#8B0000'
    elif 680 <= temp < 740:
        return '#A52A2A'
    elif 740 <= temp < 770:
        return '#B22222'
    elif 770 <= temp < 800:
        return '#DC143C'
    elif 800 <= temp < 850:
        return '#FF0000'
    elif 850 <= temp < 900:
        return '#FF4500'
    elif 900 <= temp < 950:
        return '#FF6347'
    elif 950 <= temp < 1000:
        return '#FF8C00'
    elif 1000 <= temp < 1100:
        return '#FFD700'
    elif 1100 <= temp < 1200:
        return '#FFFF00'
    elif 1200 <= temp < 1300:
        return '#FFFACD'
    elif temp > 1300:
        return '#FFFFFF'

for row_idx, ax_row in enumerate(axs):
    for col_idx, ax in enumerate(ax_row):
        if col_idx == 0:
            ax.set_xlim(0, x_limit)
            ax.set_ylim(300, 1000)
        elif col_idx == 1:
            ax.set_xlim(0, x_limit)
            ax.set_ylim(0, 0.5)
            ax.set_yticklabels([])
            ax.set_yticks([])
        elif col_idx == 2:
            ax.set_xlim(0, x_limit)
            ax.set_ylim(-1, 2)
            ax.set_yticklabels(['', '', 'Выкл.', '', 'Вкл.', ''])
        ax.set_title(graph_titles[row_idx][col_idx])

points = [[[], [], []], [[], [], []]]
req_quantities = [['temp_seeming', 'temp_seeming', 'state_true'], ['temp_true', 'temp_true', 'state_true']]

first_read = True
pos = 0
df = pd.DataFrame()

def update(frame):
    # if is_paused:
    #     return
        
    x_lim = 5
    time_p = 1
    pth = 'F1.txt'

    # global first_read
    # if first_read:
    #     print(1)
    #     df = parse_file(pth)
    #     first_read = False
    # else:
    #     print(2)
    #     df = update_df(pth)
    #     print(df)

    # df = parse_file(pth) if first_read else update_df(pth)

    global pos
    global df
    # df, pos = parse_file(pth, pos)
    if pos == 0:
        df, pos = parse_file(pth, pos)
    else:
        new_batch, pos = parse_file(pth, pos)
        df = df.append(new_batch)
    print(df)

    temp_tr = None
    temp_seem = None

    for row_idx, point_row in enumerate(points):
        for col_idx, point_list in enumerate(point_row):
            
            ax = axs[row_idx, col_idx]

            # Добавление без смещения
            if len(point_list) < x_lim:
                time_value = len(point_list) * time_p
                req_values = get_values_for_time(df, time_value)

                req_quantity = req_quantities[row_idx][col_idx]

                if req_values is not None:
                    req_value = req_values[req_quantity]
                    req_value = float(req_value)
                    if math.isnan(req_value):
                        req_value = None
                else:
                    req_value = None

                if (row_idx == 0 and col_idx == 1) or (row_idx == 1 and col_idx == 1):
                    if req_value is not None:
                        curr_color = get_color(req_value)
                    else:
                        curr_color = point_list[-1].get_facecolor()
                    color_rect = plt.Rectangle((len(point_list), 0), 1, 0.5, facecolor=curr_color)
                    ax.add_patch(color_rect)
                    point_list.append(color_rect)
                else:
                    if req_value is None:
                        req_value = point_list[-1].get_offsets().tolist()[0][1]
                    point = ax.scatter(len(point_list), req_value, color='black')
                    point_list.append(point)

                if row_idx == 0 and col_idx == 0:
                    temp_seem = req_value
                elif row_idx == 1 and col_idx == 0:
                    temp_tr = req_value

                for text in ax.texts:
                    text.remove()

                if row_idx == 1 and col_idx == 0:
                    ax.text(0.95, 0.95, f'Температура кажущаяся: {temp_seem:.2f}\nТемпература реальная: {temp_tr:.2f}', verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='black', fontsize=10)
                elif row_idx == 1 and col_idx == 2:
                    last_time = len(point_list) * time_p
                    # append_to_file('F1_generated.txt', time_value=last_time)

            # Добавление со смещением
            elif len(point_list) >= x_lim:
                if (row_idx == 0 and col_idx == 1) or (row_idx == 1 and col_idx == 1):
                    for rect in point_list:
                        rect.set_x(rect.get_x() - 1)
                    rect_del = point_list.pop(0)
                    rect_del.remove()
                else:
                    for point in point_list:
                        xy = point.get_offsets().tolist()[0]
                        point.set_offsets((xy[0] - 1, xy[1]))
                    point_del = point_list.pop(0)
                    point_del.remove()

                xticklabels = ax.get_xticklabels()
                new_xticklabels = [int(l.get_text()) + time_p for l in xticklabels]
                ax.set_xticks(range(x_lim + 1))
                ax.set_xticklabels(new_xticklabels)
                new_time = new_xticklabels[-1]
                time_value = new_time - time_p
                req_values = get_values_for_time(df, time_value)

                req_quantity = req_quantities[row_idx][col_idx]
                if req_values is not None:
                    req_value = req_values[req_quantity]
                    req_value = float(req_value)
                    if math.isnan(req_value):
                        req_value = None
                else:
                    req_value = None

                if (row_idx == 0 and col_idx == 1) or (row_idx == 1 and col_idx == 1):
                    if req_value is not None:
                        curr_color = get_color(req_value)
                    else:
                        curr_color = point_list[-1].get_facecolor()
                    color_rect = plt.Rectangle((x_lim - 1, 0), 1, 0.5, facecolor=curr_color)
                    ax.add_patch(color_rect)
                    point_list.append(color_rect)
                else:
                    if req_value is None:
                        req_value = point_list[-1].get_offsets().tolist()[0][1]
                    point = ax.scatter(len(point_list), req_value, color='black')
                    point_list.append(point)

                if row_idx == 0 and col_idx == 0:
                    temp_seem = req_value
                elif row_idx == 1 and col_idx == 0:
                    temp_tr = req_value

                for text in ax.texts:
                    text.remove()

                if row_idx == 1 and col_idx == 0:
                    ax.text(0.95, 0.95, f'Температура кажущаяся: {temp_seem:.2f}\nТемпература реальная: {temp_tr:.2f}', verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='black', fontsize=10)
                elif row_idx == 1 and col_idx == 2:
                    last_time = new_time
                    # append_to_file('F1_generated.txt', time_value=last_time)

            # Обновление линии
            if not ((row_idx == 0 and col_idx == 1) or (row_idx == 1 and col_idx == 1)):
                if hasattr(ax, 'line'):
                    ax.line.remove()
                ax.line = ax.plot([p.get_offsets().tolist()[0][0] for p in point_list],
                                [p.get_offsets().tolist()[0][1] for p in point_list], color='black')[0]

import warnings
warnings.filterwarnings("ignore")

path = 'F1.txt'
# append_to_file(path, time_value=0, select_all=True)

ani = FuncAnimation(fig, update, frames=range(10), interval=500)

is_paused = False
def pause_resume_animation(event):
    global is_paused
    if is_paused:
        is_paused = False
        ani.event_source.start()
    else:
        is_paused = True
        ani.event_source.stop()

fig.canvas.mpl_connect('button_press_event', pause_resume_animation)

plt.tight_layout()
plt.show()
