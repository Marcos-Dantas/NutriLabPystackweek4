from django.db import models
from django.contrib.auth.models import User

class Patients(models.Model):
    choices_sexo = (('F', 'Feminino'),
                    ('M', 'Maculino'))
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=choices_sexo)
    age = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=19)
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

class PatientData(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE)
    data = models.DateTimeField()
    weight = models.IntegerField()
    height = models.FloatField()
    percentage_grease = models.IntegerField()
    percentage_muscle = models.IntegerField()
    colesterol_hdl = models.IntegerField()
    colesterol_ldl = models.IntegerField()
    colesterol_total = models.IntegerField()
    trigliceridios = models.IntegerField()
 
    def __str__(self):
        return f"Paciente({self.patient.name}, {self.weight})"

    class Meta:
        verbose_name = 'PatientData'
        verbose_name_plural = 'PatientDatas'
