from rest_framework import serializers
from .models import Reviews
from apps.products.serializers import ProductSerializer
from apps.users.serializers import CustomerSerializer
from django.utils import timezone


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)

    # write-only input for creating reviews
    product_id = serializers.IntegerField(write_only=True, required=True)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    reviews_comment = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Reviews
        fields = '__all__'

    def create(self, validated_data):
        # Pop write-only fields
        product_id = validated_data.pop('product_id', None)
        rating = validated_data.get('rating')
        reviews_comment = validated_data.get('reviews_comment', '')

        request = self.context.get('request') if hasattr(self, 'context') else None
        customer = None
        if request and getattr(request, 'user', None):
            # CustomJWTAuthentication attaches .customer to user when available
            user = request.user
            customer = getattr(user, 'customer', None)

        from apps.products.models import Products
        from django.utils import timezone as dj_timezone

        # Create review record; do not modify models
        review = Reviews()
        if product_id:
            try:
                review.product = Products.objects.get(product_id=product_id)
            except Products.DoesNotExist:
                review.product = None

        review.customer = customer
        review.rating = rating
        review.reviews_comment = reviews_comment
        review.publication_date = dj_timezone.now()
        review.status = 'published'
        review.save()
        return review
