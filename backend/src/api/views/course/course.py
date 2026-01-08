# src/api/views/course/course.py
from src.api.views.base import *
from django.db import IntegrityError



class CourseViewSet(BaseViewSet):
    queryset = CourseModel.objects.all()
    search_fields = ("title", "description")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    ordering_fields = ("created_at", "title")
    ordering = ("-created_at",)
    serializer_class = CourseSerializer

    # def get_serializer_class(self):
    #     if self.action == "retrieve":
    #         return CourseDetailSerializer
    #     return CourseSerializer



# src/api/views/course/course.py
from src.api.views.base import *
from django.db import IntegrityError



class CourseViewSet(BaseViewSet):
    queryset = CourseModel.objects.all()
    search_fields = ("title", "description")
    filter_backends = [DjangoFilterBackend, SearchFilter]
    ordering_fields = ("created_at", "title")
    ordering = ("-created_at",)
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOnly()]
        return []



    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def enroll(self, request, pk=None):
        course = self.get_object()
        user = request.user

        if not user or not course:
            return Response({"detail": "User or course invalid"}, status=400)

        # Oldindan tekshirish: agar foydalanuvchi allaqachon enroll qilgan bo‘lsa
        if EnrollmentModel.objects.filter(user=user, course=course).exists():
            return Response({"detail": "Already enrolled"}, status=200)

        try:
            EnrollmentModel.objects.create(user=user, course=course)
        except IntegrityError as e:
            print("Enrollment IntegrityError:", e)  # console log
            return Response({"detail": "DB error, enrollment failed"}, status=400)

        return Response({"detail": "Successfully enrolled"}, status=201)
    
    
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_path='is-enrolled')
    def is_enrolled(self, request, pk=None):
        course = self.get_object()
        user = request.user
        enrolled = EnrollmentModel.objects.filter(user=user, course=course).exists()
        return Response({"enrolled": enrolled})


    