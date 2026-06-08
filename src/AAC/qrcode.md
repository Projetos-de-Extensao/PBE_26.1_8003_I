# Roteiro: Geração de QR Code para AtividadeComplementar

## Visão Geral

Ao criar uma `AtividadeComplementar`, o sistema gera automaticamente uma imagem QR Code que codifica a URL da página daquela atividade. A imagem é salva no servidor e associada ao registro via o campo `imagem_qr`.

---

## 1. Dependências

Instale as bibliotecas necessárias:

```bash
pip install "qrcode[pil]" Pillow
```

| Biblioteca | Finalidade |
|---|---|
| `qrcode` | Geração do QR Code |
| `Pillow` | Renderização da imagem PNG |

---

## 2. Configuração no `settings.py`

Adicione a URL base do projeto para que o QR Code aponte para o endereço correto:

```python
# aac/settings.py
SITE_URL = 'https://seu-dominio.com'  # ou http://localhost:8000 em desenvolvimento

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

> Sem `SITE_URL`, o sistema usa `http://localhost:8000` como padrão.

---

## 3. Modelo (`core/models.py`)

### 3.1 Imports adicionados

```python
import io
import qrcode
from django.conf import settings
from django.core.files.base import ContentFile
```

### 3.2 Campo `imagem_qr`

Adicionado ao modelo `AtividadeComplementar`:

```python
imagem_qr = models.ImageField(
    upload_to='qrcodes/',
    null=True,
    blank=True
)
```

As imagens são salvas em `media/qrcodes/`.

### 3.3 Método `_gerar_qr_code()`

Responsável por criar a imagem PNG do QR Code:

```python
def _gerar_qr_code(self):
    base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    url = f"{base_url}/atividades/{self.pk}/"
    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return ContentFile(buffer.getvalue(), name=f'qr_atividade_{self.pk}.png')
```

**Fluxo:**
1. Monta a URL da atividade usando o `pk` do registro
2. Gera o QR Code com `qrcode.make()`
3. Salva em memória (`BytesIO`) no formato PNG
4. Retorna um `ContentFile` pronto para ser salvo no banco

### 3.4 Método `save()` sobrescrito

Aciona a geração automática do QR Code ao criar uma atividade:

```python
def save(self, *args, **kwargs):
    gerar_qr = not self.pk or not self.imagem_qr
    super().save(*args, **kwargs)
    if gerar_qr:
        self.imagem_qr.save(
            f'qr_atividade_{self.pk}.png',
            self._gerar_qr_code(),
            save=True
        )
```

**Por que salvar antes de gerar?**  
O `pk` só existe após o primeiro `super().save()`. Por isso, o QR Code é gerado na segunda etapa, já com o ID disponível.

---

## 4. Migration

Arquivo: `core/migrations/0006_atividadecomplementar_imagem_qr.py`

```python
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
```

Aplicar a migration:

```bash
python manage.py migrate
```

---

## 5. Estrutura de arquivos gerados

```
media/
└── qrcodes/
    ├── qr_atividade_1.png
    ├── qr_atividade_2.png
    └── ...
```

---

## 6. Exibir o QR Code em template HTML

```html
{% if atividade.imagem_qr %}
    <img src="{{ atividade.imagem_qr.url }}" alt="QR Code da Atividade" width="150">
{% endif %}
```

---

## 7. Fluxo completo resumido

```
Usuário cadastra atividade
        │
        ▼
AtividadeComplementar.save() chamado
        │
        ├─► super().save() → registro salvo no banco (pk gerado)
        │
        └─► _gerar_qr_code()
                │
                ├─► Monta URL: {SITE_URL}/atividades/{pk}/
                ├─► qrcode.make(url) → imagem QR
                ├─► Salva como PNG em memória (BytesIO)
                └─► imagem_qr.save() → grava em media/qrcodes/
```
