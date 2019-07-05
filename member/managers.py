from django.contrib.auth.base_user import BaseUserManager


class MemberManager(BaseUserManager):
    use_in_migrations = True

    def _create_member(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("email must be Given.")
        email = self.normalize_email(email)
        member = self.model(email=email, **extra_fields)
        member.set_password(password)
        member.save(using=self._db)
        return member

    def create_member(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)

        return self._create_member(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self._create_member(email, password, **extra_fields)









