from django.test import TestCase
import time

# Create your tests here.
localTime = time.localtime()
strTime = time.strftime("%Y-%m-%d %H:%M:%S", localTime)
print(strTime)
