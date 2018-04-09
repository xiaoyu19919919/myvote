# -*- coding: utf-8 -*-
from django import forms
from mysite import models

class PollForm(forms.ModelForm):
	class Meta:
		model = models.Poll
		fields = ['name',]
		
	def __init__(self, *args, **kwargs):
		super(PollForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = '名称'