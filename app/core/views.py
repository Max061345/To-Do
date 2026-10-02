from django.http import JsonResponse
from django.db import connection
from django.db.utils import OperationalError

def health_check(request):
    db_status = "ok"
    try:
        connection.ensure_connection()
    except OperationalError:
        db_status = "error"

    status = "ok" if db_status == "ok" else "error"

    return JsonResponse({"status": status, "db": db_status}, status=200 if status == "ok" else 503)