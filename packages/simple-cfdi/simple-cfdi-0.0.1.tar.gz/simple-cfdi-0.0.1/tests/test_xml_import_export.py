import decimal
import os
import unittest

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from simple_cfdi.spec import CFDI_4_0_NAMESPACES, CFDI_4_0_SCHEMA_LOCATION, Comprobante
from tests.utils import assert_equal_xml


class TestXMLImportExport(unittest.TestCase):
    def test_import_export_xml(self):
        """
        Test importing cfdi_4_0_invoice.xml into Comprobante class
        """

        current_module_path = os.path.dirname(__file__)
        with open(current_module_path + "/fixtures/cfdi_4_0_invoice.xml", "rb") as f:
            fixture = f.read()

        xml_parser = XmlParser()
        invoice_cfdi = xml_parser.from_bytes(fixture, Comprobante)

        ###
        # Check that CFDI fields are correctly loaded from xml_data
        ###

        # check CFDI general fields
        self.assertEqual(invoice_cfdi.version, "4.0")
        self.assertEqual(invoice_cfdi.serie, "Serie")
        self.assertEqual(invoice_cfdi.folio, "Folio")
        self.assertEqual(invoice_cfdi.fecha, "2022-07-19T00:18:10")
        self.assertTrue(invoice_cfdi.sello)
        self.assertEqual(invoice_cfdi.forma_pago, "99")
        self.assertEqual(invoice_cfdi.sub_total, "200")
        self.assertEqual(invoice_cfdi.moneda, "AMD")
        self.assertEqual(invoice_cfdi.total, "198.96")
        self.assertEqual(invoice_cfdi.tipo_de_comprobante, "I")
        self.assertEqual(invoice_cfdi.metodo_pago, "PPD")
        self.assertEqual(invoice_cfdi.exportacion, "01")
        self.assertEqual(invoice_cfdi.lugar_expedicion, "20000")

        # check CFDI Emisor fields
        emisor = invoice_cfdi.emisor
        self.assertEqual(emisor.rfc, "EKU9003173C9")
        self.assertEqual(emisor.nombre, "ESCUELA KEMPER URGATE")
        self.assertEqual(emisor.regimen_fiscal, "601")

        # check CFDI Receptor fields
        receptor = invoice_cfdi.receptor
        self.assertEqual(receptor.rfc, "URE180429TM6")
        self.assertEqual(receptor.nombre, "UNIVERSIDAD ROBOTICA ESPAÑOLA")
        self.assertEqual(receptor.domicilio_fiscal_receptor, "65000")
        self.assertEqual(receptor.regimen_fiscal_receptor, "601")
        self.assertEqual(receptor.uso_cfdi, "G01")

        # check CFDI Conceptos fields
        conceptos = invoice_cfdi.conceptos.concepto
        self.assertEqual(len(conceptos), 1)
        concepto = conceptos[0]
        self.assertEqual(concepto.clave_prod_serv, "50211503")
        self.assertEqual(concepto.cantidad, 1.0)
        self.assertEqual(concepto.clave_unidad, "H87")
        self.assertEqual(concepto.descripcion, "Cigarros")
        self.assertEqual(concepto.valor_unitario, "200.00")
        self.assertEqual(concepto.importe, "200.00")
        self.assertEqual(concepto.objeto_imp, "02")

        impuestos_traslados = concepto.impuestos.traslados.traslado
        self.assertEqual(len(impuestos_traslados), 1)
        impuesto_traslado = impuestos_traslados[0]
        self.assertEqual(impuesto_traslado.base, 1)
        self.assertEqual(impuesto_traslado.impuesto, "002")
        self.assertEqual(impuesto_traslado.tipo_factor, "Tasa")
        self.assertEqual(impuesto_traslado.tasa_ocuota, decimal.Decimal("0.160000"))
        self.assertEqual(impuesto_traslado.importe, "0.16")

        # create xml from Comprobante class using  XmlSerializer
        serializer_config = SerializerConfig(
            schema_location=CFDI_4_0_SCHEMA_LOCATION,
        )
        serializer = XmlSerializer(config=serializer_config)
        xml_data = serializer.render(invoice_cfdi, ns_map=CFDI_4_0_NAMESPACES)

        assert_equal_xml(self, xml_data.encode("utf-8"), fixture)


if __name__ == "__main__":
    unittest.main()
