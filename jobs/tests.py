from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import JobApplication


class JobApplicationModelTests(TestCase):
    """Does the model itself store and default data correctly?"""

    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='testpass123')

    def test_create_job_application_with_required_fields(self):
        """A JobApplication saves correctly with just company/title and is linked to its owner."""
        job = JobApplication.objects.create(
            user=self.user,
            company_name='Acme Corp',
            job_title='Backend Engineer',
        )
        self.assertEqual(job.company_name, 'Acme Corp')
        self.assertEqual(job.job_title, 'Backend Engineer')
        self.assertEqual(job.user, self.user)

    def test_status_defaults_to_applied(self):
        """If you don't set a status, new applications default to 'applied' rather than blank."""
        job = JobApplication.objects.create(
            user=self.user, company_name='Acme Corp', job_title='Backend Engineer'
        )
        self.assertEqual(job.status, 'applied')

    def test_string_representation(self):
        """__str__ renders as 'Job Title at Company', the label used in admin/shell/debugging."""
        job = JobApplication.objects.create(
            user=self.user, company_name='Acme Corp', job_title='Backend Engineer'
        )
        self.assertEqual(str(job), 'Backend Engineer at Acme Corp')

    def test_date_applied_is_set_automatically(self):
        """date_applied (auto_now_add) is populated on save without being passed explicitly."""
        job = JobApplication.objects.create(
            user=self.user, company_name='Acme Corp', job_title='Backend Engineer'
        )
        self.assertIsNotNone(job.date_applied)


class UserDataIsolationTests(TestCase):
    """The important suite: proves one user can never see or modify another user's data."""

    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='testpass123')
        self.bob = User.objects.create_user(username='bob', password='testpass123')

        self.alice_job = JobApplication.objects.create(
            user=self.alice, company_name='Alice Co', job_title='Engineer'
        )
        self.bob_job = JobApplication.objects.create(
            user=self.bob, company_name='Bob Co', job_title='Designer'
        )

    def test_job_list_only_shows_own_applications(self):
        """Alice's job list contains her job and never Bob's, even though both exist in the DB."""
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('job_list'))
        jobs_shown = list(response.context['jobs'])
        self.assertIn(self.alice_job, jobs_shown)
        self.assertNotIn(self.bob_job, jobs_shown)

    def test_dashboard_counts_only_own_applications(self):
        """The dashboard's 'total' stat counts only the logged-in user's rows, not everyone's."""
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context['total'], 1)

    def test_user_cannot_view_edit_form_for_another_users_job(self):
        """Alice can't load Bob's edit form by guessing his job's ID in the URL: she gets a 404."""
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('job_edit', args=[self.bob_job.pk]))
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_edit_another_users_job_via_post(self):
        """A crafted POST to Bob's job-edit URL is rejected with 404 and leaves his data untouched."""
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(reverse('job_edit', args=[self.bob_job.pk]), {
            'company_name': 'Hacked Co',
            'job_title': 'Hacked Title',
            'status': 'applied',
        })
        self.assertEqual(response.status_code, 404)
        self.bob_job.refresh_from_db()
        self.assertEqual(self.bob_job.company_name, 'Bob Co')

    def test_user_cannot_delete_another_users_job(self):
        """Alice can't delete Bob's application; posting to its delete URL 404s and it still exists."""
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(reverse('job_delete', args=[self.bob_job.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(JobApplication.objects.filter(pk=self.bob_job.pk).exists())

    def test_job_list_status_filter_still_respects_ownership(self):
        """Combining the ?status= filter with the user filter never leaks another user's matching rows."""
        JobApplication.objects.create(
            user=self.alice, company_name='Alice Interview Co', job_title='Engineer II',
            status='interview',
        )
        self.client.login(username='alice', password='testpass123')
        response = self.client.get(reverse('job_list'), {'status': 'applied'})
        jobs_shown = list(response.context['jobs'])
        self.assertIn(self.alice_job, jobs_shown)
        self.assertNotIn(self.bob_job, jobs_shown)

    def test_user_can_edit_own_job(self):
        """The ownership check only blocks other people's data — editing your own job still works."""
        self.client.login(username='alice', password='testpass123')
        response = self.client.post(reverse('job_edit', args=[self.alice_job.pk]), {
            'company_name': 'Alice Co Updated',
            'job_title': 'Engineer',
            'status': 'interview',
        })
        self.assertRedirects(response, reverse('job_list'))
        self.alice_job.refresh_from_db()
        self.assertEqual(self.alice_job.company_name, 'Alice Co Updated')


class ViewAccessTests(TestCase):
    """Basic endpoint behavior: can a logged-in user use the app, and is a logged-out user kept out?"""

    def setUp(self):
        self.user = User.objects.create_user(username='carol', password='testpass123')

    def test_logged_out_user_redirected_from_dashboard(self):
        """An anonymous visitor hitting the dashboard is redirected to the login page, not shown content."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_logged_out_user_redirected_from_job_list(self):
        """The same @login_required protection applies to the job list, not just the dashboard."""
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_logged_out_user_redirected_from_job_add(self):
        """You can't reach the 'add application' form without logging in first."""
        response = self.client.get(reverse('job_add'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_view_dashboard(self):
        """A logged-in user gets a normal 200 from the dashboard — the auth check doesn't over-block."""
        self.client.login(username='carol', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_create_job_application(self):
        """Submitting the add-job form as a logged-in user creates a DB row owned by that user."""
        self.client.login(username='carol', password='testpass123')
        response = self.client.post(reverse('job_add'), {
            'company_name': 'New Co',
            'job_title': 'Data Analyst',
            'status': 'applied',
        })
        self.assertRedirects(response, reverse('job_list'))
        self.assertTrue(
            JobApplication.objects.filter(user=self.user, company_name='New Co').exists()
        )

    def test_logged_in_user_can_view_job_list(self):
        """The job list page actually renders the user's applications in the HTML, not just a 200."""
        JobApplication.objects.create(user=self.user, company_name='Carol Co', job_title='PM')
        self.client.login(username='carol', password='testpass123')
        response = self.client.get(reverse('job_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carol Co')

    def test_register_view_creates_user_and_logs_in(self):
        """Registering creates a real user account and logs them straight into the dashboard."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'SuperSecret123!',
            'password2': 'SuperSecret123!',
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_view_authenticates_existing_user(self):
        """Submitting correct credentials on the login form logs you in and redirects to the dashboard."""
        response = self.client.post(reverse('login'), {
            'username': 'carol',
            'password': 'testpass123',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_view_rejects_wrong_password(self):
        """A wrong password re-renders the login form instead of granting access."""
        response = self.client.post(reverse('login'), {
            'username': 'carol',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_view_logs_out_user(self):
        """After logout the session is actually cleared — the next dashboard request is redirected again."""
        self.client.login(username='carol', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        response2 = self.client.get(reverse('dashboard'))
        self.assertEqual(response2.status_code, 302)

    def test_export_pdf_requires_login(self):
        """The PDF export endpoint is behind login too — no anonymous downloads of anyone's data."""
        response = self.client.get(reverse('export_pdf'))
        self.assertEqual(response.status_code, 302)

    def test_export_pdf_returns_pdf_for_logged_in_user(self):
        """A logged-in user hitting export gets back an actual PDF response, not an error."""
        JobApplication.objects.create(user=self.user, company_name='Carol Co', job_title='PM')
        self.client.login(username='carol', password='testpass123')
        response = self.client.get(reverse('export_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
