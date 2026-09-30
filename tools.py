def calculator(expression: str):
    return eval(expression)


FAQS = {
    "refund": "Customers can request a refund within 30 days of purchase.",
    "delivery": "Standard delivery takes 3 to 5 business days.",
    "support": "Customer support is available Monday to Friday, 9 AM to 6 PM.",
}


def faq_lookup(topic: str):
    return FAQS.get(topic.lower(), "I couldn't find information about that topic.")
