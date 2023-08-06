from .comprobante import Comprobante
from .timbre_fiscal_digital import TimbreFiscalDigital

__all__ = [
    "Comprobante",
    "TimbreFiscalDigital",
    "CFDI_4_0_SCHEMA_LOCATION",
    "CFDI_4_0_NAMESPACES",
]

CFDI_4_0_SCHEMA_LOCATION = "http://www.sat.gob.mx/cfd/4 http://www.sat.gob.mx/sitio_internet/cfd/4/cfdv40.xsd"

CFDI_4_0_NAMESPACES = {
    'cfdi': 'http://www.sat.gob.mx/cfd/4',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}
