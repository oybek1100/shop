from django.db import models
from django.db.models import Avg

# Create your models here.

class baseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    

class Category(baseModel):
    title = models.CharField(max_length=100, unique=True)
    

    def __str__(self):
        return self.title
    
class Product(baseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    discount = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='products' , null=True, blank=True)
    quantity = models.IntegerField(default=1 , blank =True)

    @property
    def avg_rating(self):
        from django.db.models import Avg
        return self.comments.aggregate(Avg('rating'))['rating__avg'] or 0

    @avg_rating.setter
    def avg_rating(self, value):
        self._avg_rating = value

    @property
    def discounted_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class OrderDetail(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"
    
class Comment(baseModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, '1 Star'
        TWO = 2, '2 Stars'
        THREE = 3, '3 Stars'
        FOUR = 4, '4 Stars'
        FIVE = 5, '5 Stars'
        
    def __str__(self):
        return f"{self.product.name} - {self.rating} Stars"

    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    rating = models.IntegerField(choices=RatingChoices.choices, default=RatingChoices.THREE.value)

    
