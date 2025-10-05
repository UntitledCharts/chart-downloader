from downloaders import chcy, ns, unch, sb

SUPPORTED_DOWNLOADERS = {
    "pjsk": [sb.exporter, sb.arguments, sb.locale_keys],
    "chcy": [chcy.exporter, chcy.arguments, chcy.locale_keys],
    "ns": [ns.exporter, ns.arguments, ns.locale_keys],
    "unch": [unch.exporter, unch.arguments, unch.locale_keys],
}
