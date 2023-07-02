import matplotlib.pyplot as plt
import numpy as np
import japanize_matplotlib
from function import *

# みんなで決める方式の生産性の平均 #0
# トップダウン方式の生産性の平均 #1
# 安定マッチング方式の生産性の平均#2
# みんなで決める方式の自己決定比率の平均 #3
# トップダウン方式の自己決定比率の平均  #4
# 安定マッチング方式の自己決定比率の平均 #5
# 得意の指標の平均 #6
#  得意の指標の個人間の偏差 # 7
# 得意の指標の個人内の偏差  #8

strength_mean_values = list(range(0,11,1) )
strength_variance = 5
num_trials = 10000

results_nomination_mean = []
results_assignment_mean = []
results_stable_matching_mean = []

results_nomination_self_choice_mean = []
results_assignment_self_choice_mean = []
results_stable_matching_self_choice_mean = []

results_average_strengths = []
results_std_by_person_strengths = []
results_std_in_person_strengths = []
people_list = []

for mean in strength_mean_values:
    result = perform_simulation(mean, strength_variance, num_trials) 

    results_nomination_mean.append(result[0])  
    results_assignment_mean.append(result[1])  
    results_stable_matching_mean.append(result[2])  

    results_nomination_self_choice_mean.append(result[3])  
    results_assignment_self_choice_mean.append(result[4])  
    results_stable_matching_self_choice_mean.append(result[5])  

    results_average_strengths.append(result[6])  
    results_std_by_person_strengths.append(result[7])  
    results_std_in_person_strengths.append(result[8])

    people_list.append(result[9])

# Create a new figure and a subplot
fig, ax1 = plt.subplots()

# First plot with solid line and circle marker
line1, = ax1.plot(results_average_strengths[3:], 
                  (np.array(results_assignment_mean)[3:]-np.array(results_stable_matching_mean)[3:])/np.array(results_assignment_mean)[3:]* 100, 
                  marker='o', markersize=5, linestyle='-', color='k', label='生産性の差異(%)')

# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('生産性の差異(%)')
ax1.tick_params('y', colors='k')

# Create a second y-axis that shares the same x-axis
ax2 = ax1.twinx()

# Second plot with dashed line and square marker
line2, = ax2.plot(results_average_strengths[3:],results_std_by_person_strengths[3:]/np.array([5,5,5,5,5,5,5,5])* 100,
                  marker='s', markersize=5, linestyle='--', color='k', label='個人間のスキルの偏差(%)')

ax2.set_ylabel('個人間のスキルの差異(%)')
ax2.tick_params('y', colors='k')

# Remove x-axis label
ax1.set_xlabel('10人の平均スキル値（10段階）')

# No title
plt.title('')

# Legend
fig.legend(loc="lower left", bbox_to_anchor=(0,0), bbox_transform=ax1.transAxes)

# Output as png
plt.savefig("TopdownVsAlltogether.png", format='png', dpi=300)

plt.show()

fig, ax = plt.subplots()

# First plot with solid line and circle marker
line1, = ax.plot(results_average_strengths[3:], 
                 np.array(results_assignment_self_choice_mean[3:] )* 100, 
                 marker='o', markersize=5, linestyle='-', color='k', label='トップダウン方式')

# Second plot with dashed line and square marker
line2, = ax.plot(results_average_strengths[3:], 
                 np.array(results_nomination_self_choice_mean[3:]) * 100, 
                 marker='s', markersize=5, linestyle='--', color='k', label='みんなで決める方式')

# Set y-axis label
ax.set_ylabel('自分の得意が仕事になった比率(%)')

ax.set_xlabel('10人の平均スキル値（10段階）')

ax.set_ylim(0,100)

# Get current handles and labels
handles, labels = ax.get_legend_handles_labels()

# Reverse the order
ax.legend(handles[::-1], labels[::-1], loc='lower right', bbox_to_anchor=(1, 0))


# No title
plt.title('')

# Output as png
plt.savefig("TopdownVsAlltogether2.png", format='png', dpi=300)

plt.show()
