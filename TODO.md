# TODO - Deploy Render (Workscape/AAC)

- [ ] Atualizar settings.py para produção (DEBUG/ALLOWED_HOSTS/SECRET_KEY via env, MEDIA_ROOT, STATIC_ROOT, CORS)
- [ ] Garantir persistência do SQLite e arquivos de upload no Render via volumes
- [ ] Validar migrações (python manage.py makemigrations --check e migrate)
- [ ] Atualizar requisitos/arquitetura de start (gunicorn presente)
- [ ] Comitar mudanças na branch deploy
- [ ] Rodar check local: manage.py check e collectstatic (opcional)

