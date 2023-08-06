from lxml import etree


def assert_equal_xml(test_case, xml1_data: bytes, xml2_data: bytes):
    """
    Assert that two xml trees are equal by comparing their nodes
    and attributes
    """
    xml1 = etree.fromstring(xml1_data)
    xml2 = etree.fromstring(xml2_data)

    return assert_equal_xml_etree(test_case, xml1, xml2)


def assert_equal_xml_etree(test_case, node1: etree, node2: etree):
    """
    Compare two nodes by tag name, attributes and children nodes
    """

    test_case.assertEqual(node1.tag, node2.tag)

    # compare attributes
    node1_attrib_keys = sorted(node1.attrib.keys())
    node2_attrib_keys = sorted(node2.attrib.keys())

    test_case.assertEqual(node1_attrib_keys, node2_attrib_keys)
    for key in node1_attrib_keys:
        try:
            # try cast to float
            val1 = float(node1.attrib[key])
            val2 = float(node2.attrib[key])
        except ValueError:
            val1 = node1.attrib[key]
            val2 = node2.attrib[key]

        test_case.assertEqual(val1, val2, f"key: {key}, val1: {val1}, val2: {val2}")

    node_1_test = node1.text or ""
    node_2_test = node2.text or ""

    test_case.assertEqual(
        node_1_test.strip(),
        node_2_test.strip(),
        f"node1.text: {node_1_test}, node2.text: {node_2_test}",
    )

    node1_children = list(node1)
    node2_children = list(node2)
    test_case.assertEqual(
        len(node1_children),
        len(node2_children),
        f"node {node1.tag}: different children number:"
        f"{len(node1_children)} != {len(node2_children)}",
    )

    for child1, child2 in zip(node1_children, node2_children):
        assert_equal_xml_etree(test_case, child1, child2)
