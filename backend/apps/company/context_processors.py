from typing import Optional

from .models import CompanyInfo


def company_info(request) -> dict:
    """Make the company info singleton available in every template context."""
    info: Optional[CompanyInfo] = None
    try:
        info = CompanyInfo.objects.filter(is_active=True).first()
    except Exception:
        # Table may not exist yet during initial migrations.
        pass

    return {"company_info": info}
