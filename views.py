from rest_framework.viewsets import ModelViewSet 
from .models import Usuario, Medicamento, Recordatorio, Historial, Cuidador 
from .serializers import ( 
    UsuarioSerializer, MedicamentoSerializer, RecordatorioSerializer, HistorialSerializer, CuidadorSerializer 
) 
 
class UsuarioViewSet(ModelViewSet): 
    queryset = Usuario.objects.all() 
    serializer_class = UsuarioSerializer 
 
 
class MedicamentoViewSet(ModelViewSet): 
    queryset = Medicamento.objects.all() 
    serializer_class = MedicamentoSerializer 
 
 
class RecordatorioViewSet(ModelViewSet): 
    queryset = Recordatorio.objects.all() 
    serializer_class = RecordatorioSerializer 
 
 
class HistorialViewSet(ModelViewSet): 
    queryset = Historial.objects.all() 
    serializer_class = HistorialSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        if instance.estado == 'completado':
            # Llamar al método para incrementar el contador
            instance.incrementar_veces_enviado()

 
class CuidadorViewSet(ModelViewSet): 
    queryset = Cuidador.objects.all() 
    serializer_class = CuidadorSerializer