from django.db import models

# Create your models here.


class category(models.Model):
	name = models.CharField(max_length = 100)
	status = models.BooleanField(default = True)

	def __str__(self):
		return self.name



class product(models.Model):
	prdtname=models.CharField(max_length = 100)
	prdtprice=models.CharField(max_length = 100)
	shrtdesc=models.TextField()
	longdesc=models.TextField()
	prdtcat=models.ForeignKey(category,on_delete=models.CASCADE)
	quant=models.CharField(max_length = 100)
	slug=models.SlugField(unique=True)
	active=models.BooleanField(default = True)


	def __str__(self):
		return self.slug

class prdt_imag(models.Model):
	singleprdt=models.ForeignKey(product,on_delete=models.CASCADE)
	img=models.ImageField(upload_to = 'product_image/',null=True)
	active=models.BooleanField(default = True)


	def __str__(self):
		return self.singleprdt.prdtname




class signup1(models.Model):
	name=models.CharField(max_length=100)
	userid=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	email=models.CharField(max_length=100)
	phoneno=models.IntegerField()

class Orders(models.Model):
    order_id= models.AutoField(primary_key=True)
    items_json= models.CharField(max_length=5000)
    amount=models.IntegerField()
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone=models.CharField(max_length=111, default="")

class OrderUpdate(models.Model):
    update_id  = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
