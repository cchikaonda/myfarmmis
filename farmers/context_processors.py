from .models import Season

def season_context(request):
    season_id = request.GET.get("season")
    selected_season = None

    if season_id:
        selected_season = Season.objects.filter(id=season_id).first()

    # If no season selected, use latest
    if not selected_season:
        selected_season = Season.objects.order_by('-year').first()

    seasons = Season.objects.order_by('-year')

    return {
        "seasons": seasons,
        "selected_season": selected_season
    }
