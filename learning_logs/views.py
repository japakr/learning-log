from django.shortcuts import render, redirect
from learning_logs.models import Topic, Entry
from learning_logs.forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

def index(request):
    """A página inicial de Learning Log"""
    return render(request, 'learning_logs/index.html', {})

@login_required
def topics(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    return render(request, 'learning_logs/topics.html', {'topics': topics})

@login_required
def topic(request, pk):
    topic = Topic.objects.get(id=pk)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    return render(request, 'learning_logs/entries.html', {'entries': entries, 'topic': topic})

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('topics')

    return render(request, 'learning_logs/new_topic.html', {'form': form})

@login_required
def new_entry(request, pk):
    topic = Topic.objects.get(id=pk)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('../')

    return render(request, 'learning_logs/new_entry.html', {'form': form, 'topic':topic})

@login_required
def edit_entry(request, topic_pk, entry_pk):
    entry = Entry.objects.get(pk=entry_pk)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            #entry = form.save(commit=False)
            #entry.date_added = timezone.now()
            entry.save()
            return redirect('../')

    return render(request, 'learning_logs/edit_entry.html', {'form': form, 'topic_pk': topic_pk, 'entry_pk': entry_pk})
