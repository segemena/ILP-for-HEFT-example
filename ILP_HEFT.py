# Step 2 - Prepare Data
NbDags = 1
#Deadline =  48

PEs = ['P1', 'P2', 'P3']

Tasks = ['task_0', 'task_1', 'task_2', 'task_3', 'task_4',
             'task_5', 'task_6', 'task_7', 'task_8', 'task_9']

# =============================================================================
# # Task duration if executed on P1
# Task_Dur_P1 = [14, 13, 11, 13, 12, 13,  7,  5, 18, 21]
# 
# # Task duration if executed on P2
# Task_Dur_P2 = [16, 19, 13,  8, 13, 16, 15, 11, 12,  7]
# 
# # Task duration if executed on P3
# Task_Dur_P3 = [ 9, 18, 19, 17, 10,  9, 11, 14, 20, 16]
# =============================================================================

Functionality = [("P1","task_0",14),("P2","task_0",16),("P3","task_0", 9),
                 ("P1","task_1",13),("P2","task_1",19),("P3","task_1",18),
                 ("P1","task_2",11),("P2","task_2",13),("P3","task_2",19),
                 ("P1","task_3",13),("P2","task_3", 8),("P3","task_3",17),
                 ("P1","task_4",12),("P2","task_4",13),("P3","task_4",10),
                 ("P1","task_5",13),("P2","task_5",16),("P3","task_5", 9),
                 ("P1","task_6", 7),("P2","task_6",15),("P3","task_6",11),
                 ("P1","task_7", 5),("P2","task_7",11),("P3","task_7",14),
                 ("P1","task_8",18),("P2","task_8",12),("P3","task_8",20),
                 ("P1","task_9",21),("P2","task_9", 7),("P3","task_9",16)]

# =============================================================================
# Precedences = [("task_0", "task_1",18), ("task_0", "task_2",12),
#                ("task_0", "task_3", 9), ("task_0", "task_4",11),
#                ("task_0", "task_5",14), ("task_2", "task_6",23),  
#                ("task_1", "task_7",19), ("task_3", "task_7",27),
#                ("task_5", "task_7",15), ("task_1", "task_8",16),
#                ("task_3", "task_8",23), ("task_4", "task_8",13),  
#                ("task_6", "task_9",17), ("task_7", "task_9",11),
#                ("task_8", "task_9",13)]
# =============================================================================

Con_Precedence = [('P1',"task_0", "task_1", 18),('P2',"task_0", "task_1", 18),('P3',"task_0", "task_1", 18),
                  ('P1',"task_0", "task_2", 12),('P2',"task_0", "task_2", 12),('P3',"task_0", "task_2", 12),
                  ('P1',"task_0", "task_3",  9),('P2',"task_0", "task_3",  9),('P3',"task_0", "task_3",  9),
                  ('P1',"task_0", "task_4", 11),('P2',"task_0", "task_4", 11),('P3',"task_0", "task_4", 11),
                  ('P1',"task_0", "task_5", 14),('P2',"task_0", "task_5", 14),('P3',"task_0", "task_5", 14),
                  ('P1',"task_2", "task_6", 23),('P2',"task_2", "task_6", 23),('P3',"task_2", "task_6", 23),
                  ('P1',"task_1", "task_7", 19),('P2',"task_1", "task_7", 19),('P3',"task_1", "task_7", 19),
                  ('P1',"task_3", "task_7", 27),('P2',"task_3", "task_7", 27),('P3',"task_3", "task_7", 27),
                  ('P1',"task_5", "task_7", 15),('P2',"task_5", "task_7", 15),('P3',"task_5", "task_7", 15),
                  ('P1',"task_1", "task_8", 16),('P2',"task_1", "task_8", 16),('P3',"task_1", "task_8", 16),
                  ('P1',"task_3", "task_8", 23),('P2',"task_3", "task_8", 23),('P3',"task_3", "task_8", 23),
                  ('P1',"task_4", "task_8", 13),('P2',"task_4", "task_8", 13),('P3',"task_4", "task_8", 13),
                  ('P1',"task_6", "task_9", 17),('P2',"task_6", "task_9", 17),('P3',"task_6", "task_9", 17),
                  ('P1',"task_7", "task_9", 11),('P2',"task_7", "task_9", 11),('P3',"task_7", "task_9", 11),
                  ('P1',"task_8", "task_9", 13),('P2',"task_8", "task_9", 13),('P3',"task_8", "task_9", 13),]

