from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .models import top_post, response_post, Profile
from .models import tags as modelsTag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.forms import modelformset_factory
# from .forms import ImageForm, PostForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import top_post, response_post, image
from .models import image as dbimage
from .forms import PostForm, ImageForm, TagForm
from random import randrange
from django.contrib import messages
from .forms import *
import json
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator1
import requests as Requests
import json as Json
from geopy.geocoders import Nominatim
#######
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Profile
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib import messages
import random
import time
#######

@login_required
def new_top_post(request):
    ImageFormSet = modelformset_factory(dbimage,
                                        form=ImageForm, extra=10)

    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=dbimage.objects.none())
        tagsForm = TagForm(request.POST)
        if postForm.is_valid() and formset.is_valid():
            title = request.POST['title']
            text = request.POST['text']
            tags = request.POST['tag']
            tags = tags.split(',')
            newTopPost = top_post(title=title,
                                  text=text,
                                  created_date=timezone.now(),
                                  published_date=timezone.now(),
                                  user_id=request.user, )
            newTopPost.author = request.user.username
            newTopPost.save()
            # Get object to save with images
            topPostInstance = get_object_or_404(top_post, post_id=newTopPost.post_id)
            for form in formset.cleaned_data:
                try:
                    image = form['image']
                    photo = dbimage(image=image, top_post_id=topPostInstance)
                    photo.save()
                except KeyError:
                    pass

            for tag in tags:
                tag = tag.strip()
                newTag = modelsTag(tag=tag, top_post_id=topPostInstance)
                newTag.save()

            return HttpResponseRedirect(reverse('blog'))
        else:
            print(tagsForm.errors)
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=dbimage.objects.none())
        tagForm = TagForm()
    return render(request, 'blog/new_post.html',
                  {'postForm': postForm, 'formset': formset, 'tagForm': TagForm})

