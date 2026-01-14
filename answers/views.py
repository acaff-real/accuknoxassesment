import threading
from django.http import JsonResponse
from django.dispatch import Signal, receiver
from django.db import transaction
from .models import AuditEntry
from .geometry import Rectangle
order_processed = Signal()

@receiver(order_processed)
def inventory_notification(sender, **kwargs):
    receiver_thread = threading.current_thread().name
    kwargs['audit_log'].append(f"Receiver ran on: {receiver_thread}")


def proof_by_thread_view(request):
    audit_log = []
    
    view_thread = threading.current_thread().name
    audit_log.append(f"View started on: {view_thread}")

    order_processed.send(sender=None, audit_log=audit_log)
    audit_log.append("View finished execution")
    return JsonResponse({
        "proof_logic": "If the Thread Names are identical, the signal ran synchronously.",
        "execution_log": audit_log
    })

order_signal = Signal()

@receiver(order_signal)
def order_receiver(sender, **kwargs):
    receiver_thread_id = threading.get_native_id()
    kwargs['audit_log'].append(f"Receiver Thread ID: {receiver_thread_id}")


def question_two_view(request):
    audit_log = []
    caller_thread_id = threading.get_native_id()
    audit_log.append(f"Caller Thread ID: {caller_thread_id}")
    order_signal.send(sender=None, audit_log=audit_log)
    return JsonResponse({
        "question": "Do django signals run in the same thread as the caller",
        "conclusion": "Yes, Django signals run in the same thread as the caller",
        "log": audit_log
    })

rollback_signal = Signal()


@receiver(rollback_signal)
def transaction_receiver(sender, **kwargs):
    
    AuditEntry.objects.create(message="Receiver Entry")
    print("Receiver: Created entry in DB.")


def question_three_view(request):
    initial_count = AuditEntry.objects.count()
    
    try:
        with transaction.atomic():
            AuditEntry.objects.create(message="Caller Entry")
            rollback_signal.send(sender=None)
            raise Exception("Force Rollback")
            
    except Exception as e:
        print(f"Transaction rolled back due to: {e}")

    final_count = AuditEntry.objects.count()
    if final_count == initial_count:
        result = "SAME TRANSACTION (Both rolled back)"
    else:
        result = "DIFFERENT TRANSACTION"

    return JsonResponse({
        "question": "By default do django signals run in the same database transaction as the caller?",
        "conclusion": result,
        "initial_db_count": initial_count,
        "final_db_count": final_count,
        "logic": "Due to the receiver's entry disappearing after the caller rolled back, the transaction is rolled back as well."
    })



class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

def question_four_view(request):
    rect = Rectangle(length=7, width=3)
    results = [item for item in rect]
    
    return JsonResponse({
        "topic": "Custom Classes in Python",
        "input_values": {"length": 7, "width": 3},
        "iteration_output": results
    })