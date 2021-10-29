from django.shortcuts import render
from .forms import ResumeForm
from .models import Resume
from django.contrib import messages
from django.views import View
from django.db.models import Q
import os
from django.utils.safestring import mark_safe


class ProfileView(View):

    def get(self, request):
        form = ResumeForm()
        resumes = Resume.objects.all()
        return render(request, 'profiles.html', {"resumes": resumes, "form": form})

    def post(self, request):

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        keywords = request.POST.get('keywords')

        if first_name or last_name or keywords:
            lookups = Q(first_name__icontains=first_name) & \
                      Q(last_name__icontains=last_name) & \
                      Q(keywords__icontains=keywords)

            resumes = Resume.objects.filter(lookups).distinct()

            # make searched parts bold
            for resume in resumes:
                if first_name:
                    resume.first_name = resume.first_name.replace(first_name, f'<strong>{first_name}</strong>')
                    resume.first_name = mark_safe(resume.first_name)

                if last_name:
                    resume.last_name = resume.last_name.replace(last_name, f'<strong>{last_name}</strong>')
                    resume.last_name = mark_safe(resume.last_name)

                if keywords:
                    resume.keywords = resume.keywords.replace(keywords, f'<strong>{keywords}</strong>')
                    resume.keywords = mark_safe(resume.keywords)

            context = {"resumes": resumes}
            return render(request, 'profiles.html', context)

        resumes = Resume.objects.all()
        context = {"resumes": resumes}
        return render(request, 'profiles.html', context)


def create_profile(request):
    form = ResumeForm(data=request.POST, files=request.FILES)
    if request.method == "POST":
        form = ResumeForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            resume = form.save(commit=False)
            file_ext = os.path.splitext(resume.resume_file.name)[1]
            resume.resume_file.name = resume.first_name + "_" + resume.last_name + file_ext
            form.save()
            messages.success(request, "Your profile was created successfully!")
            return render(request, 'create_profile.html', {"form": form})

        messages.error(request, "Unsupported file type! Supported types are: pdf, doc, txt")
        return render(request, 'create_profile.html', {"form": form})

    return render(request, 'create_profile.html', {"form": form})
