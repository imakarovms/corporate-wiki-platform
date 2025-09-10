from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0002_alter_article_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='articles/', verbose_name='Файл'),
        ),
    ]