from django.contrib.auth.hashers import check_password
from .models import User


class UserBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, email=None, password=None):
        try:
            # Try to find a user matching your username
            user = User.objects.filter(email=email).first()
            print(user)
            #  Check the password is the reverse of the username
            if check_password(password, user.password):
                # Yes? return the Django user object
                return user, True
            else:
                # No? return None - triggers default login failed
                return None, True
        except User.DoesNotExist:
            # No user was found, return None - triggers default login failed
            return None, False
        except Exception as e:
            print(e)
            return None, False

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None