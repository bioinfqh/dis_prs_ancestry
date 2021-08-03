
from plot_curve import make_risk_plot
from plot_curve import make_risk_plot_2
import sys
import pdfkit 
import imgkit
import os
import json
#from risk_calc_2 import get_absolute_risk_and_percentile

colorscale_width = 1100
sep = "<hr>"
#disease_name_input = sys.argv[1]
risk_limit = 0.9
params_from_file = "true"
part1 = "part1.html"
part2 = "part2.html"

def export_prs_as_json(patient_id,disease_names,risks,percs):
    dict_for_ret = {}
    for i in range(0,len(disease_names)):
        new_dict = {}
        new_dict["risk_score"] = str(risks[i])
        new_dict["percentile"] = str(percs[i])
        dict_for_ret[disease_names[i]] = new_dict
    json_str = json.dumps(dict_for_ret)
    return(json_str)

def read_param_file(path):
    table_file = open(path)
    htmlstr=table_file.read()
    table_file.close()
    lines = htmlstr.split("\n")
    diseases = []
    result_files = []
    for line in lines:
        #print(line)
        lineSplit = line.split()
        #print(len(lineSplit))
        if(len(lineSplit) < 2):
            #print("continue")
            continue
        disease = lineSplit[0].replace("_"," ")
        result_file = lineSplit[1].replace("\n","")
        diseases.append(disease)
        result_files.append(result_file)
        print(disease)
        print(result_file)
    return(diseases,result_files)
        
## write string in html and convert to pdf
def make_pdf_from_str(htmlstr,outfile):
    fh=open("temp_out_file.html",'w+')
    fh.write(htmlstr)
    fh.close()
    pdfkit.from_file("temp_out_file.html", outfile)

def get_info(disease_names,distr_paths,patient_id):
    outfiles = []
    risks = []
    percs = []
    scores = []
    for i in range(0,len(disease_names)):
        path = distr_paths[i]
        outfile="distr_" +(str(disease_names[i]).replace(" ","_")) + ".png"
        print(path)
        [risk,perc,score] = make_risk_plot(path,patient_id,outfile)
        outfiles.append(outfile)
        risks.append(risk)
        percs.append(perc)
        scores.append(score)
    return(disease_names,outfiles,risks,percs,scores)

def make_scale_image(path,outfile):
    imgkit.from_file(path,outfile)

