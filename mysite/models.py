# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Poll(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=False)
	created_at = models.DateField(auto_now_add=True)
	enabled = models.BooleanField(default=False)
	def __unicode__(self):
		return self.name

class PollItem(models.Model):
	poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=False)
	image_url = models.CharField(max_length=200, null=True, blank=True)
	vote = models.PositiveIntegerField(default=0)
	
	def __unicode__(self):
		return self.name
		
class VoteCheck(models.Model):
	userid = models.PositiveIntegerField()
	pollid = models.PositiveIntegerField()
	vote_date = models.DateField()

