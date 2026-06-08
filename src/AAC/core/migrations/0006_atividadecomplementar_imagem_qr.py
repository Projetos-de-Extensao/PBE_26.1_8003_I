from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_atividadecomplementar_aluno_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividadecomplementar',
            name='imagem_qr',
            field=models.ImageField(blank=True, null=True, upload_to='qrcodes/'),
        ),
    ]
