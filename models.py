from django.db import models 
 
class Cuidador(models.Model): 
    nombre = models.CharField(max_length=255) 
    correo = models.EmailField(unique=True) 
    telefono = models.CharField(max_length=20) 
    usuarios_asignados = models.ManyToManyField('Usuario', related_name='cuidadores') 
 
    def __str__(self): 
        return self.nombre 
 
    def ver_recordatorios(self): 
        """Obtiene todos los recordatorios de los usuarios asignados.""" 
        return Recordatorio.objects.filter(medicamento__usuario__in=self.usuarios_asignados.all()) 
 
    def ver_historial(self): 
        """Obtiene todo el historial de los medicamentos de los usuarios asignados.""" 
        return Historial.objects.filter(medicamento__usuario__in=self.usuarios_asignados.all()) 
 
    def gestionar_medicamentos(self): 
        """Retorna los medicamentos de los usuarios asignados.""" 
        return Medicamento.objects.filter(usuario__in=self.usuarios_asignados.all()) 
 
class Usuario(models.Model): 
    nombre = models.CharField(max_length=255) 
    correo = models.EmailField(unique=True) 
 
    def __str__(self): 
        return self.nombre 
 
class Medicamento(models.Model): 
    nombre = models.CharField(max_length=255) 
    dosis = models.CharField(max_length=100) 
    frecuencia = models.IntegerField(help_text="Frecuencia en horas") 
    duracion = models.IntegerField(help_text="Duración en días") 
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='medicamentos') 
 
    def __str__(self): 
        return f"{self.nombre} - {self.usuario.nombre}" 
 
class Recordatorio(models.Model): 
    hora = models.DateTimeField() 
    fecha_inicio = models.DateTimeField() 
    fecha_fin = models.DateTimeField() 
    estado = models.CharField(max_length=50, choices=[ 
        ('pendiente', 'Pendiente'), 
        ('completado', 'Completado'), 
    ]) 
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='recordatorios') 
    frecuencia_envio = models.IntegerField(help_text="Frecuencia en horas")  # Nuevos campos
    cantidad_pastillas = models.IntegerField(help_text="Cantidad de pastillas que tiene el usuario")  # Nuevos campos

    def __str__(self): 
        return f"Recordatorio para {self.medicamento.nombre} - {self.hora}"

    def calcular_numero_notificaciones(self):
        """Método para calcular cuántas notificaciones se deben enviar."""
        # Suponiendo que la duración del tratamiento está en días y multiplicando por la cantidad de pastillas
        duracion_tratamiento = self.medicamento.duracion
        return (duracion_tratamiento * self.cantidad_pastillas) // self.frecuencia_envio
 
 
class Historial(models.Model):
    evento = models.CharField(max_length=255)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    medicamento = models.ForeignKey(Medicamento, on_delete=models.CASCADE, related_name='historial')
    estado = models.CharField(max_length=50, choices=[('pendiente', 'Pendiente'), ('completado', 'Completado')], default='pendiente')
    veces_enviado = models.IntegerField(default=0)  # Asegúrate de que este campo esté aquí

    def __str__(self):
        return f"{self.evento} - {self.medicamento.nombre} ({self.fecha_hora})"

    def incrementar_veces_enviado(self):
        """Método para incrementar el contador de veces_enviado"""
        self.veces_enviado += 1
        self.save()
