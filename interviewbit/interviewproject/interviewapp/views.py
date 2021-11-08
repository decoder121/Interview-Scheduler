from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from . models import *
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.urls import reverse_lazy
from . forms import *
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse



# Create your views here.

class InterviewList(ListView):
    model = Interview
    context_object_name = 'interviews'
    def get_context_data(self, **kwargs):
    	context = super().get_context_data(**kwargs)
    	queryset = super().get_queryset().values_list(flat=True)	
    	context['interviews']=context['interviews']
    	context['count'] = context['interviews'].count()
    	return context

class ParticipantRegister(CreateView):
	model=Participant
	fields= ['name','email','resume']
	success_url=reverse_lazy('interviews'	)

	def form_valid(self,form):
		form.instance.user= self.request.user
		return super(ParticipantRegister,self).form_valid(form)


class InterviewCreate(CreateView):
	model= Interview
	form_class = CreateForm
	success_url=reverse_lazy('interviews')

	def form_valid(self,form):
		form.instance.user= self.request.user
		start_time=form.cleaned_data['start_time']
		end_time=form.cleaned_data['end_time']
		participants = form.cleaned_data['participants']
	

		if (len(participants)>=2):
			lis=[]
			for i in participants:
				c=Interview.objects.filter(start_time__range=(start_time,end_time),end_time__range=(start_time,end_time),participants=i)
				d=Interview.objects.filter(start_time__lte=start_time,end_time__range=(start_time,end_time),participants=i)
				e=Interview.objects.filter(start_time__range=(start_time,end_time),end_time__gte=end_time,participants=i)
				f=Interview.objects.filter(start_time__lte=start_time,end_time__gte=end_time,participants=i)
				if(c or d or e or f):
					#print("cannot schedule " + str(i))
					lis.append(i)
			if lis:
				#print("Not Scheduling")
				for participant in lis:
					messages.info(self.request,"Participant " + str(participant) + " is already busy in another interview schedule! ")
				return redirect('interview-create')	
			else:
				for p in participants:
					subject = "Interview Schedule" 
					body = {
					    'Interview message': "Your inteview has been scheduled for this respective time.We request you to be present on time. ",
						'Interview start time': str(form.cleaned_data['start_time']), 
						'Interview End time': str(form.cleaned_data['end_time']), 
					}
					message = "\n".join(body.values())
					try:
						send_mail(subject, message, 'shrey.agarwal343@gmail.com', [p.email]) 
					except BadHeaderError:
						return HttpResponse('Invalid header found.')		
				return super(InterviewCreate,self).form_valid(form)

		messages.info(self.request,'Atleast 2 participants')
		return redirect('interview-create')
	
class Update(UpdateView):
	model = Interview
	fields = ['start_time','end_time','participants']
	template_name_suffix = '_update_form'
	success_url= reverse_lazy('interviews')

class DeleteView(DeleteView):
	model = Interview
	context_object_name='interview'
	success_url=reverse_lazy('interviews')

 