### this is the main method for disease gene report generation.
def make_html_easy(html_path,outfile,results_path,patient_id,risk_threshold,is_abs_risk_file,customer_id):
    table_file = open(html_path)
    htmlstr=table_file.read()
    table_file.close()
    header_file = open(part1)
    header_str=header_file.read()
    header_file.close()
    footer_file = open(part2)
    footer_str=footer_file.read()
    footer_file.close()
    result_file = open(results_path)
    resultstr=result_file.read()
    result_file.close()
    resultlist = resultstr.split("\n")
    disease_names = []
    percs = []
    risks = []
    distrs = []
    ## read result file
    for line in resultlist:
        lineSplit = line.split()
        if(len(lineSplit) < 4):
            continue
        else:
            disease_names.append(lineSplit[0])
            risks.append(float(lineSplit[1]))
            percs.append(float(lineSplit[2]))
            distrs.append(str(lineSplit[3]))
    json_str = export_prs_as_json(patient_id,disease_names,risks,percs)
    #print(json_str)
    endstrs = []
    #print(header_str)
    risk_text_final = "No increased disease risks detected."
    is_risk = []
    for i in range(0,len(disease_names)):
        print(distrs[i])
        path = distrs[i]
        # generate risk plot
        distr_img="distr_" +(str(disease_names[i]).replace(" ","_")) + ".png"
        #print(path)
        [risk,perc,score] = make_risk_plot(path,patient_id,distr_img)
        # write explanation if risk is above threshold
        if(float(percs[i]) > float(risk_threshold)):
            is_risk.append(str(disease_names[i]).replace("_"," "))
            expl_str = "Since your risk of " + str(disease_names[i]).replace("_"," ") + " is above average, we recommend to show this report to your doctor."
        else:
            expl_str = "Since your risk of " + str(disease_names[i]).replace("_"," ") + " is around or below average, no additional action is recommended."
        #width1_tmp = round(float(colorscale_width) * float(scores[i]))
        ## specify position of bold indicator line in scale
        width1_tmp = round(float(colorscale_width) * float(percs[i]))
        width2 = str(width1_tmp - 10) + "px"
        width1 = str(width1_tmp) + "px"
        if(is_abs_risk_file == "t"):
            percentage_str = str("{:.2%}".format(risks[i]))
        else:
            percentage_str = str("{:.2}".format(risks[i]))
        percentile_str = str("{:.2%}".format(percs[i]))
        percentile_even_nbr = percentile_str.split(".")[0]
        ## draw risk scale
        if(is_abs_risk_file == "t"):
            bash_code = 'bash dis_calc/draw_and_save.sh '+ str((risks[i] * 100.0)) + ' ' + str((percs[i] * 100.0))
        else:
            bash_code = 'bash dis_calc/draw_and_save.sh '+ str(risks[i]) + ' ' + str((percs[i] * 100.0))
        os.system(bash_code)
        scale_file = "dis_calc/yourscale_" + str(percentile_even_nbr) + ".png"
        ## put variable data in html string
        htmlstr_temp = htmlstr.replace("distr_img",distr_img).replace("width1",str(width1)).replace("width2",str(width2)).replace("percentage_value",percentage_str).replace("percentile_value",percentile_str).replace("disease_name",str(disease_names[i]).replace("_"," ")).replace("scale_image",scale_file).replace("expl_str",expl_str)
        endstrs.append(htmlstr_temp)
    content_str = sep.join(endstrs)
    if(len(is_risk) > 0):
        risk_text_final = "Increased risk of the following diseases detected: " + "; ".join(is_risk) +"."
        bg_color = "yellow"
    else:
        bg_color = "green"
    header_str = header_str.replace("bg_color",bg_color).replace("result_text",risk_text_final)
    #header_str.raplace("
    endstr = header_str + content_str + footer_str
    if not(outfile=="none"):
        fh=open(outfile,'w')
        fh.write(endstr)
        fh.close()
    fh=open("dis_calc/static/prs_" + patient_id + ".json",'w')
    fh.write(json_str)
    fh.close()
    return(endstr)        
    
    
def make_html(html_path,outfile,disease_names,plot_paths,risks,percs,scores,patient_id,risk_threshold):
    table_file = open(html_path)
    htmlstr=table_file.read()
    table_file.close()
    header_file = open(part1)
    header_str=header_file.read()
    header_file.close()
    footer_file = open(part2)
    footer_str=footer_file.read()
    footer_file.close()
    #print(header_str)
    #comments_style = ""
    #if(comment_html == ""):
    #    comments_style = "display: none;"
    #if(is_risk == "true"):
        #bg_color = "yellow"
    #    result_text = "Increased risk o ."
    #else:
        #bg_color = "green"
    #    result_text = "No pathogenic sequence variant(s) in gene related to reported phenotype detected ."
    #resultstr = "Increased risk of Cancer detected."
    endstrs = []
    print(header_str)
    risk_text_final = "No increased disease risks detected."
    is_risk = []
    for i in range(0,len(disease_names)):
        if(float(percs[i]) > float(risk_threshold)):
            is_risk.append(disease_names[i])
            expl_str = "Since your risk of " + str(disease_names[i]) + " is above average, we recommend to show this report to your doctor."
        else:
            expl_str = "Since your risk of " + str(disease_names[i]) + " is around or below average, no additional action is recommended."
        #width1_tmp = round(float(colorscale_width) * float(scores[i]))
        width1_tmp = round(float(colorscale_width) * float(percs[i]))
        width2 = str(width1_tmp - 10) + "px"
        width1 = str(width1_tmp) + "px"
        percentage_str = str("{:.2%}".format(risks[i]))
        percentile_str = str("{:.2%}".format(percs[i]))
        percentile_even_nbr = percentile_str.split(".")[0]
        bash_code = 'bash dis_calc/draw_and_save.sh '+ str((risks[i] * 100.0)) + ' ' + str((percs[i] * 100.0))
        os.system(bash_code)
        scale_file = "yourscale_" + str(percentile_even_nbr) + ".png"
        htmlstr_temp = htmlstr.replace("distr_img",plot_paths[i]).replace("width1",str(width1)).replace("width2",str(width2)).replace("percentage_value",percentage_str).replace("percentile_value",percentile_str).replace("disease_name",disease_names[i]).replace("scale_image",scale_file).replace("expl_str",expl_str)
        endstrs.append(htmlstr_temp)
    content_str = sep.join(endstrs)
    if(len(is_risk) > 0):
        risk_text_final = "Increased risk of the following diseases detected: " + "; ".join(is_risk) +"."
        bg_color = "yellow"
    else:
        bg_color = "green"
    header_str = header_str.replace("bg_color",bg_color).replace("result_text",risk_text_final)
    #header_str.raplace("
    endstr = header_str + content_str + footer_str
    if not(outfile=="none"):
        fh=open(outfile,'w')
        fh.write(endstr)
        fh.close()
    return(endstr)

