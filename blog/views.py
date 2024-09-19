from django.views.generic import DetailView

from blog.models import Blog


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """Увеличение счетчика просмотров, для этого требуется queryset и аргумент pk в urls."""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object
