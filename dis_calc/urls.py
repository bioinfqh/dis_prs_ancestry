from django.urls import path


from django.conf.urls import include, url
from . import views
#from . import views_2
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
app_name = 'polls'
urlpatterns = [
	url(r'infopage.html', views.infopage),
	url(r'sources.html', views.sources),
	url(r'errorpage.html', views.errorpage),
	url(r'reportpage.html', views.dis_calc),
	url(r'data_upload.html', views.dis_calc),
	url(r'get_reports.html', views.dis_calc),
	url(r'get_reports_customer.html', views.result_page_customer),
	url(r'ancestry_data_upload.html', views.ancestry_calc),
	url(r'ancestry_table.html', views.ancestry_calc),
	url(r'overview_for_uploads.html', views.overview_for_uploads),
	url(r'overview_for_customer.html', views.overview_for_customer),
	url(r'ancestry_overview_customer.html', views.ancestry_results_customer),
	url(r'ancestry_overview.html', views.ancestry_calc),
	url(r'local_ancestry_upload.html', views.local_ancestry_calc),
	url(r'local_ancestry_report.html', views.local_ancestry_calc),
	url(r'local_ancestry_report_customer.html', views.local_ancestry_results_customer),
	url(r'ancestry_upload.html', views.ancestry_calc),
	url(r'pdf_test.html', views.pdf_test),
	url(r'no_permission.html', views.dis_calc),
	url(r'login.html', views.login_2),
	url(r'logout.html', views.logout_2),
	url(r'signup.html', views.signup),
	url(r'delete_user.html', views.delete_user),
	url(r'^infopage/$', views.infopage, name='infopage'),
	url(r'^sources/$', views.sources, name='sources'),
	url(r'^errorpage/$', views.errorpage, name='errorpage'),
	url(r'^reportpage/$', views.dis_calc, name='reportpage.html'),
	url(r'^data_upload/$', views.dis_calc, name='data_upload.html'),
	url(r'^no_permission/$', views.dis_calc, name='no_permission.html'),
	url(r'^get_reports/$', views.dis_calc, name='get_reports.html'),
	url(r'^get_reports_customer/$', views.result_page_customer, name='get_reports_customer.html'),
	url(r'^ancestry_data_upload/$', views.ancestry_calc, name='ancestry_data_upload.html'),
	url(r'^ancestry_table/$', views.ancestry_calc, name='ancestry_table.html'),
	url(r'^overview_for_uploads/$', views.overview_for_uploads, name='overview_for_uploads.html'),
	url(r'^overview_for_customer/$', views.overview_for_uploads, name='overview_for_customer.html'),
	url(r'^ancestry_overview_customer/$', views.ancestry_results_customer, name='ancestry_overview_customer.html'),
	url(r'^ancestry_overview/$', views.ancestry_calc, name='ancestry_overview.html'),
	url(r'^local_ancestry_upload/$', views.local_ancestry_calc, name='local_ancestry_upload.html'),
	url(r'^local_ancestry_report/$', views.local_ancestry_calc, name='local_ancestry_report.html'),
	url(r'^local_ancestry_report_customer/$', views.local_ancestry_results_customer, name='local_ancestry_report_customer.html'),
	url(r'^ancestry_upload/$', views.ancestry_calc, name='ancestry_upload.html'),
	url(r'^pdf_test/$', views.pdf_test, name='pdf_test.html')
] 
urlpatterns += staticfiles_urlpatterns()
