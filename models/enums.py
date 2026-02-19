import enum

class TipoResiduo(str, enum.Enum):
    plastico = "plastico"
    papel = "papel"
    vidrio = "vidrio"
    organico = "organico"
    electronico = "electronico"

class EstadoResiduo(str, enum.Enum):
    pendiente = "pendiente"
    reciclado = "reciclado"
