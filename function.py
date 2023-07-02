import math
from collections import deque
import random
import matplotlib.pyplot as plt
import numpy as np


def create_strengths(mean, variance):
    strengths = []
    for _ in range(5):
        value = random.gauss(mean, math.sqrt(variance))
        value = max(0, min(value, 10)) 
        strengths.append(value)
    return strengths

class Person:
    def __init__(self, id, strengths):
        self.id = id
        self.strengths = strengths
        self.assigned_job = None
        self.job_preferences = sorted(range(5), key=lambda j: self.strengths[j], reverse=True)
        self.original_job_preferences = self.job_preferences.copy() 
        
    @property
    def productivity(self):
        if self.assigned_job is not None:
            return self.strengths[self.assigned_job]
        else:
            return max(self.strengths)
        
    def nominate(self):
        self.assigned_job = np.argmax(self.strengths)

    def assign(self, job):
        self.assigned_job = job
        
def create_people(people_num, strength_mean, strength_variance):
    strength_mean_numbers = np.random.normal(loc=strength_mean, scale=math.sqrt(strength_variance), size=people_num)
    strength_mean_numbers = np.clip(strength_mean_numbers, 0, 10)
    strength_variance_numbers =[strength_variance for _ in range(people_num)]

    people=[]
    for idx, (mean,variance) in enumerate(zip(strength_mean_numbers, strength_variance_numbers)):
        strengths = create_strengths(mean, variance)
        person = Person(idx, strengths)  # Personのインスタンスを作成
        people.append(person)  # リストに追加
    return people

def simulate_assignment(people, job_coefficients):
    job_productivities = [0 for _ in range(5)]
    for job in sorted(range(5), key=lambda j: job_coefficients[j], reverse=True):
        candidates = sorted([p for p in people if p.assigned_job is None], key=lambda p: p.strengths[job], reverse=True)
        for person in candidates[:2]:
            person.assign(job)
        job_productivities[job] = sum([p.productivity for p in [candidates[0], candidates[1]] if p.assigned_job == job])
    total_productivity = sum(job_productivities[i] * job_coefficients[i] for i in range(5))
    return total_productivity

def simulate_nomination(people, job_coefficients):
    for person in people:
        person.nominate()

    while True:
        overfilled_jobs = [job for job in range(5) if sum(p.assigned_job == job for p in people) > 2]
        if not overfilled_jobs:
            break

        for job in overfilled_jobs:
            candidates = sorted([p for p in people if p.assigned_job == job], key=lambda p: p.strengths[job] - sorted(p.strengths)[-2], reverse=False)
            candidate_to_resign = candidates[0]
            candidate_to_resign.assigned_job = None
            for preference in candidate_to_resign.job_preferences:
                if sum(p.assigned_job == preference for p in people) < 2:
                    candidate_to_resign.assigned_job = preference
                    break

    job_productivities = [0 for _ in range(5)]
    for job in range(5):
        candidates = [p for p in people if p.assigned_job == job]
        if candidates:
            job_productivities[job] = sum(sorted([p.productivity for p in candidates], reverse=True)[:2])

    total_productivity = sum(job_productivities[i] * job_coefficients[i] for i in range(5))
    return total_productivity

def simulate_stable_matching(people,job_coefficients):
    free_people = set(people)
    
    # Gale-Shapley algorithm
    while free_people:
        person = free_people.pop() 

        while person.job_preferences:  
            job = person.job_preferences.pop(0)
            candidates = [p for p in people if p.assigned_job == job]

            # If the job is not full
            if sum(p.assigned_job == job for p in people) < 2:
                person.assign(job)
                break
            else:
                least_preferred = min(candidates, key=lambda p: p.strengths[job])
                if person.strengths[job] > least_preferred.strengths[job]:
                    least_preferred.assigned_job = None
                    person.assign(job)
                    free_people.add(least_preferred)  
                    break
                else:
                    pass

    # After Gale-Shapley algorithm
    unassigned_people = [person for person in people if person.assigned_job is None]
    unfilled_jobs = [i for i in range(5) if sum(p.assigned_job == i for p in people) < 2]

    for person in unassigned_people:
        if unfilled_jobs: 
            job = unfilled_jobs.pop(0) 
            person.assign(job) 
        else:
            pass
