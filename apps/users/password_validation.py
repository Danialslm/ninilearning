from django.contrib.auth.password_validation import UserAttributeSimilarityValidator


class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    DEFAULT_USER_ATTRIBUTES = ('phone_number', 'first_name', 'last_name')

    def __init__(self, user_attributes=DEFAULT_USER_ATTRIBUTES, max_similarity=0.7):
        super().__init__(user_attributes, max_similarity)
