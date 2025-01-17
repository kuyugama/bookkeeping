from fastapi import Query


def require_page(page: int = Query(1, ge=1, description="№ Сторінки")):
    """Return page number provided by user"""
    return page