#             print(f"Person {person.id} could not be assigned a job.")

    job_productivities = [0 for _ in range(5)]
    for job in range(5):
        candidates = [p for p in people if p.assigned_job == job]
        if candidates:
            job_productivities[job] = sum(sorted([p.productivity for p in candidates], reverse=True)[:2])

    total_productivity = sum(job_productivities[i] * job_coefficients[i] for i in range(5))
    return total_productivity

def random_coefficients():
    coefficients = [random.random() for _ in range(5)]
    total = sum(coefficients)
    return [c / total for c in coefficients]

def calculate_self_choice(people):
    return sum([1 if person.assigned_job == person.original_job_preferences[0] else 0 for person in people]) / len(people)

def perform_simulation(strength_mean, strength_variance, num_trials):
    
    nomination_productivities = []
    assignment_productivities = []
    stable_matching_productivities = []
    nomination_self_choices = []
    assignment_self_choices = []
    stable_matching_self_choices = []
    average_strengths_per_trial = []
    average_std_by_person_strengths_per_trial = []
    average_std_in_person_strengths_per_trial=[]
    people_list_per_trial = []

    for i in range(num_trials):
        # ５つの仕事の重要度を設定（ランダムに行う）
        job_coefficients = random_coefficients()
        #10人の人を作成（得意分野の平均と分散から設定する。ただし、皆が均等にならないように分散させる）
        people = create_people(10, strength_mean, strength_variance)
        people_by_trial=[]
        for person in people:
             people_by_trial.append(person.strengths)
        people_list_per_trial.append(people_by_trial)
        
        average_strengths = [sum(person.strengths) / len(person.strengths) for person in people]
        average_strength = sum(average_strengths) / len(people)
        average_strengths_per_trial.append(average_strength)
        
        average_std_by_person_strength = math.sqrt(sum([(strength - average_strength) ** 2 for strength in average_strengths]) / len(average_strengths))
        average_std_by_person_strengths_per_trial.append(average_std_by_person_strength)

        std_in_person_strengths = [math.sqrt(sum([(strength - sum(person.strengths)/len(person.strengths))**2 for strength in person.strengths]) / len(person.strengths)) for person in people]
        average_std_in_person_strengths = sum(std_in_person_strengths) / len(std_in_person_strengths)
        average_std_in_person_strengths_per_trial.append(average_std_in_person_strengths)
        
        # みんなで決める方式
        nomination_productivities.append(simulate_nomination(people, job_coefficients))
        nomination_self_choices.append(calculate_self_choice(people))

        for person in people:
            person.assign(None)

        # トップダウン方式
        assignment_productivities.append(simulate_assignment(people, job_coefficients))
        assignment_self_choices.append(calculate_self_choice(people))
        
        for person in people:
            person.assign(None)

        # 安定マッチング方式
        stable_matching_productivities.append(simulate_stable_matching(people, job_coefficients))
        stable_matching_self_choices.append(calculate_self_choice(people))
        
        # Reset assignments
        for person in people:
            person.assign(None)

    # 生産性の値の取得
    average_nomination_productivity = sum(nomination_productivities) / num_trials
    average_assignment_productivity = sum(assignment_productivities) / num_trials
    average_stable_matching_productivity = sum(stable_matching_productivities) / num_trials

    # 自主選択の値の取得
    average_nomination_self_choice = sum(nomination_self_choices) / num_trials
    average_assignment_self_choice = sum(assignment_self_choices) / num_trials
    average_stable_matching_self_choice = sum(stable_matching_self_choices) / num_trials
    
    # 10人の平均の得意の指数の平均と標準偏差の取得
    average_strengths = sum(average_strengths_per_trial) / num_trials
    std_by_person_strengths = sum(average_std_by_person_strengths_per_trial) / num_trials
    std_in_person_strengths = sum(average_std_in_person_strengths_per_trial) / num_trials
    
    return (average_nomination_productivity, average_assignment_productivity, average_stable_matching_productivity, 
        average_nomination_self_choice, average_assignment_self_choice, average_stable_matching_self_choice,
        average_strengths, std_by_person_strengths,std_in_person_strengths,people_list_per_trial)