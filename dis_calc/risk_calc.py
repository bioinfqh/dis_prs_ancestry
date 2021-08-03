import sys
import operator
from lifelines import CoxPHFitter
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np


results = open(sys.argv[1])
id_col = 1
pheno_col = 3
risk_col = 2
steps=500
#target_id = str(sys.argv[2])
#if(len(sys.argv) > 3):
#    prs_pos = int(str(sys.argv[4])) - 1
#    id_pos = int(str(sys.argv[3])) - 1
htmlstr=results.read()
lines= htmlstr.split("\n")
#print(len(lines))
#firstline=lines[0].split()
#print(firstline)
#if(len(sys.argv) < 4):
#    prs_pos = firstline.index("PRS")
#    id_pos = firstline.index("IID")
prs_dict={}
pheno_dict={}
age_dict={}
for i in range(0,len(lines)):
    line = lines[i]
    if(len(line.split()) < 3):
        continue
    id_curr = line.split()[id_col-1]
    prs_curr = line.split()[risk_col-1]
    pheno_curr = line.split()[pheno_col-1]
    prs_dict[id_curr]=float(prs_curr)
    pheno_dict[id_curr]=str(pheno_curr)
    age_dict[id_curr]=random.randint(25, 70)
    #print(id_curr)
sorted_prs = dict(sorted(prs_dict.items(), key=operator.itemgetter(1)))
sorted_prs_keys = [key for key in sorted_prs]
#print(pheno_dict)
#print(sorted_prs_keys)
stepwise_pheno={}
max_step=0
for i in range(0,len(pheno_dict)):
    step_curr = int(round((i / len(pheno_curr))/steps))
    #print(step_curr)
    if not(step_curr in stepwise_pheno):
        stepwise_pheno[step_curr] = []
    #print(pheno_dict[sorted_prs_keys[i]])
    stepwise_pheno[step_curr].append(pheno_dict[sorted_prs_keys[i]])
    if(i == (len(pheno_dict) -1)):
        max_step=step_curr
    
risk_per_group={}
for i in stepwise_pheno:
    sum_of_positives = [1 for k in stepwise_pheno[i] if (k == "2")]
    risk_per_group[str(float(i)*(1.0/float(max_step)))]=(float(len(sum_of_positives))/float(steps))
    #print(len(sum_of_positives))
    #print(stepwise_pheno[i])
    
df = pd.read_csv(sys.argv[1], sep='\t')
df.columns = ['ID','risk','pheno']
#print(df)
id_col = [str(i) for i in df['ID'].tolist()]
nbr_pat = len(id_col)
df['ID'] = [i for i in range(0,len(df.index))]
df['age'] = [age_dict[key] for key in age_dict][:-1]
#print(df)
cph = CoxPHFitter()
cph.fit(df, duration_col='age', event_col='pheno')
cph.print_summary()
df_copy = df.copy()
age_col=df_copy['age']
pred_df = cph.predict_survival_function(df_copy)
preds={}
#print(pred_df.columns)
row_nbr = len(list(pred_df.index))
row_nbr_05 = int(round(float(row_nbr) / 2.0))
#print(pred_df.loc[list(pred_df.index)[1], :].values.tolist())
preds_all=[]
x_new=[]
y_new=[]
preds_dict={}
for i in range(0,len(pred_df.columns)):
    step_curr = int(round((i / len(pheno_curr))/steps))
    if not(step_curr in preds):
        preds[step_curr] = []
    #print(pheno_dict[sorted_prs_keys[i]])
    #row_curr = row_nbr_05
    row_curr = (age_col[i]-25-1)
    #preds[step_curr].append(pred_df.loc[list(pred_df.index)[row_curr],i])
    #preds_all.append(pred_df.loc[list(pred_df.index)[row_curr],i])
    #preds_dict[id_col[i]] = pred_df.loc[list(pred_df.index)[row_curr],i]
    curr_pred = 1.0 - float(pred_df.loc[list(pred_df.index)[row_curr],i])
    preds[step_curr].append(curr_pred)
    preds_all.append(curr_pred)
    preds_dict[id_col[i]] = curr_pred
    
