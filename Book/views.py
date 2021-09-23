from django.shortcuts import render,redirect
from .models import Book

# Create your views here.

from datetime import date
def homepage(request):
    if request.method=="POST":
        data=request.POST
        if not data.get("id"):
            if data["ispub"]=="Yes":
                Book.objects.create(name=data["nm"],
                qty=data["qty"],
                price=data["price"],
                is_published=True,
                published_date=date.today())
            elif data["ispub"]=="No":
                Book.objects.create(name=data["nm"],
                qty=data["qty"],
                price=data["price"],
                is_published=False)
            
            return redirect("home")
        else:
            did=data.get("id")
            book=Book.objects.get(id=did)
            book.name=data["nm"]
            book.qty=data["qty"]
            book.price=data["price"]
            if data["ispub"]=="Yes":
                if book.published_date:
                    pass
                else:
                    book.Is_Published=True
                    book.published_date=date.today()
            elif data['ispub']=="No":
                if book.published_date:
                    book.is_published=False
            book.save()
            return redirect("home")
    


    else:
        return render(request=request,template_name="Base.html")

def show_books(request):
    all_books=Book.objects.all()
    return render(request,template_name="show_book.html",context={"all_books":all_books})

def soft_delete(request,id):
    book=Book.objects.get(id=id)
    book.is_deleted="Y"
    book.save()
    return redirect("showbook")


def delete_book(request,id):
    Book.objects.get(id=id).delete()
    return redirect("showbook")

def edit_book(request,id):
    book=Book.objects.get(id=id)
    return render(request,template_name="Base.html",context={"single_book":book})

def show_active_books(request):
    books=Book.objects.filter(is_deleted="N")
    return render(request,template_name="show_book.html",context={"all_books":books})


def show_inactive_books(request):
    books=Book.objects.filter(is_deleted="Y")
    return render(request,template_name="show_book.html",context={"all_books":books,"book_status":"inactive"})