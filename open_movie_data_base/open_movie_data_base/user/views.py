from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic as views

from open_movie_data_base.user.forms import AppUserForm, MovieDirectorEditForm, ActorEditForm, RegularUserEditForm, \
    UserSignInForm
from open_movie_data_base.user.models import MovieDirector, Actor, RegularUser
from open_movie_data_base.utils.func import user_is_owner_of_profile

UserModel = get_user_model()


class SignUp(views.CreateView):
    model = UserModel
    form_class = AppUserForm
    template_name = 'user/sign-up.html'
    success_url = reverse_lazy('dispatcher')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return result


class SignIn(auth_views.LoginView):
    form_class = UserSignInForm
    template_name = 'user/sign-in.html'


class ProfileDetails(views.DetailView):
    model = RegularUser
    template_name = 'user/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_movies'] = self.get_liked_movie()
        context['posted_reviews'] = self.get_posted_reviews()
        return context

    def get_liked_movie(self):
        return self.object.user.like_set.all().count()

    def get_posted_reviews(self):
        return self.object.user.review_set.all().count()


class MovieDirectorDetails(views.DetailView):
    model = MovieDirector
    template_name = 'user/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movies = self.get_directed_movies()
        context['movie_count'] = movies.count
        context['likes'] = self.get_movie_likes()
        context['overall_rating'] = self.get_overall_rating()
        context['recent_movies'] = self.get_directed_movies().order_by('uploaded_on')[:4]

        return context

    def get_movie_likes(self):
        movies = self.get_directed_movies()
        likes = 0
        for movie in movies:
            likes += movie.like_set.all().count()
        return likes

    def get_overall_rating(self):
        movies = self.get_directed_movies()
        rating = 0
        for movie in movies:
            rating += movie.averagereviewscore.score
        if rating > 0:
            return rating / movies.count()
        return 0.00

    def get_directed_movies(self):
        return self.object.movie_set.all()


class ActorProfileDetails(views.DetailView):
    model = Actor
    template_name = 'user/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stars_in'] = self.stars_in()
        context['known_for'] = self.get_most_rated_movie()
        return context

    def stars_in(self):
        return self.object.movie_set.all()

    def get_most_rated_movie(self):
        movie_set = self.stars_in()
        if movie_set:
            return movie_set.order_by('-averagereviewscore__score')[:1][0]
        return None


def profile_dispatcher(request):
    user = request.user
    if user.is_movie_director:
        return redirect('edit-movie-director', user.moviedirector.slug)
    elif user.is_actor:
        return redirect('actor-details', user.actor.slug)
    elif user.is_regular_user:
        return redirect('profile-details', user.regularuser.slug)


def edit_profile(request, slug):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    user = RegularUser.objects.filter(slug=slug).get()
    if not user_is_owner_of_profile(request, user):
        return redirect('profile-dispatcher')

    if request.method == 'POST':
        form = RegularUserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile-details', user.slug)
    else:
        form = RegularUserEditForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'user/edit-profile.html', context)


def edit_movie_director(request, slug):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    user = MovieDirector.objects.filter(slug=slug).get()
    if not user_is_owner_of_profile(request, user):
        return redirect('profile-dispatcher')

    if request.method == 'POST':
        form = MovieDirectorEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('director-details', user.slug)
    else:
        form = MovieDirectorEditForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'user/edit-profile.html', context)


def edit_actor(request, slug):
    if not request.user.is_authenticated:
        return redirect('sign-in')
    user = Actor.objects.filter(slug=slug).get()
    if not user_is_owner_of_profile(request, user):
        return redirect('profile-dispatcher')

    if request.method == 'POST':
        form = ActorEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('actor-details', user.slug)
    else:
        form = ActorEditForm(instance=user)

    context = {
        'form': form,
        'user': user,
    }

    return render(request, 'user/edit-profile.html', context)
