from downloaders import chcy, ns, unch

SUPPORTED_DOWNLOADERS = {
    "chcy": [chcy.exporter, chcy.arguments, chcy.locale_keys],
    "ns": [ns.exporter, ns.arguments, ns.locale_keys],
    "unch": [unch.exporter, unch.arguments, unch.locale_keys],
}
