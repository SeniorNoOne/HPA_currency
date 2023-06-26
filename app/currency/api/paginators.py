from rest_framework.pagination import CursorPagination, LimitOffsetPagination


class CurrencyApiLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100


# Have some problems with cursor pagination
class CurrencyApiCursorPagination(CursorPagination):
    page_size = 50
    ordering = '-id'
