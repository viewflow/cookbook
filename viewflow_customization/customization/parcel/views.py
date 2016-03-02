from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from viewflow.flow import flow_view, flow_start_view

from . import forms, models


@login_required
@flow_start_view()
def register_shipment(request, activation):
    if not activation.has_perm(request.user):
        raise PermissionDenied

    activation.prepare(request.POST or None, user=request.user)
    form = forms.ParcelForm(request.POST or None)

    if form.is_valid():
        activation.process.parcel = form.save()
        activation.done()
        return redirect('parcels')

    return render(request, 'parcel/shipmentflow/start.html', {
        'form': form,
        'activation': activation,
    })


@login_required
@flow_view()
def approve_shipment(request, activation):
    if not activation.has_perm(request.user):
        raise PermissionDenied

    activation.prepare(request.POST or None)
    form = forms.ApproveForm(request.POST or None, instance=activation.process)

    if form.is_valid():
        form.save()
        activation.done()
        return redirect('parcels')

    created_by = models.ShipmentTask.objects.get(
        process=activation.process,
        flow_task_type='START').owner

    return render(request, 'parcel/shipmentflow/approve.html', {
        'form': form,
        'activation': activation,
        'created_by': created_by
    })


@login_required
@flow_view()
def deliver(request, activation):
    activation.prepare(request.POST or None)
    if 'done' in request.POST:
        activation.done()
        return redirect('parcels')

    return render(request, 'parcel/shipmentflow/deliver.html', {
        'activation': activation,
    })


@login_required
@flow_view()
def deliver_assign(request, activation):
    if 'assign' in request.POST:
        activation.assign(user=request.user)
        activation.task.save()
        return redirect('parcels')

    return render(request, 'parcel/shipmentflow/deliver_assign.html', {
        'activation': activation,
    })


@login_required
@flow_view()
def deliver_report(request, activation):
    activation.prepare(request.POST or None)
    form = forms.ReportForm(request.POST or None, instance=activation.process)

    if form.is_valid():
        form.save()
        activation.done()
        return redirect('parcels')

    return render(request, 'parcel/shipmentflow/report.html', {
        'form': form,
        'activation': activation,
    })


@login_required
def details(request, process_pk):
    pass


@login_required
def task_list(request):
    tasks = models.ShipmentTask.objects.user_queue(request.user).order_by('-created')
    paginator = Paginator(tasks, 25)

    page = request.GET.get('page')
    try:
        tasks_page = paginator.page(page)
    except PageNotAnInteger:
        tasks_page = paginator.page(1)
    except EmptyPage:
        tasks_page = paginator.page(paginator.num_pages)

    return render(request, 'parcel/shipmentflow/tasks.html', {'tasks_page': tasks_page})


@login_required
def process_list(request):
    processes = models.ShipmentProcess.objects.all().order_by('-created')
    paginator = Paginator(processes, 25)

    page = request.GET.get('page')
    try:
        process_page = paginator.page(page)
    except PageNotAnInteger:
        process_page = paginator.page(1)
    except EmptyPage:
        process_page = paginator.page(paginator.num_pages)

    return render(request, 'parcel/shipmentflow/processes.html',
                  {'process_page': process_page})
