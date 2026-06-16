from django.test import TestCase, Client
from .models import Category, Course

class CourseViewTest(TestCase):
    def setUp(self):
        # Pregătim date de test într-o bază de date temporară securizată
        self.client = Client()
        self.category = Category.objects.create(name='Computer Science')
        self.course = Course.objects.create(
            title='Web Programming',
            instructor='Popescu Ion',
            year=2026,
            semester='spring',
            category=self.category,
            credits=5
        )

    def test_list_view(self):
        """Verifică dacă pagina principală se încarcă și conține cursul"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Web Programming')

    def test_detail_view(self):
        """Verifică dacă pagina de detalii a cursului funcționează"""
        response = self.client.get(f'/{self.course.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Popescu Ion')

    def test_detail_404(self):
        """Verifică dacă o pagină de curs care nu există întoarce corect 404"""
        response = self.client.get('/9999/')
        self.assertEqual(response.status_code, 404)

    def test_create_requires_login(self):
        """Verifică dacă încercarea de adăugare fără login face redirect (302)"""
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_api(self):
        """Verifică dacă API-ul întoarce JSON valid cu datele corecte"""
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data[0]['title'], 'Web Programming')