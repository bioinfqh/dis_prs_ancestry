import sys
import operator
from lifelines import CoxPHFitter
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as cm

id_col = 1
pheno_col = 3
risk_col = 2
steps=500

def get_risk_groups(pheno_df,pred_df):    
    return(0)

def get_relative_risk(pheno_dict,pred_dict,patient_id):
    avg_risk = sum([float(pred_dict[i]) for i in pred_dict]) / len(pred_dict)
    avg_pheno = sum([float(pheno_dict[i]) for i in pheno_dict]) / len(pheno_dict)
    pat_risk = pred_dict[patient_id]
    rel_risk = float(pat_risk) / float(avg_risk)
    return(rel_risk)

def get_absolute_risk_and_percentile(file_path,patient_id,age_dict,seperator,outfile):
    df = pd.read_csv(file_path, sep=seperator)
    df.columns = ['ID','risk','pheno']
    id_col = [str(i) for i in df['ID'].tolist()]
    pheno_col = [str(i) for i in df['pheno'].tolist()]
    if("2" in pheno_col):
        df['pheno'].replace({1: 0, 2: 1}, inplace=True)
    nbr_pat = len(id_col)
    pat_pos = id_col.index(patient_id)
    df['ID'] = [i for i in range(0,len(df.index))]
    if(age_dict == "random_age"):
        rand_ages = [random.randint(25, 70) for i in range(0,len(df.index))]
        #print(rand_ages)
        df['age'] = rand_ages
    else:
        df['age'] = [age_dict[key] for key in age_dict][:-1]
    phenos=[str(i) for i in df['pheno'].tolist()]
    cph = CoxPHFitter()
    cph.fit(df, duration_col='age', event_col='pheno')
    #cph.print_summary()
    df_copy = df.copy()
    age_col=df_copy['age']
    pred_df = cph.predict_survival_function(df_copy)
    pheno_dict={}
    for i in range(0,len(id_col)):
        pheno_dict[id_col[i]] = phenos[i]
    preds={}
    #print(pred_df.columns)
    #row_nbr = len(list(pred_df.index))
    #row_nbr_05 = int(round(float(row_nbr) / 2.0))
    #print(pred_df.loc[list(pred_df.index)[1], :].values.tolist())
    preds_all=[]
    preds_dict = {}
    for i in range(0,len(pred_df.columns)):
        step_curr = int(round((i / len(id_col))/steps))
        if not(step_curr in preds):
            preds[step_curr] = []
        #print(pheno_dict[sorted_prs_keys[i]])
        #row_curr = row_nbr_05
        row_curr = (age_col[i]-25-1)
        curr_pred = 1.0 - float(pred_df.loc[list(pred_df.index)[row_curr],i])
        preds[step_curr].append(curr_pred)
        preds_all.append(curr_pred)
        preds_dict[id_col[i]] = curr_pred
    pred_pat = preds_all[pat_pos]
    #print(str(patient_id) + " : " + str(pred_pat))
    sorted_pred = dict(sorted(preds_dict.items(), key=operator.itemgetter(1)))
    sorted_pred_keys = [key for key in sorted_pred]
    perc_pat = float(sorted_pred_keys.index(patient_id)) / float(nbr_pat)
    #print(str(patient_id) + " : Percentile " + str(perc_pat))
    pred_sums = [(1.0 - (sum(preds[i])/float(steps))) for i in preds]
    ctr = 0
    textArray = [(str(i) + "\t" + str(preds_dict[i]) + "\t" + str(pheno_dict[i])) for i in preds_dict]
    endText = "\n".join(textArray)
    if not(outfile=="none"):
        fh=open(outfile,'w')
        fh.write(endText)
        fh.close()
    if(patient_id == "return_dataframes"):
        pred_df.columns = id_col
        return(df,pred_df)
    if(patient_id == "return_dicts"):
        return(pheno_dict,preds_dict)
    return(pred_pat,perc_pat)

