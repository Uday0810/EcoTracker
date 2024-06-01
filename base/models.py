from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum 
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Room(models.Model):
    name=models.CharField(max_length=200)
    description =models.TextField(null=True,blank=True)

    def __str__(self):
        return self.name
    
''''class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)'''

'''class CarbonFootprint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)'''
    #cf = models.FloatField()
    # Details related to carbon footprint calculation

class SustainabilityChallenge(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_challenges',null=True)
    participants = models.ManyToManyField(User, related_name='joined_challenges')
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    points_awarded = models.IntegerField(default=0)  # New field for awarded points

    # Other challenge details
   

class ChallengeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(SustainabilityChallenge, on_delete=models.CASCADE)
    submission_text = models.TextField()
    
class Reward(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)
    progress = models.FloatField(default=0)

    def __str__(self):
        return f"{self.user.username} - Total Points: {self.total_points} - Progress: {self.progress}"
    

class EducationalContent(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

class UserInput(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    twoWheeler = models.FloatField(default = 0)
    bus = models.FloatField(default = 0)
    car = models.FloatField(default = 0)
    trains = models.FloatField(default = 0)
    longHaulFlights = models.FloatField(default = 0)
    shortFlights = models.FloatField(default = 0)
    shortHaulFlights = models.FloatField(default = 0)
    ferry = models.FloatField(default = 0)
    naturalGas = models.FloatField(default = 0)
    coal = models.FloatField(default = 0)
    lpg = models.FloatField(default = 0)
    oil = models.FloatField(default = 0)
    metalBurned = models.FloatField(default = 0)
    glassBurned = models.FloatField(default = 0)
    paperBurned = models.FloatField(default = 0)
    organicWaste = models.FloatField(default = 0)
    electricityConsumed = models.FloatField(default = 0)
    waterConsumed = models.FloatField(default = 0)
    paperConsumed = models.FloatField(default = 0)
    cf = models.FloatField(null=True, blank=True)
    time_calculated = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calculate the CF before saving
        self.cf = self.calculate_cf()
        super().save(*args, **kwargs)

        leaderboard, created = Leaderboard.objects.get_or_create(user=self.user)
        leaderboard.update_total_cf()



    def calculate_cf(self):
        # Calculate CF using the formula: f1*e1 + f2*e2 + f3*e3
        return self.twoWheeler*0.117 + self.bus*0.065 + self.car*0.180 + self.longHaulFlights*0.065 + self.shortFlights*0.153 + self.shortHaulFlights*0.120 + self.ferry*0.116 + self.naturalGas*56 + self.coal*101 + self.lpg*72 + self.oil*85 + self.metalBurned*10.66 + self.glassBurned*6.8 + self.paperBurned*19.18 + self.organicWaste*74.09 + self.electricityConsumed*1.003 + self.waterConsumed*0.344 + self.paperConsumed*0.876

    def __str__(self):
        return f"{self.user} - CF: {self.cf}, Calculated at: {self.time_calculated}"
    
@receiver(post_save, sender=UserInput)
def update_leaderboard(sender, instance, **kwargs):
    # Update the Leaderboard whenever a User_Input instance is saved
    leaderboard, created = Leaderboard.objects.get_or_create(user=instance.user)
    leaderboard.update_total_cf()

class Leaderboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_cf = models.FloatField(default=0)  # Initial total CF is set to 0
    latest_cf = models.FloatField(default=0)

    def update_total_cf(self):
        # Calculate the total CF by summing the CF values from User_Input instances
        total_cf = UserInput.objects.filter(user=self.user).aggregate(Sum('cf'))['cf__sum']
        self.total_cf = total_cf if total_cf else 0

        # Get the latest UserInput instance for the user
        latest_user_input = UserInput.objects.filter(user=self.user).latest('time_calculated')
        self.latest_cf = latest_user_input.cf if latest_user_input else 0

        self.save()

    def __str__(self):
        return f"{self.user_id} - Total CF: {self.total_cf}, Latest CF: {self.latest_cf}"
    


'''class EcoProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    carbon_footprint = models.OneToOneField(Leaderboard, on_delete=models.CASCADE)'''
    #sustainability_score = models.IntegerField(default=0)
    # Other metrics and details

class UserChallenge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(SustainabilityChallenge, on_delete=models.CASCADE)
    #progress = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')],null=True)
    description = models.TextField(default="")

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({self.status})"
    
