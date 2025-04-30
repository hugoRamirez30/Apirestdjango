from rest_framework import serializers 
from .models import Usuario, Medicamento, Recordatorio, Historial, Cuidador 
 
class UsuarioSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Usuario 
        fields = ['id', 'nombre', 'correo'] 
 
 
class MedicamentoSerializer(serializers.ModelSerializer): 
    usuario_nombre = serializers.CharField(source='usuario.nombre', read_only=True) 
 
    class Meta: 
        model = Medicamento 
        fields = ['id', 'nombre', 'dosis', 'frecuencia', 'duracion', 'usuario', 'usuario_nombre'] 
 
 
class RecordatorioSerializer(serializers.ModelSerializer): 
    numero_notificaciones = serializers.SerializerMethodField() 
    medicamento_nombre = serializers.CharField(source='medicamento.nombre', read_only=True) 

    class Meta: 
        model = Recordatorio 
        fields = ['id', 'frecuencia_envio', 'cantidad_pastillas', 'medicamento', 'medicamento_nombre', 'numero_notificaciones'] 

    def get_numero_notificaciones(self, obj): 
        return obj.calcular_numero_notificaciones()

 
 
class HistorialSerializer(serializers.ModelSerializer): 
    medicamento_nombre = serializers.CharField(source='medicamento.nombre', read_only=True) 
    veces_enviado = serializers.IntegerField(read_only=True)  # Mostrar el contador de veces enviados

    class Meta: 
        model = Historial 
        fields = ['id', 'evento', 'fecha_hora', 'medicamento', 'medicamento_nombre', 'veces_enviado']

 
 
class CuidadorSerializer(serializers.ModelSerializer): 
    usuarios_asignados = UsuarioSerializer(many=True, read_only=True) 
    usuarios_ids = serializers.PrimaryKeyRelatedField( 
        many=True, queryset=Usuario.objects.all(), write_only=True, source='usuarios_asignados' 
    ) 
 
    class Meta: 
        model = Cuidador 
        fields = ['id', 'nombre', 'correo', 'telefono', 'usuarios_asignados', 'usuarios_ids']