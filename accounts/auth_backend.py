

from .models import User
class EmailOrUsernameBackend:
    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = username

        user = (
            User.objects.filter(email=identifier).first()
            or User.objects.filter(username=identifier).first()
        )

        if user and user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
