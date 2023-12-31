from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
import json
from datetime import datetime


@login_required
def homePageView(request):
    return render(request, 'main/header.html', {})


def register(request):
    if request.method == 'POST':
        user_form = forms.UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        user_form = forms.UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})


@login_required
def facilities(request):
    if request.method == "POST":
        form = forms.FacilityForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.create_user = request.user.id
            post.create_date = timezone.now()
            post.save()    
    else:
         form = forms.FacilityForm()
    facilities = models.Facilities.objects.all()
    return render(request, 'lists/facilities.html', {'form': form, 'facilities': facilities})


@login_required
def activities(request):    
    if request.method == "POST":
        form = forms.ActivityForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.create_user = request.user.id
            post.create_date = timezone.now()
            post.save()    
    else:
         form = forms.ActivityForm()
    activities = models.Activities.objects.all()
    return render(request, 'lists/activities.html', {'form': form, 'activities': activities})


@login_required
def update_list(request): 
    if request.method == "POST":
        list_name = request.POST.get('list_name')
        id = int(request.POST.get('id'))
        name = request.POST.get('name')
        if list_name and id is not None and name:
            model_dict = {
                'activities': (models.Activities, forms.ActivityForm),
                'facilities': (models.Facilities, forms.FacilityForm),
            }

            model_class, form_class = model_dict.get(list_name, (None, None))

            if model_class and form_class:
                model = get_object_or_404(model_class, id=id)
                form = form_class(request.POST, instance=model)
                
                if form.is_valid():
                    model.name = name
                    model.create_user = request.user.id
                    model.create_date = timezone.now()
                    model.save()
    referer_url = request.META.get('HTTP_REFERER')
    if referer_url:
         return HttpResponseRedirect(referer_url)
    else:
         return HttpResponseRedirect('')


@login_required
def dashboard(request): 
    dateLogs = datetime.now().strftime("%Y-%m-%d")

    if request.method == "POST":
        if 'formname' in request.POST:
            if request.POST['formname'] == 'dellog':
                delLog = models.Worklog.objects.get(id=request.POST['worklogid'])
                delLog.delete()
                dateLogs = request.POST['changedatelog']

            if request.POST['formname'] == 'logs':
                dateLogs = request.POST['changedatelog']
         
            if request.POST['formname'] == 'addnew':
                form = forms.WorkLogForm(request.POST)
                if form.is_valid():           
                    post = form.save(commit=False)
                    post.user_id = request.user.id
                    post.created_date = timezone.now()
                    post.updated_date = timezone.now()
                    post.facility_id = int(request.POST['facility_id_name'])
                    post.activity_id = int(request.POST['activity_id_name'])
                    post.earned_hours = float(request.POST['earned_hours'])
                    post.pgl = float(request.POST['pgl'])
                    post.save()
            
    form = forms.WorkLogForm()

    worklogs = models.Worklog.objects.filter(user_id=request.user.id, date=dateLogs)

    dayly_total = {}
    dayly_total['Sum_earned_hours'] = 0
    dayly_total['Sum_hours_worked'] = 0
    dayly_total['activity_count'] = len(worklogs)

    for worklog in worklogs:

        worklog.facility_id = models.Facilities .objects.get(id=worklog.facility_id)
        worklog.activity_id = models.Activities.objects.get(id=worklog.activity_id)

        dayly_total['Sum_earned_hours'] = dayly_total['Sum_earned_hours'] + worklog.earned_hours
        dayly_total['Sum_hours_worked'] = dayly_total['Sum_hours_worked'] + worklog.hours_worked
     
    activity_id_data = models.Activities.objects.all().values('id', 'name')
    activity_id_data = list(activity_id_data)
    facility_id_data = models.Facilities.objects.all().values('id', 'name')
    facility_id_data = list(facility_id_data)

    return render(request, 'dashboard/worklog.html', {'form': form, 
                                                      'dateLogs':dateLogs, 
                                                      'dayly_total':dayly_total, 
                                                      'worklogs':worklogs, 
                                                      'activity_id_data':activity_id_data, 
                                                      'facility_id_data':facility_id_data})


@login_required
def api_get_pgl(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            facility_id = data.get('facility_id')
            activity_id = data.get('activity_id')
            try:
                pgl_data = models.Pgl.objects.filter(facility_id=facility_id, activity_id=activity_id).values_list('pgl', flat=True)
   
                if pgl_data.exists():
                    pgl_value = pgl_data.first()
                    return JsonResponse({'pgl': pgl_value})
                else:
                    return JsonResponse({'pgl': 0})
            except models.Pgl.DoesNotExist:
                return JsonResponse({'error': 'PGL data not found.'}, status=404)
        except:
            return JsonResponse({'error': 'Invalid facility_id or activity_id.'}, status=400)
    else:
        return JsonResponse({'error': 'POST method required.'}, status=400)


