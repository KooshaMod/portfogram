from django.shortcuts import render

# Create your views here.
def agent_ren(request):
	return render(request,'agent.html')