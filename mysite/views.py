# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from mysite import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import datetime
from django.contrib import messages
from mysite import forms

def index(request):
	all_polls = models.Poll.objects.all().order_by('-created_at')
	paginator = Paginator(all_polls, 2)
	p = request.GET.get('p')
	try:
		polls = paginator.page(p)
	except PageNotAnInteger:
		polls = paginator.page(1)
	except EmptyPage:
		polls = paginator.page(paginator.num_pages)

	return render(request, 'index.html', locals())
	
@login_required
def poll(request, pollid):
	try:
		poll = models.Poll.objects.get(id=int(pollid))
	except:
		poll = None
	if poll is not None:
		pollitems = models.PollItem.objects.filter(poll=poll)
	
	return render(request, 'poll.html', locals())
	
@login_required
def vote(request, pollid, pollitemid):
	if models.VoteCheck.objects.filter(userid=request.user.id, pollid=pollid, vote_date=datetime.date.today()):
		return redirect('/poll/{}'.format(pollid))
	else:
		voteCheck = models.VoteCheck(userid=request.user.id, pollid=pollid, vote_date=datetime.date.today())
		voteCheck.save()
	try:
		pollitem = models.PollItem.objects.get(id=pollitemid)
	except:
		pollitem = None
	if pollitem is not None:
		pollitem.vote = pollitem.vote + 1
		pollitem.save()
	return redirect('/poll/{}'.format(pollid))

@login_required
def govote(request):
	if request.is_ajax():
		pollitemid = request.POST.get('pollitemid')
		pollid = request.POST.get('pollid')
		bypass = False
		if models.VoteCheck.objects.filter(userid=request.user.id, pollid=pollid, vote_date=datetime.date.today()):
			bypass = True
		else:
			voteCheck = models.VoteCheck(userid=request.user.id, pollid=pollid, vote_date=datetime.date.today())
			voteCheck.save()
		try:
			pollitem = models.PollItem.objects.get(id=pollitemid)
			if not bypass:
				pollitem.vote = pollitem.vote + 1
				pollitem.save()
			votes = pollitem.vote
		except:
			votes = 0
	else:
		votes = 0
	return HttpResponse(votes)
	
@login_required	
def mypoll(request):
	all_polls = models.Poll.objects.filter(user=request.user).order_by('-created_at')
	paginator = Paginator(all_polls, 2)
	p = request.GET.get('p')
	try:
		polls = paginator.page(p)
	except PageNotAnInteger:
		polls = paginator.page(1)
	except EmptyPage:
		polls = paginator.page(paginator.num_pages)

	return render(request, 'mypoll.html', locals())

@login_required	
def delpoll(request, pollid):
	try:
		poll = models.Poll.objects.get(id=pollid)
		poll.delete()
	except:
		messages.add_message(request, messages.INFO, '删除失败')
	
	return redirect('/mypoll/')
	
@login_required	
def addpoll(request):
	if request.method=='POST':
		poll = models.Poll(user=request.user, enabled=True)
		poll_form = forms.PollForm(request.POST, instance=poll)
		if poll_form.is_valid():
			poll_form.save()
			messages.add_message(request, messages.INFO, '保存成功，请继续编辑')
			return redirect('/mypoll/')
		else:
			messages.add_message(request, messages.INFO, '保存失败')
	else:
		poll_form = forms.PollForm()
		
	return render(request, 'addpoll.html', locals())
	
@login_required	
def editpoll(request, pollid):
	try:
		poll = models.Poll.objects.get(id=pollid)
		pollitems = models.PollItem.objects.filter(poll=poll)
	except:
		return redirect('/mypoll/')
	
	return render(request, 'editpoll.html', locals())
	
@login_required	
def changename(request):
	if request.is_ajax():
		newname = request.POST.get('pollname')
		pollid = request.POST.get('pollid')
		try:
			poll = models.Poll.objects.get(id=int(pollid))
			poll.name = newname
			poll.save()
			res = {'status':'success', 'newname':poll.name}
		except:
			res = {'status':'fail', 'message':'找不到信息'}
	else:
		res = {'status':'fail', 'message':'出错了'}
	
	return JsonResponse(res)
		
		
		
		
		