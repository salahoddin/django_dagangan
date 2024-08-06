from django.shortcuts import render, redirect
from . forms import CreateUserForm


# Create your views here.
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save() 
            return redirect('store')

    return render(request, 'account/registration/register.html', {'form': form})