from math import ceil


def paginate(
    items: list,
    total: int,
    page: int,
    size: int
) -> dict:
    """페이지네이션 결과 생성"""
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": ceil(total / size) if size > 0 else 0
    }
