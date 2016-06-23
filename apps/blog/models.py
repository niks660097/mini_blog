import datetime
from django.db import models

class BlogManager(models.Manager):
    def create_new(self, title, content_list):
        blog = None
        if title and content_list:
            blog = Blog.objects.create(title=title)
            prev_para = Paragraph.objects.create(text=content_list[0], blog=blog)
            if len(content_list) > 1:
                for i in content_list[1:]:
                    para = Paragraph.objects.create(text=i, blog=blog)
                    prev_para.next = para
                    prev_para.save()
                    prev_para = para
        return blog


    def edit_blog(self):
        '''
        Not in the requirements
        '''
        pass

    def get_blog_data(self, blog_id, comments=False):
        blog_content, blog = None, None
        try:
            blog = Blog.objects.filter(pk=blog_id).first()
            if blog:
                blog_content = []
                for i in blog.content:
                    paragraph = [[i.text, i.pk]]
                    if comments:
                        paragraph.append([j.text for j in i.comments])
                    blog_content.append(paragraph)
        except Exception:
            #not concerned right now
            pass
        return blog_content, blog


class Blog(models.Model):
    title = models.TextField()

    objects = BlogManager()

    @property
    def content(self):
        final_content = []
        paragraph_end = self.paragraph_set.filter(next=None).first()
        if paragraph_end:
            final_content.append(paragraph_end)
            paragraph_cursor = paragraph_end.previous.first()
            while paragraph_cursor:
                final_content.append(paragraph_cursor)
                paragraph_cursor = paragraph_cursor.previous.first()
        final_content.reverse()
        return final_content

    def get_paragraph(self, para_id):
        return self.paragraph_set.get(pk=para_id)

class Paragraph(models.Model):
    '''
    This model can store more details, like formatting of text, meta data etc.
    '''
    next = models.ForeignKey('self', null=True, related_name='previous')
    blog = models.ForeignKey('blog.Blog')
    text = models.TextField()

    @property
    def comments(self):
        return self.comment_set.all()

    def add_comment(self, comm_txt):
        comment = Comment.objects.create(text=comm_txt, paragraph=self)
        return comment


class Comment(models.Model):
    text = models.TextField()
    paragraph = models.ForeignKey('blog.Paragraph')
    created_on = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_on = datetime.datetime.now()
        return super(Comment, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']
