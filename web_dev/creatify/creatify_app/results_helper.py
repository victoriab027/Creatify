from django.http import JsonResponse

def change_playlist_name(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        # Call the change_playlist_name() function with the selected title
        change_playlist_name(title)
        # Return a success JSON response
        return JsonResponse({'status': 'success'})
    # Return an error JSON response if the request method is not POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
