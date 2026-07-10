from django.db import models
from django.conf import settings # Best practice for linking to the User model

# It's good practice to import your CustomUser model directly for type hinting,
# but use settings.AUTH_USER_MODEL for ForeignKey relationships.
from users.models import CustomUser


class Tag(models.Model):
    """Represents a category tag for a question, like 'python' or 'placements'."""
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    """Represents a question posted by a user in the forum."""
    # --- THIS IS THE CORRECTED FIELD ---
    # Using 'author' is clearer than 'user'.
    # settings.AUTH_USER_MODEL always points to your active user model (CustomUser).
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # auto_now_add=True automatically sets this field to the current time
    # only when the object is first created.
    created_at = models.DateTimeField(auto_now_add=True)
    
    # A question can have many tags, and a tag can be on many questions.
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    """Represents an answer to a specific question, posted by a user."""
    # A ForeignKey relationship to the Question model.
    # related_name='answers' lets us use question.answers.all() to get all answers for a question.
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    
    # --- THIS IS THE CORRECTED FIELD ---
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Answer by {self.author.username} to "{self.question.title}"'