nbPEs = len(PEs)
Dags = range(NbDags)

# Step 3 - Create the interval variables
import sys
from docplex.cp.model import *
mdl_2 = CpoModel()
import docplex.cp.utils_visu as visu
import matplotlib.pyplot as plt
plt.close("all")

tasks = {}
pe_tasks = {}
for d in Dags:
    for i,t in enumerate(Tasks):
        
        tasks[(d,t)] = mdl_2.interval_var(start=[0,INTERVAL_MAX], name = t) #Tasks[i]
        #print(Tasks[i])
    for f in Functionality:
        pe_tasks[(d,f)] = mdl_2.interval_var(optional=True, size =f[2], name = f[1])
#print(tasks[0,'task_0'].end)
#print(pe_tasks[0,Functionality[0]].name)
#print(pe_tasks)

# Step 4 - Add the temporal constraints    
for d in Dags:
# =============================================================================
#     for p in Precedences:
#         mdl_2.add( mdl_2.end_before_start(tasks[d,p[0]], tasks[d,p[1]]) )
# =============================================================================
    for c in Con_Precedence:
        for (p1, task1, d1) in Functionality:
            if p1 == c[0] and task1 == c[1]:
                for (p2, task2, d2) in Functionality:
                    if p2 == c[0] and task2 == c[2]:
                        #print (p1,p2, task1,task2, 0)
                        #print(pe_tasks[d,(p1,task1,d1)])
                        #print(pe_tasks[d,(p2,task2,d2)])
                        mdl_2.add( mdl_2.end_before_start(pe_tasks[d,(p1,task1,d1)], pe_tasks[d,(p2,task2,d2)], 0) )
                    elif p2 != c[0] and task2 == c[2]:
                        #print (p1,p2, task1,task2, c[3])
                        mdl_2.add( mdl_2.end_before_start(pe_tasks[d,(p1,task1,d1)], pe_tasks[d,(p2,task2,d2)], c[3]) )

# Step 5 - Add the alternative constraints
for d in Dags:
    for t in Tasks:
        #mdl_2.add( mdl_2.alternative(tasks[d,t], [tasks_P1[(d,t)], tasks_P2[(d,t)], tasks_P3[(d,t)]]) )
        mdl_2.add( mdl_2.alternative(tasks[d,t], [pe_tasks[d,f] for f in Functionality if f[1]==t]) )
 
# Step 7 - Add the no overlap constraints
for p in PEs:
    mdl_2.add( mdl_2.no_overlap([pe_tasks[d,f] for d in Dags for f in Functionality if f[0]==p]) )
       
# Step 8 - Add the objective
mdl_2.add(mdl_2.minimize(mdl_2.max([mdl_2.end_of(tasks[(d,t)]) for d in Dags for t in Tasks])))
#mdl_2.add(mdl_2.minimize(mdl_2.end_of(tasks[(d,'task_9')])))

# Step - Solve the model
# Solve the model
print("\nSolving model....")
msol_2 = mdl_2.solve(FailLimit=30000)
print("done")

#print("Cost will be "+str( msol_2.get_objective_values()[0] ))
pe_idx = {p : i for i,p in enumerate(PEs)}
#print(pe_idx)
pe_tasks_real = [[] for p in range(nbPEs)]  # Tasks assigned to a given worker
#print(pe_tasks_real)
for d in Dags:
    for f in Functionality:
        pe = f[0]
        pe_t = pe_tasks[(d,f)]
        pe_tasks_real[pe_idx[pe]].append(pe_t)
        
#print(len(pe_tasks_real[0]))
#print(len(pe_tasks_real[1]))
#print(pe_idx)
        

colors = ['blue', 'red', 'green']
visu.timeline('Solution SchedOptional', 0, 75)
for i,p in enumerate(PEs):
    visu.sequence(name=p)
    for t in pe_tasks_real[pe_idx[p]]:
        wt = msol_2.get_var_solution(t)
        if wt.is_present():
            #if desc[t].skills[w] == max(desc[t].skills):
                # Green-like color when task is using the most skilled worker
            #    color = 'lightgreen'
            #else:
                    # Red-like color when task does not use the most skilled worker
            #    color = 'salmon'
            #color = colors[i]
            color = 'y'
            visu.interval(wt, color, wt.get_name())
            print(t)
            
visu.show()