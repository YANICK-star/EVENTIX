from .models import Category, Event

def eventix_globals(request):
    try:
        categories = Category.objects.all()
    except Exception:
        categories = []
    
    return {
        'global_categories': categories,
        'global_cities': [c[0] for c in Event.CITY_CHOICES],
        'current_year': 2026,
    }
