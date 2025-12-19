from rest_framework import serializers
from .models import Course, Chapter, CourseAssignment, ChapterProgress


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = "__all__"
        read_only_fields = ("course",)


class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ("mentor", "created_at")


class CourseAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseAssignment
        fields = "__all__"


class ChapterProgressSerializer(serializers.ModelSerializer):
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)
    sequence = serializers.IntegerField(source='chapter.sequence_number', read_only=True)

    class Meta:
        model = ChapterProgress
        fields = ['chapter', 'chapter_title', 'sequence', 'completed', 'completed_at']

class CourseProgressSerializer(serializers.ModelSerializer):
    """
    Shows overall progress for a specific course assigned to the student.
    """
    course_title = serializers.CharField(source='course.title', read_only=True)
    total_chapters = serializers.IntegerField(read_only=True)
    completed_chapters = serializers.IntegerField(read_only=True)
    percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = CourseAssignment
        fields = ['course', 'course_title', 'total_chapters', 'completed_chapters', 'percentage']