from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import Image, Vote
from .elo import calculate_elo_rating
import random
from .models import Visitor, VisitorCounter

def index(request):
    
    unique_visitors_count = Visitor.objects.values('ip_address').distinct().count() # Assuming there's only one counter instance
    images = list(Image.objects.all())
    if len(images) < 2:
        return render(request, 'comparison/index.html', {'error': 'Not enough images to compare.'})
    
    image1, image2 = random.sample(images, 2)
    return render(request, 'comparison/index.html', {'image1': image1, 'image2': image2, 'counter': unique_visitors_count})

@transaction.atomic
def vote(request, image1_id, image2_id, winner_id):
    image1 = get_object_or_404(Image, pk=image1_id)
    image2 = get_object_or_404(Image, pk=image2_id)
    winner = get_object_or_404(Image, pk=winner_id)

    if winner not in [image1, image2]:
        return redirect('index')

    loser = image1 if winner == image2 else image2

    winner_rating, loser_rating = calculate_elo_rating(winner.elo_rating, loser.elo_rating)
    winner.elo_rating = winner_rating
    loser.elo_rating = loser_rating
    winner.save()
    loser.save()

    Vote.objects.create(image1=image1, image2=image2, winner=winner)
    return redirect('index')


from django.shortcuts import render
from .models import Vote

def winner(request):
    top_images = Image.objects.order_by('-elo_rating')[:3]
    
    context = {
        'top_images': top_images,
    }
    return render(request, 'comparison/winner.html', context)