@login_required
def getForecast(request):

    lat = request.GET['lat']
    lon = request.GET['lon']
    ZIP = request.GET['zip']

    getHistorical = False
    year = request.GET['year']
    month = request.GET['month']
    day = request.GET['day']

    unixTime = ''
    if year != '' and month != '' and day != '':
        getHistorical = True

        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            pass

        if not year.isdigit():
            pass
        elif not month.isdigit():
            pass
        elif not day.isdigit():
            pass

        pattern = '%Y%m%d'
        date_time = str(year) + str(month) + str(day)
        unixTime = str(int(time.mktime(time.strptime(date_time, pattern))))

    if ZIP == '':
        # If no user zipcode, get one from a large US city/zip
        if request.user.profile.zipcode:
            ZIP = request.user.zipcode
        else:
            ZIP = random.choice(['79936', '90011', '60629', '90650', '90201',
                                 '77084','92335','78521','77449','78572','90250',])

    openFailure = True
    wunderFailure = True
    darkSkyFailure = True
    json = {}

    showingZIP = False
    showingLatLon = False
    # Dark Sky Key = 02ec64c91583d9ce29f972682bbfb4cf

    # Gets data for each api based on input
    # The resulting lat long is pass to the javascript google map on the dashboard    
    if lat != '' and lon != '':
        r = Requests.get('http://api.openweathermap.org/data/2.5/forecast?lat=' + str(lat) + '&lon=' + str(lon) + '&APPID=431a44405aef953371bcbe245588e0c7')
        wund = Requests.get('http://api.wunderground.com/api/f807def6b862d1f5/alerts/q/' + str(lat) + ',' + str(lon) + '.json')
        if getHistorical:
            darkSky = Requests.get('https://api.darksky.net/forecast/02ec64c91583d9ce29f972682bbfb4cf/' + str(lat) + ',' + str(lon) + ',' + unixTime)
            if darkSky.status_code == 200:
                darkSkyFailure = False
                darkSkyText = darkSky.json()
        if r.status_code == 200:
            openFailure = False
            json = r.json()
        if wund.status_code == 200:
            wunderFailure = False
            wundText = wund.json()

        showingLatLon = True
    elif ZIP != '':
        r = Requests.get('http://api.openweathermap.org/data/2.5/forecast?zip=' + str(ZIP) + '&APPID=431a44405aef953371bcbe245588e0c7')
        wund = Requests.get('http://api.wunderground.com/api/f807def6b862d1f5/alerts/q/' + str(ZIP) + '.json')
        if r.status_code == 200 or wund.status_code == 200:
            openFailure = False
            json = r.json()
        if wund.status_code == 200:
            wunderFailure = False
            wundText = wund.json()
       
        geolocator = Nominatim()
        location = geolocator.geocode(ZIP)
        lat = location.latitude
        lon = location.longitude
        if getHistorical:
            darkSky = Requests.get('https://api.darksky.net/forecast/02ec64c91583d9ce29f972682bbfb4cf/' + str(lat) + ',' + str(lon) + ',' + unixTime)
            if darkSky.status_code == 200:
                darkSkyFailure = False
                darkSkyText = darkSky.json()

        showingZIP = True
    else:
        ZIP = random.choice(['79936', '90011', '60629', '90650', '90201',
                                 '77084','92335','78521','77449','78572','90250',])
            
    # Unpack Open weathermap
    headers = ['Time (UTC)', 'Avg Temp (F)', 'Max Temp (F)', 'Min Temp (F)', 'Pressure', 'Cloudiness', 'Wind Speed', 'Wind Direction', 'Weather Main', 'Weather Descriptions']

    times = []
    avgTemps = []
    maxTemps = []
    minTemps = []
    pressures = []
    clouds = []
    windSpeed = [] 
    windDirection = [] 
    weatherMains = []
    weatherDescs = []
    displayForecast = [times, avgTemps,maxTemps, minTemps, pressures, 
                       clouds, windSpeed, windDirection, weatherMains, weatherDescs,]
    displayFiveDayForecast = False
    if not openFailure:
        displayFiveDayForecast = True

        for item in json['list']:
        
            times.append(item['dt_txt'][:16])
            avgTemps.append(item['main']['temp'])
            maxTemps.append(item['main']['temp_max'])
            minTemps.append(item['main']['temp_min'])
            pressures.append(item['main']['pressure'])
            clouds.append(item['clouds']['all'])
            windSpeed.append(item['wind']['speed'])
            windDirection.append(item['wind']['deg'])
            weatherMains.append(item['weather'][0]['main'])
            weatherDescs.append(item['weather'][0]['description'])
        displayForecast2 = []
        temps = [avgTemps, maxTemps, minTemps]
        def kelvinToFarenheight(list):
            newTemps = []
            for temp in list:
                temp = round(1.8 * (temp - 273) + 32, 1)
                newTemps.append(temp)
            return newTemps

        avgTemps = kelvinToFarenheight(avgTemps)
        maxTemps = kelvinToFarenheight(maxTemps)
        minTemps = kelvinToFarenheight(minTemps)

        displayForecast[1] = avgTemps
        displayForecast[2] = maxTemps
        displayForecast[3] = minTemps

        for pred in displayForecast:
            displayForecast2 += pred
    else:
        displayForecast2 = []

    # WUnderground Alerts UnPacking
    displayAlerts = False
    alertsForDisplay = []
    if not wunderFailure:
        displayAlerts = True
        if not wundText['alerts']:
            for alert in wundText['alerts']:
                alertsForDisplay.append([alert['description'], alert['date'], alert['expires'], alert['message']])
        else:
            alertsForDisplay.append(['No Alerts', 'No Alerts',
                                    'No Alerts', 'No Alerts'])

    # DarkSky Alert Unpacking
    # Histical Times = 6:00am - 12pm - 6pm - 12am - avg daily temp
    displayHistorical = False
    darkSkyDisplayDict = {}
    if not darkSkyFailure:
        displayHistorical = True
        darkSkyDisplay = []
        minTempHistorical = 999
        maxTempHistorical = -999
        avgTempHistorical = 0
        avgHumidity = 0
        avgWindSpeed = 0
        avgCloudCover = 0
        avgPrecipProb = 0
        avgPrecipIntensity = 0
        summary = []
        counter = 0
        try:
            for data in darkSkyText['hourly']['data']:
                summary.append(data['summary'])
                if data['temperature'] < minTempHistorical:
                    minTempHistorical = data['temperature']
                if data['temperature'] > maxTempHistorical:
                    maxTempHistorical = data['temperature']
                avgTempHistorical += data['temperature']
                avgHumidity += data['humidity']
                avgPrecipProb += data['precipProbability']
                avgPrecipIntensity += data['precipIntensity']
                avgWindSpeed += data['windSpeed']
                avgCloudCover += data['cloudCover']
                counter += 1
        except KeyError:
            print('Error')

        try:
            summary = random.choice(summary)
            avgHumidity = round(avgHumidity / counter, 2)
            avgWindSpeed = round(avgWindSpeed / counter, 2)
            avgCloudCover = round(avgCloudCover / counter, 2)
            avgPrecipProb = round(avgPrecipProb / counter, 2)
            avgPrecipIntensity = round(avgPrecipIntensity / counter, 2)
        except ZeroDivisionError:
            print('Error')



        darkSkyDisplayDict = {'summary':summary, 'minTempHistorical':minTempHistorical,
                              'maxTempHistorical':maxTempHistorical, 'avgTempHistorical':avgTempHistorical,
                              'avgHumidity':avgHumidity, 'avgWindSpeed':avgWindSpeed, 'avgCloudCover':avgCloudCover,
                              'avgPrecipProb':avgPrecipProb, 'avgPrecipIntensity':avgPrecipIntensity,}


    return render(request, 'blog/dashboard.html', {'lat':lat, 'lon':lon,
                                                   'ZIP':ZIP, 'openFailure':openFailure,
                                                   'displayForecast':displayForecast2,
                                                   'headers':headers, 'alertsForDisplay':alertsForDisplay,
                                                   'showingZIP':showingZIP, 'showingLatLon':showingLatLon,
                                                   'darkSkyDisplayDict':darkSkyDisplayDict, 'displayHistorical':displayHistorical,
                                                   'displayAlerts':displayAlerts, 'displayFiveDayForecast':displayFiveDayForecast,
                                                   'year':year, 'month':month, 'day':day,
                                                    })