if(params_from_file == "true"):
    #imgkit.from_file("gauge.html","new_scale.jpg")
    #make_scale_image("gauge.html","new_scale.jpg")
    #pdfkit.from_file("gauge.html","new_scale.pdf")
    print(sys.argv[1])
    ## this is the main mode that is actually used
    if(sys.argv[1] == "easy"):
        result_file=str(sys.argv[2])
        patient_id=str(sys.argv[3])
        output_file = str(sys.argv[4])
        is_abs_risk = str(sys.argv[5])
        #outfile_curr = outfile + "_prs.html"
        print(output_file)
        patient_id_new = output_file.replace("dis_calc/static/prs_report_","").replace(".pdf","")
        make_html_easy("PRS_to_fill.html","html_page.html",result_file,patient_id,float("0.7"),is_abs_risk,patient_id_new)
        #make_pdf_from_str(make_html_easy("PRS_to_fill.html","html_page.html",result_file,patient_id,float("0.7"),is_abs_risk,patient_id_new),output_file)
        #make_pdf_from_str(make_html_easy("PRS_to_fill.html","none",result_file,patient_id,float("0.7"),is_abs_risk),output_file)
    else:
        paramfile = sys.argv[1]
        patient_id = str(sys.argv[2])
        output_file = sys.argv[3]
        [diseases,result_files] = read_param_file(paramfile)
        print(diseases)
        print(result_files)
        #for i in range(0, len(diseases)):
        [disease_names,outfiles,risks,percs,scores] = get_info(diseases,result_files,patient_id)
        #outfile_curr = outfile + "_prs.html"
        make_pdf_from_str(make_html("PRS_to_fill.html","html_page.html",disease_names,outfiles,risks,percs,scores,patient_id,float("0.7")),output_file)
        #make_pdf_from_str(make_html("PRS_to_fill.html","none",disease_names,outfiles,risks,percs,scores,patient_id,float("0.7")),output_file)
elif(len(sys.argv) < 3):
    [disease_names,outfiles,risks,percs,scores] = get_info(["Cancer"],["scores_test.0.1.profile"],"HG00096")
    make_pdf_from_str(make_html("../VEP_test/PRS_to_fill.html","none",disease_names,outfiles,risks,percs,scores,"HG00096",float("0.7")),"prs_report.pdf")
else:
    [disease_names,outfiles,risks,percs,scores] = get_info([sys.argv[1]],[sys.argv[2]],sys.argv[3])
    make_pdf_from_str(make_html("../VEP_test/PRS_to_fill.html","none",disease_names,outfiles,risks,percs,scores,"HG00096",float("0.7")),sys.argv[4])
