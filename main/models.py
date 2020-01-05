from django.db import models

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

class ProductManager(models.Model):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='marca')
    name = models.CharField('nombre', max_length=40)
    description = models.TextField('descripción', blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(max_length=50)
    active = models.BooleanField('activo',default=True)
    in_stock = models.BooleanField('en stock', default=True)
    tags = models.ManyToManyField(ProductTag, blank=True)
    date_updated = models.DateTimeField('última actualización', auto_now=True)

    def get_image_url(self):
        img = self.productimage_set.first().thumbnail.url
        if img:
            return img
        return img #None

    class Meta:
        verbose_name = 'Producto'

    def __str__(self):
        return self.name
    
    def natural_key(self):
        return (self.slug,)

    slug_objects = ProductManager()
    objects = ActiveManager()

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='producto')
    image = models.ImageField('imagen', upload_to="product-images")
    thumbnail = models.ImageField('miniatura', upload_to="product-thumbnails", null=True)

    def __str__(self):
        return self.image.name.split('/')[-1]

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'
 