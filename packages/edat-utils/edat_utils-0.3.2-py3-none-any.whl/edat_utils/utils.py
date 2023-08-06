from strawberry.types import Info

EDAT_USER = 'X-EDAT-USER'


class EdatUtils:
    @staticmethod
    def get_fields(info: Info):
        selected_fields = {item.name for field in info.selected_fields
                           for selection in field.selections for item in selection.selections}
        return selected_fields
    
    @staticmethod
    def get_user(info: Info):
        request = info.context['request']
        user =  None
        if EDAT_USER in request.headers:
            user = request.headers[EDAT_USER]
        return user