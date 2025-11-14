from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "topic"
        verbose_name_plural = "topics"

    def __str__(self):
        return f"{self.name}"


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(
        default=0,
        verbose_name="years of experience"
    )

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("catalog:redactor-detail", kwargs={"pk": self.pk})


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="title")
    content = models.TextField(verbose_name="content")
    published_date = models.DateField(verbose_name="published date")
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        verbose_name="topic",
        related_name="articles"
    )
    redactors = models.ManyToManyField(
        Redactor,
        related_name="articles",
        verbose_name="redactors"
    )

    class Meta:
        verbose_name = "article"
        verbose_name_plural = "articles"
        ordering = ["-published_date"]

    def __str__(self):
        return self.title
