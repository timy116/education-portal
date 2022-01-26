from django.urls import reverse

SUBJECT_PREFIX = "Education Portal"


def signature_line(request):
    return (
        f"\n\n本郵件是由系統自動寄發，請勿直接回覆，謝謝您。"
        f"\n\n\n祝一切順心，Education Portal 團隊\n"
        f"{request.build_absolute_uri(reverse('index'))}"
    )



def generate_message(request, subject, text_content):
    return {
        "subject": f"{SUBJECT_PREFIX}: {subject}",
        "text_content": (
            f"{text_content}"
            f"{signature_line(request)}"
        )
    }


def email_verification(request, token):
    subject = "電子郵件地址驗證"
    text_content = (
        f"請點擊此連結 "
        f"{request.build_absolute_uri(reverse('', kwargs={'token': token}))} "
        f"來驗證您的電子郵件地址。"
    )

    return generate_message(request, subject, text_content)
