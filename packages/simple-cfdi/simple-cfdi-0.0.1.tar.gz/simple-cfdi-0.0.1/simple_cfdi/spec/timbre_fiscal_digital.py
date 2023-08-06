from dataclasses import dataclass, field
from typing import Optional

__NAMESPACE__ = "http://www.sat.gob.mx/TimbreFiscalDigital"


@dataclass
class TimbreFiscalDigital:
    """
    Complemento requerido para el Timbrado Fiscal Digital que da validez al
    Comprobante fiscal digital por Internet.

    :ivar version: Atributo requerido para la expresión de la versión
        del estándar del Timbre Fiscal Digital
    :ivar uuid: Atributo requerido para expresar los 36 caracteres del
        folio fiscal (UUID) de la transacción de timbrado conforme al
        estándar RFC 4122
    :ivar fecha_timbrado: Atributo requerido para expresar la fecha y
        hora, de la generación del timbre por la certificación digital
        del SAT. Se expresa en la forma AAAA-MM-DDThh:mm:ss y debe
        corresponder con la hora de la Zona Centro del Sistema de
        Horario en México.
    :ivar rfc_prov_certif: Atributo requerido para expresar el RFC del
        proveedor de certificación de comprobantes fiscales digitales
        que genera el timbre fiscal digital.
    :ivar leyenda: Atributo opcional para registrar información que el
        SAT comunique a los usuarios del CFDI.
    :ivar sello_cfd: Atributo requerido para contener el sello digital
        del comprobante fiscal o del comprobante de retenciones, que se
        ha timbrado. El sello debe ser expresado como una cadena de
        texto en formato Base 64.
    :ivar no_certificado_sat: Atributo requerido para expresar el número
        de serie del certificado del SAT usado para generar el sello
        digital del Timbre Fiscal Digital.
    :ivar sello_sat: Atributo requerido para contener el sello digital
        del Timbre Fiscal Digital, al que hacen referencia las reglas de
        la Resolución Miscelánea vigente. El sello debe ser expresado
        como una cadena de texto en formato Base 64.
    """
    class Meta:
        namespace = "http://www.sat.gob.mx/TimbreFiscalDigital"

    version: str = field(
        init=False,
        default="1.1",
        metadata={
            "name": "Version",
            "type": "Attribute",
            "required": True,
        }
    )
    uuid: Optional[str] = field(
        default=None,
        metadata={
            "name": "UUID",
            "type": "Attribute",
            "required": True,
            "length": 36,
            "white_space": "collapse",
            "pattern": r"[a-f0-9A-F]{8}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{12}",
        }
    )
    fecha_timbrado: Optional[str] = field(
        default=None,
        metadata={
            "name": "FechaTimbrado",
            "type": "Attribute",
            "required": True,
            "white_space": "collapse",
            "pattern": r"(20[1-9][0-9])-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])T(([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9])",
        }
    )
    rfc_prov_certif: Optional[str] = field(
        default=None,
        metadata={
            "name": "RfcProvCertif",
            "type": "Attribute",
            "required": True,
            "min_length": 12,
            "white_space": "collapse",
            "pattern": r"[A-Z&Ñ]{3}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]",
        }
    )
    leyenda: Optional[str] = field(
        default=None,
        metadata={
            "name": "Leyenda",
            "type": "Attribute",
            "min_length": 12,
            "max_length": 150,
            "white_space": "collapse",
            "pattern": r"([A-Z]|[a-z]|[0-9]| |Ñ|ñ|!|\"|%|&|'|´|-|:|;|>|=|<|@|_|,|\{|\}|`|~|á|é|í|ó|ú|Á|É|Í|Ó|Ú|ü|Ü){1,150}",
        }
    )
    sello_cfd: Optional[str] = field(
        default=None,
        metadata={
            "name": "SelloCFD",
            "type": "Attribute",
            "required": True,
            "white_space": "collapse",
        }
    )
    no_certificado_sat: Optional[str] = field(
        default=None,
        metadata={
            "name": "NoCertificadoSAT",
            "type": "Attribute",
            "required": True,
            "length": 20,
            "white_space": "collapse",
            "pattern": r"[0-9]{20}",
        }
    )
    sello_sat: Optional[str] = field(
        default=None,
        metadata={
            "name": "SelloSAT",
            "type": "Attribute",
            "required": True,
            "white_space": "collapse",
        }
    )
