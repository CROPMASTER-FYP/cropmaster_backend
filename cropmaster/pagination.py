from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        response = super(StandardResultsSetPagination,
                         self).get_paginated_response(data)
        response.data['total_pages'] = self.page.paginator.num_pages
        response.data['page_size'] = self.page_size
        return response
    