def percentile_calc(dicts,nbr_steps,from_file):
    if(from_file == "true" and not(isinstance(dicts, list))):
        fh= open(dicts)
        content=fh.read()
        fh.close()
        lines = content.split("\n")
        pheno_dict = {}
        preds_dict = {}
        for line in lines:
            lineSplit = line.split("\t")
            if(len(lineSplit)<3):
                continue
            preds_dict[lineSplit[0]] = lineSplit[1]
            pheno_dict[lineSplit[0]] = lineSplit[2]
    else:
        [pheno_dict,preds_dict] = dicts
    nbr_patients = len([key for key in preds_dict])
    step_cts = [int(round(float(i+1) * float(nbr_patients) / nbr_steps)) for i in range(0,nbr_steps)]
    sorted_preds_tmp = dict(sorted(preds_dict.items(), key=operator.itemgetter(1)))
    sorted_preds = [float(sorted_preds_tmp[i]) for i in sorted_preds_tmp]
    sorted_ids = [key for key in sorted_preds_tmp]
    sorted_phenos = [float(pheno_dict[i]) for i in sorted_ids]
    pred_per_step = [float(0) for i in range(1,len(step_cts))]
    absol_pred_per_step = [float(0) for i in range(1,len(step_cts))]
    pheno_per_step = [float(0) for i in range(1,len(step_cts))]
    step_last = 0
    steplens = [max(nbr_patients,step_cts[i]) - step_cts[i-1] for i in range(1,len(step_cts))]
    for i in range(0,nbr_patients):
        found = "false"
        curr_step = 0
        for j in range(step_last,len(step_cts)-1):
            if(step_cts[j] > i):
                step_last = j
                curr_step = j
                break
        pred_per_step[j] = pred_per_step[j] + sorted_preds[i]
        pheno_per_step[j] = pheno_per_step[j] + sorted_phenos[i]
        if(float(sorted_preds[i]) > 0.5):
            absol_pred_per_step[j] = absol_pred_per_step[j] + 1
    pred = [(float(pred_per_step[i]) / float(steplens[i])) for i in range(0,len(pred_per_step))]
    abs_pred = [(float(absol_pred_per_step[i]) / float(steplens[i])) for i in range(0,len(absol_pred_per_step))]
    pheno = [(float(pheno_per_step[i]) / float(steplens[i])) for i in range(0,len(pheno_per_step))]
    return(pred,abs_pred,pheno)

def make_distr_plot(arrays,outfile):
    if(sum([1 for arr in arrays if not(len(arr) == len(arrays[0]))]) > 0):
        return("null")
    arr_len = len(arrays[0])
    x = [(float(i * 100) / float(arr_len)) for i in range(0,arr_len)]
    colors = cm.rainbow(np.linspace(0, 1, len(arrays)))
    #ctr = 0
    #ax = plt.gca()
    #ax.set_yscale('log')
    for i in range(0,len(arrays)):
        plt.scatter(x[:-1],arrays[i][:-1],color=colors[i])
    #plt.show()
    plt.savefig(outfile)
    
    
def risk_by_group(pred,pheno,outfile):
    ctr = 0
    cases = [0]
    sum_of_phenos = sum([float(i) for i in pheno])
    x = []
    y = []
    for i in range(0,len(pred)):
        curr_perc =( float(i) / float(len(pred))) + 0.00001
        cases.append(cases[i-1] + pheno[i])
        x.append(curr_perc)
        y.append(float(cases[i]) / float(sum_of_phenos))
    print(x)
    print(y)
    plt.clf()
    plt.scatter(x,y)
    plt.savefig(outfile)


        #ctr = curr_perc
if(sys.argv[1] == "verify"):
    if(len(sys.argv) < 3):
        print("arguments missing")
        quit()
    infile = str(sys.argv[2])
    outfile = str(sys.argv[3])
    [preds,abs_pred,pheno] = percentile_calc(infile,50,"true")
    make_distr_plot([pheno],outfile)
    risk_by_group(preds,pheno,"perc_cases_tmp.png")
    quit()
if(len(sys.argv) < 2):
    print("arguments missing")
    quit()
#results = open(sys.argv[1])
results = str(sys.argv[1])
patient_id_curr = str(sys.argv[2])
if(len(sys.argv) > 2):
    outfile=str(sys.argv[3])
else:
    outfile="none"
[prediction,percentile] = get_absolute_risk_and_percentile(results,patient_id_curr,"random_age"," ",outfile)
print(patient_id_curr + "\t" + str("{:.2}".format(prediction)) + "\t" + str("{:.2}".format(percentile)))
#print("Patient ID :" + patient_id_curr + ":")
#print("Predicted Risk: " + str("{:.2%}".format(prediction)) + " ;")
#print("Percentile: " + str("{:.2%}".format(percentile)) + ".")
#hist_new = [(float(i) / float(y_len)) for i in hist]
#plt.plot(x_new,pred_sums_new)
#plt.plot(x_new,y_2)

#plt.plot(x_new,pred_sums_new)
#plt.plot(x_new,y_2)
#plt.show()
