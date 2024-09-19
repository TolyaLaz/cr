from django.conf import settings
from django.core.cache import cache

from blog.models import Blog


def get_cached_blogs():
    if settings.CACHE_ENABLED:
        key = 'blog_list'
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Blog.objects.all()
            cache.set(key, blog_list)
    else:
        blog_list = Blog.objects.all()

    return blog_list