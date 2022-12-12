from django.contrib import admin
from .models import Book
from .models import User

admin.site.site_header = 'User Admin'
admin.site.site_title = 'LibrarySystem Admin'
admin.site.index_title = 'Welcome!'
class BookAdmin (admin.ModelAdmin): 
    list_display = ['image_tag', 'book_title','book_authors','book_college', 'book_course', 'pub_month', 'pub_year',
                     'book_abstract', 'book_type']
    search_fields = ['book_title', 'book_authors', 'book_college', 'book_course', 'book_abstract']


admin.site.register(Book, BookAdmin),
admin.site.register(User),
