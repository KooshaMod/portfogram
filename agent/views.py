from django.shortcuts import render
from stocks.models import DataShare
import numpy as np
import pandas as pd

# Create your views here.
def agent_ren(request):
	return render(request,'agent.html')