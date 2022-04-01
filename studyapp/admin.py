from django.contrib import admin

from .models import Course, Reply, Meeting, Profile

# Register your models here.

class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 3

# class CourseAdmin(admin.CourseAdmin):
#     model = Course
#     fieldsets = [
#         (None, {'fields': ['course_name']})
#     ]

class MeetingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['post_text']}),
        ('Date information', {'fields': ['post_date'], 'classes': ['collapse']}),
    ]
    inlines = [ReplyInline]
    list_display = ('post_text', 'post_date', 'was_posted_recently')
    list_filter = ['post_date']
    search_fields = ['post_text']

admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Profile)