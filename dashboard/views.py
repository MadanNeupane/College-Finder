from django.shortcuts import render
import time
from universities.models import University
from django.utils.timezone import localtime

try:
    universities = University.objects.all().order_by('id')
    uni_bookmark_counts = []
    trending_unis = []
    for university in universities:
        num = university.bookmarks.count()
        uni_bookmark_counts.append(num)

    trending_unis_index = sorted(range(
        len(uni_bookmark_counts)), key=lambda i: uni_bookmark_counts[i], reverse=True)[:10]

    for index in trending_unis_index:
        trending_unis.extend(University.objects.filter(id=index))
except:
    pass


def dashboard_page(request):
    last_login_utc = request.user.last_login

    if last_login_utc:
        last_login_local = localtime(last_login_utc)
    else:
        last_login_local = None


    context = {
        'title': 'Dashboard',
        'name': 'there',
        'last_login_local': last_login_local,
        'profile_completed': 0,
        'bookmarks_count': 0,
    }

    name = request.user.get_short_name()
    if name != '':
        context['name'] = name.upper()

    profile_obj = request.user.profile
    null_count = 0
    for f in ["gpa", "gre_score", "toefl_score", "lor_score", "sop_score", "research", "chance_of_admit"]:
        if getattr(profile_obj, f, None) is None:
            null_count += 1
    context['profile_completed'] = int((10 - null_count) / 10 * 100)

    bookmarks_count = request.user.bookmarks.count()
    context['bookmarks_count'] = bookmarks_count

    context['trending_unis'] = trending_unis

    return render(request, 'dashboard/dashboard.html', context)
