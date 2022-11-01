from django.test import TestCase, SimpleTestCase, Client
from django.urls import reverse, resolve
from . models import AuditTriple, Dataset
from django.contrib.auth import get_user_model
import json
from . import views
# Create your tests here.

class TestUrls(TestCase):

    def setUp(self):
        self.client = Client()
        new_user = get_user_model().objects.create_user(
            username='newuser'
        )

        new_user.set_password('testpassword123') 
        new_user.save()

        self.client.login(username='newuser',password='testpass123')

        d = Dataset.objects.create(name='testdata')
        self.at = AuditTriple.objects.create(user=new_user,entityA='entA',relation='relation',entityB='entB',dataset=d,verified=True,comment='')

    def test_groups_resolved(self):
        url = reverse('Audit:audit_groups')
        self.assertEquals(resolve(url).func.view_class,views.GroupsView)

    def test_audit_comments_is_resolved(self):
        url = reverse('Audit:audit_comments')
        self.assertEquals(resolve(url).func.view_class,views.CommentView)

    def test_audit_triple_cards_is_resolved(self):
        url = reverse('Audit:audit_triple_cards')
        self.assertEquals(resolve(url).func,views.audit_triple_cards)

    def test_audit_triple_list_is_resolved(self):
        url = reverse('Audit:audit_triple_list')
        self.assertEquals(resolve(url).func,views.audit_triples)

    def test_audit_triple_update(self):
        url = reverse('Audit:audit_triple_update',args=[self.at.id])
        self.assertEquals(resolve(url).func.view_class,views.AuditTripleUpdate)

    def test_audit_user_triple_cards_is_resolved(self):
        url = reverse('Audit:audit_user_triple_cards')
        self.assertEquals(resolve(url).func,views.admin_view_triple_cards)

    def test_audit_user_triple_list(self):
        url = reverse('Audit:audit_user_triple_list')
        self.assertEquals(resolve(url).func,views.admin_view_triples)

    def test_audit_triple_detail(self):
        url = reverse('Audit:audit_triple_cards')
        self.assertEquals(resolve(url).func,views.audit_triple_cards)

    def test_audit_list_dataset(self):
        url = reverse('Audit:audit_list_datasets')
        self.assertEquals(resolve(url).func.view_class,views.ListDatasets)

class TestViews(TestCase):

    # setup code for tests
    def setUp(self): 
        self.client = Client()
        self.groups_view_url = reverse('Audit:audit_groups')
        self.comment_view_url = reverse('Audit:audit_comments')

        new_user = get_user_model().objects.create_user(
            username='newuser'
        )

        new_user.set_password('testpassword123') 
        new_user.save()

        self.client.login(username='newuser',password='testpass123')

        d = Dataset.objects.create(name='testdata')
        AuditTriple.objects.create(user=new_user,entityA='entA',relation='relation',entityB='entB',dataset=d,verified=True,comment='')
        
    # test that the url resolves and returns the correct template
    def test_groups_view(self):
        response = self.client.get(self.groups_view_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'audit_groups.html')

    # if user is not logged in they are redirected to a login url
    def test_user_comments_not_logged_in(self):
        response = self.client.get(self.comment_view_url)
        self.assertEquals(response.status_code,302)

    # if the user is logged in they can view the user comments
    def test_user_comments_logged_in(self):
        self.client.login(username='newuser',password='testpassword123')
        response = self.client.get(self.comment_view_url)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'audit_comments.html')

class TestAdminViews(TestCase):
    def setUp(self):

        self.client = Client()

        new_staff = get_user_model().objects.create_user(
            username='newstaff',
            is_staff=True,
        )

        self.d = Dataset.objects.create(name='testdata')
        self.at = AuditTriple.objects.create(user=new_staff,entityA='entA',relation='relation',entityB='entB',dataset=self.d,verified=True,comment='')

        self.dataset_list = reverse('Audit:audit_list_datasets')
        self.delete_dataset = reverse('Audit:audit_delete_dataset',args=[self.at.pk])

        self.audit_user_triple_list = reverse('Audit:audit_user_triple_list')
        self.audit_user_triple_cards = reverse('Audit:audit_user_triple_cards')

        new_staff.set_password('testpassword123') 
        new_staff.save()
        self.client.login(username='newstaff',password='testpassword123')

    def test_list_datasets_view(self):
        response = self.client.get(self.dataset_list)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'audit_list_datasets.html')

    def test_audit_user_triple_list(self):
        response = self.client.get(self.audit_user_triple_list)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'audit_user_triple_list.html')

    def test_audit_user_triple_cards(self):
        response = self.client.get(self.audit_user_triple_cards)
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'audit_user_triple_cards.html')

   # def test_delete_dataset_view(self):
   #     response = self.client.delete(self.delete_dataset)
   #     self.assertEquals(response.status_code,200)
   #     self.assertTemplateUsed(response,'audit_dataset_confirm_delete.html')