@login_required
def post_deleted(request, id):
    post = top_post.objects.get(post_id=id).delete()
    return render(request, 'blog/post_deleted_after.html')

@login_required
def post_detail(request, post_id):
    topPost = get_object_or_404(top_post, post_id=post_id)
    images = image.objects.filter(top_post_id=topPost.post_id)
    isAuthor = False

    if request.user.username == topPost.user_id.username:
        isAuthor = True
    dateNow = timezone.now()
    return render(request, 'blog/post_detail.html', {'post': topPost, 'images': images,
                                                     'isAuthor': isAuthor, 'dateNow': dateNow})


@login_required
def delete_image(request, id):
    # Get the ID for the page to redirect to after deletion
    postId = image.objects.get(id=id)
    postId = postId.top_post_id.post_id
    images = image.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('post_edit', kwargs={'post_id': postId}))


@login_required
def post_edit(request, post_id):
    topPost = get_object_or_404(top_post, post_id=post_id)
    # Need to lay these out in an editable way
    images = image.objects.filter(top_post_id=topPost.post_id)
    if request.method == "POST":
        postForm = PostForm(request.POST, prefix='PostForm')
        if postForm.is_valid():
            title = request.POST['PostForm-title']
            text = request.POST['PostForm-text']
            newTopPost = top_post.objects.get(post_id=post_id)
            newTopPost.title = title
            newTopPost.text = text
            newTopPost.save()
            # newTopPost = top_post.objects.get(post_id=post_id)
            return redirect('post_detail', post_id=newTopPost.post_id)
    else:
        form = PostForm(instance=topPost, prefix='PostForm')
        # images = ImageForm()
        return render(request, 'blog/post_edit.html', {'form': form, 'images': images})

def home(request):
    return render(request, 'blog/home.html')


@login_required
def dashboard(request):
    return render(request, 'blog/dashboard.html')


@login_required
def locations(request):
    return render(request, 'blog/locations.html')


def blog(request):
    topPosts = top_post.objects.all().order_by('-post_id')
    displayImages = []
    # Get some default image if posts don't have an image
    defaultImage = None  # image.objects.get(image='blogImages/2018/03/20/instructor.jpg')
    for post in topPosts:
        allBlogImages = image.objects.filter(top_post_id=post.post_id)
        try:
            randomImage = allBlogImages[randrange(0, len(allBlogImages))]
        except:
            randomImage = defaultImage
        displayImages.append(randomImage)
    return render(request, 'blog/blog.html', {'topPosts': topPosts, 'blogImages': displayImages})


