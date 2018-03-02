import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from models import Post, Tag
from services import (extract_uploaded_zip_file_into_post_folder,
                      remove_old_version_post_folder_on_disk_if_exists)


def display_post_index(request):
    if 'tag_id' in request.GET:
        tag_chosen = Tag.objects.get(id=int(request.GET['tag_id']))
        context = {
            'tag_chosen': tag_chosen,
            'posts': tag_chosen.linked_posts.all(),
            'tags': Tag.objects.all(),
        }
    else:
        context = {
            'posts': Post.objects.all().order_by('-post_time'),
            'tags': Tag.objects.all(),
            'nav_and_sidebar_animated': True
        }
    return render(request, 'post/post_index.html', context)


def display_post(request):
    post = Post.objects.get(id=int(request.GET['post_id']))
    post.num_view += 1
    post.save()
    context = {
        'post': post,
        'tags': Tag.objects.all(),
        'nav_and_sidebar_animated': True
    }
    return render(request, 'post/post_page.html', context)


def _post_zip_handler(post, zip_uploaded):
    # create the correct folder and move content inside
    post_folder_path = os.path.join(settings.MEDIA_ROOT, str(post.id))
    remove_old_version_post_folder_on_disk_if_exists(post_folder_path)
    os.mkdir(post_folder_path)  # create a new folder
    extract_uploaded_zip_file_into_post_folder(zip_uploaded, post_folder_path)

    # create a new html file named 'index.html', add '/media/[post.pk]/' in front of reference to the static file
    for file in os.listdir(post_folder_path):
        if file.endswith('.htm') or file.endswith('.html'):
            file_name = file.split('.')[0]
            index = open(os.path.join(post_folder_path, 'index.htm'), 'wb+')
            original_index = open(os.path.join(post_folder_path, file), 'r')
            for line in original_index:
                line = line.replace(file_name + '.file',
                                    '/media/' + str(post.pk) + '/' + file_name + '.file')
                line = line.replace(file_name + '.fld',
                                    '/media/' + str(post.pk) + '/' + file_name + '.fld')
                # restrict style of the anchor tag only within the post content part
                # provent the style to influence other parts of the page
                # line = line.replace('a:visited', '#content_from_file a:visited').replace('a:link', '#content_from_file a:link')
                index.write(line)
            original_index.close()
            index.close()

def _post_html_handler(post, html_uploaded):
    post_folder_path = os.path.join(settings.MEDIA_ROOT, str(post.id))
    remove_old_version_post_folder_on_disk_if_exists(post_folder_path)
    os.mkdir(post_folder_path)

    html_on_disk_path = os.path.join(post_folder_path, 'index.htm')
    html_on_disk = open(html_on_disk_path, 'wb+')
    for chunk in html_uploaded.chunks():
        html_on_disk.write(chunk)
    html_on_disk.close()

def upload_post(request):
    if not request.user.is_staff:
        return HttpResponse()
    post = Post(title=request.POST['title'])
    post.save()

    # request.FILES['file_uploaded'] is an UploadedFile object
    uploaded_file = request.FILES['file_uploaded']
    if uploaded_file.name.endswith('html') or uploaded_file.name.endswith('htm'):
        _post_html_handler(post, uploaded_file)
    else:
        _post_zip_handler(post, uploaded_file)
    return redirect('/post/?post_id=' + str(post.pk))


def update_post(request):
    if not request.user.is_staff:
        return HttpResponse()
    post = Post.objects.get(id=int(request.POST['post_id']))
    post.title = request.POST['title']
    post.save()

    if 'file_uploaded' in request.FILES:
        uploaded_file = request.FILES['file_uploaded']
        if uploaded_file.name.endswith('html') or uploaded_file.name.endswith('htm'):
            _post_html_handler(post, uploaded_file)
        else:
            _post_zip_handler(post, uploaded_file)
    return redirect('/post/?post_id=' + str(post.pk))


def display_upload_page(request):
    return render(request, 'post/upload_post_page.html')


def search_post(request):
    # search post by title
    search_key = request.GET['search_key']
    search_result_posts = Post.objects.filter(title__icontains=search_key)  # case-insensitive contain
    context = {
        'tags': Tag.objects.all(),
        'posts': search_result_posts,
        'search_key': search_key,
    }
    return render(request, 'post/post_index.html', context)


def display_raw(request, pk):
    post = Post.objects.get(id=pk);
    return render(request, post.content_path)
