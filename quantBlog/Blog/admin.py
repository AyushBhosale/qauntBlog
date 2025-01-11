from django.contrib import admin
from .models import Post, Comment



class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0 
    readonly_fields = ('created_date',)

class PostAdmin(admin.ModelAdmin):
    # Fields shown in the list view
    list_display = ('title', 'author', 'status', 'created_date', 'updated_date')
    
    # Fields you can filter by in the right sidebar
    list_filter = ('status', 'created_date', 'author')
    
    # Fields you can search through
    search_fields = ('title', 'content', 'excerpt')
    
    # Automatically create slug from title
    prepopulated_fields = {'slug': ('title',)}
    
    # Organize fields into logical groups
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'featured_image')
        }),
        ('Metadata', {
            'fields': ('author', 'status')
        })
    )
    
    # Show comments inline with posts
    inlines = [CommentInline]
    
    # Fields that are shown as read-only
    readonly_fields = ('created_date', 'updated_date')
    
    # Add date hierarchy navigation
    date_hierarchy = 'created_date'

# Comment Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_date', 'is_approved')
    list_filter = ('is_approved', 'created_date')
    search_fields = ('content', 'author__username', 'post__title')
    actions = ['approve_comments']  # Custom action to approve comments

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

# Register all models with their admin classes
# admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