pred_sums = [(1.0 - (sum(preds[i])/float(steps))) for i in preds]
x_new = [(i*steps) for i in range(0,max_step)]

#print(preds)
pheno_all=df_copy['pheno']

#prs_all=[]
prs_all=df_copy['risk']
for i in preds:
    pred_sum=sum([(1.0-float(k)) for k in preds[i]])
    pheno_pos=[1 for k in stepwise_pheno[i] if (k == "1")]
    y_new.append(float(len(pheno_pos))/len(preds[i]))
    #print(str(pred_sum) + "\t" + str(len(pheno_pos)))
pred_sums_new = [((pred_sums[i] + pred_sums[i-1])/float(2.0)) for i in range(1,len(pred_sums))]
y_2 = [((y_new[i] + y_new[i-1])/float(2.0)) for i in range(1,len(y_new))]
#y_len = len(pheno_all)
risk_ratios = {}
for i in range(0,len(pred_sums_new)):
    print(pred_sums_new[i])
    print(y_2[i])



sorted_pred = dict(sorted(preds_dict.items(), key=operator.itemgetter(1)))
sorted_pred_keys = [key for key in sorted_pred]
sorted_pred_values = [float(sorted_pred[key]) for key in sorted_pred]
sum_1 = float(sum(sorted_pred_values) - sorted_pred_values[1])
sum_3 = float(sum(pheno_all) - pheno_all[1])
sum_2 = float(sorted_pred_values[1])
sum_4 = float(pheno_all[1])
ctr_1 = float(len(preds_all))
ctr_2 = float(1)
risk_ratio_ct_dict = {}
pheno_ratio_ct_dict = {}
preds_all_len = len(preds_all)
for i in range(1,len(preds_all)):
    #print(sum_1)
    #print(sum_2)
    curr_risk_ratio = (sum_1 / ctr_1) / (sum_2 / ctr_2)
    curr_pheno_ratio = (sum_3 / ctr_1) / (sum_4 / ctr_2)
    if not(i  % 1000):
        print(i)
        print(sum_1 / ctr_1)
        print(sum_2 / ctr_2)
        print(curr_risk_ratio)
    risk_ratio_ct_dict[curr_risk_ratio] = (ctr_2 / preds_all_len)
    pheno_ratio_ct_dict[curr_pheno_ratio] = (ctr_2 / preds_all_len)
    sum_1 = sum_1 - sorted_pred_values[i]
    sum_2 = sum_2 + sorted_pred_values[i]
    sum_3 = sum_3 - pheno_all[i]
    sum_4 = sum_4 + pheno_all[i]
    ctr_1 = ctr_1 - 1
    ctr_2 = ctr_2 + 1

#print(risk_ratio_ct_dict)
risk_ratio_steps_dict={}
pheno_ratio_steps_dict={}
is_in_dict = []
for i in risk_ratio_ct_dict:
    i_str = str(i)
    for j in range(1,10):
        #print(j)
        if(j in is_in_dict):
            continue
        if(float(i) > float(j)):
            if not(j in is_in_dict):
                #print(j)
                #print(i)
                risk_ratio_steps_dict[j] = risk_ratio_ct_dict[i] * preds_all_len
                is_in_dict.append(j)
is_in_dict = []
for i in pheno_ratio_ct_dict:
    i_str = str(i)
    for j in range(1,10):
        #print(j)
        if(j in is_in_dict):
            continue
        if(float(i) > float(j)):
            if not(j in is_in_dict):
                #print(j)
                #print(i)
                pheno_ratio_steps_dict[j] = pheno_ratio_ct_dict[i] * preds_all_len
                is_in_dict.append(j)
print(risk_ratio_steps_dict)
print(pheno_ratio_steps_dict)
#hist_new = [(float(i) / float(y_len)) for i in hist]
#plt.plot(x_new,pred_sums_new)
#plt.plot(x_new,y_2)

#plt.plot(x_new,pred_sums_new)
#plt.plot(x_new,y_2)
#plt.show()
