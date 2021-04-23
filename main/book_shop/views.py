import django
from rest_framework import viewsets
from django.http import HttpResponse
from book_shop.models import Book
from account.models import User


class BookShopGateway(viewsets.ViewSet):
    def handle_request(self, request):
        try:
            token = request.data['token']
            request = request.data['request']
        except KeyError:
            return HttpResponse('Wrong input', status=406)
        try:
            user = User.objects.get(token=token)
            if not user:
                return HttpResponse('Invalid Token', status=409)
        except:
            return HttpResponse('Invalid Token', status=409)

        if request == 'Create':
            if not user.isAdmin:
                return HttpResponse('Unauthorized', status=401)
            return self.create(request)
        elif request == 'Read':
            return self.read(request)
        elif request == 'Update':
            if not user.isAdmin:
                return HttpResponse('Unauthorized', status=401)
            return self.update(request)
        if request == 'Delete':
            return self.delete(request)

    @staticmethod
    def create(request):
        try:
            title = request.data['title']
            authors = request.data['authors']
            category = request.data['category']
            book = Book()
            book.title, book.authors, book.category = title, authors, category
            book.save()
        except KeyError:
            return HttpResponse('Input error', status=406)
        except django.db.utils.IntegrityError:
            return HttpResponse('Book exists', status=409)
        return HttpResponse('Book added to shop', status=200)

    @staticmethod
    def read(request):
        if 'title' in request.data:
            search_by = 't'
            to_search = request.data['title']
        elif 'category' in request.data:
            search_by = 'c'
            to_search = request.data['category']
        else:
            return HttpResponse('Input error', status=406)

        if search_by == 't':
            try:
                book = Book.objects.get(title=to_search)
                if not book:
                    return HttpResponse('Wrong title', status=409)
            except:
                return HttpResponse('Wrong title', status=409)
            return HttpResponse(
                'Book found!\n'
                'Title: ' + book.title + ', Authors: ' + book.authors + ', Category: ' + book.category, status=200)
        elif search_by == 'c':
            try:
                books = Book.objects.filter(category=to_search)
                if not books:
                    return HttpResponse('Wrong category', status=409)
            except:
                return HttpResponse('Wrong category', status=409)
            str_to_return = ''
            for book in books:
                str_to_return += '[' + 'Title: ' + book.title + '\nAuthors: ' + book.authors + '\nCategory: ' + book.category + ']\n'
            return HttpResponse(str_to_return, status=200)

    @staticmethod
    def update(request):
        try:
            title = request.data['title']
            try:
                book = Book.objects.get(title=title)
            except:
                return HttpResponse('Wrong title', status=409)
            book.title = request.data['new_title']
            new_authors = request.data['new_authors']
            book.authors = new_authors
            new_cat = request.data['new_category']
            book.category = new_cat
            book.save()
        except KeyError:
            return HttpResponse('Wrong input', status=406)
        except django.db.utils.IntegrityError:
            return HttpResponse('Conflict', status=409)
        return HttpResponse('The book updated', status=200)

    @staticmethod
    def delete(request):
        if 'title' in request.data:
            title = request.data['title']
            try:
                book = Book.objects.get(title=title)
                if not book:
                    return HttpResponse('Title not valid', status=409)
            except:
                return HttpResponse('Title not valid', status=409)
        else:
            return HttpResponse('Wrong input', status=406)
        book.delete()
        return HttpResponse('Book removed', status=200)
