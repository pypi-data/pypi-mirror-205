from django import forms
from .models import File

class FileUpload(forms.ModelForm):
	class Meta:
		model = File
		fields = ('file', 'description')
		def save(self):
			file = super(FileUpload, self).save()
			return file


class ImageUpload(forms.ModelForm):
	class Meta:
		model = Image
		fields = ('file', 'description')
		def save(self):
			image = super(ImageUpload, self).save()
			return image