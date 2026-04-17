from src.api.views.base import *
from django.contrib.auth.models import User
from django.db.models import Sum, Count


@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    top_users = (
        User.objects
        .filter(submissions__is_correct=True)
        .annotate(
            total_points=Sum('submissions__points_earned'),
            solved_count=Count('submissions__task', distinct=True),
        )
        .order_by('-total_points', '-solved_count')[:50]
    )

    data = [
        {
            'rank': i + 1,
            'username': u.username,
            'total_points': u.total_points or 0,
            'solved_count': u.solved_count or 0,
        }
        for i, u in enumerate(top_users)
    ]
    return Response(data)
