from django.db import models
from ckeditor.fields import RichTextField

class InfoPage(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(unique=True, verbose_name="URL-имя")
    content = RichTextField(verbose_name="Содержимое")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Информационная страница"
        verbose_name_plural = "Информационные страницы"

class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    answer = RichTextField(verbose_name="Ответ")

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = "Часто задаваемый вопрос"
        verbose_name_plural = "Часто задаваемые вопросы"