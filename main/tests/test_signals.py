from django.test import TestCase
from main import models
from django.core.files.images import ImageFile
from decimal import Decimal

class TestSignal(TestCase):
    def test_thumbnails_are_generated_on_save(self):
        product = models.Product(name="Breguet-Classique-Automatic-40mm", price=Decimal("10000.00"),)
        product.save()

        with open("main/fixtures/Breguet-Classique-Automatic-40mm.jpg", "rb") as f:
            image = models.ProductImage(product=product, image=ImageFile(f, name="xxx.jpg"),)
            with self.assertLogs("main", level="INFO") as cm:
                image.save()

        self.assertGreaterEqual(len(cm.output), 1)
        image.refresh_from_db()

        with open("main/fixtures/Breguet-Classique-Automatic-40mm.jpg", "rb",) as f:
            expected_content = f.read()
            assert image.thumbnail.read() == expected_content

        image.thumbnail.delete(save=False)
        image.image.delete(save=False)
