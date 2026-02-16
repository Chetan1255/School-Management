def school_context(request):
    if request.user.is_authenticated:
        return {
            "current_school": request.user.school
        }
    return {}
