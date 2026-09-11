from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Chore, Housemate, ChoreLog

def chore_list(request):
    housemates = Housemate.objects.all().order_by('name')
    selected_housemate_id = request.GET.get('housemate')
    
    chores = Chore.objects.select_related('assigned_to').all()
    if selected_housemate_id:
        chores = chores.filter(assigned_to_id=selected_housemate_id)
        
    pending_chores = chores.filter(status=Chore.Status.PENDING).order_by('due_date')
    completed_chores = chores.filter(status=Chore.Status.DONE).order_by('-due_date')
    recent_logs = ChoreLog.objects.select_related('chore', 'completed_by').order_by('-completed_at')[:10]

    context = {
        'pending_chores': pending_chores,
        'completed_chores': completed_chores,
        'housemates': housemates,
        'selected_housemate_id': selected_housemate_id,
        'recent_logs': recent_logs,
        'recurrence_choices': Chore.Recurrence.choices,
    }
    return render(request, 'chores/index.html', context)

def add_chore(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        recurrence = request.POST.get('recurrence', Chore.Recurrence.WEEKLY)
        assigned_to_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date') or timezone.now().date()

        if title:
            assigned_to = Housemate.objects.filter(id=assigned_to_id).first() if assigned_to_id else None
            Chore.objects.create(
                title=title,
                description=description,
                recurrence=recurrence,
                assigned_to=assigned_to,
                due_date=due_date
            )
    return redirect('chore_list')

def toggle_chore_status(request, chore_id):
    chore = get_object_or_404(Chore, id=chore_id)
    if chore.status == Chore.Status.PENDING:
        chore.status = Chore.Status.DONE
        chore.save()
        if chore.assigned_to:
            ChoreLog.objects.create(
                chore=chore,
                completed_by=chore.assigned_to,
                notes="Marked complete via web dashboard"
            )
    else:
        chore.status = Chore.Status.PENDING
        chore.save()
    return redirect('chore_list')

def add_housemate(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        if name and email:
            Housemate.objects.get_or_create(email=email, defaults={'name': name})
    return redirect('chore_list')
