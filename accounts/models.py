from django.db import models
from django.contrib.auth.hashers import make_password

class userType(models.TextChoices):
    REGULAR = 'regular', 'Regular'
    DEV = 'dev', 'Dev'


class User(models.Model):
    username    = models.CharField(max_length=50, unique=True)
    email       = models.EmailField(unique=True)
    full_name   = models.CharField(max_length=120)
    password_hash = models.CharField(max_length=128)  # stores make_password(value)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    user_type   = models.CharField(max_length=20, default='regular')

    USERNAME_FIELD = 'email'        # what we use to log in
    REQUIRED_FIELDS = ['full_name'] # for createsuperuser (optional)

    class Meta:
        db_table = "Users"
    def __str__(self):
        return self.email

    def set_unusable_password(self):
        self.password = None

    def has_usable_password(self):
        return False

    # --- helper to set password ---------------------------------
    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    # --- helper to check password -------------------------------
    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password as chk
        return chk(raw_password, self.password_hash)

    # --- attribute expected by Django’s login_required ----------
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    # --- required by Django’s admin -----------------------------


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    device = models.CharField(max_length=250, blank=True)
    ip = models.CharField(max_length=45, blank=True)
    status = models.CharField(max_length=30, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "user_sessions"

    def __str__(self):
        return f"{self.user} - {self.session_key} - {self.status}"
