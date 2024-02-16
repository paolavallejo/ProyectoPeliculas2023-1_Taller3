from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
import matplotlib.pyplot as plt

from .models import Movie, Review

from .forms import ReviewForm

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm: 
       movies = Movie.objects.filter(title__icontains=searchTerm) 
    else: 
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies': movies})


def about(request):
    return render(request, 'about.html')


def detail(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie = movie)
    return render(request, 'detail.html',{'movie':movie, 'reviews': reviews})

@login_required
def createreview(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if request.method == 'GET':
        return render(request, 'createreview.html',{'form':ReviewForm(), 'movie': movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(request, 'createreview.html',{'form':ReviewForm(),'error':'bad data passed in'})

@login_required       
def updatereview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.method =='GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html',{'review': review,'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            return render(request, 'updatereview.html',{'review': review,'form':form,'error':'Bad data in form'})
        
@login_required
def deletereview(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    review.delete()
    return redirect('detail', review.movie.id)


def movies_by_year():
    movies = Movie.objects.values('year').annotate(total=Count('id'))
    return movies

def prepare_data():
    movies = movies_by_year()
    years = [movie['year'] for movie in movies]
    totals = [movie['total'] for movie in movies]
    print(years)
    print(totals)
    return years, totals

def plot_movies_by_year(request):
    years, totals = prepare_data()
    plt.bar(years, totals)
    plt.xlabel('Año')
    plt.ylabel('Cantidad de películas')
    plt.title('Cantidad de películas por año')
    plt.grid(True)
    plt.show()