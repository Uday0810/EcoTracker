from django.contrib import admin

# Register your models here.

from .models import Room, EducationalContent, SustainabilityChallenge, ChallengeSubmission,Reward, Leaderboard, UserInput, UserChallenge

admin.site.register(Room)
admin.site.register(ChallengeSubmission)
admin.site.register(Leaderboard)
admin.site.register(Reward)
admin.site.register(SustainabilityChallenge)
admin.site.register(EducationalContent)
admin.site.register(UserInput)
admin.site.register(UserChallenge)