import json
from django.views.generic.base import View
from django.http.response import JsonResponse
from models import Blog, Paragraph, Comment

class BlogEntry(View):

    def get(self, request, *args, **kwargs):
        '''
        get a blog by id
        '''
        blog_id = kwargs['blog_id']
        response_dict = {'status': '', 'msg': ''}
        blog_content, blog = Blog.objects.get_blog_data(blog_id, comments=True)
        if blog:
            response_dict['blog_details'] = {'title': blog.title,
                                             'content': blog_content}
        else:
            response_dict['status'] = 'Request failed!!'
            response_dict['msg'] = 'No such blog!'
        return JsonResponse(response_dict)


    def post(self, request, *args, **kwargs):
        '''
        creates new blog
        '''
        response_dict = {'status': '', 'msg': ''}
        try:

            request_data = json.loads(request.body)
            title = request_data['title']
            content = request_data['content'].split('\n\n')
            new_blog = Blog.objects.create_new(title,content)
            response_dict['status'] = 'Request Successful.'
            response_dict['msg'] = 'Blog created.'
            response_dict['blog_id'] = new_blog.pk
        except Exception:
            response_dict['status'] = 'Request failed!!'
            response_dict['msg'] = 'Invalid Json!'
        return JsonResponse(response_dict)


class BlogCollection(View):
    '''
    we are not maintaining(using) session.
    '''

    def get_blog_page(self, page, page_size=5):
        blogs, total_pages = [], None#to be returned
        if page > 0:
            blogs_list = Blog.objects.all()
            if blogs_list.exists():
                total_blogs = blogs_list.count()
                total_pages = blogs_list.count()/page_size
                extra_blogs = blogs_list.count() % page_size
                if total_pages == 0:
                    total_pages = 1
                else:
                    if extra_blogs:
                        total_pages += 1
                if page <= total_pages:
                    if extra_blogs and page == total_pages:
                        page_start = total_blogs-extra_blogs
                        if page_start > 0:
                            page_start -= 1
                        page_end = total_blogs
                    else:
                        page_start = 0 if page==1 else ((page-1)*page_size)-1
                        page_end = (page*page_size)
                    blogs, total_pages = blogs_list[page_start:page_end], total_pages
        return blogs, total_pages

    def get(self, request, *args, **kwargs):
        '''
        get iterator over blogs
        '''
        response_dict = {'status': '', 'msg': ''}
        try:
                page_no = 1 if not kwargs.get('page_number') else int(kwargs['page_number'])
                blogs, total_pages = self.get_blog_page(page_no)
                response_dict['total_pages'] = total_pages
                response_dict['blogs'] = {}
                response_dict['current_page'] = page_no
                if blogs:
                    for i in blogs:
                        blog_content, blog = Blog.objects.get_blog_data(i.pk)
                        response_dict['blogs'][blog.pk] = blog_content
        except Exception:
            response_dict['status'] = 'Request Failed!'
            response_dict['msg'] = 'Invalid request params!'
        return JsonResponse(response_dict)


class BlogComment(View):

    def post(self, request, *args, **kwargs):
        response_dict = {'status': '', 'msg': ''}
        try:
            req_data = json.loads(request.body)
            para_id = kwargs['paragraph_id']
            blog_id = req_data['blog_id']
            comment_txt = req_data['comment_text']
            blog = Blog.objects.get(pk=blog_id)
            paragraph = blog.get_paragraph(para_id)
            new_comment = paragraph.add_comment(comment_txt)
            response_dict['comment_id'] = new_comment.pk
            response_dict['status'] = 'Request successfull.'
            response_dict['msg'] = 'Comment added.'
        except Exception:
            response_dict['status'] = 'Request Failed!'
            response_dict['msg'] = 'Invalid request.'
        return JsonResponse(response_dict)