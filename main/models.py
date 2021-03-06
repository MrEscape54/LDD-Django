from django.contrib.auth.models import (AbstractUser, BaseUserManager,)
from django.urls import reverse
from django.db import models
from django.core.validators import MinValueValidator

class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)

class BrandManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Brand(models.Model):
    name = models.CharField('nombre', max_length=20)
    slug = models.SlugField(max_length=20)
    active = models.BooleanField('activo',default=True)
    logo = models.ImageField(upload_to='logo-images', null=True)

    def __str__(self):
        return self.name
    
    def natural_key(self):
        return (self.slug,)

    objects = BrandManager()

    class Meta:
        verbose_name = 'Marca'

class ProductTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)
        
class ProductTag(models.Model):
    name = models.CharField('nombre', max_length=40)
    slug = models.SlugField(max_length=40)
    active = models.BooleanField('activo', default=True)

    def __str__(self):
        return self.name
   
    def natural_key(self):
        return (self.slug,)
   
    objects = ProductTagManager()

    class Meta:
        verbose_name = 'Etiqueta'

class ProductManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='marca')
    name = models.CharField('nombre', max_length=100)
    description = models.TextField('descripción', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(max_length=100)
    active = models.BooleanField('activo',default=True)
    in_stock = models.BooleanField('en stock', default=True)
    tags = models.ManyToManyField(ProductTag, blank=True)
    date_updated = models.DateTimeField('última actualización', auto_now=True)

    def get_image_url(self):
        try:
            return self.productimage_set.first().thumbnail.url
        except :
            return None
            
    class Meta:
        verbose_name = 'Producto'

    def __str__(self):
        return self.name
    
    def natural_key(self):
        return (self.slug,)

    slug_objects = ProductManager()
    objects = ActiveManager()

class ProductImageManager(models.Manager):
    def get_by_natural_key(self, image):
        return self.get(image=image)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
    image = models.ImageField('imagen', upload_to="product-images")
    thumbnail = models.ImageField('miniatura', upload_to="product-thumbnails", null=True)

    def __str__(self):
        return self.image.name.split('/')[-1]
    
    def natural_key(self):
        return (self.image,)
   
    objects = ProductImageManager()

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, first_name, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, first_name, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("email address", unique=True)
    first_name = models.CharField(max_length=40, blank=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

class Address(models.Model):
    SUPPORTED_COUNTRIES = (
        ('AR', 'Argentina'),
        ('UY', 'Uruguay'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField('nombre completo',max_length=60)
    address1 = models.CharField('dirección 1', max_length=120)
    phone = models.CharField('teléfono', max_length=20)
    zip_code = models.CharField('código postal', max_length=12)

    city = models.CharField('ciudad', max_length=50)
    country = models.CharField('país', max_length=3, choices=SUPPORTED_COUNTRIES)

    def get_absolute_url(self):
        return reverse("main:address_list")

    def __str__(self):
        return ", ".join(self.name, self.address1, self.phone, self.zip_code, self.city, self.country)

class Basket(models.Model):
    OPEN = 10
    SUBMITTED = 20
    STATUSES = ((OPEN, 'Open'), (SUBMITTED, 'Submitted'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.IntegerField(choices=STATUSES, default=OPEN)

    def is_empty(self):
        return self.basketline_set.all().count() == 0

    def count(self):
        return sum(i.quantity for i in self.basketline_set.all())

class BasketLine(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name='carrito')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
    quantity = models.PositiveIntegerField('cantidad', default=1, validators=[MinValueValidator(1)])
    
 