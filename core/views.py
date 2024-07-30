from django.shortcuts import get_object_or_404, render
from requests import get
from .models import Movie
from django.core.files.base import ContentFile
from django.conf import settings
import os

def task1(request):
    api_key = settings.OMDB_API_KEY
    response = get(f'http://www.omdbapi.com/?apikey={api_key}&s=avengers&page=1')
    data = response.json()
    movies = data.get('Search', [])  
    response = get(f'http://www.omdbapi.com/?apikey={api_key}&s=avengers&page=2')
    data = response.json()
    movies += data.get('Search', [])
    response = get(f'http://www.omdbapi.com/?apikey={api_key}&s=avengers&page=3')
    data = response.json()
    movies += data.get('Search', [])
    return render(request, 'core/task1.html', context={'movies': movies})

def task2(request):
    query = request.GET.get('query')
    t = request.GET.get('type')
    no = request.GET.get('no')
    print(query, t, no)

    api_key = settings.OMDB_API_KEY

    if query and t and no:
        if no == 't':
            api_url = f"http://www.omdbapi.com/?t={query}&type={t.lower()}&apikey={api_key}"
        else:
            api_url = f"http://www.omdbapi.com/?s={query}&type={t.lower()}&apikey={api_key}"
        
        response = get(api_url)
        data = response.json()
        if no == 't':
            movies = [data]
            # Download the image
            poster_url = data['Poster']
            response = get(poster_url)
            if response.status_code == 200:
                # Save the image to a ContentFile
                image_name = os.path.basename(poster_url)
                image_file = ContentFile(response.content)
                # Create the movie instance
                if Movie.objects.filter(title=data['Title']).exists():
                    m = Movie.objects.get(title=data['Title'])
                    m.searched += 1
                    m.save()
                else:
                    m = Movie(
                        title=data['Title'],
                        year=data['Year'],
                        plot=data['Plot'],
                        type=data['Type'],
                        box_office=int(data['BoxOffice'].replace(',', '').replace('$', '')),
                        rating=float(data['Ratings'][0]['Value'].split('/')[0])
                    )
                    # Save the image to the poster field
                    m.searched += 1
                    m.poster.save(image_name, image_file)
                    m.save()
        else:
            movies = data.get('Search', [])
    else:
        movies = []

    return render(request, 'core/task2.html', {'movies': movies})

def task3(request):
    movies = Movie.objects.all()
    print(movies)
    return render(request, 'core/task3.html', {'movies': movies})

def task4(request):
    movie1_title = request.GET.get('movie1')
    movie2_title = request.GET.get('movie2')

    if movie1_title and movie2_title:
        movie1 = get_object_or_404(Movie, title=movie1_title)
        movie2 = get_object_or_404(Movie, title=movie2_title)

        # Comparison logic
        if movie1.rating > movie2.rating:
            winner = movie1
        elif movie2.rating > movie1.rating:
            winner = movie2
        else:
            winner = "It's a draw!"

        return render(request, 'core/task4.html', {
            'movie1': movie1,
            'movie2': movie2,
            'winner': winner
        })
    else:
        movies = Movie.objects.all()
        return render(request, 'core/task4.html', {'movies': movies})
