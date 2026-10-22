from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import apptracker_tracking
from django.views.decorators.http import require_POST
from django.db import IntegrityError, DatabaseError, transaction
from django.contrib import messages
from datetime import date
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)
# Update the tracker


#For creating new application




@login_required
def application_create(request):
    if request.method == "POST":
        username = request.user.username

        college_name = request.POST.get("college_name", "").strip()
        program_name = request.POST.get("program_name", "").strip()
        application_type = request.POST.get("application_type")
        application_status = request.POST.get("application_status")
        test_score_needed = request.POST.get("test_score_needed")
        cv_needed = request.POST.get("cv_needed")
        personal_statement_needed = request.POST.get("personal_statement_needed")
        transcripts_needed = request.POST.get("transcripts_needed")

        # Convert deadline to a date
        deadline_raw = request.POST.get("application_deadline", "").strip()

        try:
            application_deadline = (
                date.fromisoformat(deadline_raw) if deadline_raw else None
            )
        except ValueError:
            messages.error(request, "Please enter a valid application deadline.")
            return render(request, "apptracker/application_form.html")

        # Convert application fee to Decimal
        fee_raw = request.POST.get("application_fee", "").strip()

        try:
            application_fee = Decimal(fee_raw) if fee_raw else None
        except InvalidOperation:
            messages.error(request, "Please enter a valid application fee.")
            return render(request, "apptracker/application_form.html")

    
        # Convert recommendation letters to int
        reco_raw = request.POST.get("reco_letters_needed", "").strip()

        try:
            reco_letters_needed = int(reco_raw) if reco_raw else None
        except InvalidOperation:
            messages.error(request, "Please enter a valid number for recommendation letter.")
            return render(request, "apptracker/application_form.html")

        # Save the application
        apptracker_tracking.objects.create(
            username=username,
            college_name=college_name,
            program_name=program_name,
            application_type=application_type,
            application_deadline=application_deadline,
            application_status=application_status,
            test_score_needed=test_score_needed,
            transcripts_needed=transcripts_needed,
            cv_needed=cv_needed,
            application_fee=application_fee,
            personal_statement_needed=personal_statement_needed,
            reco_letters_needed=reco_letters_needed,
        )

        messages.success(request, "Application created successfully.")
        return redirect("application_search")

    # Display the form for GET requests
    return render(request, "apptracker/application_form.html")


# For Querying after creating new application
def application_list(request):
    query = request.GET.get("q", "").strip()

    applications = apptracker_tracking.objects.filter(
        username=request.user.username, delete_flag=False,
    )

    return render(
        request,
        "apptracker/application_list.html",
        {
            "applications": applications,
            "query": query,
        }
    )


 #For Querying applications
def application_search(request):

    query = request.GET.get("q", "").strip()

    applications = apptracker_tracking.objects.filter(
    username=request.user.username, delete_flag=False,)

    if query:
        applications = applications.filter(
            Q(college_name__icontains=query) |
            Q(program_name__icontains=query) |
            Q(application_type__icontains=query) |
            Q(application_status__icontains=query)
        )
        

    return render(
        request,
        "apptracker/application_search.html",
        {
            "applications": applications,
            "query": query,
        }
    )


 #For updting application
@login_required
def application_update(request, pk):
    application = get_object_or_404(
        apptracker_tracking,
        pk=pk,
        username=request.user.username
    )

    if request.method == "POST":
        application.college_name = request.POST.get("college_name")
        application.program_name = request.POST.get("program_name")
        application.application_type = request.POST.get("application_type")
        application.application_status = request.POST.get("application_status")

        # Convert deadline to a date
        deadline_raw = request.POST.get(
            "application_deadline", ""
        ).strip()

        try:
            application.application_deadline = (
                date.fromisoformat(deadline_raw)
                if deadline_raw else None
            )
        except ValueError:
            messages.error(
                request,
                "Please enter a valid application deadline."
            )
            return render(
                request,
                "apptracker/application_update.html",
                {"application": application}
            )

        # Convert application fee to Decimal
        fee_raw = request.POST.get("application_fee", "").strip()

        try:
            application.application_fee = (
                Decimal(fee_raw) if fee_raw else None
            )
        except InvalidOperation:
            messages.error(
                request,
                "Please enter a valid application fee."
            )
            return render(
                request,
                "apptracker/application_update.html",
                {"application": application}
            )

        # Convert recommendation letters to int
        reco_raw = request.POST.get(
            "reco_letters_needed", ""
        ).strip()

        try:
            application.reco_letters_needed = (
                int(reco_raw) if reco_raw else None
            )
        except ValueError:
            messages.error(
                request,
                "Please enter a valid number of recommendation letters."
            )
            return render(
                request,
                "apptracker/application_update.html",
                {"application": application}
            )

        # Save all updated fields
        application.save()

        messages.success(request, "Application updated successfully.")
        return redirect("application_search")

    return render(
        request,
        "apptracker/application_update.html",
        {"application": application}
    )


#For application view only
def application_view(request, pk):
    application = get_object_or_404(
        apptracker_tracking,
        pk=pk,
        username=request.user.username
    )

    return render(
        request,
        "apptracker/application_update.html",
        {
            "application": application,
            "readonly": True,
        }
    )


#for soft deleting application
@login_required
def record_list(request):
    records = apptracker_tracking.objects.filter(delete_flag=False)

    return render(request, 'application_search.html', {
        'records': records
    })

@login_required
@require_POST
def application_delete(request, pk):
    record = get_object_or_404(
        apptracker_tracking,
        pk=pk,
        delete_flag=False,
    )

    record.delete_flag = True
    record.save(update_fields=["delete_flag"])

    return redirect("application_search")