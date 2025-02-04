def user_permissions(request):
    """Make user permissions available globally in templates."""
    return {
        "can_create_caterer": request.user.has_perm("orders.add_caterer") if request.user.is_authenticated else False
    }