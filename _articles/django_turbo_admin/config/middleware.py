def TurboMiddleware(get_response):
    def middleware(request):
        response = get_response(request)
        if request.path.startswith('/admin/') and request.method == 'POST':
            if response.status_code == 200:
                response.status_code = 422
            elif response.status_code == 301:
                response.status_code = 303
        return response

    return middleware
