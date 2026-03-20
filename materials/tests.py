from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro", password="qwe123")
        self.course = Course.objects.create(
            title_course="Python-программист",
            description="Описание курса Python-программист",
            owner=self.user,
        )
        self.lesson = Lesson.objects.create(
            title_lesson="Первый урок",
            description="Описание первого урока",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title_course"),
            self.course.title_course,
        )

    def test_course_create(self):
        url = reverse("materials:course-list")
        data = {
            "title_course": "Python-программист, дополнение",
            "description": "Описание курса Python-программист",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "title_course": "Python-программист, дополнение № 1",
            "description": "Описание курса",
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data.get("title_course"),
            "Python-программист, дополнение № 1",
        )

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LessonTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create(email="admin@mail.ru")
        self.course = Course.objects.create(
            title_course="Python-программист",
            description="Описание курса Python-программист",
        )
        self.lesson = Lesson.objects.create(
            title_lesson="Первый урок",
            description="Описание первого урока",
            course=self.course,
            owner=self.user,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_create(self):
        course = Course.objects.create(
            title_course="Python-программист",
            description="Описание курса Python-программист",
            owner=self.user,
        )

        url = reverse("materials:lesson-create")
        data = {
            "course": course.id,
            "title_lesson": "Первый урок",
            "description": "Описание урока",
            "video_url": "https://www.youtube.com/watch?v=test",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_update(self):
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            "title_lesson": "Первый урок, дополнительный",
            "description": "Описание урока",
            "video_url": "https://www.youtube.com/watch?v=test",
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data.get("title_lesson"), "Первый урок, дополнительный"
        )

    def test_lesson_delete(self):
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_list(self):
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