@login_required
def blog_search(request):  # , formTags):
    if request.method == 'GET':
        # SearchForm
        newSearch = request.GET['search']
        # I should upgrade this to also split on a comma
        searchTerms = newSearch.split()
        postIds = []
        for tag in searchTerms:
            dataBaseTags = modelsTag.objects.filter(tag=tag)
            for dataBaseTag in dataBaseTags:
                post = dataBaseTag.top_post_id
                postIds.append(post.post_id)
        # #topPosts = top_post.objects.all().order_by('-post_id')
        topPosts = top_post.objects.filter(post_id__in=postIds)
        displayImages = []
        # Get some default image if posts don't have an image
        defaultImage = None
        for post in topPosts:
            allBlogImages = image.objects.filter(top_post_id=post.post_id)
            try:
                randomImage = allBlogImages[randrange(0, len(allBlogImages))]
            except:
                randomImage = defaultImage
            displayImages.append(randomImage)
        # Display search error if no posts are found
        if len(topPosts) > 0:
            return render(request, 'blog/blog.html', {'topPosts': topPosts, 'blogImages': displayImages})
        else:
            topPosts = []
            errorPost = top_post(post_id=999999999, published_date=timezone.now(), title="No Results!",
                                 text='Separate Search Terms by a Space', user_id=request.user)
            errorPost.author = 'Oh No'
            topPosts.append(errorPost)

            return render(request, 'blog/blog.html', {'topPosts': topPosts, 'blogImages': displayImages})

    else:
        topPosts = None
        displayImages = None
        return render(request, 'blog/blog.html', {'topPosts': topPosts, 'blogImages': displayImages})




def about_us(request):
    language_translator = LanguageTranslator(
        username='90cbe197-3db2-45e1-8d4b-0a95444275f0',
        password='jxPHFLuHnTra')

    translation = language_translator.translate(
        text=['Join us in the quest to witness a tornado close and personal.We are the StormChasers.Storm chasing,also referred to as tornado chasing tours, tornado safaris or storm safaris,with organized tours is a rapidly growing tourism industry where experienced storm chasers guide adventurers and tourists to amazing severe weather.The hunt for tornadoes, super cells, hail, lightning goes all over the Midwestern states of USA.The tours are usually between 5-10 days in order to maximize your chances of seeing Mother Nature in her worst mood. Storm Chasing usually takes place in the spring, around May-June, but you can go chasing in April and July as well. The tour could take you from the Rocky Mountains in the West to the East coast and from the Mexican border in the South up to the Canadian border in the North.The nature of weather makes it impossible to know where you will be any given day.The StormChasers community will guide you towards an experience of a lifetime, which will become truly addicting.StormChasers is not a Tour company, we just provide the information about the storm chasing.We like to be a one stop storm chasing blog on the web.'],
        source='en',
        target='fr')

    translatedtext = json.dumps(translation, indent=2, ensure_ascii=False)

    t = json.loads(translatedtext)

    translation = t['translations'][0]['translation']

    return render(request, 'blog/about_us.html', {'translations': translation})



# def about_us1(request):
#     language_translator1 = LanguageTranslator1(
#         username='0a1ec0ad-b7d8-4b8c-a6cc-d368be0c96ac',
#         password='I6lRukwzjTo4')
#
#     translation1 = language_translator1.translate(
#         text=['Join us in the quest to witness a tornado close and personal.We are the StormChasers.'],
#         source='en',
#         target='es')
#
#     translatedtext1 = json.dumps(translation1, indent=2, ensure_ascii=False)
#
#     t1 = json.loads(translatedtext1)
#
#     translationes = t1['translations'][0]['translation']
#
#     print(translationes)
#
#     return render(request, 'blog/about_us.html', {'translationsp': translationes})

@login_required
def subscriptions(request):
    return render(request, 'blog/subscriptions.html')


@login_required
def add_comment_to_post(request, post_id):
    post = get_object_or_404(top_post, post_id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.top_post_id = post
            comment.user_id = request.user
            comment.author = request.user.username
            comment.is_approved = True
            comment.save()
            return redirect('post_detail', post_id=post.post_id)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


'''Uses old django girls post object
@login_required
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now())
    return render(request, 'blog/post_list.html', {'posts': posts})
'''

'''Uses old django girls post object
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
'''

'''Uses old django girls post object
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
'''


def pwd_recover(request):
    return render(request, 'blog/pwd_recover.html',
                  {'xxx': pwd_recover})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = Profile.objects.create(user=new_user)
            return render(request, 'blog/register_done.html', {'profile': profile, 'new_user': new_user})
        # return render(request,
        #  'blog/register_done.html',
        # {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'user_form': user_form})


@login_required
def comment_approve(request, post_id):
    comment = get_object_or_404(response_post, post_id=post_id)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, post_id):
    comment = get_object_or_404(response_post, post_id=post_id)
    comment.text = 'COMMENT DELETED'
    comment.save()
    return redirect('post_detail', post_id=comment.top_post_id.post_id)

####
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

@login_required
def my_profile(request):
    return render(request, 'blog/my_profile.html', {'section':'my_profile'})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'blog/my_profile.html', {'section': 'my_profile'})
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile)
    return render(request,
                  'blog/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
