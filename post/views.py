from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from models import Post, Tag
from services import extract_uploaded_zip_file_into_post_folder, \
    remove_old_version_post_folder_on_disk_if_exists
import os


def display_post_index(request):
    if "tag_id" in request.GET:
        tag_chosen = Tag.objects.get(id=int(request.GET["tag_id"]))
        context = {
            "tag_chosen": tag_chosen,
            "posts": tag_chosen.linked_posts.all(),
            "tags": Tag.objects.all(),
        }
    else:
        context = {
            "posts": Post.objects.all(),
            "tags": Tag.objects.all(),
            "nav_and_sidebar_animated": True
        }
    return render(request, "post/post_index.html", context)


def display_post(request):
    post = Post.objects.get(id=int(request.GET["post_id"]))
    post.num_view += 1
    post.save()
    context = {
        "post": post,
        "tags": Tag.objects.all(),
        "nav_and_sidebar_animated": True
    }
    return render(request, "post/post_page.html", context)


def post_zip_handler(post, zip_uploaded):
    # create the correct folder and move content inside
    post_folder_path = os.path.join(settings.MEDIA_ROOT, str(post.id))
    remove_old_version_post_folder_on_disk_if_exists(post_folder_path)
    os.mkdir(post_folder_path)  # create a new folder
    extract_uploaded_zip_file_into_post_folder(zip_uploaded, post_folder_path)

    # create a new html file named "index.html", add "/media/[post.pk]/" in front of reference to the static file
    for file in os.listdir(post_folder_path):
        if file.endswith(".htm") or file.endswith(".html"):
            file_name = file.split(".")[0]
            index = open(os.path.join(post_folder_path, "index.htm"), 'wb+')
            original_index = open(os.path.join(post_folder_path, file), 'r')
            for line in original_index:
                index.write(line.replace(file_name + ".file", '/media/' + str(post.pk) + "/" + file_name + ".file").replace("a:visited", "#content_from_file a:visited").replace("a:link", "#content_from_file a:link"))
            original_index.close()
            index.close()


def upload_post(request):
    if not request.user.is_staff:
        return HttpResponse()
    post = Post(title=request.POST["title"])
    post.save()
    post_zip_handler(post, request.FILES["zip_uploaded"])  # request.FILES["zip_uploaded"] is an UploadedFile object
    return redirect("/post/?post_id=" + str(post.pk))


def update_post(request):
    if not request.user.is_staff:
        return HttpResponse()
    post = Post.objects.get(id=int(request.POST["post_id"]))
    post.title = request.POST["title"]
    post.save()
    if "zip_uploaded" in request.FILES:
        post_zip_handler(post, request.FILES["zip_uploaded"])
    return redirect("/post/?post_id=" + str(post.pk))


def display_upload_page(request):
    return render(request, "post/upload_post_page.html")


def search_post(request):
    # search post by title
    search_key = request.GET["search_key"]
    search_result_posts = Post.objects.filter(title__icontains=search_key)  # case-insensitive contain
    context = {
        "tags": Tag.objects.all(),
        "posts": search_result_posts,
        "search_key": search_key,
    }
    return render(request, "post/post_index.html", context)
