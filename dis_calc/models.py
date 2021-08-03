import datetime
from django.db import models
from django.utils import timezone
# Create your models here.
import os, sys
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
##from scipy.stats.stats import pearsonr
##import plotly
##import plotly.plotly as py
##import plotly.graph_objs as go
##import plotly.io as pio
##import plotly.offline
#from .models import Choice, Question
from datetime import datetime
##from networkx.readwrite import json_graph
##import json
from django.shortcuts import render_to_response,render
from django.template import RequestContext
##from django.http import HttpResponseRedirect
##from django.urls import reverse
import dis_calc
#from polls.models import Document
##from clustering.forms import DocumentForm
#from polls.models import Upload,UploadForm
##import numpy as np
##import matplotlib.pyplot as plt
#import mpld3

##import seaborn as sns
##import pandas as pd
##from numpy import array

import matplotlib.patches as mpatches


#import networkx as nx
#from bokeh.io import show, output_notebook, output_file, save
#from bokeh.plotting import figure
#from bokeh.models import Circle, HoverTool, TapTool, BoxSelectTool
#from bokeh.models.graphs import from_networkx
#from bokeh.transform import linear_cmap
#from bokeh.models import ColumnDataSource, LabelSet
#from bokeh.models.graphs import NodesAndLinkedEdges, EdgesAndLinkedNodes
#from biomart import BiomartServer
#from bokeh.embed import components
#from bokeh.palettes import Spectral4
#from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, TapTool, BoxSelectTool

##from pybiomart import Dataset

from django.forms import ModelForm

#class Upload(models.Model):
#        pic = models.FileField(upload_to="images/")
#        upload_date=models.DateTimeField(auto_now_add =True)

# FileUpload form class.
#class UploadForm(ModelForm):
#        class Meta:
#                model = Upload
#                fields = ('pic',)

class user_with_data(models.Model):
    customer_id = models.CharField(max_length=100)
    firstname= models.CharField(max_length=100)
    lastname= models.CharField(max_length=100)
    email= models.CharField(max_length=200)
    has_reports = models.CharField(max_length=100)
    prs_report = models.CharField(max_length=100,default='none')
    dis_report = models.CharField(max_length=100,default='none')
    #diseases_with_prs = models.CharField(max_length=100)
    diseases_with_dis_report = models.CharField(max_length=100,default='none')

class report(models.Model):
    customer_id = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    is_current = models.CharField(max_length=100)
    type_of_report = models.CharField(max_length=100)
    disease_type = models.CharField(max_length=100,default='all')
    path = models.CharField(max_length=200)
    

class ancestry_report(models.Model):
    customer_id = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    is_current = models.CharField(max_length=100)
    result_path = models.CharField(max_length=100)
    path = models.CharField(max_length=200)
    
    
class local_ancestry_report(models.Model):
    customer_id = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    is_current = models.CharField(max_length=100)
    img_path = models.CharField(max_length=100)
    
class GraphForm(models.Model):
	#def makehref(term):
	#	ret = term + ""
	#	ret = "<a href=\"https://www.ncbi.nlm.nih.gov/gene/?term="+ret+"\">"+ret+"</a>"
	#	return(ret)diseases_with_dis_report
	#def is_logged_in(username,password):
	#	return(1)
	
	def save_user_data(fn,prot_fn,username):
		user_dir = "user_uploaded_files/" + username
		if not(os.path.isdir(user_dir)):
			os.mkdir(user_dir)
		fn.seek(0)
		prot_fn.seek(0)
		str1 = fn.read().decode('utf-8')
		str2 = prot_fn.read().decode('utf-8')
		#print(str1)
		filename_1 = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
		filename_2 = user_dir + "/" + filename_1 + "_expr.txt"
		filename_3 = user_dir + "/" + filename_1 + "_prot.txt"
		outfile1 = open(filename_2, "w")
		outfile1.write(str1)
		outfile1.close()
		outfile2 = open(filename_3, "w")
		outfile2.write(str2)
		outfile2.close()
